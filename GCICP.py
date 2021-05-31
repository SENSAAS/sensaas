#!/usr/bin/python3.7

import os, sys
import math
import open3d as o3d
import numpy as np

def preprocess_point_cloud(pcd, voxel_size):
    
    #open0.7
    #pcd_down = o3d.geometry.voxel_down_sample(pcd, voxel_size)
    #open0.12
    pcd_down = pcd.voxel_down_sample(voxel_size)
    
    radius_normal = voxel_size * 2
    
    #open0.7
    #o3d.geometry.estimate_normals(pcd_down, o3d.geometry.KDTreeSearchParamHybrid(radius = radius_normal, max_nn = 30))
    #open0.12
    pcd_down.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius = radius_normal, max_nn = 30))
    
    radius_feature = voxel_size * 5
    #open0.7
    #pcd_fpfh = o3d.registration.compute_fpfh_feature(pcd_down,o3d.geometry.KDTreeSearchParamHybrid(radius = radius_feature, max_nn = 100))
    #open0.12
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(pcd_down,o3d.geometry.KDTreeSearchParamHybrid(radius = radius_feature, max_nn = 100))
    return pcd_down, pcd_fpfh

def prepare_dataset(spcd,tpcd,voxel_size):
    source_down, source_fpfh = preprocess_point_cloud(spcd, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(tpcd, voxel_size)
    return spcd, tpcd, source_down, target_down, source_fpfh, target_fpfh

def execute_global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    #open0.7
    #result = o3d.registration.registration_ransac_based_on_feature_matching(
    #    source_down, target_down, source_fpfh, target_fpfh,
    #    distance_threshold,
    #    o3d.registration.TransformationEstimationPointToPoint(False), 4,
    #    [o3d.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
    #    o3d.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold)],
    #    o3d.registration.RANSACConvergenceCriteria(400000, 1000))
    #open0.12 ! check mutual_filter (bool) = True
    #Enables mutual filter such that the correspondence of the source point’s correspondence is itself True/False ?
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
            source_down, target_down, source_fpfh, target_fpfh, True,
            distance_threshold,
            o3d.pipelines.registration.TransformationEstimationPointToPoint(False), 4,
            [o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
                o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold)],
            o3d.pipelines.registration.RANSACConvergenceCriteria(400000, 1000))
    return result

def colored_point_cloud(source_down,target_down,globaltran,voxel_size):
    max_iter = 100
    radius = voxel_size * 2
    
    #open0.7
    #o3d.geometry.estimate_normals(source_down, o3d.geometry.KDTreeSearchParamHybrid(radius = voxel_size * 2, max_nn = 30))
    #o3d.geometry.estimate_normals(target_down, o3d.geometry.KDTreeSearchParamHybrid(radius = voxel_size * 2, max_nn = 30))
    #open0.12
    source_down.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius = voxel_size * 2, max_nn = 30))
    target_down.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius = voxel_size * 2, max_nn = 30))

    #open0.7
    #result = o3d.registration.registration_colored_icp(source_down, target_down,radius, globaltran,
    #    o3d.registration.ICPConvergenceCriteria(relative_fitness = 1e-6,
    #    relative_rmse = 1e-6, max_iteration = max_iter),lambda_geometric=0.8)
    #open0.12 with keeping explicit lamda
    result = o3d.pipelines.registration.registration_colored_icp(source_down, target_down,radius, globaltran,
            o3d.pipelines.registration.TransformationEstimationForColoredICP(lambda_geometric=0.8),
            o3d.pipelines.registration.ICPConvergenceCriteria(relative_fitness = 1e-6,
                relative_rmse = 1e-6, max_iteration = max_iter))
    return result

def gcicp_registration(spcd,tpcd,threshold,output,pcds2,pcds3,pcds4,pcdt2,pcdt3,pcdt4,Slabel2,Slabel3,Slabel4):

