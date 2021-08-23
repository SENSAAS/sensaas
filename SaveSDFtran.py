#!/usr/bin/python3.7

import os, sys
import numpy as np
import re

def save_trans_sdf(SDFfile,tran,output):
    
    filesdf=open(SDFfile,'r')
    getstr=filesdf.read().split('\n')
    filesdf.close()

    tabLignesSdf=[]
    tabLignesSdf.append(re.split('\s+', getstr[3].strip()))
    testspace=[]
    testspace.append(re.split('', getstr[3]))
    if(len(tabLignesSdf[0][0]) > 2):
        if(testspace[0][1]==' '):
            tabLignesSdf[0][1]=tabLignesSdf[0][0][2:]
            tabLignesSdf[0][0]=tabLignesSdf[0][0][0:2]
        elif(testspace[0][4]!=' '):
            tabLignesSdf[0][1]=tabLignesSdf[0][0][3:]
            tabLignesSdf[0][0]=tabLignesSdf[0][0][:3]
        nbatom=int(tabLignesSdf[0][0])
        nbbond=int(tabLignesSdf[0][1])
    else:
        nbatom=int(tabLignesSdf[0][0])
        nbbond=int(tabLignesSdf[0][1])
    #print("nbatom= %3s nbbond= %3s" % (nbatom,nbbond))
    
    xyz=np.empty(shape=[nbatom,3], dtype=np.float64)
    compt=4
    compt2=0
    while(compt < (4+nbatom)):
        tabLine=re.split(' +', getstr[compt].strip())
        x=float(tabLine[0])
        y=float(tabLine[1])
        z=float(tabLine[2])
        #print(tabLine)
        #print("x= %6s y= %6s z= %6s" %(x,y,z))
        xyz[compt2,:]=[x,y,z] 
        compt=compt+1
        compt2=compt2+1
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
    while (compt < len(getstr)):
        if(compt>=4 and compt <(nbatom+4)):
            line=""
            tabLine=re.split(' +', getstr[compt].strip())
            #print(tabLine)
            tabLine[0]=str('%5.3f' % (xyz_tran[compt2,[0]]))
            tabLine[1]=str('%5.3f' % (xyz_tran[compt2,[1]]))
            tabLine[2]=str('%5.3f' % (xyz_tran[compt2,[2]]))
            #print(tabLine)
            line=line + str('%10s%10s%10s' % (tabLine[0],tabLine[1],tabLine[2]))
            elt=tabLine[3]
            longa=len(tabLine[3])
            if(longa==1):
                line=line + ' ' + str('%1s' % tabLine[3]) + ' '
            else:
                line=line + ' ' + str('%2s' % tabLine[3])
            maxi=len(tabLine)
            for i in range(4,maxi):
                line=line + ' ' + str('%2s' % tabLine[i])
            fd.write(line+'\n')
        else:
            if(compt==(len(getstr)-1)):
                fd.write(getstr[compt])
            else:
                fd.write(getstr[compt]+'\n')
        if(compt>=4):
            compt2=compt2+1
        compt=compt+1
    
    fd.close()
    return

##################################
