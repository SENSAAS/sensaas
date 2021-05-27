#!/usr/bin/python3.7

#execute ./<>.py sdf_file_target sdf_file_source -r nb -s score_type  
# -r ; number_of_repeats (used only on first molecule target and first molecule source sdf)
# -s ; score_type { source target mean }

import os, sys
import re
from sys import platform
import math
import random

# sys.argv[0] is the name of the program itself
target=sys.argv[1]
source=sys.argv[2]

#Default:
score_type="source"
repeat=1
rmsdthreshold=3

nbarg=len(sys.argv)
#print ("nb arg %s" % nbarg)
if(nbarg==5):
    if(sys.argv[3]=="-s"):
        if(sys.argv[4]=="mean" or sys.argv[4]=="source" or sys.argv[4]=="target"):
            score_type=sys.argv[4]
    if(sys.argv[3]=="-r"):
        repeat=int(sys.argv[4])
if(nbarg==7):
    if(sys.argv[3]=="-s"):
        if(sys.argv[4]=="mean" or sys.argv[4]=="source" or sys.argv[4]=="target"):
            score_type=sys.argv[4]
    if(sys.argv[3]=="-r"):
        repeat=int(sys.argv[4])
    if(sys.argv[5]=="-s"):
        if(sys.argv[6]=="mean" or sys.argv[6]=="source" or sys.argv[6]=="target"):
            score_type=sys.argv[6]
    if(sys.argv[5]=="-r"):
        score_type=int(sys.argv[6])

# sys.argv[0] is the name of the program itself
sensaasexe=sys.argv[0]
sensaasexe=re.sub('meta-sensaas\.py','',sensaasexe)
#sensaasexe="./"
#if environment variable is set (eg: .bashr SENSAASBASE=/home/user/sensaas-executables )
#sensaasexe=os.environ['SENSAASBASE'] + "/"
whichexe='linux'
if(whichexe in platform):
    # linux
    sensaasexe=sensaasexe+ "sensaas.py"
elif platform == "darwin":
    # OS X - linux version?
    sensaasexe=sensaasexe+ "sensaas.py"
else:
    #windows
    sensaasexe="python " + sensaasexe+ "sensaas.py"
print(sensaasexe)

#verbose=0 (keep important files only) or verbose=1
verbose=0

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
    #initiate output file
    ofile=open(osdf, 'w')
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
#def randomizesdf(inputfile,outputfile)
def randomizesdf(fsdf,osdf):
    #create random matrix 4D with 16 values
    alpha=random.randint(0,180)
    a1=math.cos(alpha)
    a2=math.sin(alpha)
    a3=0
    b1=-1*(math.sin(alpha))
    b2=math.cos(alpha)
    b3=0
    c1=0
    c2=0
    c3=1
    a4=random.uniform(0,5)
    t2=random.uniform(0,1)
    if (t2<=0.5):
        a4=a4*-1
    b4=random.uniform(0,5)
    t2=random.uniform(0,1)
    if (t2<=0.5):
        b4=b4*-1
    c4=random.uniform(0,5)
    t2=random.uniform(0,1)
    if (t2<=0.5):
        c4=c4*-1
    d1=0
    d2=0
    d3=0
    d4=1
    #read input file
    tabsdf=open(fsdf,'r')
    getstr=tabsdf.read().split('\n')
    tabsdf.close()
    tabLignesSdf=[]
    tabLignesSdf.append(re.split('\s+', getstr[3].strip()))
    if(len(tabLignesSdf[0][0]) > 2):
        tabLignesSdf[0][1]=tabLignesSdf[0][0][3:]
        tabLignesSdf[0][0]=tabLignesSdf[0][0][:3]
        nbatom=int(tabLignesSdf[0][0])
        nbbond=int(tabLignesSdf[0][1])
    else:
        nbatom=int(tabLignesSdf[0][0])
        nbbond=int(tabLignesSdf[0][1])
    #initiate output file
    ofile=open(osdf, 'w')
    compt=0
    while(compt < len(getstr)):
        if(compt > 3 and compt <= nbatom+3):
            tabLine=re.split(' +', getstr[compt].strip())
            x=float(tabLine[0])
            y=float(tabLine[1])
            z=float(tabLine[2])
            x1 = x*a1 + y*a2 + z*a3 + a4
            y1 = x*b1 + y*b2 + z*b3 + b4
            z1 = x*c1 + y*c2 + z*c3 + c4
            line=""
            tabLine[0]=str('%5.3f' % (x1))
            tabLine[1]=str('%5.3f' % (y1))
            tabLine[2]=str('%5.3f' % (z1))
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
            ofile.write(line+'\n')
        else:
            if(compt==(len(getstr)-1)):
                ofile.write(getstr[compt])
            else:
                ofile.write(getstr[compt]+'\n')
        compt=compt+1
    ofile.close()
    return

