#!/bin/bash

echo "Ejecutando download_model.py para descargar el modelo..."
python download_model.py

MODEL_PATH="/tmp/model/best_model_manual.keras"
if [ -f "$MODEL_PATH" ]; then
  echo "El archivo de modelo se descargó correctamente."
else
  echo "Error: el archivo de modelo no se encontró en $MODEL_PATH."
  exit 1  # Salir si el archivo de modelo no está presente
fi

echo "Iniciando la aplicación con Gunicorn..."
gunicorn app:app --bind 0.0.0.0:$PORT
