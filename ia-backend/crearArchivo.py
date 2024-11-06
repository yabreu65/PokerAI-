import os
import shutil

# Directorio de origen donde están las imágenes individuales
source_dir = 'dataset/cartas'

# Directorio de destino donde están las carpetas organizadas
destination_base_dir = 'dataset'

# Lista de nombres de cartas en el orden especificado
card_names = [
    '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AH',
    '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AD',
    '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC',
    '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AS'
]

# Copia cada imagen a su carpeta correspondiente
for index, card_name in enumerate(card_names):
    # Determina el nombre de la carpeta de destino
    suit_index = index // 13  # Cada 13 cartas cambiamos de palo
    card_index = index % 13   # Índice dentro del palo
    destination_folder = f"{suit_index:02d}_{card_index:02d}_{card_name}"  # Usar dos dígitos para el orden
    destination_path = os.path.join(destination_base_dir, destination_folder)
    
    # Crear la carpeta de destino si no existe
    os.makedirs(destination_path, exist_ok=True)
    
    # Ubica la imagen en la carpeta de origen
    image_name = f"{card_name}.png"  # Asegúrate de que las imágenes tengan esta extensión
    source_image_path = os.path.join(source_dir, image_name)
    
    # Copia la imagen a la carpeta de destino si existe
    if os.path.exists(source_image_path):
        shutil.copy2(source_image_path, destination_path)
        print(f"Copiado {image_name} a {destination_path}")
    else:
        print(f"Imagen {image_name} no encontrada en {source_dir}")
