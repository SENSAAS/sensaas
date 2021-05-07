## sensaas


[![badgepython](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/downloads/release/python-370/)  [![forthebadge](https://forthebadge.com/images/badges/built-with-science.svg)](https://chemoinfo.ipmc.cnrs.fr/)

**SENSAAS** is a shape-based alignment program to superimpose molecules as described in the publication [SenSaaS: Shape-based Alignment by Registration of Colored Point-based Surfaces](https://onlinelibrary.wiley.com/doi/full/10.1002/minf.202000081). https://doi.org/10.1002/minf.202000081

![example](/images/sensaas-core-eg.png)

**Documentation**: Full documentation is available at [https://sensaas.readthedocs.io](https://sensaas.readthedocs.io)

**Website**: A web demo is available at https://chemoinfo.ipmc.cnrs.fr/SENSAAS/index.html

**Tutorial**: This video on YouTube XXXX provides a tutorial


## Requirements

SENSAAS relies on the open-source library [Open3D](http://www.open3d.org). The current release of SENSAAS uses **Open3D version 0.12.0 along with Python3.7**.

Visit the following URL for using Python packages distributed via PyPI: [http://www.open3d.org/docs/release/getting_started.html](http://www.open3d.org/docs/release/getting_started.html) or conda: [https://anaconda.org/open3d-admin/open3d/files](https://anaconda.org/open3d-admin/open3d/files). For example, for windows-64, you can download *win-64/open3d-0.12.0-py37_0.tar.bz2*


## Virtual environment for python with conda

Install conda or Miniconda from [https://conda.io/miniconda.html](https://conda.io/miniconda.html)  
Then complete the installation:

	conda update conda
	conda create -n sensaas
	conda activate sensaas
	conda install python=3.7 numpy
 
 After downloading the appropriate version of Open3D:
  
 	conda install open3d-0.12.0-py37_0.tar.bz2

(Optional) Additional packages for using scripts in the directory utils/ or visualization with PyMOL:

  	conda install perl
  	install -c conda-forge rdkit
  	conda install -c schrodinger -c conda-forge pymol-bundle
  
Retrieve and unzip SENSAAS repository

## Linux

Install:

1. Python3.7 and numpy
2. Open3D version 0.12.0 (more information at [http://www.open3d.org/docs/release/getting_started.html](http://www.open3d.org/docs/release/getting_started.html))

(Optional) Install additional packages for using scripts in the directory utils/ or visualization with PyMOL:

4. perl (usually it is already installed)
5. RDKit (Open-Source Cheminformatics Software; more information at [https://rdkit.org](https://rdkit.org) or [https://github.com/rdkit/rdkit](https://github.com/rdkit/rdkit))
6. PyMOL (a molecular viewer; more information at [https://pymolwiki.org](https://pymolwiki.org))
  
Retrieve and unzip SENSAAS repository

## MacOS

	Not tested

## Information on the third-party program nsc

nsc is used to efficiently generate point cloud of molecules. It is written in C and was developed by Frank Eisenhaber who kindly accepted its use in SENSAAS. **Please be advised that its use is strictly tied to SENSAAS and its code is released under the following [license](https://github.com/SENSAAS/sensaas/blob/main/License_NSC.txt)**. We recommend the use of nsc but if this type of license is an issue then, please contact us for using an alternative method or contact the author F. Eisenhaber (Bioinformatics Institute A*STAR).

References :

1. F. Eisenhaber, P. Lijnzaad, P. Argos, M. Scharf, The Double Cubic Lattice Method: Efficient Approaches to Numerical Integration of Surface Area and Volume and to Dot Surface Contouring of Molecular Assemblies, *Journal of Computational Chemistry*, **1995**, 16, N3, pp.273-284.
2. F. Eisenhaber, P. Argos, Improved Strategy in Analytic Surface Calculation for Molecular Systems: Handling of Singularities and Computational Efficiency, 	*Journal of Computational Chemistry*, **1993**,14, N11, pp.1272-1280.


Executables nsc (for Linux) or ncs-win (for windows) are included in this repository. In case they do not work on your system, you may have to compile it using the source file nsc.c in directory src/


**for Linux**:

	cc src/nsc.c -lm
	
rename a.out as nsc because 'nsc' is used to set the variable nscexe in the Python script sensaas.py:

	cp a.out nsc
	
**for Windows**:

The current executable nsc-win.exe was compiled by using [http://www.codeblocks.org](http://www.codeblocks.org). Rename the executable as nsc-win.exe because 'nsc-win.exe' is used to set the variable nscexe in the Python script sensaas.py



## Run Sensaas
To align a Source molecule on a Target molecule, run:
	
	sensaas.py sdf molecule-target.sdf sdf molecule-source.sdf slog optim
	
Example:

	sensaas.py sdf examples/IMATINIB.sdf sdf examples/IMATINIB_mv.sdf slog optim

Here, the source file IMATINIB_mv.sdf is aligned (**moved**) on the target file IMATINIB.sdf (**that does not move**). The output **tran.txt** contains the transformation matrix allowing the alignment of the source file (result in **Source_tran.sdf**). The **slog** file details results with final scores on the last line. In this example, the last line must look like:

	gfit= 1.000 cfit= 0.999 hfit= 0.996 gfit+hfit= 1.996

There are three different fitness scores but we only use 2 of them, gfit and hfit to calculate gfit+hfit.

- gfit score estimates the geometric matching of point-based surfaces; It ranges between 0 and 1

- hfit score estimates the matching of colored points representing pharmacophore features; It ranges between 0 and 1

Thus, we calculate a hybrid score = gfit + hfit scores; **gfit+hfit ranges between 0 and 2**

   A gfit+hfit score close to 2.0 means a perfect superimposition.

   A gfit+hfit score > 1.0 means that similaries were identified.

Here IMATINIB.sdf and IMATINIB_mv.sdf are the 2 same molecules thus you can evaluate the RMSD value by using rdkit tool:

	utils/rdkit-CalcLigRMSD.py ../DATASET/IMATINIB.sdf Source_tran.sdf

Here, it returns RMSD= 0.00

## Licenses
1. SENSAAS code is released under [the 3-Clause BSD License](https://opensource.org/licenses/BSD-3-Clause)

2. nsc code is released under the following [license](https://github.com/SENSAAS/sensaas/blob/main/License_NSC.txt)

## Copyright
Copyright (c) 2018-2021, CNRS, Inserm, Université Côte d'Azur, Dominique Douguet and Frédéric Payan, All rights reserved.

## Reference
[Douguet D. and Payan F., SenSaaS: Shape-based Alignment by Registration of Colored Point-based Surfaces, *Molecular Informatics*, **2020**, 8, 2000081](https://onlinelibrary.wiley.com/doi/full/10.1002/minf.202000081). doi: 10.1002/minf.202000081
   