#######################################
#def coordgeomcenter(filesdf)
def coordgeomcenter(fsdf):
    tabsdf=open(fsdf,'r')
    getstr=tabsdf.read().split('\n')
    tabsdf.close()
    tabLignesSdf=[]
    compt=3
    while(compt < len(getstr)):
        tabLignesSdf.append(re.split('\s+', getstr[compt].strip()))
        compt=compt+1
    if(len(tabLignesSdf[0][0]) > 2):
        tabLignesSdf[0][1]=tabLignesSdf[0][0][3:]
        tabLignesSdf[0][0]=tabLignesSdf[0][0][:3]
        nbatomes=int(tabLignesSdf[0][0])
        nbLiaisons=int(tabLignesSdf[0][1])
    else:
        nbatomes=int(tabLignesSdf[0][0])
        nbLiaisons=int(tabLignesSdf[0][1])
    #print(nbatomes)
    compt=1
    getx=[]
    getx.append(0)
    gety=[]
    gety.append(0)
    getz=[]
    getz.append(0)
    while (compt <= nbatomes):
        xAtome=float(tabLignesSdf[compt][0])
        yAtome=float(tabLignesSdf[compt][1])
        zAtome=float(tabLignesSdf[compt][2])
        getx.append(xAtome)
        gety.append(yAtome)
        getz.append(zAtome)
        compt=compt+1
    meanx=sum(getx)/nbatomes
    meany=sum(gety)/nbatomes
    meanz=sum(getz)/nbatomes
    meanx='%.2f' % meanx
    meany='%.2f' % meany
    meanz='%.2f' % meanz
    return meanx, meany, meanz

#######################################
# MAIN program

nbt=nbsdf(target)
if(verbose==1):
    print ("nb target %s" % nbt)
nbs=nbsdf(source)
if(verbose==1):
    print ("nb source %s" % nbs)
nbcalc=nbt * nbs

#option repeat only available if 1 target and 1 source
if(repeat > 1):
    nbt=1
    nbs=1
    nbcalc=repeat

if(verbose==1):
    print ("nb of calculations with score_type %s = %s (%s repeats)" % (score_type,nbcalc,repeat))

#scores of source
scoregfithfit=[]
scoregfit=[]
scorehfit=[]
#score of target
scoregfithfit_target=[]
scoregfit_target=[]
scorehfit_target=[]
#mean
scoregfithfit_mean=[]
scoregfit_mean=[]
scorehfit_mean=[]

