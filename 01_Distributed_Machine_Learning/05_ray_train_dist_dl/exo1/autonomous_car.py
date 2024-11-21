import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Conv2D, Flatten, MaxPool2D, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.metrics import SparseCategoricalAccuracy
import json
import pandas as pd
import os
from typing import Dict
from ray import train
from ray.train import Checkpoint, ScalingConfig
from ray.train.tensorflow import TensorflowTrainer
from ray.train.tensorflow.keras import ReportCheckpointCallback
import tempfile


# Get working directory path
dir_path = os.getcwd()
# Load dataset into a working directory
tf.keras.utils.get_file(
    f"{dir_path}/content/cifar10.zip",
    origin="https://full-stack-assets.s3.eu-west-3.amazonaws.com/datasets/M08/cifar-10/train.zip",
    extract=True,
    cache_subdir=f"{dir_path}/content",
)


# Load dataset
def cifar_dataset(batch_size=64):

    # Import labels and add .png extension to ids
    data = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/datasets/M08/cifar-10/trainLabels.csv")
    data["id"] = data["id"].astype("str") + ".png"
    # Data Augmentation preprocessing
    img_generator = ImageDataGenerator(
        brightness_range=(0.5, 1),  # Random brightness modification
        channel_shift_range=50.0,  # Random hue modification
        horizontal_flip=True,  # Randomly flips image horizontally
        vertical_flip=True,  # Randomly flips image virtically
        rescale=1 / 255.0,  # Rescaling values from [0,255]->[0,1]
        validation_split=0.3,  # Portion of the data that can be saved for validation
    )

    train_generator = img_generator.flow_from_dataframe(
        dataframe=data,  # the dataframe containing the filename and label column
        directory=f"{dir_path}/content/train",  # the directory containing the image files
        x_col="id",  # the name of the column with the filenames
        y_col="label",  # the name of the column with the labels
        target_size=(32, 32),
        batch_size=batch_size,
        class_mode="sparse",
        shuffle=True,
        subset="training",
    )

    val_generator = img_generator.flow_from_dataframe(
        dataframe=data,  # the dataframe containing the filename and label column
        directory=f"{dir_path}/content/train",  # the directory containing the image files
        x_col="id",  # the name of the column with the filenames
        y_col="label",  # the name of the column with the labels
        target_size=(32, 32),
        batch_size=batch_size,
        class_mode="sparse",
        shuffle=True,
        subset="validation",
    )

    return train_generator, val_generator


# Building model
def build_and_compile_model(config):

    model = Sequential(
        [
            Conv2D(32, (3, 3), padding="same", input_shape=([32, 32, 3])),
            MaxPool2D(),
            Flatten(),
            Dense(10, activation="softmax"),
        ]
    )

    model.compile(optimizer=Adam(), loss=SparseCategoricalCrossentropy(), metrics=[SparseCategoricalAccuracy()])
    return model


def train_func_distributed(config):
    per_worker_batch_size = 64
    # This environment variable will be set by Ray Train.
    tf_config = json.loads(os.environ["TF_CONFIG"])
    num_workers = len(tf_config["cluster"]["worker"])

    strategy = tf.distribute.MultiWorkerMirroredStrategy()

    global_batch_size = per_worker_batch_size * num_workers
    multi_worker_dataset, validation_set = cifar_dataset(global_batch_size)

    start_epoch = 0
    with strategy.scope():
        # Model building/compiling need to be within `strategy.scope()`.
        multi_worker_model = build_and_compile_model(config)

    results = []
    for epoch in range(start_epoch, start_epoch + config["num_epochs"]):
        print(f"##### Epoch: {epoch} #####")
        history = multi_worker_model.fit(
            multi_worker_dataset, epochs=1, validation_data=validation_set, callbacks=[ReportCheckpointCallback()]
        )
        with tempfile.TemporaryDirectory() as temp_checkpoint_dir:
            multi_worker_model.save(os.path.join(temp_checkpoint_dir, "model.keras"))
            checkpoint_dict = os.path.join(temp_checkpoint_dir, "checkpoint.json")
            with open(checkpoint_dict, "w") as f:
                json.dump({"epoch": epoch}, f)
            checkpoint = Checkpoint.from_directory(temp_checkpoint_dir)

            train.report({"loss": history.history["loss"][0]}, checkpoint=checkpoint)

        results.append(history.history)

    return results


# For GPU Training, set `use_gpu` to True.
# trainer = Trainer(backend="tensorflow", num_workers=3, use_gpu=True)
trainer = TensorflowTrainer(
    train_loop_per_worker=train_func_distributed,
    train_loop_config={"num_epochs": 10},
    scaling_config=ScalingConfig(num_workers=1, use_gpu=False),
    # run_config=train.RunConfig(storage_path="s3://lead-demo-2024/ray_persistent_storage/", name="autonomous_car"),
    run_config=train.RunConfig(storage_path="s3://demo-lead-bucket/artifacts/", name="autonomous_car"),
)
results = trainer.fit()
print(results)
