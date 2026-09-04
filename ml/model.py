import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

IMG_SIZE = (224, 224)
NUM_CLASSES = 5


def create_model():
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,
        weights="imagenet"
    )

    # Start with the MobileNetV2 base frozen
    base_model.trainable = False

    # Data augmentation
    data_augmentation = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
        layers.RandomContrast(0.1),
    ], name="data_augmentation")

    # Input
    inputs = keras.Input(shape=(*IMG_SIZE, 3))

    # Augmentation
    x = data_augmentation(inputs)

    # MobileNetV2 preprocessing
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)

    # Feature extraction
    x = base_model(x, training=False)

    # Classification head
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)

    # Five waste classes
    outputs = layers.Dense(
        NUM_CLASSES,
        activation="softmax"
    )(x)

    model = keras.Model(inputs, outputs)

    return model


if __name__ == "__main__":
    model = create_model()
    model.summary()