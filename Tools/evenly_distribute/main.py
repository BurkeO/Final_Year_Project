import argparse
from pathlib import Path
from shutil import copy


def main(args: argparse.Namespace):
    recordings_dir = Path(args.recordings)
    even_dir = Path(args.even)

    species_to_count = {}
    for file in recordings_dir.glob('**/*.wav'):
        species = str(file.parents[0]).split('\\')[-1]
        species_to_count[species] = 1 if species not in species_to_count else species_to_count[species] + 1

    species_to_count = {k: v for k, v in sorted(species_to_count.items(), key=lambda item: item[1], reverse=True)}

    for species, count in species_to_count.items():
        print(f"{species} : {count}")

    species_list = species_to_count.keys()

    number_to_copy = min([species_to_count[species] for species in species_list])
    print(number_to_copy)

    species_to_files = {}
    for species in species_list:
        species_to_files[species] = []

    for file in recordings_dir.glob('**/*.wav'):
        species = str(file.parents[0]).split('\\')[-1]
        if species in species_list and len(species_to_files[species]) < number_to_copy:
            species_to_files[species].append(file)

    count = 1
    for species, file_list in species_to_files.items():
        for file in file_list:
            copy_species_path = Path(f"{even_dir}/{species}")
            copy_species_path.mkdir(exist_ok=True, parents=True)
            print(f"copying {file.stem} ({count}/{number_to_copy * len(species_to_files)})")
            output_path = Path(f"{copy_species_path}/{file.name}")
            copy(file, output_path)
            count += 1


def parse_args():
    parser = argparse.ArgumentParser("Evenly distribute a directory of birdsong recordings")
    parser.add_argument('-r', '--recordings', type=str, help="path to folder that contains recordings", required=True)
    parser.add_argument('-e', '--even', type=str, help="path to folder to write evenly distributed files",
                        required=True)
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
