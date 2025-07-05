#!/usr/bin/python3.7

#execute ./sensaas.py target-type target-file-name source-type source-file-name output-file-name mode
#target-type or source-type are either {sdf pdb dot xyzrgb pcd}
# sdf = SDF format file (only the first molecule is read)
# pdb = PDB format file (only reads ATOM or HETATM lines with coordinates)
# dot = PDB format file where HETATM lines contain coordinates of dots and the atom element defining the label
# pcd = PCD format file (used in 3D data processing such as Open3d)
# xyzrgb = xyzrgb format file (ascii file used in 3D data processing such as Open3d; contains coordinates of dots and color)
#
#colors: set in ReadDotsPDB.py and SDFtoDots.py and PDBtoDots.py and XYZRGB2labels.py
#label 1 {H, Cl, Br, I} rgb= 0.9 0.9 0.9 (white/grey)
#label 2 {O, N, S, F, HO, HN} rgb= 1 0 0 (red)
#label 3 {C, P, B} rgb= 0 1 0 (green)
#label 4 {others} rgb= 0 0 1 (blue)
#
#target file remains fixed and source file moves
#mode "optim" generates a transformation matrix
#mode "eval" to evaluate the alignment "in place" (without aligning)
#Examples:
# ./sensaas.py sdf molecule1.sdf sdf molecule2.sdf slog optim
# ./sensaas.py sdf molecule1.sdf sdf molecule2.sdf slog eval
# ./sensaas.py sdf molecule1.sdf xyzrgb molecule2.xyzrgb slog optim
# ./sensaas.py pdb molecule1.pdb sdf molecule2.sdf slog optim
# ./sensaas.py pcd molecule1.pcd pcd molecule2.pcd slog optim
# ./sensaas.py xyzrgb molecule1.xyzrgb pcd molecule2.pcd slog optim
# ./sensaas.py dot molecule1-dots.pdb xyzrgb molecule2.xyzrgb slog optim

import os, shutil
import sys
import re
import platform
import open3d as o3d
import numpy as np
import time
from GCICP import *
from ReadDotsPDB import *
from SaveSDFtran import *
from SavePDBtran import *
from XYZRGB2labels import *
from SDFtoDots import *
from PDBtoDots import *

start_time = time.perf_counter()

if len(sys.argv) < 7:
    print(
        "usage: sensaas.py target-type target-file-name source-type source-file-name slog optim\n"
        "eg:\nsensaas.py sdf DATASET/IMATINIB.sdf sdf DATASET/IMATINIB-part1.sdf slog optim"
    )
    sys.exit(1)

targettype, target, sourcetype, source, output, mode = sys.argv[1:7]

sensaasexe = sys.argv[0]
sensaasexe = re.sub(r'sensaas\.py$', '', sensaasexe)

if sensaasexe and not sensaasexe.endswith(os.sep):
    sensaasexe += os.sep

current_platform = platform.system().lower()
if 'linux' in current_platform or 'darwin' in current_platform:
    nscexe = os.path.join(sensaasexe, 'nsc')
else:
    nscexe = os.path.join(sensaasexe, 'nsc-win.exe')

verbose = 0

#######################################
# MAIN program

fd = open(output, 'w')
fd.write('SENSAAS executables at %s\n' % (sensaasexe))
fd.write('Open3D version %s\n' % (o3d.__version__))

#PARAMETERS:

#threshold to evaluate correspondence set = dots that match (fitness and rmse) in GCICP.py
# molecular surface space between dots = 0.3 then threshold = 0.3-0.4
threshold = 0.3

fd.write("#label 1 {H, Cl, Br, I}\n")
fd.write("#label 2 {O, N, S, F, HO, HN}\n")
fd.write("#label 3 {C, P, B}\n")
fd.write("#label 4 {others}\n")
fd.write('Threshold for evaluation (maximum correspondence points-pair distance) = %3.3f\n' % (threshold))

# ALGORITHM:

#TARGET
##Generate or upload surfaces and create label tables
fd.write("Target that does not move:\n")
if targettype == "sdf":
    pcdxyz, pcdrgb, pcd1xyz, pcd1rgb, pcd2xyz, pcd2rgb, pcd3xyz, pcd3rgb, pcd4xyz, pcd4rgb = sdfsurface(target, nscexe)
elif targettype == "pdb":
    pcdxyz, pcdrgb, pcd1xyz, pcd1rgb, pcd2xyz, pcd2rgb, pcd3xyz, pcd3rgb, pcd4xyz, pcd4rgb = pdbsurface(target, nscexe)
