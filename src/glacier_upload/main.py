import os
import sys
import argparse
from glacier_upload.libraries.glacier_library import GlacierLib


def setup_parser():
    parser = argparse.ArgumentParser(
        prog='glacier_upload',
        usage='%(prog)s [options] vault file',
        description='Upload files to AWS S3 Glacier',
        epilog='Keep uploading!'
        )
    parser.add_argument(
        'vault',
        metavar='vault',
        type=str,
        help='Glacier vault instance name'
        )
    parser.add_argument(
        'file',
        metavar='file',
        type=str,
        help='File path for the upload'
        )
    parser.add_argument(
        '-o',
        '--onepart',
        action='store_true',
        help='One part upload'
    )
    parser.add_argument(
        '-m',
        '--multipart',
        action='store_true',
        help='Multipart upload'
    )
    parser.add_argument(
        '-s',
        '--size',
        type=int,
        default=8388608,
        help='Multipart upload part size e.g. 1048576 (1 MB), 2097152 (2 MB), 4194304 (4 MB) and so on'
    )    
    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    glacier = GlacierLib(vault_name=args.vault)
    glacier.upload(files=args.file)


if __name__ == "__main__":
    main()
