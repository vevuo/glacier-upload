import os
import sys
import argparse
from libraries.glacier_library import Glacier
from libraries.packager_library import Packager


def setup_parser():
    parser = argparse.ArgumentParser(
        prog='glacier_backup',
        usage='%(prog)s [options] instance folder',
        description='Backup files to AWS Glacier',
        epilog='Happy backuping!'
        )
    parser.add_argument(
        'folder',
        metavar='folder',
        type=str,
        help='Folder holding files for backup'
        )        
    parser.add_argument(
        'instance',
        metavar='instance',
        type=str,
        help='AWS Glacier instance name'
        )
    parser.add_argument(
        '-s',
        '--size',
        default='32000',
        type=int,
        help='Size of the sent packages',
        )
    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
