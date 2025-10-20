import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras import models, layers
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image

# Install necessary packages (if not already installed)
os.system('pip install pillow pillow-heif')

# Load VGG16 without the top layers
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))
base_model.trainable = False

# Add custom layers
model = models.Sequential([
    base_model,
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(1, activation='sigmoid')  # Binary classification
])

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.00005),
              loss='binary_crossentropy', metrics=['accuracy'])

# Data augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    'C:/Users/phama/Downloads/Dataset-20241121T011202Z-001/Dataset/Train',
    target_size=(150, 150),
    batch_size=16,
    class_mode='binary'
)
test_generator = test_datagen.flow_from_directory(
    'C:/Users/phama/Downloads/Dataset-20241121T011202Z-001/Dataset/Test',
    target_size=(150, 150),
    batch_size=16,
    class_mode='binary',
    shuffle=False
)

# Wrapping generators in tf.data.Dataset and adding repeat()
train_dataset = tf.data.Dataset.from_generator(
    lambda: train_generator,
    output_signature=(
        tf.TensorSpec(shape=(None, 150, 150, 3), dtype=tf.float32),
        tf.TensorSpec(shape=(None,), dtype=tf.float32)
    )
).repeat()

test_dataset = tf.data.Dataset.from_generator(
    lambda: test_generator,
    output_signature=(
        tf.TensorSpec(shape=(None, 150, 150, 3), dtype=tf.float32),
        tf.TensorSpec(shape=(None,), dtype=tf.float32)
    )
).repeat()

# Calculate steps per epoch
steps_per_epoch = np.ceil(train_generator.samples / train_generator.batch_size).astype(int)
validation_steps = np.ceil(test_generator.samples / test_generator.batch_size).astype(int)

# Train the model
history = model.fit(
    train_dataset,
    steps_per_epoch=steps_per_epoch,
    epochs=50,
    validation_data=test_dataset,
    validation_steps=validation_steps
)

# Save the trained model in the Keras format (.keras)
model.save('real_vs_fake_vgg16_model.keras')

# Evaluate the model
test_loss, test_acc = model.evaluate(test_dataset, steps=validation_steps)
print(f'Test Accuracy: {test_acc * 100:.2f}%')

# Load the trained model
model = tf.keras.models.load_model('real_vs_fake_vgg16_model.keras')

# Function to load and preprocess the input image
def load_and_preprocess_image(img_path, target_size=(150, 150)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

# Function to predict whether the image is Real or Fake
def predict_image(img_path):
    preprocessed_image = load_and_preprocess_image(img_path)
    prediction = model.predict(preprocessed_image)
    img = image.load_img(img_path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

    if prediction[0] > 0.5:
        print(f'The image is predicted as: Real (Probability: {prediction[0][0]})')
    else:
        print(f'The image is predicted as: Fake (Probability: {prediction[0][0]})')

# Example usage
img_path = r'C:\Users\phama\Downloads\Real Airpods-20241121T011149Z-001\Real Airpods\IMG_7569.jpg'
predict_image(img_path)

