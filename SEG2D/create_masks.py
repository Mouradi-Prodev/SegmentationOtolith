import os
import cv2
from skimage import io
# Fonction pour générer des masques pour un dossier d'images
def generate_masks_for_images(input_folder, output_folder):
    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Parcourir toutes les images dans le dossier d'entrée
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Vérifier les extensions des fichiers d'image
            # Charger l'image
            image = cv2.imread(os.path.join(input_folder, filename))
            # Convertir l'image en niveaux de gris
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Appliquer un seuillage pour créer le masque
            _, mask = cv2.threshold(gray_image, 95, 254, cv2.THRESH_BINARY_INV)
            # Sauvegarder le masque
            mask_filename = os.path.splitext(filename)[0] + ".png"  # Vous pouvez ajuster l'extension du masque si nécessaire
            cv2.imwrite(os.path.join(output_folder, mask_filename), mask)

# Spécifier le dossier d'entrée contenant les images
input_folder = "images"

# Spécifier le dossier de sortie pour les masques
output_folder = "masks"

# Appeler la fonction pour générer les masques
generate_masks_for_images(input_folder, output_folder)