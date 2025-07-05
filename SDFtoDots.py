#!/usr/bin/python3.7

#Author: Lucas GRANDMOUGIN 

import sys
import subprocess
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

    # Read file more efficiently
    with open(filesdf, 'r') as f:
        getstr = f.read().splitlines()

    # Parse only relevant lines starting from line 3
    tabLignesSdf = [line.strip().split() for line in getstr[3:] if line.strip()]

    # Determine atom and bond count from first parsed line
    first_line = tabLignesSdf[0]
    if len(first_line[0]) > 2:
        raw = first_line[0]
        # Handle possible spacing issues in atom count
        if raw[1] == ' ':
            first_line[1] = raw[2:]
            first_line[0] = raw[:2]
        elif len(raw) >= 5 and raw[4] != ' ':
            first_line[1] = raw[3:]
            first_line[0] = raw[:3]

    # Convert to integers
    nbatomes = int(first_line[0])
    nbLiaisons = int(first_line[1])

    compt=1
    getx = ['']
    gety = ['']
    getz = ['']
    getA = ['']
    getRayon = ['']

    valid_atoms = {'C', 'O', 'N', 'P', 'B', 'H', 'F', 'Br', 'Cl', 'S', 'I', 'X', 'Hp'}

    for line in tabLignesSdf[1:nbatomes + 1]:
        xAtome, yAtome, zAtome = map(float, line[:3])
        atom = line[3]

        getx.append(xAtome)
        gety.append(yAtome)
        getz.append(zAtome)

        if zAtome == 0.0:
            fichier2D += 1

        if atom not in valid_atoms:
            print(f"Warning: atom {atom} set as C because it is not the tab (unusual in medchem)")
            atom = 'C'

        getA.append(atom)
        getRayon.append(tabR[atom])

    if fichier2D == nbatomes:
        print("Warning: sdf file in 2D; SenSaaS needs 3D coordinates to work properly")

    for line in getstr[nbatomes + 4: nbatomes + nbLiaisons + 1]:
        try:
            a1 = int(line[:3])
            a2 = int(line[3:6])
        except ValueError:
            print(f"Invalid line: {line}")
            quit()

        if a1 < 0 or a1 > nbatomes or a2 < 0 or a2 > nbatomes:
            print(f"invalid atom number {a1:6d} or {a2:6d}")
            quit()

        a1_type = getA[a1]
        a2_type = getA[a2]

        if (a1_type == 'O' and a2_type == 'H') or (a1_type == 'H' and a2_type == 'O'):
            getRayon[a1 if a1_type == 'H' else a2] = tabR['Hp']

        elif (a1_type == 'N' and a2_type == 'H') or (a1_type == 'H' and a2_type == 'N'):
            getRayon[a1 if a1_type == 'H' else a2] = tabR['Hp']

