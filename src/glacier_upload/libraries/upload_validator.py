from pathlib import Path
from .setup_logger import logger
from .partlify import get_allowed_sizes


class Validator:
    def __init__(self):
        self.logger = logger

    def preupload_checks(self, path_to_file, part_size=None):
        checks = [
            {'method': self._check_if_file_exist, 'args': [path_to_file]},
        ]
        multipart_checks = [
            {'method': self._check_if_valid_part_size_for_glacier, 'args': [part_size]},
            {'method': self._check_if_part_size_smaller_than_total, 'args': [path_to_file, part_size]},
        ]
        results = []
        if part_size:  # Multipart upload
            checks.extend(multipart_checks)
        for check in checks:
            check_method = check.get('method')
            args = check.get('args')
            result = check_method(*args)
            results.append(result)
            if not result:
                break
        return all(results)

    def _check_if_file_exist(self, path_to_file):
        file_found = False
        if Path(path_to_file).is_file():
            file_found = True
            self.logger.info(f"File {path_to_file} found.")
        else:
            self.logger.error(f"File {path_to_file} can't be found. Cancelling upload.")
        return file_found

    def _check_if_valid_part_size_for_glacier(self, part_size):
        valid_part_size = False
        allowed = get_allowed_sizes()
        if str(part_size) in allowed.keys():
            valid_part_size = True
        else:
            self.logger.error(f"{part_size} is not allowed by Glacier. The allowed part sizes are listed below.")
            self.logger.error(f"In megabytes: {', '.join([str(size) for size in allowed.keys()])}")
        return valid_part_size

    def _check_if_part_size_smaller_than_total(self, path_to_file, part_size):
        valid_part_size = False
        total_size = Path(path_to_file).stat().st_size
        try:
            assert total_size > part_size
        except AssertionError:
            self.logger.error(f"The part size ({part_size}) is larger than the total upload size ({total_size}).")
            self.logger.error("Please specify smaller part size.")
        else:
            valid_part_size = True
        return valid_part_size

    def _is_response_ok(self, response):
        if response["ResponseMetadata"]["HTTPStatusCode"] in [200, 201, 204]:
            return True
        else:
            return False
