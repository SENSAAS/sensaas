Usage Examples:

To optimize an alignment:

        sensaas.py sdf target.sdf sdf source.sdf slog optim

Here the source file is aligned (moved) on the target file.
the output tran.txt contains the transformation matrix allowing the alignment of the source file:
    if Source input file is sdf then Source_tran.sdf is the transformed sdf source file
    if Source input file is pdb then Source_tran.pdb is the transformed pdb source file
    if Source input file is dot then Source-dots_tran.pdb is the transformed dot file in pdb format
    if Source input file is xyzrgb then Source_tran.xyzrgb is the transformed xyzrgb file
    if Source input file is pcd then Source_tran.pcd is the transformed pcd file
slog (whatever you want to call it) details results with final scores on the last line
.pcd or .xyzrgb file contains coordinates and rgb colors of points and can be read by Open3D (visualize.py in directory utils)

|||||||||||||||||||||||||||||||||||||||||

example (IMATINIB_mv.sdf was reoriented when compared with IMATINIB.sdf):

sensaas.py sdf DATASET/IMATINIB.sdf sdf DATASET/IMATINIB_mv.sdf slog optim

the last line of slog must display a score "gfit+hfit=" close to 2.0 and the superimposition of sdf files must be perfect 

|||||||||||||||||||||||||||||||||||||||||

To evaluate an alignment (in place):

        sensaas.py sdf molecule1.sdf sdf molecule2.sdf slog eval

slog (whatever you want to call it) details results with final scores on the last line

|||||||||||||||||||||||||||||||||||||||||

Final scores are written in the log file (eg: slog) at the last line. It looks like "gfit= 1.000 cfit= 0.999 hfit= 0.996 gfit+hfit= 1.996"
There are three different fitness scores but we only use 2 of them, gfit and hfit to calculate gfit+hfit.

- gfit score estimates the geometric matching of point-based surfaces; It ranges between 0 and 1
- hfit score estimates the matching of colored points representing pharmacophore features; It ranges between 0 and 1
Thus, we calculate a hybrid score = gfit + hfit scores; It ranges between 0 and 2

For more information, please read the publication in open access:
   Douguet D. and Payan F., SenSaaS: Shape-based Alignment by Registration of Colored Point-based Surfaces,
   Molecular Informatics, 2020, 8, 2000081. doi: 10.1002/minf.202000081
   https://onlinelibrary.wiley.com/doi/full/10.1002/minf.202000081


