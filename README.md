## sensaas


[![badgepython](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/downloads/release/python-370/)  [![forthebadge](https://forthebadge.com/images/badges/built-with-science.svg)](https://chemoinfo.ipmc.cnrs.fr/)

**SENSAAS** is a shape-based alignment program for molecular superimposition as described in the publication [SenSaaS: Shape-based Alignment by Registration of Colored Point-based Surfaces](https://onlinelibrary.wiley.com/doi/full/10.1002/minf.202000081).

**Documentation**: Full documentation is available at [https://sensaas.readthedocs.io/en/latest/.](https://sensaas.readthedocs.io/en/latest/.)

**Website**: A web demo is available at https://chemoinfo.ipmc.cnrs.fr/SENSAAS/index.html

**Tutorial**: This video on YouTube XXXX provides a tutorial


## Requirements

SENSAAS relies on the open-source library Open3D. The current release of SENSAAS uses **Open3D version 0.12.0 along with Python3.7**. Visit the following URL for downloading the appropriate package: [https://anaconda.org/open3d-admin/open3d/files](https://anaconda.org/open3d-admin/open3d/files) or for using Open3D Python packages distributed via PyPI and Conda (more information at [http://www.open3d.org/docs/release/getting_started.html](http://www.open3d.org/docs/release/getting_started.html)). For example, for windows-64, download '*win-64/open3d-0.12.0-py37_0.tar.bz2*'


## Installing with conda

A - Install conda or Miniconda from [https://conda.io/miniconda.html](https://conda.io/miniconda.html)  
Then, complete the installation:

	conda update conda
	conda create -n sensaas
	conda activate sensaas
	conda install python=3.7 numpy
 
  After donwloading the appropriate version of Open3D:
  
 	conda install open3d-0.12.0-py37_0.tar.bz2

B - (Option) Additional packages for using scripts in the directory utils or visualization with PyMol:

  	conda install perl
  	install -c conda-forge rdkit
  	conda install -c schrodinger -c conda-forge pymol-bundle
  
C - Retrieve and unzip SENSAAS repository

## Linux

## MacOS
	Not tested

## Getting started with Sensaas  
This algorithm is used to optimize an alignment of 2 molecules or proteins. We will call the molecule you want to align "source" and the one which receive
the source molecule is the "target". You can see results on [PyMol](https://pymol.org/2/). If you don’t own PyMol yet, you can check [our documentation](lien).

## Using Sensaas
To optimize an alignment:
	
	(sensaas) > ./sensaas.py <target-type> <target-file-name> <source-type> <source-file-name> <output-file-name> <mode> (with the appropriate path)

When you will us SENSAAS, it will create **3 outputs files**: slog, Source_tran, tran.txt.
