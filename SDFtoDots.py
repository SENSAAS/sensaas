#!/usr/bin/python3.7

#Author: Lucas GRANDMOUGIN 

import sys
import os
import math
import re
import numpy as np
#from subprocess import Popen,PIPE

#print('usage: <>.py <file.sdf> \nexecute nsc to generate point-based surface and create tables and if verbose==1 files dotslabel1.xyzrgb dotslabel2.xyzrgb dotslabel3.xyzrgb and dotslabel4.xyzrgb\n')

def sdfsurface(filesdf,nscexe):

    verbose=0

#label1 {H, Cl, Br, I} white/grey 0.9 0.9 0.9
#label2 {O, N, S, F} red 1 0 0
#label3 {C, P, B} green 0 1 0
#label4 {others} blue 0 0 1

    tabR= {'C':'%.2f' % 1.70, 'O':1.52, 'N':1.55, 'S':1.80, 'P':1.80, 'B':1.72, 'Br':1.85, 'Cl':1.75, 'I':1.98, 'F':1.47, 'H':'%.2f' % 1.20, 'Hp':'%.2f' % 1.10, 'X':'%.2f' % 1.10}
    #no label for 'X' Dummy atoms : no associated dots are saved
    label= {'C':3, 'P':3, 'B':3, 'O':2, 'N':2, 'S':2, 'F':2, 'Hp':2, 'H':1, 'Cl':1, 'Br':1, 'I':1}
    rgb= np.array([[0, 0, 0], [0.9, 0.9, 0.9], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    
    espace5=' '
    espace6='       '

    fichier2D=0

    filesdf=open(filesdf,'r')
    getstr=filesdf.read().split('\n')
    filesdf.close()

    tabLignesSdf=[]

    compt=3
    while(compt < len(getstr)):
        tabLignesSdf.append(re.split('\s+', getstr[compt].strip()))
        compt=compt+1
    testspace=[]
    testspace.append(re.split('', getstr[3]))
    if(len(tabLignesSdf[0][0]) > 2):
        if(testspace[0][1]==' '):
            tabLignesSdf[0][1]=tabLignesSdf[0][0][2:]
            tabLignesSdf[0][0]=tabLignesSdf[0][0][0:2]
        else:
            tabLignesSdf[0][1]=tabLignesSdf[0][0][3:]
            tabLignesSdf[0][0]=tabLignesSdf[0][0][:3]
        nbatomes=int(tabLignesSdf[0][0])
        nbLiaisons=int(tabLignesSdf[0][1])
    else:
        nbatomes=int(tabLignesSdf[0][0])
        nbLiaisons=int(tabLignesSdf[0][1])

    #print(nbatomes)
    #print(nbLiaisons)

    compt=1
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
    while (compt <= nbatomes):  
        xAtome=float(tabLignesSdf[compt][0])
        yAtome=float(tabLignesSdf[compt][1])
        zAtome=float(tabLignesSdf[compt][2])
        getx.append(xAtome)
        gety.append(yAtome)
        getz.append(zAtome)
        if (float(zAtome) == 0):
            fichier2D=fichier2D+1
        getA.append(tabLignesSdf[compt][3])
        if(getA[compt]!='C' and getA[compt]!='O' and getA[compt]!='N' and getA[compt]!='P' and getA[compt]!='B' and getA[compt]!='H' and getA[compt]!='F' and getA[compt]!='Br' and getA[compt]!='Cl' and getA[compt]!='S' and getA[compt]!='I' and getA[compt]!='X' and getA[compt]!='Hp'):
            print("Warning: atom %s set as C because it is not the tab (unusual in medchem)" % getA[compt])
            getA[compt]='C'
        getRayon.append(tabR[getA[compt]])
        compt=compt+1

    if (fichier2D==int(nbatomes)):
        print("Warning: sdf file in 2D; SenSaaS needs 3D coordinates to work properly")

    compt=nbatomes+4
    while (compt < nbatomes+nbLiaisons+1):
        if (((getA[int(getstr[compt][:3])] == 'O') and (getA[int(getstr[compt][3:6])] == 'H')) or (getA[int(getstr[compt][:3])] == 'H') and (getA[int(getstr[compt][3:6])] == 'O')):
            if(getA[int(getstr[compt][:3])]=='H'):
                getRayon[int(getstr[compt][:3])]=tabR['Hp']
            elif(getA[int(getstr[compt][3:6])]=='H'):
                getRayon[int(getstr[compt][3:6])]=tabR['Hp']

        if (((getA[int(getstr[compt][:3])] == 'N') and (getA[int(getstr[compt][3:6])] == 'H')) or (getA[int(getstr[compt][:3])] == 'H') and (getA[int(getstr[compt][3:6])] == 'N')):
            if(getA[int(getstr[compt][:3])]=='H'):
                getRayon[int(getstr[compt][:3])]=tabR['Hp']
            elif(getA[int(getstr[compt][3:6])]=='H'):
                getRayon[int(getstr[compt][3:6])]=tabR['Hp']

        if (int(getstr[compt][3:6]) > nbatomes or int(getstr[compt][3:6]) < 0 or int(getstr[compt][:3]) > nbatomes or int(getstr[compt][:3]) < 0):
            print("invalid atom number %6d or %6d" % (int(getstr[compt][3:6]),int(getstr[compt][:3])))
            quit()

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

    #whichexe='nsc-win'
    #if(whichexe in nscexe):
    #    print("windows")
    #else:
    #    print("linux")
    #    os.system("./nsc ./psa.in") #works only if working directory = directory with python executables
    #    #alternative:
    #    p1=Popen([nscexe,"psa.in"],stdout=PIPE)
    #    p2=p1.communicate()[0]
    #print(nscexe)
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
    labeltot=[]
    label1=[]
    label2=[]
    label3=[]
    label4=[]
    
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

        if(getA[mi]!='X'):
            atomeCorrespondant=getA[mi]
            rgbi=label[atomeCorrespondant]
            if(getRayon[mi]==tabR['Hp']):
                rgbi=label['O']
            
            getrgb[comptDots,:]=[rgb[rgbi,0], rgb[rgbi,1], rgb[rgbi,2]]
            getDots[comptDots,:]=[xDot,yDot,zDot]

            labeltot.append(np.vstack([getDots[comptDots], getrgb[comptDots]]))
            if (rgbi == 1):
                label1.append(np.vstack([getDots[comptDots], getrgb[comptDots]]))
            elif (rgbi == 2):
                label2.append(np.vstack([getDots[comptDots], getrgb[comptDots]]))
            elif (rgbi == 3):
                label3.append(np.vstack([getDots[comptDots], getrgb[comptDots]]))
            elif (rgbi == 4):
                label4.append(np.vstack([getDots[comptDots], getrgb[comptDots]]))
            else:
                print("no label for dot no %5s ?\n" %(comptDots))
            comptDots=comptDots+1

        compt=compt+1

    if(verbose==1):
        dotsFic=open('dots.xyzrgb', 'w')
        dotslabel1=open('dotslabel1.xyzrgb', 'w')
        dotslabel2=open('dotslabel2.xyzrgb', 'w')
        dotslabel3=open('dotslabel3.xyzrgb', 'w')
        dotslabel4=open('dotslabel4.xyzrgb', 'w')

    getDots=np.empty(shape=[len(labeltot),3], dtype='float64')
    getrgb=np.empty(shape=[len(labeltot),3], dtype='float64')
    getDots1=np.empty(shape=[len(label1),3], dtype='float64')
    getrgb1=np.empty(shape=[len(label1),3], dtype='float64')
    getDots2=np.empty(shape=[len(label2),3], dtype='float64')
    getrgb2=np.empty(shape=[len(label2),3], dtype='float64')
    getDots3=np.empty(shape=[len(label3),3], dtype='float64')
    getrgb3=np.empty(shape=[len(label3),3], dtype='float64')
    getDots4=np.empty(shape=[len(label4),3], dtype='float64')
    getrgb4=np.empty(shape=[len(label4),3], dtype='float64')

    compt=0
    while(compt < len(labeltot)):
        getDots[compt]= labeltot[compt][0]
        getrgb[compt]= labeltot[compt][1]
        if(verbose==1):
            dotsFic.write('%8s'%getDots[compt,0]+'%8s'%getDots[compt,1]+'%8s'%getDots[compt,2]+espace5+'%5s'%getrgb[compt,0]+'%5s'%getrgb[compt,1]+'%5s'%getrgb[compt,2]+'\n')
        compt=compt+1

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
        dotsFic.close()
        dotslabel1.close()
        dotslabel2.close()
        dotslabel3.close()
        dotslabel4.close()
    else:
        os.remove("psa.in")
        os.remove("psa.out")

    return getDots, getrgb, getDots1, getrgb1, getDots2, getrgb2, getDots3, getrgb3, getDots4, getrgb4
