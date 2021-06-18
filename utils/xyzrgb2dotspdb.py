#!/usr/bin/python3.7

import sys
import os
import re

ARGV=[]
try:
    ARGV.append(sys.argv[1])
except:
    print('usage: xyzrgb2dotspdb.py file.xyzrgb\neg:\ncreate dots.pdb for visualization with PyMOL for example')
    quit()

#label1 {H, Cl, Br, I} white/grey 0.9 0.9 0.9
#label2 {O, N, S, F} red 1 0 0
#label3 {C, P, B} green 0 1 0
#label4 {others} blue 0 0 1

filexyzrgb=sys.argv[1]
fxyzrgb=open(filexyzrgb,'r')
getstr=fxyzrgb.read().split('\n')
fxyzrgb.close()

output="dots.pdb"
#initiate output
solfile=open(output, 'w')

debnom="mol"
occup=1
bfactor=1

doti=0
tabLignes=[]
compt=0
while(compt < len(getstr)):
    tabLignes.append(re.split('\s+', getstr[compt].strip()))
    if(tabLignes[compt][0] != ''):
        if(float(tabLignes[compt][3]) > 0.5 and float(tabLignes[compt][4]) > 0.5 and float(tabLignes[compt][5]) > 0.5):
            elt="H"
        elif(float(tabLignes[compt][3]) > 0.5 and float(tabLignes[compt][4]) < 0.5 and float(tabLignes[compt][5]) < 0.5):
            elt="O"
        elif(float(tabLignes[compt][3]) < 0.5 and float(tabLignes[compt][4]) > 0.5 and float(tabLignes[compt][5]) < 0.5):
            elt="C"
        else:
            elt="N"
        xdot=float(tabLignes[compt][0])
        ydot=float(tabLignes[compt][1])
        zdot=float(tabLignes[compt][2])
        xdot='%4.2f' % xdot
        ydot='%4.2f' % ydot
        zdot='%4.2f' % zdot
        doti=doti+1
        solfile.write("HETATM%5s %4s %3s     1    %8s%8s%8s  %4s %5s\n" %(doti,elt,debnom,xdot,ydot,zdot,occup,bfactor))
    compt=compt+1

solfile.close()
print("See %s with %s dots in PDB format" % (output,doti))