elif targettype == "dot":
    read_pdbdot(target)
    os.rename("dots.xyzrgb", "Target.xyzrgb")
    pcdxyz, pcdrgb, pcd1xyz, pcd1rgb, pcd2xyz, pcd2rgb, pcd3xyz, pcd3rgb, pcd4xyz, pcd4rgb = xyzrgb2labels("Target.xyzrgb")
    os.remove("Target.xyzrgb")
elif targettype == "xyzrgb":
    pcdxyz, pcdrgb, pcd1xyz, pcd1rgb, pcd2xyz, pcd2rgb, pcd3xyz, pcd3rgb, pcd4xyz, pcd4rgb = xyzrgb2labels(target)
elif targettype == "pcd":
    target_pcd = o3d.io.read_point_cloud(target)
    o3d.io.write_point_cloud("Target.xyzrgb", target_pcd)
    pcdxyz, pcdrgb, pcd1xyz, pcd1rgb, pcd2xyz, pcd2rgb, pcd3xyz, pcd3rgb, pcd4xyz, pcd4rgb = xyzrgb2labels("Target.xyzrgb")
    os.remove("Target.xyzrgb")
else:
    raise ValueError(f"Unsupported targettype: {targettype}")


valid_types = {"xyzrgb", "pcd", "dot", "sdf", "pdb"}

if targettype in valid_types:
    target_pcd = o3d.geometry.PointCloud()
    pcdt1 = o3d.geometry.PointCloud()
    pcdt2 = o3d.geometry.PointCloud()
    pcdt3 = o3d.geometry.PointCloud()
    pcdt4 = o3d.geometry.PointCloud()

    # Assign points and colors efficiently
    target_pcd.points = o3d.utility.Vector3dVector(pcdxyz)
    target_pcd.colors = o3d.utility.Vector3dVector(pcdrgb)

    pcdt1.points = o3d.utility.Vector3dVector(pcd1xyz)
    pcdt1.colors = o3d.utility.Vector3dVector(pcd1rgb)

    pcdt2.points = o3d.utility.Vector3dVector(pcd2xyz)
    pcdt2.colors = o3d.utility.Vector3dVector(pcd2rgb)

    pcdt3.points = o3d.utility.Vector3dVector(pcd3xyz)
    pcdt3.colors = o3d.utility.Vector3dVector(pcd3rgb)

    pcdt4.points = o3d.utility.Vector3dVector(pcd4xyz)
    pcdt4.colors = o3d.utility.Vector3dVector(pcd4rgb)

    if verbose == 1:
        filenames = [
            ("Target.pcd", target_pcd),
            ("Target.xyzrgb", target_pcd),
            ("Tlabel1.xyzrgb", pcdt1),
            ("Tlabel2.xyzrgb", pcdt2),
            ("Tlabel3.xyzrgb", pcdt3),
            ("Tlabel4.xyzrgb", pcdt4),
        ]
        for fname, pcd in filenames:
            o3d.io.write_point_cloud(fname, pcd)


##Create pcd objects required for open3d tools
#target_pcd already loaded (see above)
Tlabel = len(target_pcd.points)
fd.write('Object nb-points [ label1 label2 label3 label4]' + "\n")
Tlabel1 = len(pcdt1.points)
Tlabel2 = len(pcdt2.points)
Tlabel3 = len(pcdt3.points)
Tlabel4 = len(pcdt4.points)
fd.write('Target %8s [%8s %8s %8s %8s]' % (Tlabel, Tlabel1, Tlabel2, Tlabel3, Tlabel4) +"\n")
#print(Tlabel, Tlabel1, Tlabel2, Tlabel3, Tlabel4) 

#SOURCE
##Generate or upload surfaces and create label tables
fd.write("Source to align/move on Target:\n")
if sourcetype == "sdf":
    pcdxyz, pcdrgb, pcd1xyz, pcd1rgb, pcd2xyz, pcd2rgb, pcd3xyz, pcd3rgb, pcd4xyz, pcd4rgb = sdfsurface(source, nscexe)
elif sourcetype == "pdb":
    pcdxyz, pcdrgb, pcd1xyz, pcd1rgb, pcd2xyz, pcd2rgb, pcd3xyz, pcd3rgb, pcd4xyz, pcd4rgb = pdbsurface(source, nscexe)
