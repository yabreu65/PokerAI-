import cv2
import numpy as np
import random
from PIL import Image, ImageEnhance, ImageFilter, UnidentifiedImageError
import os

def augment_mobile_style(image_path, output_folder, num_variations=30):
    try:
        img = Image.open(image_path)
    except UnidentifiedImageError:
        print(f"Archivo no válido (no es una imagen): {image_path}")
        return

    for i in range(num_variations):
        augmented_img = img.copy()

        # Rotación aleatoria entre -20 y +20 grados
        angle = random.uniform(-20, 20)
        augmented_img = augmented_img.rotate(angle)

        # Ajuste de brillo aleatorio entre 0.5 y 1.6
        enhancer = ImageEnhance.Brightness(augmented_img)
        augmented_img = enhancer.enhance(random.uniform(0.5, 1.6))

        # Ajuste de contraste aleatorio entre 0.6 y 1.4
        enhancer = ImageEnhance.Contrast(augmented_img)
        augmented_img = enhancer.enhance(random.uniform(0.6, 1.4))

        # Desenfoque aleatorio
        if random.choice([True, False]):
            augmented_img = augmented_img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 3)))

        # Rotación leve adicional para simular perspectiva
        augmented_img = augmented_img.rotate(random.uniform(-5, 5))

        # Conversión a OpenCV para aplicar transformaciones adicionales
        augmented_img_cv = cv2.cvtColor(np.array(augmented_img), cv2.COLOR_RGB2BGR)

        # Ruido aleatorio
        if random.choice([True, False]):
            noise = np.random.normal(0, 15, augmented_img_cv.shape)
            augmented_img_cv = cv2.add(augmented_img_cv, noise.astype(np.uint8))

        # Distorsión de perspectiva adicional
        rows, cols, _ = augmented_img_cv.shape
        pts1 = np.float32([[0, 0], [cols, 0], [0, rows], [cols, rows]])
        shift_x = random.randint(-25, 25)
        shift_y = random.randint(-25, 25)
        pts2 = np.float32([
            [shift_x, shift_y],
            [cols - shift_x, shift_y],
            [shift_x, rows - shift_y],
            [cols - shift_x, rows - shift_y]
        ])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        augmented_img_cv = cv2.warpPerspective(augmented_img_cv, M, (cols, rows))

        # Convertir de nuevo a PIL para guardar
        augmented_img_final = Image.fromarray(cv2.cvtColor(augmented_img_cv, cv2.COLOR_BGR2RGB))
        
        # Guardar en la misma carpeta que la imagen original
        file_name = os.path.splitext(os.path.basename(image_path))[0]
        augmented_img_final.save(os.path.join(output_folder, f"{file_name}_aug_{i + 1}.png"))

# Función para aplicar el aumento de datos en todas las imágenes del dataset
def augment_all_images_mobile_style(dataset_folder):
    for subdir, _, files in os.walk(dataset_folder):
        # Aumentar el número de variaciones para cartas problemáticas (J, Q, K, corazones, diamantes)
        num_variations = 150 if any(card in subdir for card in ['J', 'Q', 'K', 'H', 'D']) else 20
        for file in files:
            image_path = os.path.join(subdir, file)
            # Ignorar archivos que no sean de imagen
            if not file.lower().endswith(('.png')):
                print(f"Ignorado: {image_path}")
                continue
            print(f"Generando {num_variations} variaciones para: {image_path}")
            augment_mobile_style(image_path, subdir, num_variations=num_variations)

# Ejecutar la función para todo el dataset
dataset_folder = 'dataset'
augment_all_images_mobile_style(dataset_folder)
