import boto3
from .setup_logger import logger
from .response_storage import Storage
from .upload_validator import Validator
from .partlify import get_allowed_sizes, get_file_size, get_needed_parts, add_byte_ranges
from .hash_helpers import get_part_hash, get_total_hash


class GlacierLib:
    def __init__(self, vault_name, upload_log="uploaded_log.json", region_name=None):
        """Uploads a file in to the specified AWS S3 Glacier vault. Options for
        executing the upload either in one single chunk or multiple smaller parts.

        Args:
            vault_name (str): Name of the vault in Glacier.
            region_name (str, optional): Where the vault is located in aws. Defaults to "eu-west-1".
            log_file (str, optional): Logs the responses from Glacier. Defaults to "uploaded_log.json".
        """
        self.logger = logger
        self.client = boto3.client('glacier', region_name=region_name)
        self.vault_name = vault_name
        self.upload_log = upload_log
        self.storage = Storage(file_name=self.upload_log)
        self.validator = Validator()
        self.hashes = []

    def upload(self, path_to_file, description="", **kwargs):
        """Handles uploading a file in a single chunk. The "default" option.

        Args:
            path_to_file (str): Path to the file.
            description (str, optional): Description of what is uploaded.
        """
        if self.validator.preupload_checks(path_to_file) and self._vault_exists(self.vault_name):
            total_size = get_file_size(path_to_file)
            self._start_upload(path_to_file, description, total_size)

    def multipart_upload(self, path_to_file, description="", **kwargs):
        """Handles the multipart upload of a file.

        Args:
            path_to_file (str): Path to the file.
            description (str, optional): Description of what is uploaded.
            part_size (int, optional): Size for the multipart parts. Defaults to 4 megabytes.
        """
        part_size = kwargs["part_size"]
        if self.validator.preupload_checks(path_to_file, part_size) and self._vault_exists(self.vault_name):
            total_size = get_file_size(path_to_file)
            part_size_bytes = get_allowed_sizes().get(str(part_size))
            parts = get_needed_parts(path_to_file, part_size_bytes, total_size)
            parts = add_byte_ranges(parts)
            response = self._initiate_multipart_upload(description, part_size_bytes, total_size)
            if self.validator._is_response_ok(response):
                upload_id = response.get("uploadId")
                upload_success = self._start_multipart_upload(upload_id, path_to_file, parts)
                if upload_success:
                    total_hash = get_total_hash(self.hashes)
                    self._complete_multipart_upload(upload_id, total_size, total_hash)

    def _vault_exists(self, vault_name):
        """Checks if a vault exists with the specified name (and in the region)."""
        response = self._execute_call(self.client.list_vaults, {})
        vault_list = response.get("VaultList")
        exists = any([True for vault in vault_list if vault['VaultName'] == vault_name])
        try:
            assert exists
        except AssertionError:
            self.logger.error(f"Could not locate a vault with the name '{vault_name}'.")
        return exists

    def _start_upload(self, path_to_file, description, total_size):
        """This is the default single chunk upload option."""
        self.logger.info(f"Starting upload. File size {total_size} bytes.")
        with open(path_to_file, "rb") as file_object:
            upload_kwargs = {
                "vaultName": self.vault_name,
                "archiveDescription": description,
                "body": file_object,
            }
            self.logger.info("Uploading...")
            response = self._execute_call(
                self.client.upload_archive,
                upload_kwargs
            )
            if self.validator._is_response_ok(response):
                self.logger.info("Upload completed.")
                self.storage.save(response)
            else:
                self.logger.error("Upload failed!")

    def _initiate_multipart_upload(self, description, part_size_bytes, total_size):
        """This initiates the multipart upload in the Glacier."""
        self.logger.info(f"Starting multipart upload with part size {part_size_bytes} bytes.")
        self.logger.info(f"Total upload size {total_size} bytes.")
        initiate_kwargs = {
            "vaultName": self.vault_name,
            "archiveDescription": description,
            "partSize": str(part_size_bytes),
        }
        response = self._execute_call(
            self.client.initiate_multipart_upload,
            initiate_kwargs
        )
        return response

    def _start_multipart_upload(self, upload_id, path_to_file, parts):
        """Uploads the file part by part. Gets tree hashes for the parts at the same time."""
        part_count = len(parts)
        with open(path_to_file, "rb") as file_object:
            for i, part in enumerate(parts, 1):
                self.logger.info(f"Uploading part {i}/{part_count}...")
                file_object.seek(part.get("range_start"))
                part_data = file_object.read(part.get("part_size"))
                self.hashes.append(get_part_hash(part_data))
                response = self._upload_part(part, upload_id, part_data)
                if self.validator._is_response_ok(response):
                    part.update({"success": True})
                    self.logger.info("Done.")
                else:
                    # TODO: Retry?
                    part.update({"success": False})
                    self.logger.error("Fail.")
                    break
        return all([True for part in parts if part["success"]])

    def _upload_part(self, part, upload_id, body):
        """Uploading a single part."""
        upload_kwargs = {
            "vaultName": self.vault_name,
            "uploadId": upload_id,
            "range": part.get("range"),
            "body": body,
        }
        response = self._execute_call(
            self.client.upload_multipart_part,
            upload_kwargs
        )
        return response

    def _complete_multipart_upload(self, upload_id, total_size, total_hash):
        """After all parts have been succesfully uploaded this ends the process."""
        complete_kwargs = {
            "vaultName": self.vault_name,
            "uploadId": upload_id,
            "archiveSize": str(total_size),
            "checksum": total_hash
        }
        response = self._execute_call(
            self.client.complete_multipart_upload,
            complete_kwargs
            )
        return response

    def _abort_multipart_upload(self, upload_id):
        """TODO: Possibility to abort a failed upload."""
        pass

    def _execute_call(self, call, kwargs):
        """Calls the boto3 method with provided kwargs."""
        response = None
        try:
            response = call(**kwargs)
            self.logger.debug(response)
        except self.client.exceptions.ResourceNotFoundException:
            self.logger.error("Vault not found! Aborting upload.")
        except self.client.exceptions.InvalidParameterValueException:
            raise
            self.logger.error("Invalid parameter in the request! Aborting upload.")
        except self.client.exceptions.MissingParameterValueException:
            self.logger.error("Missing a parameter in the request! Aborting upload.")
        except self.client.exceptions.RequestTimeoutException:
            self.logger.error("Request timed out! Aborting upload.")
        except self.client.exceptions.ServiceUnavailableException:
            self.logger.error("Connection error or service unavailable. Aborting upload.")
        return response
