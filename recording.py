from requests import get
from pathlib import Path
from json import dump
from typing import Callable


def remove_invalid_path_char(member_function: Callable) -> Callable[[str], str]:
    def wrapper(recording) -> str:
        value = member_function(recording)
        invalid = '<>:"/\\|?*'
        for char in invalid:
            value = value.replace(char, '')
        return value

    return wrapper


class Recording:

    def __init__(self, recording_data_dict: {}, output_dir_path: str) -> None:
        self.data_dict = recording_data_dict
        self._output_dir_path = output_dir_path
        self.recording_file = self._download_file()

    @property
    @remove_invalid_path_char
    def english_species(self) -> str:
        return self.data_dict['en']

    @property
    @remove_invalid_path_char
    def filename(self) -> str:
        return self.data_dict['file-name']

    @property
    @remove_invalid_path_char
    def country(self) -> str:
        return self.data_dict['cnt']

    @property
    def _output_path(self) -> str:
        return (f'{self._output_dir_path}/{self.country.replace(" ", "_")}/'
                f'{self.english_species.replace(" ", "_")}/{self.data_dict["id"]}')

    def _download_file(self) -> bytes:
        file_content = get(url=f"http:{self.data_dict['file']}", allow_redirects=True)
        return file_content.content

    def write(self) -> None:
        if not Path.exists(Path(self._output_path)):
            Path.mkdir(Path(self._output_path), parents=True)
        with open(f'{self._output_path}/{self.filename.replace(" ", "_")}', 'wb') as recording_file:
            recording_file.write(self.recording_file)
        with open(f'{self._output_path}/metadata.json', 'w') as metadata_file:
            (dump(self.data_dict, metadata_file, indent=4))