elif sourcetype == "dot":
    read_pdbdot(source)
    os.rename("dots.xyzrgb", "Source.xyzrgb")
    pcdxyz, pcdrgb, pcd1xyz, pcd1rgb, pcd2xyz, pcd2rgb, pcd3xyz, pcd3rgb, pcd4xyz, pcd4rgb = xyzrgb2labels("Source.xyzrgb")
    os.remove("Source.xyzrgb")
elif sourcetype == "xyzrgb":
    pcdxyz, pcdrgb, pcd1xyz, pcd1rgb, pcd2xyz, pcdrgb, pcd3xyz, pcd3rgb, pcd4xyz, pcd4rgb = xyzrgb2labels(source)
elif sourcetype == "pcd":
    source_pcd = o3d.io.read_point_cloud(source)
    o3d.io.write_point_cloud("Source.xyzrgb", source_pcd)
    pcdxyz, pcdrgb, pcd1xyz, pcd1rgb, pcd2xyz, pcd2rgb, pcd3xyz, pcd3rgb, pcd4xyz, pcd4rgb = xyzrgb2labels("Source.xyzrgb")
    os.remove("Source.xyzrgb")

if sourcetype in {"xyzrgb", "pcd", "dot", "sdf", "pdb"}:
    source_pcd = o3d.geometry.PointCloud()
    pcds1 = o3d.geometry.PointCloud()
    pcds2 = o3d.geometry.PointCloud()
    pcds3 = o3d.geometry.PointCloud()
    pcds4 = o3d.geometry.PointCloud()

    source_pcd.points = o3d.utility.Vector3dVector(pcdxyz)
    source_pcd.colors = o3d.utility.Vector3dVector(pcdrgb)

    pcds1.points = o3d.utility.Vector3dVector(pcd1xyz)
    pcds1.colors = o3d.utility.Vector3dVector(pcd1rgb)

    pcds2.points = o3d.utility.Vector3dVector(pcd2xyz)
    pcds2.colors = o3d.utility.Vector3dVector(pcd2rgb)

    pcds3.points = o3d.utility.Vector3dVector(pcd3xyz)
    pcds3.colors = o3d.utility.Vector3dVector(pcd3rgb)

    pcds4.points = o3d.utility.Vector3dVector(pcd4xyz)
    pcds4.colors = o3d.utility.Vector3dVector(pcd4rgb)

    if verbose == 1:
        o3d.io.write_point_cloud("Source.pcd", source_pcd)
        o3d.io.write_point_cloud("Source.xyzrgb", source_pcd)
        o3d.io.write_point_cloud("Slabel1.xyzrgb", pcds1)
        o3d.io.write_point_cloud("Slabel2.xyzrgb", pcds2)
        o3d.io.write_point_cloud("Slabel3.xyzrgb", pcds3)
        o3d.io.write_point_cloud("Slabel4.xyzrgb", pcds4)

##Create pcd objects required for open3d tools
#source_pcd already loaded (see above)
Slabel  = len(source_pcd.points)
fd.write('Object nb-points [ label1 label2 label3 label4]' + "\n")
Slabel1 = len(pcds1.points)
Slabel2 = len(pcds2.points)
Slabel3 = len(pcds3.points)
Slabel4 = len(pcds4.points)
#print(Slabel, Slabel1, Slabel2, Slabel3, Slabel4)
fd.write('Source %8s [%8s %8s %8s %8s]' % (Slabel, Slabel1, Slabel2, Slabel3, Slabel4) +"\n\n")
fd.close()

# EXECUTE
#mode = optimisation (default)
if mode != 'eval' :
    ## gcicp = Global + CICP registration (see subroutines)
    tran=gcicp_registration(source_pcd,target_pcd,threshold,output,pcds2,pcds3,pcds4,pcdt2,pcdt3,pcdt4,Slabel2,Slabel3,Slabel4)
else:
    tran=np.identity(4)

fd = open(output, 'a')

#fitness for all dots (no color)
#print("Threshold for evaluation (maximum correspondence points-pair distance) = %3.3f" % (threshold))
fd.write('\nSelected solution (best gfit + hfit):\n')
#open0.7
#score=o3d.registration.evaluate_registration(source_pcd,target_pcd,threshold,tran)
#open0.12 add ".pipelines"
score=o3d.pipelines.registration.evaluate_registration(source_pcd,target_pcd,threshold,tran)
fitness=score.fitness
rmse=score.inlier_rmse
dots=len(score.correspondence_set)
fitnesstarget=dots/float(Tlabel)
#print("gfit= %3.3f Source_matching_all_dots= %5s rmse_all_dots= %3.3f" % (fitness,dots,rmse))
fd.write('gfit %3.3f Source_matching_all_dots= %5s rmse_all_dots= %3.3f (Target_gfit= %3.3f)\n' % (fitness,dots,rmse,fitnesstarget))

