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
import os, sys
import re
import open3d as o3d
import numpy as np
from sys import platform
from GCICP import *
from ReadDotsPDB import *
from SaveSDFtran import *
from SavePDBtran import *
from XYZRGB2labels import *
from SDFtoDots import *
from PDBtoDots import *

import argparse

# List of supported file types for source and target
filetypes = ["sdf", "pdb", "dot", "xyzrgb", "pcd"]

p = argparse.ArgumentParser(
    description="SenSaaS: Shape-based Alignment by Registration of Colored Point-based Surfaces"
)
p.add_argument("targettype", type=str, help="Target file type", choices=filetypes)
p.add_argument("target", type=str, help="Target file")
p.add_argument("sourcetype", type=str, help="Source file type", choices=filetypes)
p.add_argument("source", type=str, help="Source file")
p.add_argument("output", type=str, help="Output (log file)")
p.add_argument("mode", type=str, help="Mode", choices=["optim", "eval"])
p.add_argument("-v", "--verbose", action="store_true", help="Verbose mode (keep all files)")
p.add_argument("-t", "--threshold", type=float, default=0.3, help="Threshold to evaluate correspondence set")
p.add_argument("-vs", "--voxel_sizes", type=float, nargs="+",
               default=[0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2],
               help="Threshold to evaluate correspondence set")

args = p.parse_args()

# sys.argv[0] is the name of the program itself
sensaasexe = p.prog  # p.prog defaults to sys.argv[0])
sensaasexe=re.sub('sensaas\.py','',sensaasexe)

targettype = args.targettype
target = args.target
sourcetype = args.sourcetype
source = args.source
output = args.output
mode = args.mode

#sensaasexe="./"
#if environment variable is set (eg: .bashr SENSAASBASE=/home/user/sensaas-executables )
#sensaasexe=os.environ['SENSAASBASE'] + "/"

#path for nsc (required by SDFtoDots.py and PDBtoDots.py)
#print(platform)
whichexe='linux'
if(whichexe in platform):
    # linux
    nscexe=sensaasexe + "nsc"
elif platform == "darwin":
    # OS X - linux version?
    nscexe=sensaasexe + "nsc"
else:
    #windows
    nscexe=sensaasexe + "nsc-win.exe"
#print(nscexe)

#verbose=0 (keep important files only) or verbose=1
verbose = 1 if args.verbose else 0

#######################################
# MAIN program

fd = open(output, 'w')
fd.write('SENSAAS executables at %s\n' % (sensaasexe))
fd.write('Open3D version %s\n' % (o3d.__version__))

#PARAMETERS:

#threshold to evaluate correspondence set = dots that match (fitness and rmse) in GCICP.py
# molecular surface space between dots = 0.3 then threshold = 0.3-0.4
threshold = args.threshold

fd.write("#label 1 {H, Cl, Br, I}\n")
fd.write("#label 2 {O, N, S, F, HO, HN}\n")
fd.write("#label 3 {C, P, B}\n")
fd.write("#label 4 {others}\n")
fd.write('Threshold for evaluation (maximum correspondence points-pair distance) = %3.3f\n' % (threshold))

# ALGORITHM:

#TARGET
##Generate or upload surfaces and create label tables
fd.write("Target that does not move:\n")
if (targettype=="sdf"):
    pcdxyz,pcdrgb,pcd1xyz,pcd1rgb,pcd2xyz,pcd2rgb,pcd3xyz,pcd3rgb,pcd4xyz,pcd4rgb = sdfsurface(target,nscexe)
elif (targettype=="pdb"):
    pcdxyz,pcdrgb,pcd1xyz,pcd1rgb,pcd2xyz,pcd2rgb,pcd3xyz,pcd3rgb,pcd4xyz,pcd4rgb = pdbsurface(target,nscexe)
elif (targettype=="dot"):
    read_pdbdot(target)
    os.rename("dots.xyzrgb","Target.xyzrgb")
    pcdxyz,pcdrgb,pcd1xyz,pcd1rgb,pcd2xyz,pcd2rgb,pcd3xyz,pcd3rgb,pcd4xyz,pcd4rgb = xyzrgb2labels("Target.xyzrgb")
    os.remove("Target.xyzrgb")
elif (targettype=="xyzrgb"):
    pcdxyz,pcdrgb,pcd1xyz,pcd1rgb,pcd2xyz,pcd2rgb,pcd3xyz,pcd3rgb,pcd4xyz,pcd4rgb = xyzrgb2labels(target)
