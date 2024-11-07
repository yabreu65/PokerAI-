import os
import requests

# Ruta donde deseas guardar el modelo
destination_dir = "/opt/render/project/src/ia-backend/training/model"
os.makedirs(destination_dir, exist_ok=True)  # Crea la carpeta si no existe

def download_model_from_drive(file_id, destination):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destination, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Modelo descargado en {destination}")
    else:
        print("Error al descargar el modelo.")

# Llama a la función con el file_id y la ruta de destino del modelo
download_model_from_drive("1hKzzE_KYzr6cV-3rmFHdTT3Zj2Lhesrm", os.path.join(destination_dir, "best_model_manual.keras"))
