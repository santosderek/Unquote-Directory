# Written by: Derek Santos

# Python Modules
from urllib.parse import unquote
from os import listdir, rename
from os.path import isfile, join
from argparse import ArgumentParser
import logging

# Equipped a logger for debugging
logging.basicConfig(filename='logger.log', level=logging.DEBUG)
LOGGER = logging.getLogger()


def parse_arguments():
    """ Parses arguments given at startup """
    parser = ArgumentParser(description='Decodes filenames with url encoding.')

    parser.add_argument('-f', '--folder', metavar='folder',
                        type=str, nargs='?', help='Change target folder')

    return parser.parse_args()


def change_name(name: str):
    """ Unqote and strip invalid characters from a filename and returns it """
    unquoted_name = unquote(name)
    stripped_name = unquoted_name.strip('/\\:*?"<>|')
    return stripped_name


def get_list_of_file_names(directory_path):
    """ Gets a list of files from a path """
    return [filename for filename in listdir(directory_path)
            if isfile(join(directory_path, filename))]


def main(directory_path='.'):
    """ Construct a list of filenames to parse, and then rename them """

    # Create two lists: One to contain original names,
    # and a second to contain changed names
    original_list = get_list_of_file_names(directory_path)
    stripped_list = [change_name(str(name)) for name in original_list]

    # Loop through both lists and change the names accordingly
    for original_name, changed_name in zip(original_list, stripped_list):
        try:
            rename(join(directory_path, original_name),
                   join(directory_path, changed_name))

            print('-------------------------------------------------------')
            print('Original Name:', original_name)
            print('Changed Name:', changed_name)
            print('-------------------------------------------------------')
        except Exception:
            LOGGER.info('Could not change %s to %s' %
                        (original_name, changed_name))


if __name__ == '__main__':
    arguments = parse_arguments()

    # If no argument passed then use working directory
    if arguments.folder is None:
        directory_path = '.'
    else:
        directory_path = str(arguments.folder)

    main(directory_path)
