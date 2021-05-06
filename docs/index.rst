.. Documentation documentation master file, created by
   sphinx-quickstart on Tue May  4 09:28:38 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Sensaas Documentation's !
====================================

.. toctree::
   :maxdepth: 2
   
This project has been created by Dr .Douguet and Dr. Payan during a collaboration between the `I3S Laboratory <https://www.i3s.unice.fr/>`_ and `IPMC Laboratory <https://www.ipmc.cnrs.fr/cgi-bin/site.cgi>`_. The algorithm is used to optimize an alignment of 2 molecules or proteins. Thanks to the `open3D library <http://www.open3d.org/>`_, molecules are represented in 3D to be align and visualize more easily. All the algorithm has been created with Python 3.7 and including a C library.

* `To start`_
* `Installation of CONDA`_
* `Installation of packages on CONDA`_
* `Getting started with Sensaas`_
* `Example with DATASET files`_
* `Associated files of Sensaas`_
* `Installation of PyMol`_
* `Indices and tables`_


To start
========
This version of SENSAAS works with Open3D-0.12.0 libraries (BSD 3-clause "New" or "Revised") along with python 3.7. To be able to use SENSAAS in the good environment with all corrects packages, you should create an environment on CONDA.

Installation of CONDA
---------------------

Install conda or miniconda using python3 (64 bits):  

`CONDA Miniconda installers <https://docs.conda.io/en/latest/miniconda.html>`_ version for Windows, Linux and MacOSX.

Installation of packages on CONDA
---------------------------------

Launch Anaconda Prompt (miniconda3). (On Anaconda: Home -> 'CMD.exe Prompt' -> Launch)::

   (base) > conda update conda
   (base) > conda create -n sensaas
   (base) > conda activate sensaas

Visit `this url <https://anaconda.org/open3d-admin/open3d/files>`_ for informations and downloads.

Then, download the version of **open3D 0.12.0.0**, according to your OS (ex: for win-64: "*win64/open3d-0.12.0-py37_0.tar.bz2*") for **python 3.7**.

.. important::  Please check that you have installed the appropriate versions (open3D 0.12.0.0 for python 3.7 with Linux/Windows/MacOSX).
 
When it is done::

   (sensaas) > conda install python=3.7 numpy    
   (sensaas) > conda install open3d-0.12.0-py37_0.tar.bz2    (with the appropriate path)

and additional packages for using additional scripts in the directory utils::

   (sensaas) > conda install -c conda-forge rdkit

Now, **your environment is ready**. Unzip and untar the SENSAAS distribution .tar.gz file.
To work on your environment on Anaconda: Environments -> sensaas -> click on the arrow -> Open Terminal


Getting started with Sensaas
============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

This algorithm is used to optimize an alignment of 2 molecules or proteins. We will call the molecule you want to align "source" and the one which receive
the source molecule is the "target". You can see results on `PyMol <https://pymol.org/2/>`_, if you don't own PyMol yet, click here: `Installation of PyMol`_.

.. warning:: Before using Sensaas, please check that your **inputs are 3D files**. The algorithm works only with **sdf/pdb/xyzrgb/pcd** 3D files. 

To optimize an alignment::
	
   (sensaas) > ./sensaas.py <target-type> <target-file-name> <source-type> <source-file-name> <output-file-name> <mode> (with the appropriate path)

**<target-type>**
   type of the target file (sdf/pdb/dot/xyzrgb/pcd)

**<target-file-name>**
   name of the target file (you need to precise the path of the target file)

**<source-type>**
   type of the source file (sdf/pdb/dot/xyzrgb/pcd)

**<source-file-name>**
   name of the source file (you need to precise the path of the source file)

**<output-file-name>**
   name of the output file that will be created. We usually named it "slog" but you can call it whatever you want. It details results of the alignement with final scores on the last line.

**<mode>** (optim or eval)
   \- "optim": generates a transformation matrix
   
   \- "eval": evaluate the alignment "in place" (without aligning)

When you will us SENSAAS, it will create **3 outputs files**: slog, Source_tran, tran.txt.

Examples
========

Example with sdf file
---------------------
::

   (sensaas) > sensaas.py sdf <target-file-name>.sdf sdf <source-file-name>.sdf slog optim

Here the source file is aligned (moved) on the target file.

	the output tran.txt contains the transformation matrix allowing the alignment of the source file:

	    if Source input file is **sdf** then **Source_tran.sdf** is the transformed sdf source file

	    if Source input file is **pdb** then **Source_tran.pdb** is the transformed pdb source file

	    if Source input file is **dot** then **Source-dots_tran.pdb** is the transformed dot file in pdb format

 	    if Source input file is **xyzrgb** then **Source_tran.xyzrgb** is the transformed xyzrgb file

	    if Source input file is **pcd** then **Source_tran.pcd** is the transformed pcd file

**slog** (whatever you want to call it) details results with final scores on the last line.

.pcd or .xyzrgb file contains coordinates and rgb colors of points and can be read by Open3D (visualize.py in directory utils)

Example with DATASET files
--------------------------

1. example (IMATINIB_mv.sdf was reoriented when compared with IMATINIB.sdf (with optim):

::

	(sensaas) > sensaas.py sdf DATASET/IMATINIB.sdf sdf DATASET/IMATINIB_mv.sdf slog optim

the last line of slog must display a score "gfit+hfit=" close to 2.0 and the superimposition of sdf files must be perfect 


2. example (IMATINIB_mv.sdf was reoriented when compared with IMATINIB.sdf)(with eval: To evaluate an alignment (in place)):

::

   (sensaas) > sensaas.py sdf DATASET/IMATINIB.sdf sdf DATASET/IMATINIB_mv.sdf slog eval

**slog** (whatever you want to call it) details results with final scores on the last line


Associated files of Sensaas
===========================

sensaas.py not work alone, it call different scripts to align molecules. Let show you how all the program works with a kind of blueprint:

.. image:: _static/schema.JPG
.. image:: _static/legend.jpg   


Installation of PyMol
=====================

To visualize sdf or pdb outputs files, you can use PyMol. PyMol is a free software, easy to implement which able to manipulate and visualize 3D molecules.

To install PyMol, `click here <https://pymol.org/2/>`_ -> click "Download" -> choose the right zip file

`To install PyMol <https://pymol.org/2/support.html?#installation>`_ with control terminal or on conda.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