elif (targettype=="pcd"):
    target_pcd = o3d.io.read_point_cloud(target)
    #convert to ascii file
    o3d.io.write_point_cloud("Target.xyzrgb",target_pcd)
    pcdxyz,pcdrgb,pcd1xyz,pcd1rgb,pcd2xyz,pcd2rgb,pcd3xyz,pcd3rgb,pcd4xyz,pcd4rgb = xyzrgb2labels("Target.xyzrgb")
    os.remove("Target.xyzrgb")

if(targettype=="xyzrgb" or targettype=="pcd" or targettype=="dot" or targettype=="sdf" or targettype=="pdb"):
    target_pcd = o3d.geometry.PointCloud()
    pcdt1 = o3d.geometry.PointCloud()
    pcdt2 = o3d.geometry.PointCloud()
    pcdt3 = o3d.geometry.PointCloud()
    pcdt4 = o3d.geometry.PointCloud()
    target_pcd.points=o3d.utility.Vector3dVector(pcdxyz)
    target_pcd.colors=o3d.utility.Vector3dVector(pcdrgb)
    pcdt1.points=o3d.utility.Vector3dVector(pcd1xyz)
    pcdt1.colors=o3d.utility.Vector3dVector(pcd1rgb)
    pcdt2.points=o3d.utility.Vector3dVector(pcd2xyz)
    pcdt2.colors=o3d.utility.Vector3dVector(pcd2rgb)
    pcdt3.points=o3d.utility.Vector3dVector(pcd3xyz)
    pcdt3.colors=o3d.utility.Vector3dVector(pcd3rgb)
    pcdt4.points=o3d.utility.Vector3dVector(pcd4xyz)
    pcdt4.colors=o3d.utility.Vector3dVector(pcd4rgb)
    if(verbose==1):
        o3d.io.write_point_cloud("Target.pcd",target_pcd)
        o3d.io.write_point_cloud("Target.xyzrgb",target_pcd)
        o3d.io.write_point_cloud("Tlabel1.xyzrgb",pcdt1)
        o3d.io.write_point_cloud("Tlabel2.xyzrgb",pcdt2)
        o3d.io.write_point_cloud("Tlabel3.xyzrgb",pcdt3)
        o3d.io.write_point_cloud("Tlabel4.xyzrgb",pcdt4)

##Create pcd objects required for open3d tools
#target_pcd already loaded (see above)
Tlabel = len(np.asarray(target_pcd.points))
fd.write('Object nb-points [ label1 label2 label3 label4]' + "\n")
Tlabel1 = len(np.asarray(pcdt1.points))
Tlabel2 = len(np.asarray(pcdt2.points))
Tlabel3 = len(np.asarray(pcdt3.points))
Tlabel4 = len(np.asarray(pcdt4.points))
fd.write('Target %8s [%8s %8s %8s %8s]' % (Tlabel, Tlabel1, Tlabel2, Tlabel3, Tlabel4) +"\n")
#print(Tlabel, Tlabel1, Tlabel2, Tlabel3, Tlabel4) 

#SOURCE
##Generate or upload surfaces and create label tables
fd.write("Source to align/move on Target:\n")
if (sourcetype=="sdf"):
    pcdxyz,pcdrgb,pcd1xyz,pcd1rgb,pcd2xyz,pcd2rgb,pcd3xyz,pcd3rgb,pcd4xyz,pcd4rgb = sdfsurface(source,nscexe)
elif (sourcetype=="pdb"):
    pcdxyz,pcdrgb,pcd1xyz,pcd1rgb,pcd2xyz,pcd2rgb,pcd3xyz,pcd3rgb,pcd4xyz,pcd4rgb = pdbsurface(source,nscexe)
elif (sourcetype=="dot"):
    read_pdbdot(source)
    os.rename("dots.xyzrgb","Source.xyzrgb")
    pcdxyz,pcdrgb,pcd1xyz,pcd1rgb,pcd2xyz,pcd2rgb,pcd3xyz,pcd3rgb,pcd4xyz,pcd4rgb = xyzrgb2labels("Source.xyzrgb")
    os.remove("Source.xyzrgb")
elif (sourcetype=="xyzrgb"):
    pcdxyz,pcdrgb,pcd1xyz,pcd1rgb,pcd2xyz,pcd2rgb,pcd3xyz,pcd3rgb,pcd4xyz,pcd4rgb = xyzrgb2labels(source)
elif (sourcetype=="pcd"):
    source_pcd = o3d.io.read_point_cloud(source)
    o3d.io.write_point_cloud("Source.xyzrgb",source_pcd)
    #convert to ascii file
    pcdxyz,pcdrgb,pcd1xyz,pcd1rgb,pcd2xyz,pcd2rgb,pcd3xyz,pcd3rgb,pcd4xyz,pcd4rgb = xyzrgb2labels("Source.xyzrgb")
    os.remove("Source.xyzrgb")

