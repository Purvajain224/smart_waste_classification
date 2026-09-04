import tensorflow as tf

from data_loader import load_datasets

MODEL_PATH = "ml/model/waste_classifier_best.keras"

FINE_TUNE_EPOCHS = 10
FINE_TUNE_LAYERS = 30


def main():
    print("Loading datasets...")
    train_dataset, validation_dataset, _ = load_datasets()

    print("Loading previously trained model...")
    model = tf.keras.models.load_model(MODEL_PATH)

    print("Preparing MobileNetV2 for fine-tuning...")

    # Get the MobileNetV2 backbone
    base_model = model.get_layer("mobilenetv2_1.00_224")

    # Unfreeze the MobileNetV2 backbone
    base_model.trainable = True

    # Freeze all layers except the last 30
    for layer in base_model.layers[:-FINE_TUNE_LAYERS]:
        layer.trainable = False

    # Keep BatchNormalization layers frozen
    # This makes fine-tuning more stable on a relatively small dataset.
    for layer in base_model.layers:
        if isinstance(layer, tf.keras.layers.BatchNormalization):
            layer.trainable = False

    print(
        f"Unfrozen top {FINE_TUNE_LAYERS} MobileNetV2 layers "
        "for fine-tuning."
    )

    # Recompile with a very small learning rate
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    # Save only when validation accuracy improves
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        MODEL_PATH,
        monitor="val_accuracy",
        save_best_only=True,
        mode="max",
        verbose=1
    )

    # Stop if the model stops improving
    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True,
        verbose=1
    )

    print("\nStarting fine-tuning...\n")

    history = model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=FINE_TUNE_EPOCHS,
        callbacks=[checkpoint, early_stopping]
    )

    print("\nFine-tuning completed!")
    print(f"Best model saved at: {MODEL_PATH}")


if __name__ == "__main__":
    main()