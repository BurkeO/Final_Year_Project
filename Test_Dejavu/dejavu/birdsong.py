from pathlib import Path

from Test_Dejavu.dejavu.dejavu import Dejavu
from Test_Dejavu.dejavu.dejavu.logic.recognizer.file_recognizer import FileRecognizer

if __name__ == '__main__':
    config = {
        "database": {
            "host": "127.0.0.1",
            "user": "root",
            "password": "your_chosen_mysql_password",
            "database": "birdsong"
        },
        "database_type": "mysql"
    }
    djv = Dejavu(config)

    for path in Path("D:\\Users\\Owen\\Final_Year_Project\\Top_Seven_Full_Recordings_Even_Train").iterdir():
        if path.is_dir():
            djv.fingerprint_directory(str(path), [".wav"])
    number_total = 0
    number_correct = 0

    print(djv.db.get_num_fingerprints())

    for path in Path("D:\\Users\\Owen\\Final_Year_Project\\Top_Seven_Full_Recordings_Even_Validation").iterdir():
        if path.is_dir():
            species_name = str(path).split("\\")[-1]
            for file in path.iterdir():
                number_total += 1
                results = djv.recognize(FileRecognizer, str(file))
                results_list = results['results']
                results_list.sort(key=lambda res: res['fingerprinted_confidence'], reverse=True)
                if len(results_list) > 0 and species_name in results_list[0]['song_name'].decode('ascii'):
                    print(f"Matched {species_name}")
                    number_correct += 1

    print(f"Accuracy = {(number_correct / number_total) * 100}%")