#fitness for each group of color

#label 1
#open0.7
#score=o3d.registration.evaluate_registration(pcds1,pcdt1,threshold,tran)
#open0.12
score=o3d.pipelines.registration.evaluate_registration(pcds1,pcdt1,threshold,tran)
fitness1=score.fitness
rmse1=score.inlier_rmse
dots1=len(score.correspondence_set)
#print("fit_label1= %3.3f Source_matching_dots_label1= %5s rmse_label1= %3.3f" % (fitness1,dots1,rmse1))
fd.write('fit_label1 %3.3f Source_matching_dots_label1= %5s rmse_label1= %3.3f\n' % (fitness1,dots1,rmse1))

#label 2
#open0.7
#score=o3d.registration.evaluate_registration(pcds2,pcdt2,threshold,tran)
#open0.12
score=o3d.pipelines.registration.evaluate_registration(pcds2,pcdt2,threshold,tran)
fitness2=score.fitness
rmse2=score.inlier_rmse
dots2=len(score.correspondence_set)
#print("fit_label2= %3.3f Source_matching_dots_label2= %5s rmse_label2= %3.3f" % (fitness2,dots2,rmse2))
fd.write('fit_label2 %3.3f Source_matching_dots_label2= %5s rmse_label2= %3.3f\n' % (fitness2,dots2,rmse2))

#label 3
#open0.7
#score=o3d.registration.evaluate_registration(pcds3,pcdt3,threshold,tran)
#open0.12
score=o3d.pipelines.registration.evaluate_registration(pcds3,pcdt3,threshold,tran)
fitness3=score.fitness
rmse3=score.inlier_rmse
dots3=len(score.correspondence_set)
#print("fit_label3= %3.3f Source_matching_dots_label3= %5s rmse_label3= %3.3f" % (fitness3,dots3,rmse3))
fd.write('fit_label3 %3.3f Source_matching_dots_label3= %5s rmse_label3= %3.3f\n' % (fitness3,dots3,rmse3))

#label 4
#open0.7
#score=o3d.registration.evaluate_registration(pcds4,pcdt4,threshold,tran)
#open0.12
score=o3d.pipelines.registration.evaluate_registration(pcds4,pcdt4,threshold,tran)
fitness4=score.fitness
rmse4=score.inlier_rmse
dots4=len(score.correspondence_set)
#print("fit_label4= %3.3f Source_matching_dots_label4= %5s rmse_label4= %3.3f" % (fitness4,dots4,rmse4))
fd.write('fit_label4 %3.3f Source_matching_dots_label4= %5s rmse_label4= %3.3f\n' % (fitness4,dots4,rmse4))

cfit = (dots1 + dots2 + dots3 + dots4) / float(Slabel)

hfit = 0.0
sumfit = fitness
non_label1 = float(Slabel - Slabel1)

if non_label1 != 0.0:
    hfit = (dots2 + dots3 + dots4) / non_label1
    sumfit += hfit
    
#print("gfit= %3.3f cfit= %3.3f hfit= %3.3f" % (fitness,cfit,hfit))
fd.write('gfit= %3.3f cfit= %3.3f hfit= %3.3f gfit+hfit= %3.3f\n' % (fitness,cfit,hfit,sumfit))

if mode != 'eval':
    np.savetxt('tran.txt', tran)

    # Save transformed/superimposed source input file
    if sourcetype == "sdf":
        save_trans_sdf(source, tran, "Source_tran.sdf")
    elif sourcetype in {"pdb", "dot"}:
        ext = "dots_tran.pdb" if sourcetype == "dot" else "Source_tran.pdb"
        save_trans_pdb(source, tran, ext)
    elif sourcetype in {"pcd", "xyzrgb"}:
        source_pcd_tran = source_pcd.transform(tran)
        ext = "Source_tran.pcd" if sourcetype == "pcd" else "Source_tran.xyzrgb"
        o3d.io.write_point_cloud(ext, source_pcd_tran)


## End
fd.close()

if verbose == 1:
    print ("Done (see %s)" % output)

end_time = time.perf_counter()
elapsed_time = end_time - start_time

print(f"Execution time: {elapsed_time:.6f} seconds")

#######################################
