#!/usr/bin/python3.7

import os, sys
import re

def read_pdbdot(PDBfile):

#label1 {H, Cl, Br, I} white/grey 0.9 0.9 0.9
#label2 {O, N, S, F} red 1 0 0
#label3 {C, P, B} green 0 1 0
#label4 {others} blue 0 0 1

    filepdb=open(PDBfile,'r')
    getstr=filepdb.read().split('\n')
    filepdb.close()

    #HETATM   29  C   MOL     1       -2.66   -6.78   -7.03     1     1
    #ATOM     29  C   MOL     1       -2.66   -6.78   -7.03     1     1

    fd=open("dots.xyzrgb", 'w')
    longa=len(getstr)
    compt=0
    while(compt < longa):
        tabLine=re.split(' +', getstr[compt].strip())
        if(tabLine[0]=="HETATM" or tabLine[0]=="ATOM"):
            x=float(tabLine[5])
            y=float(tabLine[6])
            z=float(tabLine[7])
            elt=tabLine[2]
            #label 1 {H, Cl, Br, I}
            if(elt=="H" or elt=="Cl" or elt=="Br" or elt=="I"):
                r=0.9
                g=0.9
                b=0.9
            #label 2 {O, N, S, F}
            elif(elt=="O" or elt=="N" or elt=="S" or elt=="F"):
                r=1.0
                g=0.0
                b=0.0
            #label 3 {C, P, B}
            elif(elt=="C" or elt=="P" or elt=="B"):
                r=0.0
                g=1.0
                b=0.0
            #label 4 {others}
            else:
                r=0.0
                g=0.0
                b=1.0
            fd.write('%5.3f  %5.3f  %5.3f  %5.3f  %5.3f  %5.3f' % (x,y,z,r,g,b) +"\n")
        compt=compt+1
    
    fd.close()

    return
