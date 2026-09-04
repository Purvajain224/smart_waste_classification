import tensorflow as tf


# Image configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Dataset locations
TRAIN_DIR = "ml/dataset/train"
VALIDATION_DIR = "ml/dataset/validation"
TEST_DIR = "ml/dataset/test"


def load_datasets():

    train_dataset = tf.keras.utils.image_dataset_from_directory(
        TRAIN_DIR,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=True,
        seed=42
    )

    validation_dataset = tf.keras.utils.image_dataset_from_directory(
        VALIDATION_DIR,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    test_dataset = tf.keras.utils.image_dataset_from_directory(
        TEST_DIR,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    return train_dataset, validation_dataset, test_dataset


if __name__ == "__main__":

    train_dataset, validation_dataset, test_dataset = load_datasets()

    print("\nClass names:")
    print(train_dataset.class_names)

    print("\nDataset loaded successfully!")

    print("Training batches:", tf.data.experimental.cardinality(train_dataset).numpy())
    print("Validation batches:", tf.data.experimental.cardinality(validation_dataset).numpy())
    print("Test batches:", tf.data.experimental.cardinality(test_dataset).numpy())