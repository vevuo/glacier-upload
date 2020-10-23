import argparse
from glacier_upload.libraries.glacier_library import GlacierLib


def setup_parser():
    parser = argparse.ArgumentParser(
        prog='glacier_upload',
        usage='%(prog)s [options] file vault',
        description='upload files to AWS S3 Glacier',
        epilog='happy uploading!'
        )
    parser.add_argument(
        'file',
        metavar='file',
        type=str,
        help='file path for the upload'
        )
    parser.add_argument(
        'vault',
        metavar='vault',
        type=str,
        help='glacier vault instance name'
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
        help='use multipart upload'
    )
    parser.add_argument(
        '-s',
        '--size',
        default='4',
        type=int,
        help='multipart upload part size in megabytes. Sizes allowed by Glacier are 1, 2, 4, 8 and so on.'
    )
    parser.add_argument(
        '-r',
        '--region',
        default='eu-west-1',
        help='aws region where the vault is located'
    )
    parser.add_argument(
        '-l',
        '--log_file',
        default='uploaded_log.json',
        help='logs the responses from Glacier (e.g. uploadId) in JSON format. Defaults to uploaded.json'
    )
    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    glacier = GlacierLib(
        vault_name=args.vault,
        region_name=args.region,
        upload_log=args.log_file,
        )
    upload_args = {
        "path_to_file": args.file,
        "description": args.desc,
    }
    if args.multipart is False:
        glacier.upload(**upload_args)
    else:
        upload_args.update({"part_size": args.size})
        glacier.multipart_upload(**upload_args)


if __name__ == "__main__":
    main()
