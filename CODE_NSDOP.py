import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


print("Reading CSV...")
data = pd.read_csv("fashion-mnist_test.csv")
print("Data shape:", data.shape)

# Первая колонка — метка, остальные 784 — пиксели
y = data.iloc[:, 0].values           # labels (0–9)
X = data.iloc[:, 1:].values          # pixels

# Нормализация и reshape
X = X.astype("float32") / 255.0      # [0, 1]
X = X.reshape(-1, 28, 28, 1)         # (N, 28, 28, 1)

# Разделяем на train/val/test (из одного файла)
X_train_full, X_test, y_train_full, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
X_train, X_val, y_train, y_val = train_test_split(
    X_train_full, y_train_full, test_size=0.2, random_state=42, stratify=y_train_full
)

print("Train:", X_train.shape, y_train.shape)
print("Val:  ", X_val.shape,   y_val.shape)
print("Test: ", X_test.shape,  y_test.shape)

# ===== 2. ОПРЕДЕЛЕНИЕ МОДЕЛИ =====
class FashionMNISTCNN:
    def __init__(self):
        self.model = None
        self.datagen = None

    def create_data_augmentation(self):
        # Аугментация: случайные повороты, зум, сдвиги
        self.datagen = ImageDataGenerator(
            rotation_range=10,
            zoom_range=0.1,
            width_shift_range=0.1,
            height_shift_range=0.1
        )

    def compile_model(self):
        # Архитектура из методички:
        # Conv2D(32) -> MaxPooling2D -> Conv2D(64) -> MaxPooling2D
        # -> Flatten -> Dense(128, relu) -> Dropout(0.5) -> Dense(10, softmax)
        inputs = layers.Input(shape=(28, 28, 1))
        x = layers.Conv2D(32, kernel_size=3, padding='same', activation='relu')(inputs)
        x = layers.MaxPooling2D(pool_size=2)(x)
        x = layers.Conv2D(64, kernel_size=3, padding='same', activation='relu')(x)
        x = layers.MaxPooling2D(pool_size=2)(x)
        x = layers.Flatten()(x)
        x = layers.Dense(128, activation='relu')(x)
        x = layers.Dropout(0.5)(x)
        outputs = layers.Dense(10, activation='softmax')(x)

        self.model = models.Model(inputs=inputs, outputs=outputs)
        self.model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

    def train(self, X_train, y_train, X_val, y_val, epochs=30, batch_size=32):
        if self.datagen is None:
            self.create_data_augmentation()

        self.datagen.fit(X_train)

        history = self.model.fit(
            self.datagen.flow(X_train, y_train, batch_size=batch_size),
            epochs=epochs,
            validation_data=(X_val, y_val),
            verbose=1
        )
        return history

    def evaluate(self, X_test, y_test):
        test_loss, test_acc = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"Test accuracy: {test_acc:.4f}")
        print(f"Test loss: {test_loss:.4f}")
        return test_loss, test_acc

    def predict_single(self, image_28x28):
        """
        image_28x28: numpy-массив формы (28, 28) со значениями [0,255] или [0,1].
        """
        img = image_28x28.astype("float32")
        if img.max() > 1.0:
            img = img / 255.0
        img = np.expand_dims(img, -1)   # (28, 28, 1)
        img = np.expand_dims(img, 0)    # (1, 28, 28, 1)
        probs = self.model.predict(img, verbose=0)[0]
        return int(np.argmax(probs)), probs.tolist()


# ===== 3. ОБУЧЕНИЕ И ОЦЕНКА =====
cnn = FashionMNISTCNN()
cnn.compile_model()
print(cnn.model.summary())

history = cnn.train(X_train, y_train, X_val, y_val, epochs=30, batch_size=32)
cnn.evaluate(X_test, y_test)

# предсказания на части теста
y_pred_probs = cnn.model.predict(X_test[:100])
y_pred = y_pred_probs.argmax(axis=1)

# найдём ошибки
wrong_idx = np.where(y_pred != y_test[:100])[0]

# покажем первые 9 ошибок
plt.figure(figsize=(10,10))
for i, idx in enumerate(wrong_idx[:9]):
    plt.subplot(3,3,i+1)
    plt.imshow(X_test[idx].reshape(28,28), cmap='gray')
    plt.title(f"True: {y_test[idx]}, Pred: {y_pred[idx]}")
    plt.axis('off')
plt.tight_layout()
plt.show()


# history — это то, что вернул cnn.train(...)
plt.figure(figsize=(12,4))

plt.subplot(1,2,1)
plt.plot(history.history['accuracy'], label='train acc')
plt.plot(history.history['val_accuracy'], label='val acc')
plt.title('Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1,2,2)
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.show()


# пример предсказания для первого тестового изображения
pred_class, probs = cnn.predict_single(X_test[0].reshape(28, 28))
print("Predicted class for first test image:", pred_class)
print("Probabilities:", probs)


# найдём первый сверточный слой
for layer in cnn.model.layers:
    if isinstance(layer, tf.keras.layers.Conv2D):
        conv_layer = layer
        break

# получаем веса слоя: filters shape = (kh, kw, in_ch, out_ch)
filters, biases = conv_layer.get_weights()
print("Filters shape:", filters.shape)

# нормализуем для отображения
f_min, f_max = filters.min(), filters.max()
filters_norm = (filters - f_min) / (f_max - f_min + 1e-8)

n_filters = min(16, filters_norm.shape[3])   # покажем первые 16 фильтров
plt.figure(figsize=(8, 8))

for i in range(n_filters):
    f = filters_norm[:, :, 0, i]  # у нас вход 1‑канальный, берём канал 0
    plt.subplot(4, 4, i + 1)
    plt.imshow(f, cmap='gray')
    plt.axis('off')
    plt.title(f"F{i}")

plt.suptitle("Фильтры первого Conv2D слоя")
plt.tight_layout()
plt.show()

# берём одно изображение из теста
sample = X_test[0:1]  # shape (1, 28, 28, 1)

# создаём модель, выход которой — активации после первого Conv2D
from tensorflow.keras.models import Model
feature_model = Model(inputs=cnn.model.inputs, outputs=conv_layer.output)

feature_maps = feature_model.predict(sample)  # shape (1, h, w, n_filters)
h, w, n_feat = feature_maps.shape[1:]

n_show = min(16, n_feat)
plt.figure(figsize=(8, 8))
for i in range(n_show):
    fm = feature_maps[0, :, :, i]
    plt.subplot(4, 4, i + 1)
    plt.imshow(fm, cmap='viridis')
    plt.axis('off')
    plt.title(f"Map{i}")
plt.suptitle("Карты признаков первого Conv2D слоя")
plt.tight_layout()
plt.show()

