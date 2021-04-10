from pathlib import Path


def get_number_of_recordings(folder_path: Path):
    count = 0
    for path in folder_path.iterdir():
        if path.is_dir():
            count += 1
    return count


def main():
    species_to_recordings_count_dir = {}
    for folder in Path("../../recordings").iterdir():
        if folder.is_dir():
            for sub_folder in folder.iterdir():
                recordings_count = get_number_of_recordings(sub_folder)
                species = sub_folder.name
                if species not in species_to_recordings_count_dir:
                    species_to_recordings_count_dir[species] = recordings_count
                else:
                    species_to_recordings_count_dir[species] += recordings_count

    sorted_tuples = sorted(species_to_recordings_count_dir.items(), key=lambda item: item[1], reverse=True)
    species_to_recordings_count_dir = {k: v for k, v in sorted_tuples}
    del species_to_recordings_count_dir['Identity_unknown']
    del species_to_recordings_count_dir['Soundscape']
    number_of_recordings_descending = sorted(species_to_recordings_count_dir.values(), reverse=True)
    total_number_of_recordings_for_species = sum(number_of_recordings_descending)
    print(f'Total number of recordings for species = {total_number_of_recordings_for_species}')
    species_number = 1
    for species, count in species_to_recordings_count_dir.items():
        print(f'{species_number}. {species} : {count} ({(sum(number_of_recordings_descending[:species_number]) / total_number_of_recordings_for_species) * 100}%)')
        species_number += 1


if __name__ == '__main__':
    main()
