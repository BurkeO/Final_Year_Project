import argparse
from pathlib import Path
from pydub import AudioSegment


def main(args: argparse.Namespace):
    output_folder_path = Path(args.output)
    if output_folder_path.exists() is False:
        output_folder_path.mkdir(parents=True, exist_ok=True)
    mp3_folder_path = Path(args.folder)
    for mp3_path in mp3_folder_path.glob('**/*.mp3'):
        src_mp3_absolute = str(mp3_path.absolute())
        print(f'Converting {src_mp3_absolute}')
        species = str(mp3_path).split('\\')[-2]
        dst_wav_absolute = str(output_folder_path) + "\\" + species + "\\" + mp3_path.stem + ".wav"
        Path(dst_wav_absolute).mkdir(parents=True, exist_ok=True)
        sound = AudioSegment.from_mp3(src_mp3_absolute)
        sound.export(dst_wav_absolute, format="wav")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("convert all mp3 files in sub-folders to wav files")
    parser.add_argument('-f', '--folder', type=str,
                        help="path to folder to convert all sub-file mp3s to wav files")
    parser.add_argument('-o', '--output', type=str,
                        help="output folder to save wav files")
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
