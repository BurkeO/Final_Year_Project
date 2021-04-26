import os
from pathlib import Path
import random
from shutil import copy


def main():
    data_dir = "D:/Users/Owen/Final_Year_Project/Top_Seven_Full_Recordings_Even"
    train_dir = "D:/Users/Owen/Final_Year_Project/Top_Seven_Full_Recordings_Even_Train"
    validation_dir = "D:/Users/Owen/Final_Year_Project/Top_Seven_Full_Recordings_Even_Validation"
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


if __name__ == '__main__':
    main()
