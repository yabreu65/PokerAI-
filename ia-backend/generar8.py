import os
from PIL import Image

# Lista de nombres de cartas para las cuales se generarán imágenes rotadas
card_names = [
    '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AH',
    '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AD',
    '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC',
    '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AS'
]

# Ángulos específicos para las rotaciones
angles = [90,180,270]

# Carpeta base donde se encuentran las imágenes originales
dataset_folder = 'dataset'

# Función para generar imágenes rotadas
def generate_rotated_images(image_path, output_folder, angles):
    img = Image.open(image_path)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    for angle in angles:
        rotated_img = img.rotate(angle, expand=True)  # Expande la imagen para que no recorte las esquinas
        rotated_img.save(os.path.join(output_folder, f"{base_name}_rot_{angle}.png"))
        print(f"Imagen generada: {base_name}_rot_{angle}.png")

# Itera sobre todas las subcarpetas y archivos en el dataset
for subdir, _, files in os.walk(dataset_folder):
    for file in files:
        file_path = os.path.join(subdir, file)
        
        # Verifica si el archivo coincide con alguna carta en card_names
        for card_name in card_names:
            if card_name in file:
                generate_rotated_images(file_path, subdir, angles)
                break  # Evita procesar el mismo archivo más de una vez si cumple varias condiciones
