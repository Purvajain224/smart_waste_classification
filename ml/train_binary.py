import tensorflow as tf
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

from binary_model import create_model
from binary_data_loader import load_binary_datasets


MODEL_PATH = "ml/model/binary_waste_classifier.keras"
EPOCHS = 20


def main():
    print("Loading datasets...")
    train_dataset, validation_dataset, test_dataset = load_binary_datasets()

    print("\nCalculating class weights...")

    # Class order: Inorganic = 0, Organic = 1
    class_weights = compute_class_weight(
        class_weight="balanced",
        classes=np.array([0, 1]),
        y=np.concatenate([
            labels.numpy().flatten()
            for _, labels in train_dataset
        ]).astype(int)
    )

    class_weight_dict = {
        0: float(class_weights[0]),
        1: float(class_weights[1])
    }

    print("Class weights:", class_weight_dict)

    print("\nCreating custom CNN...")
    model = create_model()
    model.summary()

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            MODEL_PATH,
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
            verbose=1
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=4,
            restore_best_weights=True,
            verbose=1
        )
    ]

    print("\nStarting training...")

    model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=EPOCHS,
        class_weight=class_weight_dict,
        callbacks=callbacks
    )

    print("\nTraining completed!")
    print("Best model saved at:", MODEL_PATH)


if __name__ == "__main__":
    main()