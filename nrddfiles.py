import trimesh
import numpy as np
import os
import nrrd
from skimage.measure import marching_cubes
import random

data_dir = "Slicer3d"
files = os.listdir(data_dir)

for f in files:
    # Read the data back from file
    filename = os.path.join(data_dir, f)
    volume, header = nrrd.read(filename)
    
    # Step 1: Extract surface mesh
    vertices, faces, _, _ = marching_cubes(volume)
    
    # Step 2: Sample points from surface mesh
    num_points = 1024  # Adjust the number of points as needed
    sampled_indices = random.sample(range(vertices.shape[0]), num_points)
    sampled_points = vertices[sampled_indices]
    
    # Step 3: Normalize sampled points
    mean = np.mean(sampled_points, axis=0)
    std = np.std(sampled_points, axis=0)
    normalized_points = (sampled_points - mean) / std
    
    # Save the normalized points
    np.save("NormalizedPoints.npy", normalized_points)

    # Load the normalized points and create a trimesh object
    normalized_points = np.load("NormalizedPoints.npy")
    mesh = trimesh.Trimesh(vertices=normalized_points, faces=faces)
    
    # Show
    mesh.show()