####################################################################
#Repeat mode:
if(repeat>1):
    output="cat-repeats.sdf"
    #initiate output
    solfile=open(output, 'w')
    solfile.close()
    #applied only on first molecules:
    i=1
    searchsdfi(target,i,"tmpt.sdf")
    j=1
    searchsdfi(source,j,"tmps.sdf")
    #coordinates of geometric center of solutions
    cgetx=[]
    cgety=[]
    cgetz=[]
    ri=1
    k=0
    while (ri <= repeat):
        i=0
        while(i < nbt):
            i=i+1
            #searchsdfi(target,i,"tmpt.sdf")
            #print ("Target no %s" % i)
            j=0
            while(j < nbs):
                j=j+1
                #searchsdfi(source,j,"tmps.sdf")
                #print ("Source no %s" % j)

                #random re-orientation using def randomizesdf(inputfile,outputfile=tmps.sdf)
                #can be commented:
                randomizesdf("tmps.sdf","tmps.sdf")

                #execute sensaas
                cmd = '%s sdf tmpt.sdf sdf tmps.sdf slog optim' % (sensaasexe)
                os.system(cmd)

                #read last line of slog and fill table scoregh, scoreg, scoreh (scoreght, scoregt scoreht if score_type= "mean" or "target")
                logfile=open('slog', 'r')
                lignelog=logfile.readlines()
                logfile.close()
                score=lignelog[-1]
                #if(verbose==1):
                print ("%s %s - %s %s score-source %s" % (target,i,source,j,score))
                tabscore=[]
                tabscore.append(re.split('\s+', score.strip()))
                #scores of source
                scoregfithfit.append(tabscore[0][7])
                scoregfit.append(tabscore[0][1])
                scorehfit.append(tabscore[0][5])

                x,y,z=coordgeomcenter("Source_tran.sdf")
                cgetx.append(float(x))
                cgety.append(float(y))
                cgetz.append(float(z))

                if(score_type=="mean" or score_type=="target"):
                    #eval target
                    #execute sensaas
                    cmd = '%s sdf Source_tran.sdf sdf tmpt.sdf slog eval' % (sensaasexe)
                    os.system(cmd)
                    logfile=open('slog', 'r')
                    lignelog=logfile.readlines()
                    logfile.close()
                    score=lignelog[-1]
                    #if(verbose==1):
                    print ("%s %s - %s %s score-target %s" % (target,i,source,j,score))
                    tabscore=[]
                    tabscore.append(re.split('\s+', score.strip()))
                    #scores of target
                    scoregfithfit_target.append(tabscore[0][7])
                    scoregfit_target.append(tabscore[0][1])
                    scorehfit_target.append(tabscore[0][5])
                    #mean
                    mgh=(float(scoregfithfit[k])+float(scoregfithfit_target[k]))/2
                    mgh='%.3f' % (mgh)
                    scoregfithfit_mean.append(mgh)
                    mg=(float(scoregfit[k])+float(scoregfit_target[k]))/2
                    mg='%.3f' % (mg)
                    scoregfit_mean.append(mg)
                    mh=(float(scorehfit[k])+float(scorehfit_target[k]))/2
                    mh='%.3f' % (mh)
                    scorehfit_mean.append(mh)

                k=k+1
                #concatenate Source_tran.sdf in cat-repeats.sdf
                lignesol=[]
                solfile=open('Source_tran.sdf', 'r')
                lignesol=solfile.readlines()
                solfile.close()
                catfile=open(output, 'a')
                for f in lignesol:
                    catfile.write(f)
                catfile.close()

                #clean
                os.remove("Source_tran.sdf")
                os.remove("tran.txt")
                os.remove("slog")
        
        ri=ri+1

    #create clusters
    #rmsdthreshold
    clusters=[]
    clustersi=[]
    order=[]
    vu=[]
    clusters.append(0)
    clustersi.append(0)
    order.append(0)
    vu.append(0)
    ci=1
    m=0
    while(m < k):
        h=0
        cf=-1
        while(h<ci and cf==-1):
            dist=math.sqrt((cgetx[m] - cgetx[clustersi[h]])**2 + (cgety[m] - cgety[clustersi[h]])**2 + (cgetz[m] - cgetz[clustersi[h]])**2)
            if(dist < rmsdthreshold):
                cf=h
            h=h+1
        if(cf==-1):
            #new cluster
            clusters.append(1)
            clustersi.append(m)
            order.append(0)
            vu.append(0)
            ci=ci+1
        else:
            #update cluster info
            clusters[cf]=clusters[cf]+1
            if(score_type=="target"):
                if(float(scoregfithfit_target[m]) > float(scoregfithfit_target[clustersi[cf]])):
                    clustersi[cf]=m
            elif(score_type=="mean"):
                if(float(scoregfithfit_mean[m]) > float(scoregfithfit_mean[clustersi[cf]])):
                    clustersi[cf]=m
            else:
                if(float(scoregfithfit[m]) > float(scoregfithfit[clustersi[cf]])):
                    clustersi[cf]=m
        m=m+1

    #order clusters
    nbcluster=len(clusters)
    if(verbose==1):
        print("%s clusters" % (nbcluster))
    h=0
    while(h<ci):
        p=0
        bestgfithfit=0
        besti=-1
        while(p<ci):
            if(vu[p]!=1):
                if(score_type=="target"):
                    if(float(scoregfithfit_target[clustersi[p]]) > bestgfithfit):
                        bestgfithfit=float(scoregfithfit_target[clustersi[p]])
                        besti=p
                elif(score_type=="mean"):
                    if(float(scoregfithfit_mean[clustersi[p]]) > bestgfithfit):
                        bestgfithfit=float(scoregfithfit_mean[clustersi[p]])
                        besti=p
                else:
                    if(float(scoregfithfit[clustersi[p]]) > bestgfithfit):
                        bestgfithfit=float(scoregfithfit[clustersi[p]])
                        besti=p
            p=p+1
        #print("besti %s" % (besti))
        order[h]=besti
        vu[besti]=1
        h=h+1

    #print and write
    #read and add tmpt.sdf to name
    lignet=[]
    tfile=open('tmpt.sdf', 'r')
    lignet=tfile.readlines()
    tfile.close()
    print("Rank ; Hybrid score gfit + hfit ; Shape gfit ; Color hfit ; percentage of solutions ; Alignment in SDF file format")
    h=0
    while(h<ci):
        no=h+1
        clusters[order[h]]='%.2f' % ((clusters[order[h]]/repeat)*100)
        #print("%s is cluster %s ( %s percent of solutions) with best solution no %s (gfit+hfit= %s )" % (no,order[h],clusters[order[h]],clustersi[order[h]],scoregfithfit[clustersi[order[h]]]))
        
        #concatenate target and solution no clustersi[order[h]] into sensaas-no.sdf
        name="sensaas-" + str(no) + ".sdf"
        catfile=open(name, 'w')
        for f in lignet:
            catfile.write(f)
        catfile.close()
        #extract clustersi[order[h]] from cat-repeats.sdf into tmpr.sdf
        nomol=clustersi[order[h]] + 1
        #print("sol no %s" % (nomol))
        searchsdfi(output,nomol,"tmpr.sdf")
        lignesol=[]
        solfile=open('tmpr.sdf', 'r')
        lignesol=solfile.readlines()
        solfile.close()
        catfile=open(name, 'a')
        for f in lignesol:
            catfile.write(f)
        catfile.close()
        #clean
        os.remove("tmpr.sdf")

        if(score_type=="mean"):
            print("%s ; %s ; %s ; %s ; %s ; %s" % (no,scoregfithfit_mean[clustersi[order[h]]],scoregfit_mean[clustersi[order[h]]],scorehfit_mean[clustersi[order[h]]],clusters[order[h]],name))
        elif(score_type=="target"):
            print("%s ; %s ; %s ; %s ; %s ; %s" % (no,scoregfithfit_target[clustersi[order[h]]],scoregfit_target[clustersi[order[h]]],scorehfit_target[clustersi[order[h]]],clusters[order[h]],name))
        else:
            print("%s ; %s ; %s ; %s ; %s ; %s" % (no,scoregfithfit[clustersi[order[h]]],scoregfit[clustersi[order[h]]],scorehfit[clustersi[order[h]]],clusters[order[h]],name))

        h=h+1
    print("cat-repeats.sdf contains the %s sdf solutions" % (repeat))

    #clean
    os.remove("tmps.sdf")
    os.remove("tmpt.sdf")


