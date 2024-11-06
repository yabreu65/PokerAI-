import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image_dataset_from_directory

# Cargar el modelo entrenado
model_path = 'training/model/naipe_model_finetuned.keras'
model = load_model(model_path)

# Definir la lista de nombres de clases para las 52 cartas
class_names = [
    '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AH',  # Corazones
    '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AD',  # Diamantes
    '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC',  # Tréboles
    '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AS'   # Espadas
]

# Clases objetivo (corazones y diamantes)
target_classes = {name for name in class_names if name.endswith('H') or name.endswith('D')}

# Configurar el dataset de test
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
test_data_path = os.path.abspath('./temp_dataset')  # Ruta del test dataset

test_data = image_dataset_from_directory(
    test_data_path,
    label_mode=None,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    color_mode='grayscale'  # Escala de grises
)

# Realizar predicciones
predictions = model.predict(test_data)
pred_classes = np.argmax(predictions, axis=1)  # Clases predecidas

# Interpretar las predicciones como corazones o diamantes
for i, pred_class in enumerate(pred_classes):
    # Obtener el nombre de la clase predicha
    predicted_name = class_names[pred_class]
    
    # Verificar si pertenece a corazones o diamantes
    if predicted_name in target_classes:
        final_prediction = 'corazones' if predicted_name.endswith('H') else 'diamantes'
    else:
        final_prediction = "Clase desconocida"

    print(f"Imagen {i + 1}: Predicción = {final_prediction}")
