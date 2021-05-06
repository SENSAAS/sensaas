## sensaas


[![badgepython](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/downloads/release/python-370/)  [![forthebadge](https://forthebadge.com/images/badges/built-with-science.svg)](https://chemoinfo.ipmc.cnrs.fr/)

**SENSAAS** is a shape-based alignment program to superimpose molecules as described in the publication [SenSaaS: Shape-based Alignment by Registration of Colored Point-based Surfaces](https://onlinelibrary.wiley.com/doi/full/10.1002/minf.202000081).

**Documentation**: Full documentation is available at [https://sensaas.readthedocs.io/en/latest/.](https://sensaas.readthedocs.io/en/latest/.)

**Website**: A web demo is available at https://chemoinfo.ipmc.cnrs.fr/SENSAAS/index.html

**Tutorial**: This video on YouTube XXXX provides a tutorial


## Requirements

SENSAAS relies on the open-source library Open3D. The current release of SENSAAS uses **Open3D version 0.12.0 along with Python3.7**. Visit the following URL for downloading the appropriate package: [https://anaconda.org/open3d-admin/open3d/files](https://anaconda.org/open3d-admin/open3d/files) or for using Open3D Python packages distributed via PyPI and Conda (more information at [http://www.open3d.org/docs/release/getting_started.html](http://www.open3d.org/docs/release/getting_started.html)). For example, for windows-64, you can download '*win-64/open3d-0.12.0-py37_0.tar.bz2*'


## Virtual environment for python with conda

Install conda or Miniconda from [https://conda.io/miniconda.html](https://conda.io/miniconda.html)  
Then, complete the installation:

	conda update conda
	conda create -n sensaas
	conda activate sensaas
	conda install python=3.7 numpy
 
 After donwloading the appropriate version of Open3D:
  
 	conda install open3d-0.12.0-py37_0.tar.bz2

(Option) Additional packages for using scripts in the directory utils or visualization with PyMol:

  	conda install perl
  	install -c conda-forge rdkit
  	conda install -c schrodinger -c conda-forge pymol-bundle
  
Retrieve and unzip SENSAAS repository

## Linux

Install:

1. Python3.7 and numpy
2. Open3D version 0.12.0 (more information at [http://www.open3d.org/docs/release/getting_started.html](http://www.open3d.org/docs/release/getting_started.html))

(Option) Install additional packages for using scripts in the directory utils or visualization with PyMOL:

4. perl (usually it is already installed)
5. RDKit (Open-Source Cheminformatics Software; more information at [https://rdkit.org](https://rdkit.org) or [https://github.com/rdkit/rdkit](https://github.com/rdkit/rdkit))
6. PyMOL (a molecular viewer; more information at [https://pymolwiki.org](https://pymolwiki.org))
  
Retrieve and unzip SENSAAS repository

## MacOS

	Not tested

## Third-party program  
This algorithm used NSC program

## Run Sensaas
To align a Source molecule on a Target molecule, run:
	
	sensaas.py sdf molecule-target.sdf sdf molecule-source.sdf slog optim

When you will us SENSAAS, it will create **3 outputs files**: slog, Source_tran, tran.txt.

## License
Code released under [the 3-Clause BSD License](https://opensource.org/licenses/BSD-3-Clause)

## Copyright
Copyright (c) 2018-2021, CNRS, Inserm, Université Côte d'Azur, Dominique Douguet and Frédéric Payan, All rights reserved.

## Reference
[Douguet D. and Payan F., SenSaaS: Shape-based Alignment by Registration of Colored Point-based Surfaces,
   '*Molecular Informatics*', **2020**, 8, 2000081.](https://onlinelibrary.wiley.com/doi/full/10.1002/minf.202000081). doi: 10.1002/minf.202000081
   
