import tensorflow as tf
import os

# Nombres de clases en el formato de las carpetas: '00_00_2H', '00_01_3H', etc.
card_names = [
    '00_00_2H', '00_01_3H', '00_02_4H', '00_03_5H', '00_04_6H', '00_05_7H', '00_06_8H', '00_07_9H', '00_08_10H', 
    '00_09_JH', '00_10_QH', '00_11_KH', '00_12_AH',
    '01_00_2D', '01_01_3D', '01_02_4D', '01_03_5D', '01_04_6D', '01_05_7D', '01_06_8D', '01_07_9D', '01_08_10D', 
    '01_09_JD', '01_10_QD', '01_11_KD', '01_12_AD',
    '02_00_2C', '02_01_3C', '02_02_4C', '02_03_5C', '02_04_6C', '02_05_7C', '02_06_8C', '02_07_9C', '02_08_10C', 
    '02_09_JC', '02_10_QC', '02_11_KC', '02_12_AC',
    '03_00_2S', '03_01_3S', '03_02_4S', '03_03_5S', '03_04_6S', '03_05_7S', '03_06_8S', '03_07_9S', '03_08_10S', 
    '03_09_JS', '03_10_QS', '03_11_KS', '03_12_AS'
]

# Ruta a tu dataset
dataset_dir = 'dataset'

# Cargar el dataset
dataset = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_dir,
    label_mode='int',
    image_size=(180, 180),
    batch_size=32
)

# Verificar si las clases en el dataset coinciden con 'card_names'
mismatch = False
for index, class_name in enumerate(dataset.class_names):
    expected_class_name = card_names[index]
    if class_name != expected_class_name:
        print(f"Desajuste: Índice {index} se asocia con {class_name}, pero se esperaba {expected_class_name}")
        mismatch = True

if not mismatch:
    print("Las clases están correctamente ordenadas y coinciden con 'card_names'.")
else:
    print("Hay desajustes en el orden de las clases.")

# Mostrar el orden de las clases detectado
print("\nOrden de clases detectado:")
for index, class_name in enumerate(dataset.class_names):
    print(f"Índice {index}: {class_name}")
