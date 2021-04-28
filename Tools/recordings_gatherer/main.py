import argparse
import logging
import time
from pathlib import Path

from requests import get

from Tools.recordings_gatherer.recording import Recording

LOGGER = logging.getLogger("recording logger")

API_URL = "https://www.xeno-canto.org/api/2/recordings"


def main(args: argparse.Namespace) -> None:
    logging.basicConfig(filename=args.log_path, level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%y-%m-%d %H:%M:%S')
    total_number_of_recordings = 0
    LOGGER.info("Recording scraping started")
    with open(args.countries_file) as countries_file:
        countries_list = countries_file.read().splitlines()
        print("Collecting recordings")
        for country in countries_list:
            temp_country = country
            invalid = '<>:"/\\|?*'
            for char in invalid:
                temp_country = temp_country.replace(char, '')
            temp_country = temp_country.replace(" ", "_")
            if Path(f"{args.output_dir}/{temp_country}").exists():  # assume if folder exists, is fully populated
                # TODO maybe change this assumption
                continue
            LOGGER.info(f"Currently on {country}")
            try:
                if " " in country:
                    country = f'\"{country}\"'
                params = {'query': f'cnt:{country}'}
                response = get(url=API_URL, params=params, timeout=3)
                time.sleep(3)
                if response.status_code != 200:
                    LOGGER.error(f'Error code for country = {country}')
                    continue
                elif not response.json()['recordings']:
                    LOGGER.warning(f'Empty recordings for country = {country}')
                    continue
                json_response_data = response.json()
                for page_number in range(1, json_response_data['numPages'] + 1):
                    try:
                        params = {'query': f'cnt:{country}', 'page': {page_number}}
                        LOGGER.info(f'Requesting page {page_number} for {country}')
                        response = get(url=API_URL, params=params, timeout=3)
                        time.sleep(3)
                        if response.status_code != 200:
                            LOGGER.error(f'Error code for country = {country}, page {page_number}')
                            continue
                        elif not response.json()['recordings']:
                            LOGGER.warning(f'Empty recordings for country = {country}, page {page_number}')
                            continue
                        json_response_data = response.json()
                        for recording in json_response_data['recordings']:
                            try:
                                LOGGER.info(f'Downloading mp3 for {recording["en"]} from {country}')
                                recording_object = Recording(recording, args.output_dir)
                                total_number_of_recordings += 1
                                recording_object.write()
                                LOGGER.info(f"Writing {recording_object.english_species} from {country}")
                            except Exception as exception:
                                LOGGER.error(f'Error : {exception}')
                    except Exception as exception:
                        LOGGER.error(f'Error : {exception}')

            except Exception as exception:
                LOGGER.error(f'Error : {exception}')
        for missing_country in [country for country in countries_list if
                                Path(f"{args.output_dir}/{country}").exists() is False]:
            LOGGER.warning(f"{missing_country} is missing with no recordings")
    LOGGER.info(f'Total number of recordings saved = {total_number_of_recordings}')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("Pull audio files from Xeno Canto API using countries list file")
    parser.add_argument('-c', '--countries_file', type=str, required=True,
                        help="A file path to a txt file containing a list of countries separated by line breaks")
    parser.add_argument('-o', '--output_dir', type=str, required=True,
                        help="A path to the output directory to store the pulled audio file")
    parser.add_argument('-l', '--log_path', type=str, help="A path to store a log file for the script", required=True)
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
