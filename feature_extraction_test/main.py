from pathlib import Path

import librosa
from pandas import DataFrame
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


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
            coefficients = librosa.lpc(test_block, order).flatten()
            list_to_append = list(coefficients)
            list_to_append.append(species)
            mfcc_coefficients_list.append(list_to_append)
    return DataFrame(mfcc_coefficients_list)


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

    mfcc_dataframe = make_mfcc_dataframe(3)
    x_input = mfcc_dataframe.iloc[:, :len(mfcc_dataframe.columns) - 1]
    y_output = mfcc_dataframe.iloc[:, len(mfcc_dataframe.columns) - 1]

    x_train, x_test, y_train, y_test = train_test_split(x_input, y_output, test_size=0.2, random_state=1)

    logistic_pipeline = make_pipeline(StandardScaler(), LogisticRegression(max_iter=10000))
    logistic_pipeline.fit(x_train, y_train)

    y_pred = logistic_pipeline.predict(x_test)

    print(f"model accuracy = {accuracy_score(y_test, y_pred) * 100}%")

    baseline = DummyClassifier(strategy="stratified")
    baseline.fit(x_train, y_train)
    print(f"baseline accuracy = {accuracy_score(y_test, baseline.predict(x_test)) * 100}%")


if __name__ == '__main__':
    main()
