import argparse
from pathlib import Path
from pydub import AudioSegment


def main(args: argparse.Namespace):
    p = Path(args.folder)
    for mp3_path in p.glob('**/*.mp3'):
        src_mp3_absolute = str(mp3_path.absolute())
        print(f'Converting {src_mp3_absolute}')
        dst_mp3_absolute = src_mp3_absolute[:-4] + ".wav"
        sound = AudioSegment.from_mp3(src_mp3_absolute)
        sound.export(dst_mp3_absolute, format="wav")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("convert all mp3 files in sub-folders to wav files")
    parser.add_argument('-f', '--folder', type=str,
                        help="path to folder to convert all sub-file mp3s to wav files")
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
