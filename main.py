import argparse
from requests import get
import time

API_URL = "https://www.xeno-canto.org/api/2/recordings"


def main(args: argparse.Namespace) -> None:
    with open(args.countries_file) as countries_file:
        countries_list = countries_file.read().splitlines()
        for country in countries_list:
            print(f'Current country = {country}')
            if " " in country:
                country = f'\"{country}\"'
            params = {'query': f'cnt:{country}'}
            response = get(url=API_URL, params=params)
            if response.status_code != 200:
                print(f'Error code for country = {country}')
            elif not response.json()['recordings']:
                print(f'Empty recordings for country = {country}')
            json_response_data = response.json()
            print(json_response_data)
            for recording in json_response_data['recordings']:
                print(f'recording = {recording}')
            time.sleep(1.5)
            break


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("Pull audio files from Xeno Canto API using countries list file")
    parser.add_argument('-c', '--countries_file', type=str,
                        help="""A file path to a txt file containing a list of countries separated by line breaks""")
    parser.add_argument('-o', '--output_dir', type=str,
                        help="""A path to the output directory to store the pulled audio file""")
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
