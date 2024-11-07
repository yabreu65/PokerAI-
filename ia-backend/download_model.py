import os
import requests

# Ruta donde deseas guardar el modelo
destination_dir = "/opt/render/project/src/ia-backend/training/model"
os.makedirs(destination_dir, exist_ok=True)  # Crea la carpeta si no existe

def download_model_from_drive(file_id, destination):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    session = requests.Session()
    print("Iniciando la descarga del modelo desde Google Drive...")

    # Primera solicitud para obtener la confirmación (si es necesaria)
    response = session.get(url, stream=True)
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            url = f"https://drive.google.com/uc?export=download&confirm={value}&id={file_id}"
            response = session.get(url, stream=True)

    # Descarga el archivo si la respuesta es exitosa
    if response.status_code == 200:
        with open(destination, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Modelo descargado en {destination}")
    else:
        print("Error al descargar el modelo. Código de estado:", response.status_code)

# Llama a la función con el file_id y la ruta de destino del modelo
model_path = os.path.join(destination_dir, "best_model_manual.keras")
download_model_from_drive("1hKzzE_KYzr6cV-3rmFHdTT3Zj2Lhesrm", model_path)

# Verifica si el archivo fue descargado
if os.path.exists(model_path):
    print("El archivo de modelo se descargó correctamente y está listo para usarse.")
else:
    print("Error: el archivo de modelo no se encontró en la ubicación esperada después de la descarga.")
