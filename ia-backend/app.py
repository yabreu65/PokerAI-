from flask import Flask, request, jsonify
import os
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite CORS en todas las rutas
CORS(app, resources={r"/*": {"origins": "*"}})
# Cargar el modelo entrenado
model_path = os.path.abspath('training/model/best_model_manual.keras')
try:
    model = load_model(model_path)
    print("Modelo cargado exitosamente desde:", model_path)
except Exception as e:
    print("Error al cargar el modelo:", e)
    model = None

card_names = [
    "00_00_2H", "00_01_3H", "00_02_4H", "00_03_5H", "00_04_6H", "00_05_7H", "00_06_8H", "00_07_9H", "00_08_10H", "00_09_JH", "00_10_QH", "00_11_KH", "00_12_AH",
    "01_00_2D", "01_01_3D", "01_02_4D", "01_03_5D", "01_04_6D", "01_05_7D", "01_06_8D", "01_07_9D", "01_08_10D", "01_09_JD", "01_10_QD", "01_11_KD", "01_12_AD",
    "02_00_2C", "02_01_3C", "02_02_4C", "02_03_5C", "02_04_6C", "02_05_7C", "02_06_8C", "02_07_9C", "02_08_10C", "02_09_JC", "02_10_QC", "02_11_KC", "02_12_AC",
    "03_00_2S", "03_01_3S", "03_02_4S", "03_03_5S", "03_04_6S", "03_05_7S", "03_06_8S", "03_07_9S", "03_08_10S", "03_09_JS", "03_10_QS", "03_11_KS", "03_12_AS"
]


def preprocess_image(img):
    img = img.resize((128, 128))  # Ajusta al tamaño de entrada esperado
    img = img.convert('L')  # Convierte a escala de grises
    img_array = np.array(img) / 255.0  # Normaliza
    img_array = np.expand_dims(img_array, axis=(0, -1))  # Agrega dimensiones para lotes y canales
    return img_array

# Ruta para predicciones
@app.route('/predict', methods=['POST'])
def predict():
    print("Solicitud recibida en /predict")
    try:
        if 'file' not in request.files:
            print("No file part in the request")
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['file']
        if file.filename == '':
            print("No selected file")
            return jsonify({'error': 'No selected file'}), 400

        img = Image.open(io.BytesIO(file.read()))
        img_array = preprocess_image(img)

        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)[0]
        predicted_card = card_names[predicted_class]

        print(f"Predicción realizada: {predicted_card}")
        return jsonify({
            'prediction': predicted_card,
            'index': int(predicted_class),
            'class': predicted_card
        })

    except Exception as e:
        print("Error en /predict:", e)
        return jsonify({'error': 'Ocurrió un error interno en el servidor'}), 500

if __name__ == '__main__':
 
    app.run(host='0.0.0.0', port=5001, debug=True)  # Cambiado a 0.0.0.0 para aceptar conexiones externas
