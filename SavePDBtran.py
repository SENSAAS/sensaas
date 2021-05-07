#!/usr/bin/python3.7

import os, sys
import numpy as np
import re

def save_trans_pdb(PDBfile,tran,output):
    
    filepdb=open(PDBfile,'r')
    getstr=filepdb.read().split('\n')
    filepdb.close()

    longa=len(getstr)
    xyz=np.empty(shape=[longa,3], dtype=np.float64)
    compt=0
    compt2=0
    while(compt < longa):
        tabLine=re.split(' +', getstr[compt].strip())
        #print(tabLine)
        if(tabLine[0]=="HETATM" or tabLine[0]=="ATOM"):
            x=float(tabLine[5])
            y=float(tabLine[6])
            z=float(tabLine[7])
            xyz[compt2,:]=[x,y,z]
            compt2=compt2+1
        compt=compt+1

    nbatom=compt2
    #print("nbatom= %3s" % (nbatom))
    #print(xyz)
    
    #create a matrix with 1 everywhere with size = xyz.shape[0]
    arr_xyz1 = np.ones((xyz.shape[0],4))
    #fill with xyz
    arr_xyz1[:,0:3] = xyz
    # multiply the rigid transformation to obtain the transformed data
    xyz_tran = np.matmul(tran,(arr_xyz1.T))[0:3,:].T
    #print(xyz_tran)

    fd = open(output, 'w')
    compt=0
    compt2=0
    while (compt < longa):
        tabLine=re.split(' +', getstr[compt].strip())
        if(tabLine[0]=="HETATM" or tabLine[0]=="ATOM"):
            line=getstr[compt]
            #print(line)
            x=str('%5.3f' % (xyz_tran[compt2,[0]]))
            y=str('%5.3f' % (xyz_tran[compt2,[1]]))
            z=str('%5.3f' % (xyz_tran[compt2,[2]]))
            #char 30 to 53 (begin at 0)
            coord=str('%8s%8s%8s' % (x,y,z))
            line2="".join((line[:30],coord,line[54:]))
            #print(line2)
            fd.write(line2 + '\n')
            compt2=compt2+1
        else:
            if(compt==(longa-1)):
                fd.write(getstr[compt])
            else:
                fd.write(getstr[compt]+'\n')
        compt=compt+1

    fd.close()
    return

##################################

