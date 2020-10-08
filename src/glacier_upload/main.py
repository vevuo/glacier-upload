import os
import sys
import argparse
from glacier_upload.libraries.glacier_library import GlacierLib


def setup_parser():
    parser = argparse.ArgumentParser(
        prog='glacier_upload',
        usage='%(prog)s [options] instance folder',
        description='Upload files to AWS S3 Glacier',
        epilog='Keep uploading!'
        )
    parser.add_argument(
        'file_folder',
        metavar='file_folder',
        type=str,
        help='A single file or Folder holding files for the upload'
        )
    parser.add_argument(
        'vault',
        metavar='vault',
        type=str,
        help='AWS S3 Glacier vault instance name'
        )
    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
