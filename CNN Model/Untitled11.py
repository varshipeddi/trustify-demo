import tensorflow as tf
import numpy as np
import random
from tensorflow.keras.applications import VGG16
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report

# Set random seed for reproducibility
seed_value = 42
tf.random.set_seed(seed_value)
np.random.seed(seed_value)
random.seed(seed_value)

# Load the VGG16 model pre-trained on ImageNet, without the top (fully connected) layers
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(150, 150, 3))

# Freeze the base model layers (don't train them)
base_model.trainable = False

# Add custom layers on top of the base model
model = models.Sequential()
model.add(base_model)
model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dropout(0.5))  # Add dropout to prevent overfitting
model.add(layers.Dense(1, activation='sigmoid'))  # For binary classification

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Print the model summary
model.summary()

# Data Augmentation for the training set
train_datagen = ImageDataGenerator(
    rescale=1./255,  # Normalize pixel values
    shear_range=0.2, 
    zoom_range=0.2, 
    horizontal_flip=True
)

# No augmentation for the test set, only rescaling
test_datagen = ImageDataGenerator(rescale=1./255)

# Load train data from the directories (with Real and Fake subdirectories)
train_generator = train_datagen.flow_from_directory(
    './Dataset/Train',
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    seed=seed_value  # Seed for reproducibility
)

# Load test data from the directories (with Real and Fake subdirectories)
test_generator = test_datagen.flow_from_directory(
    './Dataset/Test',
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary',
    seed=seed_value  # Seed for reproducibility
)

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=20,  # Adjust according to your data
    epochs=20,  # You can adjust the number of epochs
    validation_data=test_generator,
    validation_steps=25
)

# Save the trained model in the Keras format (.keras)
model.save('real_vs_fake_vgg16_model.keras')

# Evaluate the model on the test data
test_loss, test_acc = model.evaluate(test_generator, steps=25)
print(f'Test Accuracy: {test_acc}')

# To check model predictions and classification report

# Get true labels and predicted labels for the test data
y_true = test_generator.classes
y_pred = model.predict(test_generator)
y_pred_class = np.where(y_pred > 0.5, 1, 0)  # Convert probabilities to class labels

# Generate classification report
print(classification_report(y_true, y_pred_class, target_names=['Fake', 'Real']))