if(sourcetype=="xyzrgb" or sourcetype=="pcd" or sourcetype=="dot" or sourcetype=="sdf" or sourcetype=="pdb"):
    source_pcd = o3d.geometry.PointCloud()
    pcds1 = o3d.geometry.PointCloud()
    pcds2 = o3d.geometry.PointCloud()
    pcds3 = o3d.geometry.PointCloud()
    pcds4 = o3d.geometry.PointCloud()
    source_pcd.points=o3d.utility.Vector3dVector(pcdxyz)
    source_pcd.colors=o3d.utility.Vector3dVector(pcdrgb)
    pcds1.points=o3d.utility.Vector3dVector(pcd1xyz)
    pcds1.colors=o3d.utility.Vector3dVector(pcd1rgb)
    pcds2.points=o3d.utility.Vector3dVector(pcd2xyz)
    pcds2.colors=o3d.utility.Vector3dVector(pcd2rgb)
    pcds3.points=o3d.utility.Vector3dVector(pcd3xyz)
    pcds3.colors=o3d.utility.Vector3dVector(pcd3rgb)
    pcds4.points=o3d.utility.Vector3dVector(pcd4xyz)
    pcds4.colors=o3d.utility.Vector3dVector(pcd4rgb)
    if(verbose==1):
        o3d.io.write_point_cloud("Source.pcd",source_pcd)
        o3d.io.write_point_cloud("Source.xyzrgb",source_pcd)
        o3d.io.write_point_cloud("Slabel1.xyzrgb",pcds1)
        o3d.io.write_point_cloud("Slabel2.xyzrgb",pcds2)
        o3d.io.write_point_cloud("Slabel3.xyzrgb",pcds3)
        o3d.io.write_point_cloud("Slabel4.xyzrgb",pcds4)

##Create pcd objects required for open3d tools
#source_pcd already loaded (see above)
Slabel = len(np.asarray(source_pcd.points))
fd.write('Object nb-points [ label1 label2 label3 label4]' + "\n")
Slabel1 = len(np.asarray(pcds1.points))
Slabel2 = len(np.asarray(pcds2.points))
Slabel3 = len(np.asarray(pcds3.points))
Slabel4 = len(np.asarray(pcds4.points))
#print(Slabel, Slabel1, Slabel2, Slabel3, Slabel4)
fd.write('Source %8s [%8s %8s %8s %8s]' % (Slabel, Slabel1, Slabel2, Slabel3, Slabel4) +"\n\n")
fd.close()

# EXECUTE
#mode = optimisation (default)
if mode != 'eval' :
    ## gcicp = Global + CICP registration (see subroutines)
    tran=gcicp_registration(source_pcd,target_pcd,threshold,output,pcds2,pcds3,pcds4,pcdt2,pcdt3,pcdt4,Slabel2,Slabel3,Slabel4, args.voxel_sizes)
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

cfit = (dots1 + dots2 + dots3 + dots4) /float(Slabel)
hfit=0
sumfit=0
if((float(Slabel) - float(Slabel1)) != 0):
    hfit = (dots2 + dots3 + dots4) / (float(Slabel) - float(Slabel1))
    sumfit=fitness+hfit
else:
    sumfit=fitness
    
#print("gfit= %3.3f cfit= %3.3f hfit= %3.3f" % (fitness,cfit,hfit))
fd.write('gfit= %3.3f cfit= %3.3f hfit= %3.3f gfit+hfit= %3.3f\n' % (fitness,cfit,hfit,sumfit))

if mode != 'eval' :
    #print tran
    np.savetxt('tran.txt', tran)

    ## Print transformed/superimposed source input file
    if(sourcetype=="sdf"):
        #save in Source_tran.sdf
        save_trans_sdf(source,tran,"Source_tran.sdf")

    if(sourcetype=="pdb"):
        #save in Source_tran.pdb
        save_trans_pdb(source,tran,"Source_tran.pdb")

    if(sourcetype=="dot"):
        #save in Source-dots_tran.pdb
        save_trans_pdb(source,tran,"Source-dots_tran.pdb")
    
    if(sourcetype=="pcd"):
        #save in Source_tran.pcd
        source_pcd_tran=source_pcd.transform(tran)
        o3d.io.write_point_cloud("Source_tran.pcd",source_pcd_tran)

    if(sourcetype=="xyzrgb"):
        #save in Source_tran.xyzrgb
        source_pcd_tran=source_pcd.transform(tran)
        o3d.io.write_point_cloud("Source_tran.xyzrgb",source_pcd_tran)

## End
fd.close()

if(verbose==1):
    print ("Done (see %s)" % output)

#######################################
