import numpy as np
from stl import mesh
import plotly.graph_objects as go
import open3d as o3d
import streamlit as st
import streamlit.components.v1 as components
import trimesh
import os
def save_ply(ply_content, save_path='Upload'):
    os.makedirs(save_path, exist_ok=True)
    filename = os.path.join(save_path, ply_content.name)
    
    with open(filename, 'wb') as f:
        f.write(ply_content.read())
    return filename


def save_point_cloud(pcd, save_path='Upload'):
    
    filename = os.path.join(save_path, "point_cloud.ply")
    o3d.io.write_point_cloud(filename, pcd)
    return filename

def segment_file(filename):
    pcd = o3d.io.read_point_cloud(filename)
    print(pcd)
    # Centrer le nuage de points
    pcd_center = pcd.get_center()
    pcd.translate(-pcd_center)
    # Filtrage des valeurs aberrantes statistiques
    nn = 100
    std_multiplier = 10
    filtered_pcd = pcd.remove_statistical_outlier(nn, std_multiplier)
    outliers = pcd.select_by_index(filtered_pcd[1], invert=True)

    filtered_pcd = filtered_pcd[0]
    filtered_pcd.paint_uniform_color([0.6,0.6,0.6])
    o3d.visualization.draw_geometries([filtered_pcd, outliers])

    #%% Échantillonnage de voxels
    voxel_size = 0.01
    pcd_downsampled = filtered_pcd.voxel_down_sample(voxel_size=voxel_size)
    # Estimation des normales
    nn_distance = np.mean(pcd.compute_nearest_neighbor_distance())
    radius_normals = nn_distance * 4

    pcd_downsampled.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=radius_normals, max_nn=30))
    pcd_downsampled.paint_uniform_color([0.6,0.6,0.6])
    # Définition des paramètres d'affichage

    front =[  -0.16172102747213624, -0.97298960951825508, -0.16473472324579946 ]
    lookat = [ 0.12348394638268534, 0.042953382492225245, -0.019304002039019164 ]
    up = [ -0.97958611139257779, 0.13808203450573414, 0.1460972351330635 ]
    zoom = 0.35999999999999965

    pcd = pcd_downsampled

    # SEGMENTATION PLAN RANSAC

    pt_to_plane_dist = 0.15
    plane_model, inliers = pcd.segment_plane(distance_threshold=pt_to_plane_dist,
                                            ransac_n=3, num_iterations=1000)
    [a, b, c, d] = plane_model
    print(f'Équation du plan : {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0')
    inlier_cloud = pcd.select_by_index(inliers)
    outlier_cloud = pcd.select_by_index(inliers, invert=True)
    inlier_cloud.paint_uniform_color([1, 0, 0])
    outlier_cloud.paint_uniform_color([0.6, 0.6, 0.6])
    o3d.visualization.draw_geometries([outlier_cloud], zoom=zoom, front=front, up=up, lookat=lookat)
    
    pcd = outlier_cloud

    # SEGMENTATION PLAN RANSAC

    # pt_to_plane_dist = 0.17
    pt_to_plane_dist = 0.23
    plane_model, inliers = pcd.segment_plane(distance_threshold=pt_to_plane_dist,
                                            ransac_n=3, num_iterations=1000)
    [a, b, c, d] = plane_model
    print(f'Équation du plan : {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0')
    inlier_cloud = pcd.select_by_index(inliers)
    outlier_cloud = pcd.select_by_index(inliers, invert=True)
    inlier_cloud.paint_uniform_color([0.6, 0.6, 0.6])
    outlier_cloud.paint_uniform_color([1, 0, 0])
    o3d.visualization.draw_geometries([inlier_cloud], zoom=zoom, front=front, up=up, lookat=lookat)
    return inlier_cloud
    
    