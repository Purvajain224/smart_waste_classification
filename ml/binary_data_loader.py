import tensorflow as tf

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

DATASET_DIR = "ml/binary_dataset"


def load_binary_datasets():
    train_dataset = tf.keras.utils.image_dataset_from_directory(
        f"{DATASET_DIR}/train",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="binary",
        shuffle=True,
        seed=42
    )

    validation_dataset = tf.keras.utils.image_dataset_from_directory(
        f"{DATASET_DIR}/validation",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="binary",
        shuffle=False
    )

    test_dataset = tf.keras.utils.image_dataset_from_directory(
        f"{DATASET_DIR}/test",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="binary",
        shuffle=False
    )

    print("\nClass names:", train_dataset.class_names)

    # Improve data loading performance
    train_dataset = train_dataset.prefetch(
        buffer_size=tf.data.AUTOTUNE
    )
    validation_dataset = validation_dataset.prefetch(
        buffer_size=tf.data.AUTOTUNE
    )
    test_dataset = test_dataset.prefetch(
        buffer_size=tf.data.AUTOTUNE
    )

    return train_dataset, validation_dataset, test_dataset


if __name__ == "__main__":
    load_binary_datasets()