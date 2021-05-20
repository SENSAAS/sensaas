#!/usr/bin/python3.7

#execute ./<>.py <pcd or xyzrgb file> - Display

import open3d as o3d
import os, sys

# sys.argv[0] is the name of the program itself
target=sys.argv[1]
#source=sys.argv[2]

target_pcd = o3d.io.read_point_cloud(target)
#source_pcd = o3d.io.read_point_cloud(source)

o3d.visualization.draw_geometries([target_pcd],window_name='open3d-molecule',width=1000, height=800, left=50, top=50)
#to read 2 clouds
#o3d.visualization.draw_geometries([target_pcd,source_pcd],window_name='open3d-molecule',width=1000, height=800, left=50, top=50)