####################################################################
#Database mode:
else:
    output="catsensaas.sdf"
    outputbest="bestsensaas.sdf"
    outputmatrix="matrix-sensaas.txt"
    #initiate output and outputmatrix for future appends
    solfile=open(output, 'w')
    solfile.close()
    mfile=open(outputmatrix, 'w')
    mfile.close()

    #best
    bestgfithfit=0
    besti=-1
    bestt=-1
    bests=-1
    k=0
    i=0
    while(i < nbt):
        i=i+1
        searchsdfi(target,i,"tmpt.sdf")
        #print ("Target no %s" % i)
        j=0
        while(j < nbs):
            j=j+1
            searchsdfi(source,j,"tmps.sdf")
            #print ("Source no %s" % j)
        
            #execute sensaas
            cmd = '%s sdf tmpt.sdf sdf tmps.sdf slog optim' % (sensaasexe)
            os.system(cmd)

            #read last line of slog and fill table scoregh, scoreg, scoreh (scoreght, scoregt scoreht if score_type= "mean" or "target") 
            logfile=open('slog', 'r')
            lignelog=logfile.readlines()
            logfile.close()
            score=lignelog[-1]
            #if(verbose==1):
            print ("%s %s - %s %s score-source %s" % (target,i,source,j,score))
            tabscore=[]
            tabscore.append(re.split('\s+', score.strip()))
            #scores of source
            scoregfithfit.append(tabscore[0][7])
            scoregfit.append(tabscore[0][1])
            scorehfit.append(tabscore[0][5])
        
            if(score_type=="mean" or score_type=="target"):
                #eval target
                #execute sensaas
                cmd = '%s sdf Source_tran.sdf sdf tmpt.sdf slog eval' % (sensaasexe)
                os.system(cmd)
                logfile=open('slog', 'r')
                lignelog=logfile.readlines()
                logfile.close()
                score=lignelog[-1]
                #if(verbose==1):
                print ("%s %s - %s %s score-target %s" % (target,i,source,j,score))
                tabscore=[]
                tabscore.append(re.split('\s+', score.strip()))
                #scores of target
                scoregfithfit_target.append(tabscore[0][7])
                scoregfit_target.append(tabscore[0][1])
                scorehfit_target.append(tabscore[0][5])
                #mean
                mgh=(float(scoregfithfit[k])+float(scoregfithfit_target[k]))/2
                mgh='%.3f' % (mgh)
                scoregfithfit_mean.append(mgh)
                mg=(float(scoregfit[k])+float(scoregfit_target[k]))/2
                mg='%.3f' % (mg)
                scoregfit_mean.append(mg)
                mh=(float(scorehfit[k])+float(scorehfit_target[k]))/2
                mh='%.3f' % (mh)
                scorehfit_mean.append(mh)
                
                if(score_type=="target"):
                    if(bestgfithfit < float(scoregfithfit_target[k])):
                        bestgfithfit=float(scoregfithfit_target[k])
                        besti=k
                        bestt=i
                        bests=j
                        lignesol=[]
                        solfile=open('Source_tran.sdf', 'r')
                        lignesol=solfile.readlines()
                        solfile.close()
                        catfile=open(outputbest, 'w')
                        for f in lignesol:
                            catfile.write(f)
                        catfile.close()
                    #if(verbose==1):
                        #print ("gfit+hfit_target= %s gfit_target= %s hfit_target= %s" % (scoregfithfit_target[k],scoregfit_target[k],scorehfit_target[k]))
                else:
                    if(bestgfithfit < float(scoregfithfit_mean[k])):
                        bestgfithfit=float(scoregfithfit_mean[k])
                        besti=k
                        bestt=i
                        bests=j
                        lignesol=[]
                        solfile=open('Source_tran.sdf', 'r')
                        lignesol=solfile.readlines()
                        solfile.close()
                        catfile=open(outputbest, 'w')
                        for f in lignesol:
                            catfile.write(f)
                        catfile.close()
                    #if(verbose==1):
                        #print ("gfit+hfit_mean= %s gfit_mean= %s hfit_mean=%s" % (scoregfithfit_mean[k],scoregfit_mean[k],scorehfit_mean[k]))

                #print ("gfit+hfit= %s gfit= %s hfit= %s ; gfit+hfit_target= %s gfit_target= %s hfit_target= %s ; gfit+hfit_mean= %s gfit_mean= %s hfit_mean=%s" % (scoregfithfit[k],scoregfit[k],scorehfit[k],scoregfithfit_target[k],scoregfit_target[k],scorehfit_target[k],scoregfithfit_mean[k],scoregfit_mean[k],scorehfit_mean[k]))
            else:
                if(bestgfithfit < float(scoregfithfit[k])):
                    bestgfithfit=float(scoregfithfit[k])
                    besti=k
                    bestt=i
                    bests=j
                    lignesol=[]
                    solfile=open('Source_tran.sdf', 'r')
                    lignesol=solfile.readlines()
                    solfile.close()
                    catfile=open(outputbest, 'w')
                    for f in lignesol:
                        catfile.write(f)
                    catfile.close()
                #if(verbose==1):
                    #print ("gfit+hfit= %s gfit= %s hfit= %s" % (scoregfithfit[k],scoregfit[k],scorehfit[k]))

            k=k+1
            #concatenate Source_tran.sdf in catsensaas.sdf
            lignesol=[]
            solfile=open('Source_tran.sdf', 'r')
            lignesol=solfile.readlines()
            solfile.close()
            catfile=open(output, 'a')
            for f in lignesol:
                catfile.write(f)
            catfile.close()
            
            #clean
            os.remove("tmps.sdf")
            os.remove("Source_tran.sdf")
            os.remove("tran.txt")
            os.remove("slog")

        os.remove("tmpt.sdf")

    #write results:
    mfile=open(outputmatrix, 'a')
    m=0
    ns=0
    while (m < k):
        #print matrix-sensaas.txt (1 target per line ; source in column delimited by white space)
        if(score_type=="mean"):
            mfile.write(" %s" % (scoregfithfit_mean[m]))
        elif(score_type=="target"):
            mfile.write(" %s" % (scoregfithfit_target[m]))
        else:
            mfile.write(" %s" % (scoregfithfit[m]))
        m=m+1
        ns=ns+1
        if(ns==nbs):
            mfile.write("\n")
            ns=0
    mfile.close()

    if(score_type=="target"): 
        bestgfit=float(scoregfit_target[besti])
        besthfit=float(scorehfit_target[besti])
    elif(score_type=="mean"):
        bestgfit=float(scoregfit_mean[besti])
        besthfit=float(scorehfit_mean[besti])
    else:
        bestgfit=float(scoregfit[besti])
        besthfit=float(scorehfit[besti])
    print ("gfithfit= %.3f gfit= %.3f hfit= %.3f (target %d ; source %d ; outputs: %s, %s and %s)" % (bestgfithfit,bestgfit,besthfit,bestt,bests,outputbest,output,outputmatrix))

#######################################
