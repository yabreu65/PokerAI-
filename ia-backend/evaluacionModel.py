import os
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# Configuración
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
additional_epochs = 15
fine_tuned_model_path = 'training/model/naipe_model_finetuned.keras'

# Cargar el modelo ajustado existente
model = load_model(fine_tuned_model_path)

# Descongelar las últimas capas para el ajuste fino
for layer in model.layers[-5:]:  # Ajusta el número de capas a descongelar si es necesario
    layer.trainable = True

# Re-compilar el modelo con una tasa de aprendizaje baja
model.compile(optimizer=Adam(learning_rate=1e-5), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Generadores de datos para entrenamiento y validación
dataset_path = os.path.abspath('./dataset')
datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.3,
    brightness_range=[0.5, 1.5],
    horizontal_flip=True,
    vertical_flip=True,
    validation_split=0.2
)

train_data = datagen.flow_from_directory(
    dataset_path,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    color_mode='grayscale',
    class_mode='sparse',
    subset='training'
)

val_data = datagen.flow_from_directory(
    dataset_path,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    color_mode='grayscale',
    class_mode='sparse',
    subset='validation'
)

# Configurar ModelCheckpoint y EarlyStopping
checkpoint = ModelCheckpoint(
    fine_tuned_model_path,
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)

early_stopping = EarlyStopping(
    monitor='val_accuracy',
    patience=2,  # Detiene si no mejora en 2 épocas consecutivas
    restore_best_weights=True
)

# Entrenar el modelo durante 5 épocas adicionales
history = model.fit(
    train_data,
    epochs=additional_epochs,  # Ajuste adicional
    validation_data=val_data,
    callbacks=[checkpoint, early_stopping]
)

# Evaluación del modelo después del ajuste adicional
test_datagen = ImageDataGenerator(rescale=1.0/255)
test_data = test_datagen.flow_from_directory(
    'test_data',  # Asegúrate de que esta ruta apunta a tu carpeta de test
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    color_mode='grayscale',
    class_mode='sparse',
    shuffle=False
)

# Cargar el mejor modelo guardado y evaluar
model = load_model(fine_tuned_model_path)
test_loss, test_accuracy = model.evaluate(test_data)
print(f"\nPrecisión en el conjunto de prueba después de épocas adicionales: {test_accuracy:.2f}")
print(f"Pérdida en el conjunto de prueba después de épocas adicionales: {test_loss:.2f}")
