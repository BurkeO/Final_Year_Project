import argparse


def main(args: argparse.Namespace):
    print(args.number)
    print(args.species)
    print(args.folder)
    print(args.input)
    print(args.extension)


def parse_args():
    parser = argparse.ArgumentParser("gather the number of files specified (or as close as possible) for each species "
                                     "in given list and save in specified folder")
    parser.add_argument('-n', '--number', type=int, help="number of each file to gather")
    parser.add_argument('-s', '--species', nargs='+', type=str, help="the list of species to gather")
    parser.add_argument('-i', '--input', type=str, help="the input folder to gather files from")
    parser.add_argument('-f', '--folder', type=str, help="the folder to save the files in")
    parser.add_argument('-e', '--extension', type=str, help="the extension of the audio files", default=".mp3")
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
