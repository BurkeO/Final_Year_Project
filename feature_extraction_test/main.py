from pathlib import Path

import librosa
from pandas import DataFrame, Series


def make_mfcc_dataframe():
    mfcc_coefficients_list = []
    p = Path("birdsong")
    for train_wav_path in p.glob('**/*.wav'):
        species = str(train_wav_path).split('\\')[1]
        test_stream = librosa.stream(train_wav_path, block_length=256, frame_length=4096, hop_length=1024,
                                     fill_value=0.0)
        block_list = [block for block in test_stream][:-1]
        for test_block in block_list:
            mfcc_coefficients = librosa.feature.mfcc(y=test_block, sr=librosa.get_samplerate(train_wav_path)).flatten()
            list_to_append = list(mfcc_coefficients)
            list_to_append.append(species)
            mfcc_coefficients_list.append(list_to_append)
    return DataFrame(mfcc_coefficients_list)


def main():
    mfcc_dataframe = make_mfcc_dataframe()
    print(mfcc_dataframe)


if __name__ == '__main__':
    main()
