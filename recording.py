class Recording:

    def __init__(self, recording_metadata_dict: {}, english_species_name: str, output_dir_path: str) -> None:
        self.metadata = recording_metadata_dict
        self.english_species = english_species_name
        self._output_dir_path = output_dir_path
        self.recording_file = self._download_file()

    @property
    def output_path(self) -> str:
        return f'{self._output_dir_path}/{self.english_species}'

    def _download_file(self):
        pass
