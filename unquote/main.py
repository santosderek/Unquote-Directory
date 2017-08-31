# Written by: Derek Santos

# Python Modules
from urllib.parse import unquote
from os import listdir, rename, walk, getcwd
from os.path import isfile, join
from argparse import ArgumentParser
import logging

# Equipped a logger for debugging
LOG_FORMAT = "[%(levelname)s] - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

LOGGER = logging.getLogger()


def parse_arguments():
    """ Parses arguments given at startup """
    parser = ArgumentParser(description='Decodes filenames with url encoding.')
    parser.add_argument('folder', metavar='folder', nargs='?',
                        type=str, help='Target folder')
    parser.add_argument('-r', '--recursion',
                        action='store_true', help='Enable recursion.')
    return parser.parse_args()


def get_list_of_file_names(directory_path):
    """ Gets a list of files from a path """
    return [filename for filename in listdir(directory_path)
            if isfile(join(directory_path, filename))]


def unquote_name(name: str):
    """ Unqote and strip invalid characters from a filename and returns it """
    unquoted_name = unquote(name)
    stripped_name = unquoted_name.strip('/\\:*?"<>|')
    return stripped_name


def unquote_files(directory_path: str):
    """ Unquote a list of files from a specified directory """

    # Create two lists: One to contain original names,
    # and a second to contain changed names
    original_list = get_list_of_file_names(directory_path)
    unquoted_list = [unquote_name(str(name)) for name in original_list]

    # Loop through both lists and change the names accordingly
    for original_name, changed_name in zip(original_list, unquoted_list):
        try:
            # Renames a file using the path + filename
            rename(join(directory_path, original_name),
                   join(directory_path, changed_name))

            LOGGER.info('Changed %s to %s' % (join(directory_path, original_name),
                                              join(directory_path, changed_name)))
        except Exception as e:
            LOGGER.debug('ERROR: ' + e)


def unquote_directory_name(path: str, recursive=True):
    for directory, _, _ in walk(path, followlinks=False):

        if directory != '.' and getcwd() != directory:
            try:
                changed_directory_name = unquote_name(directory)
                # Renames a file using the path + filename
                rename(join(path, directory),
                       join(path, changed_directory_name))

                LOGGER.info('Changed %s to %s' %
                            (directory, changed_directory_name))

            except Exception as e:
                LOGGER.debug('ERROR: ' + str(e))

            finally:
                if not recursive:
                    return


def main():
    """ Construct a list of filenames to parse, and then rename them """

    # Parse Arguments
    arguments = parse_arguments()

    # If no argument passed then use working directory
    if arguments.folder is None:
        path = getcwd()
    else:
        path = str(arguments.folder)
        if path == '.' or path == './':
            path = getcwd()

    # If recursion argument was present, unquote all sub directories
    if arguments.recursion:

        # Unquote all directory names
        unquote_directory_name(path)

        # Unquote all file names
        for directory, _, _ in walk(path):
            if directory != '.':
                unquote_files(join(path, directory))
    else:
        unquote_directory_name(path, False)
        unquote_files(path)


if __name__ == '__main__':
    main()
