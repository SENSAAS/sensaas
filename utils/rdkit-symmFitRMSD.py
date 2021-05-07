#!/usr/bin/python3.7

#WORKS ONLY IF ATOMS ARE IN THE SAME ORDER !

#Info taken from https://sourceforge.net/p/rdkit/mailman/message/34329154/
#Author: Paolo Tosco <paolo.tosco@un...> - 2015-07-29 17:12:45
#./symmFit.py [-r] [-s] refFile.sdf prbFIle.sdf
# heavy atoms only
#The -r option triggers the computation "in place", i.e., without realigning poses.
#The -s option triggers consideration of symmetric atoms when doing the RMSD computation (as in RDKit's GetBestRMS()).
#As it is, the scripts expects refFile.sdf and prbFIle.sdf to be single conformations; however, if you look at the code, you should easily 
#manage to use the existing functions symmUniqueFit() and getRmsdImmobile() to generate the RMSD matrix out of your docking poses.

import sys
import copy
import math
import rdkit
from rdkit import Chem
from rdkit.Chem import rdmolfiles, rdMolAlign

def saveConformer(mol, confId):
  conf = mol.GetConformer(confId)
  confCopy = Chem.Conformer(conf.GetNumAtoms())
  for i in range(conf.GetNumAtoms()):
    confCopy.SetAtomPosition(i, conf.GetAtomPosition(i))
  return confCopy

def loadConformer(mol, confId, confCopy):
  conf = mol.GetConformer(confId)
  for i in range(conf.GetNumAtoms()):
    conf.SetAtomPosition(i, confCopy.GetAtomPosition(i))

def symmUniqueFit(prbMol, refMol, prbConfId = -1, refConfId = -1):
  matches = refMol.GetSubstructMatches(prbMol, uniquify = False)
  if not matches:
    raise ValueError('mols don\'t match')
  amaps = [list(enumerate(match)) for match in matches]
  first = True
  rmsdMin = 0.0
  amapBest = []
  for amap in amaps:
    conf = saveConformer(prbMol, prbConfId)
    rmsd = Chem.rdMolAlign.AlignMol(prbMol, refMol,
      prbConfId, refConfId, atomMap = amap)
    loadConformer(prbMol, prbConfId, conf)
    if (first or (rmsd < rmsdMin)):
      first = False
      rmsdMin = rmsd
      amapBest = amap
  return amapBest

def getRmsdImmobile(prbMol, refMol,
  prbConfId = -1, refConfId = -1, atomMap = None):
  refConf = refMol.GetConformer(refConfId)
  prbConf = prbMol.GetConformer(prbConfId)
  if (not atomMap):
    atomMap = []
    for i in range(0, refMol.GetNumAtoms()):
      if (refMol.GetAtomWithIdx(i).GetAtomicNum() == 1):
        continue
      atomMap.append((i, i))
  sqDist = 0.0
  for pair in atomMap:
    sqDist += (prbConf.GetAtomPosition(pair[0]) \
      - refConf.GetAtomPosition(pair[1])).LengthSq()
    #print ("%s %s dist=%s" % (pair[0], pair[1], sqDist))
  sqDist /= float(len(atomMap))
  return math.sqrt(sqDist)

dontMove = False
symm = False
n = 0
argc = len(sys.argv)
while ((n + 1) < argc):
  n += 1
  arg = sys.argv[n]
  if (arg[0] != '-'):
    break
  elif (arg == '-r'):
    dontMove = True
  elif (arg == '-s'):
    symm = True

refFile = sys.argv[n]
prbFile = sys.argv[n + 1]
refMol = Chem.rdmolfiles.MolFromMolFile(refFile,
  sanitize = True, removeHs = True)
prbMol = Chem.rdmolfiles.MolFromMolFile(prbFile,
  sanitize = True, removeHs = True)
prbMolCopy = copy.copy(prbMol)
amap = None
if (symm):
  amap = symmUniqueFit(refMol, prbMol)
  if (len(amap) != refMol.GetNumAtoms()):
    raise ValueError ('atomMap does not contain all atoms')
if (dontMove):
  rmsd = getRmsdImmobile(prbMolCopy, refMol, atomMap = amap)
else:
  (rmsd, trans) = Chem.rdMolAlign.GetAlignmentTransform \
    (prbMolCopy, refMol, atomMap = amap)
print ("RMSD= %1.2f" % (rmsd))
