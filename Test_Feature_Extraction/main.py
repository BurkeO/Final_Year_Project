import time
from pathlib import Path

import librosa
from scipy.spatial.distance import cosine
from pandas import DataFrame
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from tensorflow import keras
from tensorflow.keras import layers, regularizers
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization
from tensorflow.keras.layers import Conv2D, MaxPooling2D, LeakyReLU
import numpy as np
from tensorflow import expand_dims


def make_mfcc_dataframe(order):
    mfcc_coefficients_list = []
    p = Path("birdsong")
    for train_wav_path in p.glob('**/*.wav'):
        species = str(train_wav_path).split('\\')[1]
        test_stream = librosa.stream(train_wav_path, block_length=128, frame_length=2048, hop_length=1024,
                                     fill_value=0.0)
        block_list = [block for block in test_stream][:-1]
        for test_block in block_list:
            # coefficients = librosa.feature.mfcc(y=test_block, sr=librosa.get_samplerate(train_wav_path)).flatten()
            coefficients = librosa.feature.mfcc(y=test_block, sr=librosa.get_samplerate(train_wav_path))
            # coefficients = librosa.lpc(test_block, order).flatten()
            list_to_append = list(coefficients)
            list_to_append.append(species)
            mfcc_coefficients_list.append(list_to_append)
    return DataFrame(mfcc_coefficients_list)


def get_data():
    x_input = []
    y_output = []
    p = Path("D:/Users/Owen/Final_Year_Project/birdsong")
    for train_wav_path in p.glob('**/*.wav'):
        species = str(train_wav_path).split('\\')[-2]
        test_stream = librosa.stream(train_wav_path, block_length=128, frame_length=2048, hop_length=1024,
                                     fill_value=0.0)
        block_list = [block for block in test_stream][:-1]
        for test_block in block_list:
            # coefficients = librosa.feature.mfcc(y=test_block, sr=librosa.get_samplerate(train_wav_path))
            coefficients = librosa.lpc(y=test_block, order=3).flatten()
            x_input.append(coefficients)
            y_output.append(species)

    label_list = list(set(y_output))
    for index, label in enumerate(y_output):
        y_output[index] = label_list.index(label)
    return len(label_list), np.array(x_input), np.array(y_output)


