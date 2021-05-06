# sensaas


[![badgepython](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/downloads/release/python-370/)  [![forthebadge](https://forthebadge.com/images/badges/built-with-science.svg)](https://chemoinfo.ipmc.cnrs.fr/)

This project has been created by a chemininformatic Dr. Douguet and a Dr. Payan, it is a teamwork between the [I3S Laboratory](https://www.i3s.unice.fr/) and [IPMC Laboratory](https://www.ipmc.cnrs.fr/cgi-bin/site.cgi). This cheminformatics algorithm is used to optimize an alignment of 2 molecules or proteins. Thanks to the [open3D library](http://www.open3d.org/), molecules are represented in 3D to be align and visualize more easily. All the algorithm has been created with Python 3.7 and including a C library.

## Documentation

If you want more details about sensaas using or how to visualize molecules, let see [our documentation](lien)

## To start

This version of SENSAAS works with Open3D-0.12.0 libraries (BSD 3-clause "New" or "Revised") along with python 3.7. To be able to use SENSAAS in the good environment with all corrects packages, you should create an environment on CONDA.

### Installation of CONDA

Install conda or miniconda using python3 (64 bits):  
[CONDA Miniconda installers](https://docs.conda.io/en/latest/miniconda.html) version for Windows, Linux and MacOSX. 

### Installation of packages on CONDA

Launch Anaconda Prompt (miniconda3). (On Anaconda: Home -> 'CMD.exe Prompt' -> Launch)

        (base) > conda update conda
        (base) > conda create -n sensaas
        (base) > conda activate sensaas

Visit [this url](https://anaconda.org/open3d-admin/open3d/files) for informations and downloads.  
Then, download the version of **open3D 0.12.0.0**, according to your OS (ex: for win-64: '*win64/open3d-0.12.0-py37_0.tar.bz2*') for **python 3.7**.
Please check that you have installed the appropriate versions (open3D 0.12.0.0 for python 3.7 with Linux/Windows/MacOSX).
   
        (sensaas) > conda install python=3.7 numpy    
	    (sensaas) > conda install open3d-0.12.0-py37_0.tar.bz2    (with the appropriate path)

and additional packages for using additional scripts in the directory utils:  

        (sensaas) > conda install -c conda-forge rdkit
	
Now, your environment is ready. Unzip and untar the SENSAAS distribution .tar.gz file.  
To work on your environment on Anaconda: Environments -> sensaas -> click on the arrow -> Open Terminal

## Getting started with Sensaas  
This algorithm is used to optimize an alignment of 2 molecules or proteins. We will call the molecule you want to align "source" and the one which receive
the source molecule is the "target". You can see results on [PyMol](https://pymol.org/2/). If you don’t own PyMol yet, you can check [our documentation](lien).

### Using Sensaas
To optimize an alignment:
	
	(sensaas) > ./sensaas.py <target-type> <target-file-name> <source-type> <source-file-name> <output-file-name> <mode> (with the appropriate path)

When you will us SENSAAS, it will create **3 outputs files**: slog, Source_tran, tran.txt.
