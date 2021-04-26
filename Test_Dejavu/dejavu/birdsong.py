import os
import random
from pathlib import Path
from sys import maxsize

import librosa
import numpy

from Test_Dejavu.dejavu.dejavu import Dejavu
from Test_Dejavu.dejavu.dejavu.logic.recognizer.file_recognizer import FileRecognizer


class BirdCall(object):
    def __init__(self, file_name, species_name, hop_length=1024) -> None:
        self.species_name = species_name
        self._time_series, self._sampling_rate = librosa.load(file_name)
        self._chromo = librosa.feature.chroma_cqt(y=self._time_series, sr=self._sampling_rate, hop_length=hop_length)
        self.data_history = librosa.feature.stack_memory(self._chromo, n_steps=10, delay=3)


def get_true_sum(bird_call_one: BirdCall, bird_call_two: BirdCall):
    x_sim = librosa.segment.cross_similarity(bird_call_one.data_history, bird_call_two.data_history, metric='cosine',
                                             mode='affinity')
    return numpy.sum(x_sim)


def main():
    train_calls_list = []
    for path in Path("birdsong").iterdir():
        if path.is_dir():
            species_name = str(path).split("\\")[1]
            for file in path.iterdir():
                print(f'Bird call for {species_name}')
                train_calls_list.append(BirdCall(str(file), species_name))

    print(f'-------- Testing --------')
    number_total = 0
    number_correct = 0
    for path in Path("birdsong_test").iterdir():
        if path.is_dir():
            species_name = str(path).split("\\")[1]
            for file in path.iterdir():
                test_call = BirdCall(str(file), species_name)
                number_total += 1
                current_count = 0
                species_guess = None
                for train_call in train_calls_list:
                    guess_sum = get_true_sum(train_call, test_call)
                    if guess_sum > current_count:
                        current_count = guess_sum
                        species_guess = train_call.species_name
                if species_guess == species_name:
                    number_correct += 1
                print(f'top guess for {species_name} = {species_guess}')

    print(f"Accuracy = {(number_correct / number_total) * 100}%")

    # longer_array, array_two = (y_train, y_test) if len(y_train) > len(y_test) else (y_test, y_train)
    # sim = distance.cosine(longer_array[:len(array_two)], array_two)
    # print(sim)


if __name__ == '__main__':
    # main()
    # fn_wav_all = []
    # data_dir = Path("D:\\Users\\Owen\\Final_Year_Project\\Unique_Birds_Recordings_Even_Whole")
    # for species_folder in data_dir.iterdir():
    #     species = species_folder.stem
    #     parent_list = os.listdir(f'{data_dir}\\{species}')
    #     number_for_each = maxsize
    #     species_list = parent_list[:number_for_each]
    #     for i in range(len(species_list)):
    #         species_list[i] = f'{data_dir}\\{species}\\{species_list[i]}'
    #     fn_wav_all.extend(species_list)
    #
    # random.Random(4).shuffle(fn_wav_all)
    #
    # test_percentage = 0.2
    # wav_test_list = fn_wav_all[:int(len(fn_wav_all) * test_percentage)]
    # wav_train_list = fn_wav_all[int(len(fn_wav_all) * test_percentage):]

    # print("Test --------------")
    # print("\n".join(wav_test_list))
    # print("Train ------------")
    # print("\n".join(wav_train_list))
    # exit()


    config = {
        "database": {
            "host": "127.0.0.1",
            "user": "root",
            # TODO remove password
            "password": "database123",
            "database": "birdsong"
        },
        "database_type": "mysql"
    }
    djv = Dejavu(config)

    for path in Path("D:\\Users\\Owen\\Final_Year_Project\\Top_Seven_Full_Recordings_Even_Train").iterdir():
        if path.is_dir():
            djv.fingerprint_directory(str(path), [".wav"])
    number_total = 0
    number_correct = 0

    print(djv.db.get_num_fingerprints())

    for path in Path("D:\\Users\\Owen\\Final_Year_Project\\Top_Seven_Full_Recordings_Even_Validation").iterdir():
        if path.is_dir():
            species_name = str(path).split("\\")[-1]
            for file in path.iterdir():
                number_total += 1
                results = djv.recognize(FileRecognizer, str(file))
                results_list = results['results']
                results_list.sort(key=lambda res: res['fingerprinted_confidence'], reverse=True)
                # print(f"From file we recognized: {results_list}\n")
                if len(results_list) > 0 and species_name in results_list[0]['song_name'].decode('ascii'):
                    print(f"Matched {species_name}")
                    number_correct += 1

    print(f"Accuracy = {(number_correct / number_total) * 100}%")
