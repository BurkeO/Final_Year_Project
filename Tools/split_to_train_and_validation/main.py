import argparse
import os
from pathlib import Path
import random
from shutil import copy


def main(args: argparse.Namespace):
    data_dir = args.recordings
    train_dir = args.training
    validation_dir = args.validation
    species_to_list = {}
    for folder in os.listdir(data_dir):
        species = folder
        full_path = os.path.join(data_dir, folder)
        for file in Path(full_path).glob('**/*.wav'):
            if species not in species_to_list:
                species_to_list[species] = []
            species_to_list[species].append(file)
        random.Random(4).shuffle(species_to_list[species])
        test_percentage = 0.2
        wav_validation_list = species_to_list[species][:int(len(species_to_list[species]) * test_percentage)]
        wav_train_list = species_to_list[species][int(len(species_to_list[species]) * test_percentage):]
        for file in wav_validation_list:
            dst_path = Path(f"{validation_dir}/{species}/{file.name}")
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            copy(str(file), str(dst_path))
            print(f"Copied validation file {file.name}")
        for file in wav_train_list:
            dst_path = Path(f"{train_dir}/{species}/{file.name}")
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            copy(str(file), str(dst_path))
            print(f"Copied training file {file.name}")


def parse_args():
    parser = argparse.ArgumentParser("Split a directory of recordings into a training anc validation set (80/20)")
    parser.add_argument('-r', '--recordings', type=str, help="path to folder that contains recordings",
                        required=True)
    parser.add_argument('-t', '--training', type=str, help="path to folder to write training files",
                        required=True)
    parser.add_argument('-v', '--validation', type=str, help="path to folder to write validation files",
                        required=True)
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
