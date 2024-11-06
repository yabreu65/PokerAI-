from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Definir el orden de nombres de cartas esperado
card_names = [
    "00_00_2H", "00_01_3H", "00_02_4H", "00_03_5H", "00_04_6H", "00_05_7H", "00_06_8H", "00_07_9H", "00_08_10H", "00_09_JH", "00_10_QH", "00_11_KH", "00_12_AH",
    "01_00_2D", "01_01_3D", "01_02_4D", "01_03_5D", "01_04_6D", "01_05_7D", "01_06_8D", "01_07_9D", "01_08_10D", "01_09_JD", "01_10_QD", "01_11_KD", "01_12_AD",
    "02_00_2C", "02_01_3C", "02_02_4C", "02_03_5C", "02_04_6C", "02_05_7C", "02_06_8C", "02_07_9C", "02_08_10C", "02_09_JC", "02_10_QC", "02_11_KC", "02_12_AC",
    "03_00_2S", "03_01_3S", "03_02_4S", "03_03_5S", "03_04_6S", "03_05_7S", "03_06_8S", "03_07_9S", "03_08_10S", "03_09_JS", "03_10_QS", "03_11_KS", "03_12_AS"
]


# Configuración de rutas
dataset_path = 'dataset'  # Ruta a la carpeta del dataset

# Crear un generador de datos con ImageDataGenerator para cargar las imágenes en lotes
datagen = ImageDataGenerator()
train_data = datagen.flow_from_directory(
    dataset_path,
    target_size=(224, 224),  # Ajusta al tamaño que usa tu modelo
    batch_size=32,
    class_mode='categorical',
    shuffle=False  # Importante para mantener el orden de las carpetas
)

# Obtener el orden de las clases del generador de datos
class_indices = train_data.class_indices

# Invertir el diccionario para obtener el índice a partir del nombre de la clase
index_to_class = {v: k for k, v in class_indices.items()}

# Comparar el orden con card_names
correct_order = True
for i, card_name in enumerate(card_names):
    if index_to_class[i] != card_name:
        print(f"Desajuste: Índice {i} se asocia con {index_to_class[i]}, pero se esperaba {card_name}")
        correct_order = False

if correct_order:
    print("Todas las clases están en el orden correcto.")
else:
    print("Hay desajustes en el orden de las clases.")

# Imprimir el orden de clases detectado para referencia
print("\nOrden de clases detectado:")
for i in range(len(card_names)):
    print(f"Índice {i}: {index_to_class[i]}")