#nsc:
    with open('psa.in', 'w') as psaIn:
        psaIn.write('* XYZR\n')
        psaIn.write(f"{espace6}{nbatomes}\n")
        for i in range(1, nbatomes + 1):
            x = f"{getx[i]:.2f}"
            y = f"{gety[i]:.2f}"
            z = f"{getz[i]:.2f}"
            psaIn.write(f"{x:>8} {y:>8} {z:>8} {getRayon[i]:>8} {getA[i]:>8}\n")

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

    # Run the external command more safely and efficiently
    subprocess.run([nscexe, 'psa.in'], check=True)

    # Read and parse psa.out lines starting from line 3
    with open('psa.out', 'r') as psaOut:
        lines = psaOut.readlines()[3:]

    tabLignesPsaOut = [re.split(r'\s+', line.strip()) for line in lines]

    nbDots = int(tabLignesPsaOut[0][2])
    tabLignesPsaOut = tabLignesPsaOut[2:]  # remove first two header lines

    # Preallocate arrays
    getDots = np.empty((nbDots, 3), dtype=np.float64)
    getrgb = np.empty((nbDots, 3), dtype=np.float64)

    # Convert atom coordinates to NumPy arrays for vectorized distance computation
    atom_coords = np.column_stack((getx[1:nbatomes + 1], gety[1:nbatomes + 1], getz[1:nbatomes + 1]))
    atom_labels = getA[1:nbatomes + 1]
    atom_radii = getRayon[1:nbatomes + 1]

    # Precompute tabR['Hp'] value to compare
    hp_radius = tabR['Hp']

    # Prepare containers for labeled dots
    label_dict = {1: [], 2: [], 3: [], 4: []}
    labeltot = []

    for i, line in enumerate(tabLignesPsaOut[:nbDots]):
        if len(line) < 5:
            # skip malformed or empty lines
            continue
        xDot, yDot, zDot = map(float, line[2:5])
        dot = np.array([xDot, yDot, zDot])

        # Compute distances vectorized: (nbatomes, 3) - (3,) -> (nbatomes, 3)
        diffs = atom_coords - dot
        dists = np.linalg.norm(diffs, axis=1)

        # Find index of closest atom (mi)
        mi = np.argmin(dists)

        atom_label = atom_labels[mi]
        atom_radius = atom_radii[mi]

        if atom_label == 'X':
            # Skip dummy atoms as in original code
            continue

        # Determine rgb index
        rgbi = label.get(atom_label, 3)  # default to 3 if not found
        if atom_radius == hp_radius:
            rgbi = label['O']  # override if radius is Hp

        rgb_val = rgb[rgbi]

        getDots[i] = dot
        getrgb[i] = rgb_val

        # Store combined dot and rgb
        combined = np.vstack((dot, rgb_val))
        labeltot.append(combined)

        # Assign to respective label lists
        if rgbi in label_dict:
            label_dict[rgbi].append(combined)
        else:
            print(f"no label for dot no {i} ?")

    # Convert label lists to arrays
    label_arrays = {}
    for key in label_dict:
        arr = np.array(label_dict[key])
        label_arrays[key] = arr if arr.size else np.empty((0, 2, 3))  # handle empty case

    # Unpack for return and further use
    getDots = np.array([item[0] for item in labeltot])
    getrgb = np.array([item[1] for item in labeltot])

    getDots1, getrgb1 = (label_arrays.get(1)[:, 0, :], label_arrays.get(1)[:, 1, :]) if label_arrays.get(1).size else (
    np.empty((0, 3)), np.empty((0, 3)))
    getDots2, getrgb2 = (label_arrays.get(2)[:, 0, :], label_arrays.get(2)[:, 1, :]) if label_arrays.get(2).size else (
    np.empty((0, 3)), np.empty((0, 3)))
    getDots3, getrgb3 = (label_arrays.get(3)[:, 0, :], label_arrays.get(3)[:, 1, :]) if label_arrays.get(3).size else (
    np.empty((0, 3)), np.empty((0, 3)))
    getDots4, getrgb4 = (label_arrays.get(4)[:, 0, :], label_arrays.get(4)[:, 1, :]) if label_arrays.get(4).size else (
    np.empty((0, 3)), np.empty((0, 3)))

    if verbose == 1:
        # Open files with context managers
        with open('dots.xyzrgb', 'w') as dotsFic, \
                open('dotslabel1.xyzrgb', 'w') as dotslabel1, \
                open('dotslabel2.xyzrgb', 'w') as dotslabel2, \
                open('dotslabel3.xyzrgb', 'w') as dotslabel3, \
                open('dotslabel4.xyzrgb', 'w') as dotslabel4:

            def write_points(f, dots, rgbs):
                for pt, color in zip(dots, rgbs):
                    f.write(
                        f"{pt[0]:8.2f}{pt[1]:8.2f}{pt[2]:8.2f}{espace5}{color[0]:5.2f}{color[1]:5.2f}{color[2]:5.2f}\n")

            write_points(dotsFic, getDots, getrgb)
            write_points(dotslabel1, getDots1, getrgb1)
            write_points(dotslabel2, getDots2, getrgb2)
            write_points(dotslabel3, getDots3, getrgb3)
            write_points(dotslabel4, getDots4, getrgb4)
    else:
        os.remove("psa.in")
        os.remove("psa.out")

    return getDots, getrgb, getDots1, getrgb1, getDots2, getrgb2, getDots3, getrgb3, getDots4, getrgb4
