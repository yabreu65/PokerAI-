import cv2
import numpy as np
import random
from PIL import Image, ImageEnhance, ImageFilter, UnidentifiedImageError
import os

def augment_specific_style(image_path, output_folder, num_variations=30, is_diamond=False):
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

        # Ajuste de brillo aleatorio entre 0.7 y 1.6 para corazones y 0.5 a 1.4 para diamantes
        enhancer = ImageEnhance.Brightness(augmented_img)
        if is_diamond:
            augmented_img = enhancer.enhance(random.uniform(0.5, 1.4))
        else:
            augmented_img = enhancer.enhance(random.uniform(0.7, 1.6))

        # Ajuste de contraste con diferencias entre corazones y diamantes
        enhancer = ImageEnhance.Contrast(augmented_img)
        if is_diamond:
            augmented_img = enhancer.enhance(random.uniform(0.6, 1.3))
        else:
            augmented_img = enhancer.enhance(random.uniform(0.8, 1.5))

        # Desenfoque aleatorio
        if random.choice([True, False]):
            augmented_img = augmented_img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 2)))

        # Variación de color ligera para destacar
        if not is_diamond:
            enhancer = ImageEnhance.Color(augmented_img)
            augmented_img = enhancer.enhance(random.uniform(1.1, 1.3))

        # Conversión a OpenCV para transformaciones adicionales
        augmented_img_cv = cv2.cvtColor(np.array(augmented_img), cv2.COLOR_RGB2BGR)

        # Agregar ruido aleatorio
        if random.choice([True, False]):
            noise = np.random.normal(0, 10, augmented_img_cv.shape)
            augmented_img_cv = cv2.add(augmented_img_cv, noise.astype(np.uint8))

        # Distorsión de perspectiva
        rows, cols, _ = augmented_img_cv.shape
        pts1 = np.float32([[0, 0], [cols, 0], [0, rows], [cols, rows]])
        shift_x = random.randint(-15, 15)
        shift_y = random.randint(-15, 15)
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
        output_path = os.path.join(output_folder, f"{file_name}_aug_{i + 1}.png")
        
        # Asegurar que la imagen se guarde correctamente
        with open(output_path, 'wb') as f:
            augmented_img_final.save(f, format='PNG')

# Función para aplicar el aumento de datos en corazones y diamantes
def augment_heart_diamond(dataset_folder):
    for subdir, _, files in os.walk(dataset_folder):
        # Selección de variaciones específicas para corazones y diamantes
        is_diamond = 'diamantes' in subdir
        num_variations = 40 if 'corazones' in subdir or is_diamond else 20
        for file in files:
            image_path = os.path.join(subdir, file)
            if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
            augment_specific_style(image_path, subdir, num_variations=num_variations, is_diamond=is_diamond)

# Ejecutar la función para corazones y diamantes
dataset_folder = 'dataset'
augment_heart_diamond(dataset_folder)
