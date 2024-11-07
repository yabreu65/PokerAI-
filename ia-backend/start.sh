#!/bin/bash
# Ejecuta el script de descarga del modelo
python download_model.py

# Espera hasta que el archivo de modelo esté disponible
while [ ! -f "/opt/render/project/src/ia-backend/training/model/best_model_manual.keras" ]; do
  echo "Esperando que el archivo de modelo esté disponible..."
  sleep 5
done

# Inicia la aplicación con Gunicorn
gunicorn app:app --bind 0.0.0.0:$PORT
