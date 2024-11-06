from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import os

# Ruta de tus imágenes de entrenamiento o validación
source_dir = 'dataset'
test_dir = 'test_data'

# Crear el directorio de prueba si no existe
if not os.path.exists(test_dir):
    os.makedirs(test_dir)

# Configuración de aumentación
datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    brightness_range=[0.7, 1.3],
    fill_mode='nearest'
)

# Procesar las imágenes y guardarlas en testData
for class_dir in os.listdir(source_dir):
    class_path = os.path.join(source_dir, class_dir)
    target_class_path = os.path.join(test_dir, class_dir)
    os.makedirs(target_class_path, exist_ok=True)

    for img_name in os.listdir(class_path):
        img_path = os.path.join(class_path, img_name)
        
        # Cargar y convertir la imagen a un array
        img = load_img(img_path)
        img = img_to_array(img)
        img = img.reshape((1,) + img.shape)  # Redimensionar para ImageDataGenerator

        # Generar solo una variación por imagen
        i = 0
        for batch in datagen.flow(img, batch_size=1, save_to_dir=target_class_path, save_prefix='test_aug', save_format='jpeg'):
            i += 1
            if i >= 1:  # Solo una variación
                break
