import argparse
from glacier_upload.libraries.glacier_library import GlacierLib


def setup_parser():
    parser = argparse.ArgumentParser(
        prog='glacier-upload',
        usage='%(prog)s [options] file vault_name',
        description='upload files to AWS S3 Glacier',
        epilog='happy uploading!'
        )
    parser.add_argument(
        'file',
        metavar='file',
        type=str,
        help='uploaded file'
        )
    parser.add_argument(
        'vault_name',
        metavar='vault_name',
        type=str,
        help='glacier vault name'
        )
    parser.add_argument(
        '-d',
        '--desc',
        default='',
        help='description of the uploaded content'
    )
    parser.add_argument(
        '-m',
        '--multipart',
        action='store_true',
        help='use multipart upload. default part size is 4 megabytes.'
    )
    parser.add_argument(
        '-s',
        '--part_size',
        default='4',
        type=int,
        help='multipart upload part size in megabytes. Sizes allowed by Glacier are 1, 2, 4, 8 and so on.'
    )
    parser.add_argument(
        '-r',
        '--region',
        help='aws region (where the vault is located in)'
    )
    parser.add_argument(
        '-l',
        '--log_file',
        default='uploaded_log.json',
        help='logs the responses from Glacier (e.g. archiveId) in JSON format. defaults to uploaded_log.json'
    )
    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    settings = vars(args)
    glacier = GlacierLib(
        vault_name=settings.get("vault_name"),
        upload_log=settings.get("log_file"),
        region_name=settings.get("region_name"),
        )
    upload_args = {
        "path_to_file": settings.get("file"),
        "part_size": settings.get("part_size"),
        "description": settings.get("desc"),
    }
    if settings.get("multipart"):
        glacier.multipart_upload(**upload_args)
    else:
        glacier.upload(**upload_args)


if __name__ == "__main__":
    main()
