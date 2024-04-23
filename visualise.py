import os
import trimesh
import numpy as np

# Load and sample the mesh objects
oto1 = trimesh.load(os.path.join("otolithe", "Segmentation_05a-01.ply")).sample(2048)
sulcus1 = trimesh.load(os.path.join("Slicer3d/Segmentation_05a-01", "sulcus1.ply")).sample(2048)

# Define a distance threshold
distance_threshold = 0.05  # Adjust as needed

# Create an empty array to store sulcus labels for each point in otolith
sulcus_labels = np.zeros(len(oto1))

# Iterate over each point in otolith and check its distance to points in sulcus
for i, point_oto1 in enumerate(oto1):
    distances = np.linalg.norm(sulcus1 - point_oto1, axis=1)
    min_distance = np.min(distances)
    if min_distance < distance_threshold:
        sulcus_labels[i] = 1

# Print the number of points labeled as sulcus
print("Number of sulcus points:", np.sum(sulcus_labels))