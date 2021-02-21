from pathlib import Path
import os


def main():
    src_dir = Path("D:/Users/Owen/Final_Year_Project/Dev_Test")
    dst_dir = Path("D:/Users/Owen/Final_Year_Project/Dev_Test_10_min_split")
    for wav_file in src_dir.glob('**/*.wav'):
        species = str(wav_file.parents[0]).split('\\')[-1]
        dst_folder = Path(f"{str(dst_dir)}/{species}")
        dst_folder.mkdir(parents=True, exist_ok=True)
        os.system(f"ffmpeg -i {wav_file.absolute()} -f segment -segment_time 600 -c copy "
                  f"{str(dst_folder)}/{wav_file.stem}%03d.wav")


if __name__ == '__main__':
    main()