#Global for initialization
    fit=0
    hfit=0
    vsi=0
    rangevs = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    for i in rangevs:
        voxel_size = i

        spcdbis, tpcdbis, source_down, target_down, source_fpfh, target_fpfh = prepare_dataset(spcd,tpcd,voxel_size)
        
        result_global = execute_global_registration(source_down, target_down,source_fpfh, target_fpfh, voxel_size)
        #o3d.io.write_point_cloud("Target-downsampled.pcd", target_down)
        globaltran = result_global.transformation
        #print("globaltran %s" % globaltran)
        
        #open0.7
        #gfit=o3d.registration.evaluate_registration(spcd,tpcd,threshold,globaltran)
        #open0.12
        gfit=o3d.pipelines.registration.evaluate_registration(spcd,tpcd,threshold,globaltran)

        fitness=gfit.fitness
        rmse=gfit.inlier_rmse
        cdots=len(gfit.correspondence_set)
        #print("Global_init voxel size %.2f gfit= %3.3f rmse %3.3f" % (voxel_size,fitness,rmse))

        #CICP for optimisation
        result_cicp = colored_point_cloud(source_down,target_down,globaltran,voxel_size)
        cicptran=result_cicp.transformation
        #open0.7
        #gcicpfit=o3d.registration.evaluate_registration(spcd,tpcd,threshold,cicptran)
        #open0.12
        gcicpfit=o3d.pipelines.registration.evaluate_registration(spcd,tpcd,threshold,cicptran)
        gcicpfitness=gcicpfit.fitness
        gcicprmse=gcicpfit.inlier_rmse
        gcicpdots=len(gcicpfit.correspondence_set)

        #print("CICP_optim voxel size %.2f gfit= %3.3f rmse %3.3f" % (voxel_size,fitness,rmse))
        #print("voxel_size %.2f gfit= %3.3f dots= %5s rmse= %3.3f gcicpfit= %3.3f dots= %5s rmse= %3.3f"
        #        % (voxel_size,fitness,cdots,rmse,gcicpfitness,gcicpdots,gcicprmse))

        fd = open(output, 'a')

        #label 1 NOT used in hfit calculation
        #label 2
        #open0.7
        #score=o3d.registration.evaluate_registration(pcds2,pcdt2,threshold,cicptran)
        #open0.12
        score=o3d.pipelines.registration.evaluate_registration(pcds2,pcdt2,threshold,cicptran)
        fitness2=score.fitness
        rmse2=score.inlier_rmse
        dots2=len(score.correspondence_set)
        #print("fit_label2= %3.3f Source_matching_dots_label2= %5s rmse_label2= %3.3f" % (fitness2,dots2,rmse2))
        #fd.write('fit_label2 %3.3f Source_matching_dots_label2= %5s rmse_label2= %3.3f\n' % (fitness2,dots2,rmse2))
        #label 3
        #open0.7
        #score=o3d.registration.evaluate_registration(pcds3,pcdt3,threshold,cicptran)
        #open0.12
        score=o3d.pipelines.registration.evaluate_registration(pcds3,pcdt3,threshold,cicptran)
        fitness3=score.fitness
        rmse3=score.inlier_rmse
        dots3=len(score.correspondence_set)
        #print("fit_label3= %3.3f Source_matching_dots_label3= %5s rmse_label3= %3.3f" % (fitness3,dots3,rmse3))
        #fd.write('fit_label3 %3.3f Source_matching_dots_label3= %5s rmse_label3= %3.3f\n' % (fitness3,dots3,rmse3))
        #label 4
        #open0.7
        #score=o3d.registration.evaluate_registration(pcds4,pcdt4,threshold,cicptran)
        #open0.12
        score=o3d.pipelines.registration.evaluate_registration(pcds4,pcdt4,threshold,cicptran)
        fitness4=score.fitness
        rmse4=score.inlier_rmse
        dots4=len(score.correspondence_set)
        #print("fit_label4= %3.3f Source_matching_dots_label4= %5s rmse_label4= %3.3f" % (fitness4,dots4,rmse4))
        #fd.write('fit_label4 %3.3f Source_matching_dots_label4= %5s rmse_label4= %3.3f\n' % (fitness4,dots4,rmse4))
    
        hfittmp=0
        Slabelhfit = float(Slabel2) + float(Slabel3) + float(Slabel4)    
        if( float(Slabelhfit) != 0):
            hfittmp = (dots2 + dots3 + dots4) / float(Slabelhfit)

        sumfit = gcicpfitness + hfittmp
        fd.write("voxel_size %.2f (global_gfit= %3.3f dots= %5s rmse= %3.3f) gfit= %3.3f dots= %5s rmse= %3.3f hfit= %3.3f (gfit + hfit = %3.3f )\n"
                  % (voxel_size,fitness,cdots,rmse,gcicpfitness,gcicpdots,gcicprmse,hfittmp,sumfit))
            
        fd.close()

        if sumfit > (fit + hfit):
            bestran = cicptran
            fit=gcicpfitness
            bestgtran = globaltran
            hfit = hfittmp
            vsi = voxel_size

    #if procedure failed
    if(fit==0):
        bestran = cicptran
        bestgtran = globaltran    
        
    #np.savetxt('gtran.txt', bestgtran)        

    return bestran

