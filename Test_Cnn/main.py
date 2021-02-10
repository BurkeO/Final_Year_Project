import cv2
import librosa.display
import tensorflow as tf
from cv2 import INTER_AREA
from pathlib import Path
import librosa
from tensorflow.keras import layers
from matplotlib import pyplot as plt
import numpy as np
from tensorflow.keras.applications import vgg16


def main():
    birdsong_path = Path("D:/Users/Owen/Final_Year_Project/Dev_Recordings_Split_Wavs")
    for train_wav_path in birdsong_path.glob('**/*.wav'):
        audio, sr = librosa.load(train_wav_path, librosa.get_samplerate(train_wav_path))
        spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)
        db = librosa.power_to_db(spectrogram, ref=np.max)
        librosa.display.specshow(db, fmax=10000, y_axis='mel', x_axis='time')
        species = str(train_wav_path).split('\\')[-2]
        print(f'Making melspec for {train_wav_path.name}')
        output_path = Path(f'../Dev_Images_Melspec/{species}/{train_wav_path.stem}.png')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(str(output_path))

    images_dir_path = Path("D:/Users/Owen/Final_Year_Project/Dev_Images_Melspec")
    for image_path in images_dir_path.glob('**/*.png'):
        img = cv2.imread(str(image_path))
        resized = cv2.resize(img, (32, 32), interpolation=INTER_AREA)
        species = str(image_path).split('\\')[-2]
        Path(f"output/{species}").mkdir(parents=True, exist_ok=True)
        output_file = f"output/{species}/{image_path.name}"
        print(f'Saving to {output_file}')
        cv2.imwrite(output_file, resized)

    batch_size = 32
    img_height = 32
    img_width = 32
    data_dir = "output"

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(img_height, img_width),
        batch_size=batch_size)

    class_names = train_ds.class_names
    num_classes = len(class_names)
    labels = '\n'.join(sorted(class_names))

    with open('labels.txt', 'w') as f:
        f.write(labels)

    train_ds = train_ds.cache().prefetch(buffer_size=-1)
    val_ds = val_ds.cache().prefetch(buffer_size=-1)

    model = tf.keras.Sequential([
        layers.experimental.preprocessing.Rescaling(1. / 255),
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, activation='relu'),
        # layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes)
        # layers.Dense(num_classes, activation="softmax")
    ])

    model.compile(
        optimizer='adam',
        loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'])

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=50
    )

    saved_model_dir = 'save/fine_tuning'
    tf.saved_model.save(model, saved_model_dir)

    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    tflite_model = converter.convert()

    with open('model.tflite', 'wb') as f:
        f.write(tflite_model)


if __name__ == '__main__':
    main()
