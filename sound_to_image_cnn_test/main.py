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

NUMBER_OF_IMAGES_PER_CLASS = 20


def main():
    # species_to_count_dict = {}
    # birdsong_path = Path("birdsong")
    # for train_wav_path in ["D:/Users/Owen/Final_Year_Project/birdsong/Common_Wood_Pigeon/Common_Wood_Pigeon_0.wav"]:  # birdsong_path.glob('**/*.wav'):
    #     audio, sr = librosa.load(train_wav_path, librosa.get_samplerate(train_wav_path))
    #     # with open('audio.txt', 'w') as f:
    #     #     for item in audio:
    #     #         f.write(f'{item}, ')
    #     spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)
    #     db = librosa.power_to_db(spectrogram, ref=np.max)
    #     librosa.display.specshow(db, fmax=10000, y_axis='mel', x_axis='time')
    #     plt.savefig('test.png')
    #
    #     # species = str(train_wav_path).split('//')[1]
    #     # if species in species_to_count_dict and species_to_count_dict[species] > NUMBER_OF_IMAGES_PER_CLASS:
    #     #     continue
    #     # print(f'making images for {train_wav_path.name}')
    #     test_stream = librosa.stream(train_wav_path, block_length=128, frame_length=2048, hop_length=1024,
    #                                  fill_value=0.0)
        # block_list = [block for block in test_stream][:-1]
        # for index, test_block in enumerate(block_list):
        #     if species not in species_to_count_dict:
        #         species_to_count_dict[species] = 0
        #     species_to_count_dict[species] += 1
        #     spectrogram = librosa.feature.melspectrogram(y=test_block, sr=librosa.get_samplerate(train_wav_path))
        #     librosa.display.specshow(librosa.power_to_db(spectrogram, ref=np.max), fmax=10000, y_axis='mel',
        #                              x_axis='time')
        #     plt.savefig(f'{train_wav_path.parent}/{train_wav_path.name[:-4]}_window_{index}.png')
        #
        #     if species_to_count_dict[species] > NUMBER_OF_IMAGES_PER_CLASS:
        #         break

    # img = cv2.imread("birdsong/Common_Blackbird/Common_Blackbird_0_window_0.png")
    # height, width, channels = img.shape
    # print(height, width, channels)
    # img = cv2.imread("birdsong/Arctic_Warbler/Arctic_Warbler_0_window_0.png")
    # height, width, channels = img.shape
    # print(height, width, channels)

    ##
    birdsong_path = Path("birdsong")
    for image_path in birdsong_path.glob('**/*.png'):
        img = cv2.imread(str(image_path))
        resized = cv2.resize(img, (32, 32), interpolation=INTER_AREA)
        cv2.imwrite(str(image_path), resized)
    ##

    batch_size = 32
    img_height = 32
    img_width = 32
    data_dir = Path("birdsong")

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
    print(class_names)

    normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1. / 255)

    train_ds = train_ds.cache().prefetch(buffer_size=-1)
    val_ds = val_ds.cache().prefetch(buffer_size=-1)

    num_classes = len(class_names)

    model = tf.keras.Sequential([
        layers.experimental.preprocessing.Rescaling(1. / 255),
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes)
    ])

    model.compile(
        optimizer='adam',
        loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'])

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=20
    )


if __name__ == '__main__':
    main()
