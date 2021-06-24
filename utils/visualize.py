import open3d as o3d
import argparse

p = argparse.ArgumentParser(description="Visualize point clouds with Open3D")
p.add_argument("files", type=str, nargs="+", help="files")

args = p.parse_args()

pcds = []
for f in args.files:
    pcd = o3d.io.read_point_cloud(f)
    pcds.append(pcd)

o3d.visualization.draw_geometries(
    pcds, window_name="open3d-molecule", width=1000, height=800, left=50, top=50
)
