import tensorflow as tf

from model import create_model


def compile_model():

    model = create_model()

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.0001
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


if __name__ == "__main__":

    model = compile_model()

    print("\nModel compiled successfully!\n")

    print("Optimizer: Adam")
    print("Learning rate: 0.0001")
    print("Loss: Sparse Categorical Crossentropy")
    print("Metric: Accuracy")

    print("\nTrainable parameters:", model.count_params())