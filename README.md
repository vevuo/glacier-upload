# glacier-upload

A command line interface (CLI) for uploading files to Amazon S3 Glacier. Uses the [Boto3 SDK](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).

## Project state

Currently handles a single file upload either in a one large chunk or in mutiple small parts. The uploading works fine but it would be fair to consider the project in it's current state as a starting point for a full-fledged program. See TODO section for a list of possible additions.

## Configuration

See the boto3 configuration section [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration) (for the needed authentication credentials). The AWS region can be provided when using glacier-upload (`-r` or `--region`) or it can be set in the `~/.aws/config` file ([see the same config page](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration)).

Of course there also needs to be a suitable Glacier vault created beforehand.

## Dependencies

* [boto3](https://github.com/boto/boto3) (version 1.16.3 used)

Requires Python 3.6+ and uses pytest for the tests (needs to be installed if needed).

## Installation

Currently can only be installed from an archive:

`python -m pip install glacier-upload.zip`

## Usage

Basic usage (will upload in a one chunk):

`glacier-upload [upload_file_path] [glacier_vault_name]`

Giving description of what is uploaded (handy later on when downloading files)

`glacier-upload -d "Description of the upload" [upload_file_path] [glacier_vault_name]`

Multipart upload (using -m flag and -s for part size in mb):

`glacier-upload -m -s 4 [upload_file_path] [glacier_vault_name]`

See more details with:

`glacier-upload --help`

## Running tests

Tests are located in the `tests` folder (also configured in the `setup.cfg`). Running the tests can simply be done with:

`python -m pytest`

## TODO

* More unit tests (current coverage is )
* Possibility to abort a failed upload
* Retry for failed attempts
* Uploading multiple files (from a folder) on one go
* Progress bar
* Displaying the upload speed
...
...