def main():
    # for order in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]:
    #     mfcc_dataframe = make_mfcc_dataframe(order)
    #     x_input = mfcc_dataframe.iloc[:, :len(mfcc_dataframe.columns) - 1]
    #     y_output = mfcc_dataframe.iloc[:, len(mfcc_dataframe.columns) - 1]
    #
    #     x_train, x_test, y_train, y_test = train_test_split(x_input, y_output, test_size=0.2, random_state=1)
    #
    #     logistic_pipeline = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    #     logistic_pipeline.fit(x_train, y_train)
    #
    #     y_pred = logistic_pipeline.predict(x_test)
    #
    #     print(f"Order {order} accuracy = {accuracy_score(y_test, y_pred) * 100}%")

    # mfcc_dataframe = make_mfcc_dataframe(3)
    # x_input = mfcc_dataframe.iloc[:, :len(mfcc_dataframe.columns) - 1]
    # y_output = mfcc_dataframe.iloc[:, len(mfcc_dataframe.columns) - 1]
    #
    # x_train, x_test, y_train, y_test = train_test_split(x_input, y_output, test_size=0.2, random_state=1)
    #
    # logistic_pipeline = make_pipeline(StandardScaler(), LogisticRegression(max_iter=10000))
    # logistic_pipeline.fit(x_train, y_train)
    #
    # y_pred = logistic_pipeline.predict(x_test)
    #
    # print(f"model accuracy = {accuracy_score(y_test, y_pred) * 100}%")
    #
    # baseline = DummyClassifier(strategy="stratified")
    # baseline.fit(x_train, y_train)
    # print(f"baseline accuracy = {accuracy_score(y_test, baseline.predict(x_test)) * 100}%")
    # temp = make_mfcc_dataframe(3)
    input_shape = (20, 259)
    num_classes, x_input, y_output = get_data()

    x_train, x_test, y_train, y_test = train_test_split(x_input, y_output, test_size=0.2, random_state=42)

    # pipeline = make_pipeline(StandardScaler(), LogisticRegression())
    # pipeline.fit(x_train, y_train)
    # y_pred = pipeline.predict(x_test)
    # print(f'Logistic Accuracy = {accuracy_score(y_test,y_pred) * 100}%')

    num_correct = 0
    total_num = len(x_test)
    for test_array, test_output in zip(x_test, y_test):
        distances = []
        labels = []
        for train_array, train_output in zip(x_train, y_train):
            dist = cosine(test_array, train_array)
            distances.append(dist)
            labels.append(train_output)
        closest_index = distances.index(max(distances))
        closest_label = labels[closest_index]
        if closest_label == test_output:
            num_correct += 1

    print(f'Cosine accuracy = {(num_correct/total_num)*100}%')


    # x_train = expand_dims(x_train, axis=-1)
    # x_test = expand_dims(x_test, axis=-1)
    #
    # y_train = y_train.reshape(y_train.shape[0], 1)
    # y_test = y_test.reshape(y_test.shape[0], 1)
    #
    # y_train = keras.utils.to_categorical(y_train, num_classes)
    # y_test = keras.utils.to_categorical(y_test, num_classes)
    #
    # l1_penalty = 0.0001
    # time_to_train = None
    # use_saved_model = False
    # if use_saved_model:
    #     model = keras.models.load_model("cifar.model")
    # else:
    #     model = keras.Sequential()
    #     model.add(Conv2D(16, (3, 7), padding='same', input_shape=x_train.shape[1:], activation='relu'))
    #     model.add(MaxPooling2D(pool_size=(2, 2)))
    #     model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    #     model.add(MaxPooling2D(pool_size=(2, 2)))
    #     model.add(Dropout(0.5))
    #     model.add(Flatten())
    #     model.add(Dense(num_classes, activation='softmax', kernel_regularizer=regularizers.l1(l1_penalty)))
    #     model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=["accuracy"])
    #     model.summary()
    #
    #     batch_size = 128
    #     epochs = 20
    #     start = time.perf_counter()
    #     history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)
    #     end = time.perf_counter()
    #     time_to_train = end - start
    #     model.save("cifar.model")
    #
    #     fig, axs = plt.subplots(2)
    #     fig.tight_layout(pad=3.0)
    #
    #     axs[0].plot(history.history['accuracy'])
    #     axs[0].plot(history.history['val_accuracy'])
    #     axs[0].set_title(f'model accuracy - l1 {l1_penalty} ')
    #     axs[0].set_ylabel('accuracy')
    #     axs[0].set_xlabel('epoch')
    #     axs[0].legend(['train', 'val'], loc='upper left')
    #     axs[1].plot(history.history['loss'])
    #     axs[1].plot(history.history['val_loss'])
    #     axs[1].set_title(f'model loss - l1 {l1_penalty}')
    #     axs[1].set_ylabel('loss')
    #     axs[1].set_xlabel('epoch')
    #     axs[1].legend(['train', 'val'], loc='upper left')
    #     plt.show()
    #
    # predictions = model.predict(x_train)
    # y_pred = np.argmax(predictions, axis=1)
    # y_train1 = np.argmax(y_train, axis=1)
    # print(classification_report(y_train1, y_pred))
    # print(confusion_matrix(y_train1, y_pred))
    #
    # predictions = model.predict(x_test)
    # y_pred = np.argmax(predictions, axis=1)
    # y_test1 = np.argmax(y_test, axis=1)
    # print(classification_report(y_test1, y_pred))
    # print(confusion_matrix(y_test1, y_pred))
    #
    # # ---------------time -----------
    # print(f"Time to train model = {time_to_train} seconds")
    #
    # # ------------ baseline ----------------------
    # classes, counts = np.unique(y_train, axis=0, return_counts=True)  # get classes and their occurrences
    # baseline_y_pred_list = [np.argmax(classes[counts.argmax()])] * len(y_test)  # repeat for same size as test data
    # print(
    #     f"Baseline accuracy : {accuracy_score(np.argmax(y_test, axis=1), baseline_y_pred_list)}")  # get accuracy score
    #

if __name__ == '__main__':
    main()
