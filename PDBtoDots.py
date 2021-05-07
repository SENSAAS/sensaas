#!/usr/bin/python3.7

#Author: Lucas GRANDMOUGIN 

import sys
import os
import math
import re
import numpy as np

#print('usage: <>.py <file.pdb> \nexecute nsc to generate point-based surface and create tables and if verbose==1 files dotslabel1.xyzrgb dotslabel2.xyzrgb dotslabel3.xyzrgb and dotslabel4.xyzrgb\n')

def pdbsurface(filepdb,nscexe):

    verbose=0

#label1 {H, Cl, Br, I} white/grey 0.9 0.9 0.9
#label2 {O, N, S, F} red 1 0 0
#label3 {C, P, B} green 0 1 0
#label4 {others} blue 0 0 1

    tabR= {'C':'%.2f' % 1.70, 'O':1.52, 'N':1.55, 'S':1.80, 'P':1.80, 'B':1.72, 'Br':1.85, 'Cl':1.75, 'I':1.98, 'F':1.47, 'H':'%.2f' % 1.20, 'Hp':'%.2f' % 1.10, 'X':'%.2f' % 1.10}
    label= {'C':3, 'P':3, 'B':3, 'O':2, 'N':2, 'S':2, 'F':2, 'Hp':2, 'H':1, 'Cl':1, 'Br':1, 'I':1}
    rgb= np.array([[0, 0, 0], [0.9, 0.9, 0.9], [1, 0, 0], [0, 1, 0], [0, 1, 0]])

    espace5=' '
    espace6='       '

    fichier2D=0

    filepdb=open(filepdb,'r')
    getstr=filepdb.read().split('\n')
    filepdb.close()

    tabLignesPdb=[]
    tabLignesPdb.append('')

    compt=1
    while (compt < len(getstr)):
        tabLignesPdb.append(re.split('\s+', getstr[compt].strip()))
        compt=compt+1

    compt=1
    comptatomes=0
    getx=[]
    getx.append('')
    gety=[]
    gety.append('')
    getz=[]
    getz.append('')
    getA=[]
    getA.append('')
    getRayon=[]
    getRayon.append('')
    while (compt < len(tabLignesPdb)):
        if (tabLignesPdb[compt][0] == 'HETATM' or tabLignesPdb[compt][0] == 'ATOM'):
            xAtome=float(tabLignesPdb[compt][5])
            yAtome=float(tabLignesPdb[compt][6])
            zAtome=float(tabLignesPdb[compt][7])
            getx.append(xAtome)
            gety.append(yAtome)
            getz.append(zAtome)
            if (float(zAtome) == 0):
                fichier2D=fichier2D+1
            getA.append(tabLignesPdb[compt][2])
            getRayon.append(tabR[getA[compt]])
            comptatomes=comptatomes+1
        compt=compt+1

    nbatomes=comptatomes
    
    if (fichier2D==int(nbatomes)):
        print("Warning: pdb file in 2D; SenSaaS needs 3D coordinates to work properly")

    compt=1
    while (compt <= nbatomes):
        if (getA[compt] == 'H'):
            compt2=1
            while(compt2 <= nbatomes):
                if (getA[compt2] == 'N' or getA[compt2] == 'O'):
                    distHp= math.sqrt((getx[compt] - getx[compt2])**2 + (gety[compt] - gety[compt2])**2 + (getz[compt] - getz[compt2])**2)
                    if (distHp <= 1.2):
                        getRayon[compt]=tabR['Hp']
                compt2=compt2+1
        compt=compt+1 

