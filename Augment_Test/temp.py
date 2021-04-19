from pathlib import Path
import os
import audiomentations
# AddGaussianNoise, Shift, AddBackgroundNoise, AddBackgroundNoise, AddShortNoises, ClippingDistortion, Gain,
# AddGaussianSNR, Mp3Compression, LoudnessNormalization, Normalize
from audiomentations import (Compose, AddGaussianNoise, TimeStretch, PitchShift, Shift, AddBackgroundNoise,
                             AddShortNoises, ClippingDistortion, Gain, Mp3Compression)
import numpy as np
import librosa
import soundfile as sf
import random


MIN_AUDIO_DURATION_SECONDS = 15
MAX_NUMBER_OF_SPLITS_TO_MAKE = 7
MIN_NUMBER_OF_SPLITS_TO_MAKE = 3


def seconds_to_min_sec(seconds):
    mins = int(seconds / 60)
    seconds -= 60 * mins
    if seconds < 10:
        seconds = f"0{seconds}"
    if mins < 10:
        mins = f"0{mins}"
    return f"{mins}:{seconds}"


def make_audio_files(file_path_str):
    duration = librosa.get_duration(filename=file_path_str)
    files = [file_path_str]
    for split_number in range(random.randrange(MIN_NUMBER_OF_SPLITS_TO_MAKE, MAX_NUMBER_OF_SPLITS_TO_MAKE)):
        start = random.uniform(0, duration - MIN_AUDIO_DURATION_SECONDS)
        end = random.uniform(start + MIN_AUDIO_DURATION_SECONDS, duration)
        start_mins = seconds_to_min_sec(start)
        end_mins = seconds_to_min_sec(end)
        file_path = Path(file_path_str)
        output_file_str = f"{str(file_path.parents[0])}\\{file_path.stem}_{split_number}{file_path.suffix}"
        command = f"ffmpeg -i \"{file_path_str}\" -ss {start_mins} -to {end_mins} -acodec copy -y \"{output_file_str}\" -y"
        os.system(command)
        if Path(output_file_str).exists() is False:
            raise FileNotFoundError
        files.append(output_file_str)
    return files


def main():
    augment = Compose([
        AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=0.5),
        TimeStretch(min_rate=0.8, max_rate=1.25, p=0.5),
        PitchShift(min_semitones=-4, max_semitones=4, p=0.5),
        Shift(min_fraction=-0.5, max_fraction=0.5, p=0.5),
    ])

    # background_samples_and_rates_list = [librosa.load(str(file)) for file in Path("../Ambient-Sounds").iterdir()]

    # files_to_augment = make_audio_files("Atlantic_Puffin_0.wav")
    # print(files_to_augment)

    operations = [AddGaussianNoise(max_amplitude=0.03, p=1), AddGaussianNoise(min_amplitude=0.002),
                  Shift(min_fraction=-1, max_fraction=1, p=0.75), AddBackgroundNoise("..\\Ambient-Sounds", p=0.75),
                  AddShortNoises("..\\Ambient-Sounds"),
                  ClippingDistortion(min_percentile_threshold=20, max_percentile_threshold=30),
                  Gain(min_gain_in_db=-20, max_gain_in_db=20, p=0.625), Mp3Compression()]

    audio_file_path_str = 'Northern_Raven_4.wav'

    signal, sample_rate = librosa.load(audio_file_path_str)
    duration = librosa.get_duration(signal, sample_rate)

    # augment = Compose([AddBackgroundNoise("..\\Ambient-Sounds", p=0.75)])
    process = Mp3Compression(p=1, min_bitrate=16, max_bitrate=16)
    augment = Compose([process])

    # print(AddBackgroundNoise.__name__)

    # Augment/transform/perturb the audio data
    augmented_samples = augment(samples=signal, sample_rate=sample_rate)

    sf.write(f'{type(process).__name__}-{Path(audio_file_path_str).stem}.wav', augmented_samples, sample_rate)


if __name__ == '__main__':
    main()
