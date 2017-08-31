# Written by: Derek Santos

# Python Modules
from urllib.parse import unquote
from os import listdir, rename, walk, getcwd
from os.path import isfile, isdir, join
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


def unquote_name(name: str):
    """ Unqote and strip invalid characters from a filename and returns it """
    unquoted_name = unquote(name)
    stripped_name = unquoted_name.strip('/\\:*?"<>|')
    return stripped_name


def unquote_all(path: str):
    items = listdir(path)

    for item in items:
        try:
            if isfile(join(path, item)):
                changed_name = unquote_name(item)

                rename(join(path, item),
                       join(path, changed_name))

                LOGGER.info('Changed %s to %s' %
                            (join(path, item),
                             join(path, changed_name)))

            elif isdir(join(path, item)):
                changed_name = unquote_name(item)

                rename(join(path, item),
                       join(path, changed_name))

                LOGGER.info('Changed %s to %s' %
                            (join(path, item),
                             join(path, changed_name)))

        except Exception as e:
            LOGGER.debug('ERROR: ' + str(e))


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
        for directory, _, _ in walk(path):
            unquote_all(join(path, directory))
    else:
        unquote_all(join(path))


if __name__ == '__main__':
    main()