#nsc:
    compt=1
    psaIn=open('psa.in','w')
    psaIn.write('* XYZR\n')
    psaIn.write(espace6+str(nbatomes)+'\n')

    while (compt <= nbatomes):
        x='%.2f' % getx[compt]
        y='%.2f' % gety[compt]
        z='%.2f' % getz[compt]
        psaIn.write('%8s %8s %8s %8s %8s \n'%(x,y,z,getRayon[compt],getA[compt]))
        compt=compt+1
    
    psaIn.close()

    cmd = '%s psa.in ' % (nscexe)
    os.system(cmd)

    psaOut=open('psa.out', 'r')
    lignepsaOut= psaOut.readlines()
    psaOut.close()

    tabLignesPsaOut=[]
    compt=3
    while (compt < len(lignepsaOut)):
        tabLignesPsaOut.append(re.split('\s+', lignepsaOut[compt].strip()))
        compt=compt+1

    nbDots= int(tabLignesPsaOut[0][2])
    #print("nbDots= %6s" % (nbDots))
    del tabLignesPsaOut[0]
    del tabLignesPsaOut[0]

    getDots=np.empty(shape=[nbDots,3], dtype='float64')
    getrgb=np.empty(shape=[nbDots,3], dtype='float64')

    compt=nbatomes+2
    comptDots=0
    ligneFicDots=[]
    label1=[]
    label2=[]
    label3=[]
    label4=[]
    if(verbose==1):
        dotsFic=open('dots.xyzrgb', 'w')

    while (compt < nbatomes+nbDots+2):
        xDot=float(tabLignesPsaOut[compt][2])
        yDot=float(tabLignesPsaOut[compt][3])
        zDot=float(tabLignesPsaOut[compt][4])
        compt2=1
        m=100
        mi=0
        while(compt2 <= nbatomes):
            xa=getx[compt2]
            ya=gety[compt2]
            za=getz[compt2]
            goodDots= math.sqrt((xDot - xa)**2 + (yDot - ya)**2 + (zDot - za)**2)
            if(goodDots < m):
                m=goodDots
                mi=compt2
            compt2=compt2+1

        atomeCorrespondant=getA[mi]
        rgbi=label[atomeCorrespondant]
        if(getRayon[mi]==tabR['Hp']):
            rgbi=label['O']

        getrgb[comptDots,:]=[rgb[rgbi,0], rgb[rgbi,1], rgb[rgbi,2]]
        getDots[comptDots,:]=[xDot,yDot,zDot]

        if (getrgb[comptDots, 0] == 0.9):
            label1.append(np.vstack([getDots[comptDots], getrgb[comptDots]]))
        elif (getrgb[comptDots, 0] == 1.0):
            label2.append(np.vstack([getDots[comptDots], getrgb[comptDots]]))
        elif (getrgb[comptDots, 1] == 1.0):
            label3.append(np.vstack([getDots[comptDots], getrgb[comptDots]]))
        elif (getrgb[comptDots, 2] == 1.0):
            label4.append(np.vstack([getDots[comptDots], getrgb[comptDots]]))
        else:
            print("no label for dot no %5s ?\n" %(comptDots))

        if(verbose==1):
            dotsFic.write('%8s'%xDot+'%8s'%yDot+'%8s'%zDot+espace5+'%5s'%(rgb[rgbi,0])+'%5s'%(rgb[rgbi,1])+'%5s'%(rgb[rgbi,2])+'\n')

        comptDots=comptDots+1
        compt=compt+1

    if(verbose==1):
        dotsFic.close()
        dotslabel1=open('dotslabel1.xyzrgb', 'w')
        dotslabel2=open('dotslabel2.xyzrgb', 'w')
        dotslabel3=open('dotslabel3.xyzrgb', 'w')
        dotslabel4=open('dotslabel4.xyzrgb', 'w')

    getDots1=np.empty(shape=[len(label1),3], dtype='float64')
    getrgb1=np.empty(shape=[len(label1),3], dtype='float64')
    getDots2=np.empty(shape=[len(label2),3], dtype='float64')
    getrgb2=np.empty(shape=[len(label2),3], dtype='float64')
    getDots3=np.empty(shape=[len(label3),3], dtype='float64')
    getrgb3=np.empty(shape=[len(label3),3], dtype='float64')
    getDots4=np.empty(shape=[len(label4),3], dtype='float64')
    getrgb4=np.empty(shape=[len(label4),3], dtype='float64')

    compt=0
    while(compt < len(label1)):
        getDots1[compt]= label1[compt][0]
        getrgb1[compt]= label1[compt][1]
        if(verbose==1):
            dotslabel1.write('%8s'%getDots1[compt,0]+'%8s'%getDots1[compt,1]+'%8s'%getDots1[compt,2]+espace5+'%5s'%getrgb1[compt,0]+'%5s'%getrgb1[compt,1]+'%5s'%getrgb1[compt,2]+'\n')
        compt=compt+1

    compt=0
    while(compt < len(getDots2)):
        getDots2[compt]= label2[compt][0]
        getrgb2[compt]= label2[compt][1]
        if(verbose==1):
            dotslabel2.write('%8s'%getDots2[compt,0]+'%8s'%getDots2[compt,1]+'%8s'%getDots2[compt,2]+espace5+'%5s'%getrgb2[compt,0]+'%5s'%getrgb2[compt,1]+'%5s'%getrgb2[compt,2]+'\n')
        compt=compt+1

    compt=0
    while(compt < len(getDots3)):
        getDots3[compt]= label3[compt][0]
        getrgb3[compt]= label3[compt][1]
        if(verbose==1):
            dotslabel3.write('%8s'%getDots3[compt,0]+'%8s'%getDots3[compt,1]+'%8s'%getDots3[compt,2]+espace5+'%5s'%getrgb3[compt,0]+'%5s'%getrgb3[compt,1]+'%5s'%getrgb3[compt,2]+'\n')
        compt=compt+1

    compt=0
    while(compt < len(getDots4)):
        getDots4[compt]= label4[compt][0]
        getrgb4[compt]= label4[compt][1]
        if(verbose==1):
            dotslabel4.write('%8s'%getDots4[compt,0]+'%8s'%getDots4[compt,1]+'%8s'%getDots4[compt,2]+espace5+'%5s'%getrgb4[compt,0]+'%5s'%getrgb4[compt,1]+'%5s'%getrgb4[compt,2]+'\n')
        compt=compt+1

    if(verbose==1):
        dotslabel1.close()
        dotslabel2.close()
        dotslabel3.close()
        dotslabel4.close()
    else:
        os.remove("psa.in")
        os.remove("psa.out")

    return getDots, getrgb, getDots1, getrgb1, getDots2, getrgb2, getDots3, getrgb3, getDots4, getrgb4
