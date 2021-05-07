#!/usr/bin/python3.7

import os, sys
import numpy as np
import re

#print('usage: <>.py <xyzrgb dot file> <verbose 1/0>\ncreate tables and files dotslabel1.xyzrgb dotslabel2.xyzrgb dotslabel3.xyzrgb and dotslabel4.xyzrgb\n')

def xyzrgb2labels(filexyzrgb):

    verbose=0

#label1 {H, Cl, Br, I} white/grey 0.9 0.9 0.9
#label2 {O, N, S, F} red 1 0 0
#label3 {C, P, B} green 0 1 0
#label4 {others} blue 0 0 1

    filedots=open(filexyzrgb,'r')
    getdots=filedots.read().split('\n')
    filedots.close()
    longa=len(getdots)
    dotsxyz=np.empty(shape=[longa,3], dtype=np.float64)
    dotsrgb=np.empty(shape=[longa,3], dtype=np.float64)
    
    dots1xyz=np.empty(shape=[longa,3], dtype=np.float64)
    dots1rgb=np.empty(shape=[longa,3], dtype=np.float64)
    dots2xyz=np.empty(shape=[longa,3], dtype=np.float64)
    dots2rgb=np.empty(shape=[longa,3], dtype=np.float64)
    dots3xyz=np.empty(shape=[longa,3], dtype=np.float64)
    dots3rgb=np.empty(shape=[longa,3], dtype=np.float64)
    dots4xyz=np.empty(shape=[longa,3], dtype=np.float64)
    dots4rgb=np.empty(shape=[longa,3], dtype=np.float64)

    #files with dots
    if(verbose==1):
        fd1=open("dotslabel1.xyzrgb", 'w')
        fd2=open("dotslabel2.xyzrgb", 'w')
        fd3=open("dotslabel3.xyzrgb", 'w')
        fd4=open("dotslabel4.xyzrgb", 'w')

    compt=0
    compt1=0;
    compt2=0;
    compt3=0;
    compt4=0;
    i=0
    while(i < longa):
        tabLine=re.split(' +', getdots[compt].strip())
        longb=len(tabLine)
        #print(longb)
        if(longb==6):
            tabLine=re.split(' +', getdots[compt].strip())
            #print(tabLine)
            x=float(tabLine[0])
            y=float(tabLine[1])
            z=float(tabLine[2])
            r=float(tabLine[3])
            g=float(tabLine[4])
            b=float(tabLine[5])
            if(r>0.5 and g>0.5 and b>0.5):
                r=0.9
                g=0.9
                b=0.9
                dots1xyz[compt1,:]=[x,y,z]
                dots1rgb[compt1,:]=[r,g,b]
                compt1=compt1+1
                if(verbose==1):
                    fd1.write('%5.3f  %5.3f  %5.3f  %5.3f  %5.3f  %5.3f' % (x,y,z,r,g,b) +"\n")
            elif(r>0.5 and g<0.5 and b<0.5):
                r=1.0
                g=0.0
                b=0.0
                dots2xyz[compt2,:]=[x,y,z]
                dots2rgb[compt2,:]=[r,g,b]
                compt2=compt2+1
                if(verbose==1):
                    fd2.write('%5.3f  %5.3f  %5.3f  %5.3f  %5.3f  %5.3f' % (x,y,z,r,g,b) +"\n")
            elif(r<0.5 and g>0.5 and b<0.5):
                r=0.0
                g=1.0
                b=0.0
                dots3xyz[compt3,:]=[x,y,z]
                dots3rgb[compt3,:]=[r,g,b]
                compt3=compt3+1
                if(verbose==1):
                    fd3.write('%5.3f  %5.3f  %5.3f  %5.3f  %5.3f  %5.3f' % (x,y,z,r,g,b) +"\n")
            else:
                r=0.0
                g=0.0
                b=1.0
                dots4xyz[compt4,:]=[x,y,z]
                dots4rgb[compt4,:]=[r,g,b]
                compt4=compt4+1
                if(verbose==1):
                    fd4.write('%5.3f  %5.3f  %5.3f  %5.3f  %5.3f  %5.3f' % (x,y,z,r,g,b) +"\n")

            dotsxyz[compt,:]=[x,y,z]
            dotsrgb[compt,:]=[r,g,b]
            compt=compt+1 
        i=i+1

    if(verbose==1):
        fd1.close()
        fd2.close()
        fd3.close()
        fd4.close()

    #print('nb dots=%3s label1=%3s label2=%3s label3=%3s label4=%3s' % (compt,compt1,compt2,compt3,compt4))
    arr_dotsxyz= np.empty(shape=[0,3], dtype=np.float64)
    arr_dotsrgb= np.empty(shape=[0,3], dtype=np.float64)
    if(compt > 0):
        arr_dotsxyz= np.empty(shape=[compt,3], dtype=np.float64)
        arr_dotsrgb= np.empty(shape=[compt,3], dtype=np.float64)
        # 0:3 begin at 0 and print 3 values
        arr_dotsxyz[0:compt,0:3]=dotsxyz[0:compt,0:3]
        arr_dotsrgb[0:compt,0:3]=dotsrgb[0:compt,0:3]

    arr_dots1xyz= np.empty(shape=[0,3], dtype=np.float64)
    arr_dots1rgb= np.empty(shape=[0,3], dtype=np.float64)
    if(compt1 > 0):
        arr_dots1xyz= np.empty(shape=[compt1,3], dtype=np.float64)
        arr_dots1rgb= np.empty(shape=[compt1,3], dtype=np.float64)
        arr_dots1xyz[0:compt1,0:3]=dots1xyz[0:compt1,0:3]
        arr_dots1rgb[0:compt1,0:3]=dots1rgb[0:compt1,0:3]
    
    arr_dots2xyz= np.empty(shape=[0,3], dtype=np.float64)
    arr_dots2rgb= np.empty(shape=[0,3], dtype=np.float64)
    if(compt2  > 0):
        arr_dots2xyz= np.empty(shape=[compt2,3], dtype=np.float64)
        arr_dots2rgb= np.empty(shape=[compt2,3], dtype=np.float64)
        arr_dots2xyz[0:compt2,0:3]=dots2xyz[0:compt2,0:3]
        arr_dots2rgb[0:compt2,0:3]=dots2rgb[0:compt2,0:3]

    arr_dots3xyz= np.empty(shape=[0,3], dtype=np.float64)
    arr_dots3rgb= np.empty(shape=[0,3], dtype=np.float64)
    if(compt3  > 0):
        arr_dots3xyz= np.empty(shape=[compt3,3], dtype=np.float64)
        arr_dots3rgb= np.empty(shape=[compt3,3], dtype=np.float64)
        arr_dots3xyz[0:compt3,0:3]=dots3xyz[0:compt3,0:3]
        arr_dots3rgb[0:compt3,0:3]=dots3rgb[0:compt3,0:3]

    arr_dots4xyz= np.empty(shape=[0,3], dtype=np.float64)
    arr_dots4rgb= np.empty(shape=[0,3], dtype=np.float64)
    if(compt4 > 0):
        arr_dots4xyz= np.empty(shape=[compt4,3], dtype=np.float64)
        arr_dots4rgb= np.empty(shape=[compt4,3], dtype=np.float64)
        arr_dots4xyz[0:compt4,0:3]=dots4xyz[0:compt4,0:3]
        arr_dots4rgb[0:compt4,0:3]=dots4rgb[0:compt4,0:3]

    return arr_dotsxyz, arr_dotsrgb, arr_dots1xyz, arr_dots1rgb, arr_dots2xyz, arr_dots2rgb, arr_dots3xyz, arr_dots3rgb, arr_dots4xyz, arr_dots4rgb
