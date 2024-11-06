import os
import random

def reduce_dataset(dataset_path, images_to_keep=100):
    """
    Reduce el número de imágenes en cada subcarpeta del dataset, eliminando aleatoriamente
    las que excedan el límite especificado por `images_to_keep`.
    
    :param dataset_path: Ruta a la carpeta principal del dataset.
    :param images_to_keep: Número de imágenes que se mantendrán en cada subcarpeta.
    """
    for root, dirs, files in os.walk(dataset_path):
        if files:
            # Filtra solo los archivos de imagen (usualmente .jpg o .png)
            image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            # Si el número de imágenes supera el límite, elimina aleatoriamente el exceso
            if len(image_files) > images_to_keep:
                images_to_delete = random.sample(image_files, len(image_files) - images_to_keep)
                for image in images_to_delete:
                    image_path = os.path.join(root, image)
                    os.remove(image_path)
                    print(f"Eliminada: {image_path}")

    print(f"Reducción completada. Cada subcarpeta tiene un máximo de {images_to_keep} imágenes.")

# Ejemplo de uso:
dataset_path = '/home/yoryi/proyectos/IA/ia-backend/dataset'
  # Cambia esto a la ruta de tu dataset
reduce_dataset(dataset_path, images_to_keep=0)
