from pathlib import Path


def main():
    species_set = set()
    for folder in Path("../../recordings").iterdir():
        if folder.is_dir():
            for sub_folder in folder.iterdir():
                species_set.add(sub_folder.name)
    for species in species_set:
        print(species)


if __name__ == '__main__':
    main()
