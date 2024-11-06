import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import ModelCheckpoint

# Configuración del modelo
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 30
dataset_path = os.path.abspath('../dataset')
print(f"Usando la ruta absoluta: {dataset_path}")

# Lista de nombres de clases en el orden esperado
card_names = [
    '00_00_2H', '00_01_3H', '00_02_4H', '00_03_5H', '00_04_6H', '00_05_7H', '00_06_8H', '00_07_9H',
    '00_08_10H', '00_09_JH', '00_10_QH', '00_11_KH', '00_12_AH', '01_00_2D', '01_01_3D', '01_02_4D', 
    '01_03_5D', '01_04_6D', '01_05_7D', '01_06_8D', '01_07_9D', '01_08_10D', '01_09_JD', '01_10_QD', 
    '01_11_KD', '01_12_AD', '02_00_2C', '02_01_3C', '02_02_4C', '02_03_5C', '02_04_6C', '02_05_7C', 
    '02_06_8C', '02_07_9C', '02_08_10C', '02_09_JC', '02_10_QC', '02_11_KC', '02_12_AC', '03_00_2S', 
    '03_01_3S', '03_02_4S', '03_03_5S', '03_04_6S', '03_05_7S', '03_06_8S', '03_07_9S', '03_08_10S', 
    '03_09_JS', '03_10_QS', '03_11_KS', '03_12_AS'
]

# Confirmación de existencia de `dataset`
if not os.path.exists(dataset_path):
    print("Error: No se encontró la carpeta 'dataset' en la ruta especificada.")
else:
    print("Contenido de '../dataset':", os.listdir(dataset_path))

# Crear el modelo CNN
def create_model():
    model = Sequential([
        Conv2D(64, (3, 3), activation='relu', input_shape=(*IMG_SIZE, 1)),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        
        Conv2D(128, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        
        Conv2D(256, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        
        Conv2D(512, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(2, 2),
        
        Flatten(),
        
        Dense(512, activation='relu', kernel_regularizer=l2(0.001)),
        Dropout(0.5),
        
        Dense(256, activation='relu', kernel_regularizer=l2(0.001)),
        Dropout(0.5),
        
        Dense(52, activation='softmax')  # 52 clases para las cartas
    ])
    model.compile(optimizer=Adam(learning_rate=1e-4), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Generador de datos con aumentación
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

# Creación de datasets de entrenamiento y validación
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

# Verificación del orden de clases
class_indices = train_data.class_indices
ordered_classes = sorted(class_indices, key=lambda x: class_indices[x])

if ordered_classes != card_names:
    print("Advertencia: El orden de clases en el dataset no coincide con `card_names`.")
else:
    print("El orden de clases coincide con `card_names`.")

# Entrenamiento y guardado del modelo con ModelCheckpoint
model = create_model()
checkpoint = ModelCheckpoint(
    'model/best_model_manual.keras', monitor='val_accuracy', save_best_only=True, verbose=1
)

history = model.fit(train_data, epochs=EPOCHS, validation_data=val_data, callbacks=[checkpoint])

# Guardar el modelo final
os.makedirs('model', exist_ok=True)
final_model_path = os.path.abspath('model/naipe_model.keras')
model.save(final_model_path)
print(f"Modelo entrenado y guardado en '{final_model_path}'")
