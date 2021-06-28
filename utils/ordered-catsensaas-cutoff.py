#!/usr/bin/python3.7

#executes ./<>.py matrix-sensaas.txt catsensaas.sdf 1.0
#creates ordered-catsensaas.sdf and ordered-score.txt only with solutions having gfit+hfit >= 1.0 (cutoff)

import os, sys
import re

ARGV=[]
try:
    ARGV.append(sys.argv[1])
except:
    print('usage: ordered-catsensaas.py matrix-sensaas.txt catsensaas.sdf 1.0 ')
    quit()

# sys.argv[0] is the name of the program itself
matrix=sys.argv[1]
filesdf=sys.argv[2]
cutoff=float(sys.argv[3])

outputm="ordered-scores.txt"
outputsdf="ordered-catsensaas.sdf"

#######################################
#def (filesdf) output=number of molecules
def nbsdf(fsdf):
    tabsdf=open(fsdf,'r')
    getstr=tabsdf.read().split('\n')
    tabsdf.close()
    whichend="$$$$"
    nbmol=0
    compt=0
    while(compt < len(getstr)):
        if(whichend in getstr[compt]):
            nbmol=nbmol+1
        compt=compt+1
    if(nbmol==0): #if .mol format
        nbmol=1
    return nbmol

#######################################
#def (filesdf,i,outputname) extract sdf no i from a sdf file into outputname
def searchsdfi(fsdf,fi,osdf):
    #append output file
    ofile=open(osdf, 'a')
    #read input file
    tabsdf=open(fsdf,'r')
    getstr=tabsdf.read().split('\n')
    tabsdf.close()
    tabLignesSdf=[]
    whichend="$$$$"
    nbmol=0
    compt=0
    while(compt < len(getstr)):
        tabLignesSdf.append(getstr[compt])
        if(whichend in getstr[compt]):
            nbmol=nbmol+1
            if(nbmol==fi):
                #print
                li=0
                while(li < len(tabLignesSdf)):
                    ofile.write("%s\n" % tabLignesSdf[li])
                    li=li+1
            tabLignesSdf=[]
        compt=compt+1
    if(nbmol==0):
        #print .mol file
        li=0
        while(li < len(tabLignesSdf)):
            ofile.write("%s\n" % tabLignesSdf[li])
            li=li+1
    ofile.close()
    return

#######################################
# MAIN program

nbt=nbsdf(filesdf)
#print ("nb sdf structures  %s" % nbt)

#initiate output
mfile=open(outputm, 'w')
mfile.close()
solfile=open(outputsdf, 'w')
solfile.close()

#open matrix
fscore=open(matrix,'r')
getstr=fscore.read().split('\n')
fscore.close()

tabLignes=[]
scoregfithfit=[]
nbcol=0
compt=0
while(compt < len(getstr)):
    tabLignes.append(re.split('\s+', getstr[compt].strip()))
    nbcol=len(tabLignes[compt])
    #print(nbcol)
    compt2=0
    while(compt2 < nbcol and tabLignes[compt][compt2]!=''):
        #print(tabLignes[compt][compt2])
        valuescore=float(tabLignes[compt][compt2])
        scoregfithfit.append(valuescore)
        compt2=compt2+1
    compt=compt+1

nbm=len(scoregfithfit)
#print("nb scores in matrix %s" % nbm)
if(nbt!=nbm):
    print("Warning: the number of structures %s and the number of scores differ %s\n" % (nbt,nbm))
    quit()
else:
    #print("order")
    mfile=open(outputm, 'w')
    mfile.write("#Source_number gfit+hfit_score\n")
    compt2=0
    stop=0
    while(compt2 < nbm and stop==0):
        maval=-1
        mi=-1
        compt=0
        while(compt < nbm):
            if(scoregfithfit[compt] > maval and scoregfithfit[compt] > -1):
                maval=scoregfithfit[compt]
                mi=compt
            compt=compt+1
        if(mi > -1):
            no=mi+1
            mfile.write("%s %s\n" % (no,scoregfithfit[mi]))
            searchsdfi(filesdf,no,outputsdf)
            if(scoregfithfit[mi] < cutoff):
                stop=1
            scoregfithfit[mi]=-1
        compt2=compt2+1
    mfile.close()

#######################################
