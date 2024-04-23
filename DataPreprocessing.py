import os
import numpy as np
import open3d as o3d

def load_ply(file_path):
    """Load point cloud data from a .ply file."""
    point_cloud = o3d.io.read_point_cloud(file_path)
    points = np.asarray(point_cloud.points)
    return points

def prepare_dataset(otolith_folder, sulcus_folder):
    """Prepare the dataset by pairing otolith and sulcus point clouds."""
    otolith_files = sorted(os.listdir(otolith_folder))
    sulcus_files = sorted(os.listdir(sulcus_folder))
    
    dataset = []
    for otolith_file, sulcus_file in zip(otolith_files, sulcus_files):
        otolith_path = os.path.join(otolith_folder, otolith_file)
        sulcus_path = os.path.join(sulcus_folder, sulcus_file)
        
        # Load otolith and sulcus point clouds
        otolith_point_cloud = load_ply(otolith_path)
        sulcus_point_cloud = load_ply(sulcus_path)
        
        # Pair otolith and sulcus point clouds
        dataset.append((otolith_point_cloud, sulcus_point_cloud))
    
    return dataset

# Paths to folders containing otoliths and sulcus point clouds
otolith_folder = "otoPLY"
sulcus_folder = "sulcus"

# Prepare the dataset
dataset = prepare_dataset(otolith_folder, sulcus_folder)

