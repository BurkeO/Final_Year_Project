import argparse
from pathlib import Path
from shutil import copyfile
from sys import maxsize


def main(args: argparse.Namespace):
    input_folder = Path(args.input)
    species_to_files = {}
    for file_path in input_folder.glob(f'**/*' + args.extension):
        for species in args.species:
            if species not in species_to_files:
                species_to_files[species] = []
            species_from_path = str(file_path).split('\\')[-3]
            if species.lower() == species_from_path.lower() and len(species_to_files[species]) < args.number:
                species_to_files[species].append(str(file_path))
                print(f'Gathered {species} {len(species_to_files[species])}')

    print(f'\nCopying.........')
    for species, path_list in species_to_files.items():
        dst_path = Path(f'{args.folder}/{species}')
        dst_path.mkdir(parents=True, exist_ok=True)
        count = 0
        for path in path_list:
            copyfile(path, f'{dst_path}/{species}_{count}{args.extension}')
            print(f'Copied {species} {count+1}')
            count += 1


def parse_args():
    parser = argparse.ArgumentParser("gather the number of files specified (or as close as possible) for each species "
                                     "in given list and save in specified folder")
    parser.add_argument('-n', '--number', type=int, help="number of each file to gather", default=maxsize)
    parser.add_argument('-s', '--species', nargs='+', type=str, help="the list of species to gather")
    parser.add_argument('-i', '--input', type=str, help="the input folder to gather files from")
    parser.add_argument('-f', '--folder', type=str, help="the folder to save the files in")
    parser.add_argument('-e', '--extension', type=str, help="the extension of the audio files", default=".mp3")
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
