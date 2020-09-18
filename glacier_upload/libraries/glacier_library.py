import os.path
import boto3
from response_storage import Storage
from helpers import get_total_size, get_file_size
from hash_calculator import get_hashes


class GlacierLib:
    def __init__(self, vault_name, region_name="eu-west-1", storage_file="uploaded.json"):
        """Uploads files to the specified AWS Glacier vault.

        Args:
            vault_name (str): Name of the target vault
            region_name (str, optional): AWS region that is used. Defaults to "eu-west-1".
        """
        self.client = boto3.client('glacier', region_name=region_name)
        self.vault_name = vault_name
        self.storage_file = storage_file
        self.storage = Storage(file_name=self.storage_file)

    def upload(self, files, description):
        """Initiates the upload process for the provided files.

        Args:
            files (list): List of dicts. Containing the path to files.
            description (str): Description of what is being uploaded
        """
        if self._is_ready_for_upload(files):
            if len(files) > 1:
                files, total_hash = get_hashes(files)
                # files, total_hash = self._calculate_and_add_tree_hashes(files)
                part_size = get_file_size(files[0].get("file_path"))
                total_size = get_total_size(files)
                self._start_multipart_upload(
                    files,
                    description,
                    part_size,
                    total_size,
                    total_hash
                    )
            else:
                self._start_upload(files, description)

    def _is_ready_for_upload(self, files):
        status = [
            self._check_if_all_files_exist(files),
            self._check_if_valid_file_sizes(files),
            self._check_if_vault_exists(self.vault_name),
        ]
        return all(status)

    def _check_if_all_files_exist(self, files):
        files_found = []
        for file in files:
            file_path = file.get("file_path")
            if os.path.exists(file_path):
                files_found.append(True)
            else:
                print(f"File {file_path} can't be found. Canceling upload process.")
                files_found.append(False)
                break
        return all(files_found)

    def _check_if_vault_exists(self, vault_name):
        response = self._execute_call(
            self.client.list_vaults,
            {}
        )
        vault_list = response.get("VaultList")
        exists = any([True for vault in vault_list if vault['VaultName'] == vault_name])
        try:
            assert exists
        except AssertionError:
            print(f"Seems like a vault with the name '{vault_name}' doesn\'t exist.")
            print("Canceling upload process.")
        return exists

    def _check_if_valid_file_sizes(self, files):
        if len(files) > 1:
            """TODO: Let's check that the multipart upload will have correct
            file sizes for each file before upload (the last one can be anything
            smaller than the others).
            """
            return True
        else:
            return True

    def _start_upload(self, files, description):
        """When there is only one archive (single file) uploaded then this
        method will be used.
        """
        response = None
        with open(files[0].get("file_path"), "rb") as file_object:
            upload_kwargs = {
                "vaultName": self.vault_name,
                "archiveDescription": description,
                "body": file_object,
            }
            print("Starting single file upload.")
            response = self._execute_call(
                self.client.upload_archive,
                upload_kwargs
            )
            print(f"Upload completed. Saving response to {self.storage_file}.")
            self.storage.save(response)
        return response

    def _start_multipart_upload(self, files, description, part_size, total_size, total_hash):
        """When there are multiple files (multiple parts of an archive) we use specific
        initiate, upload and complete methods from the boto3 library.
        """
        file_count = len(files)
        initiate_kwargs = {
            "vaultName": self.vault_name,
            "archiveDescription": description,
            "partSize": part_size,
        }
        print("Initiating multipart upload.")
        initiate_response = self._execute_call(
            self.client.initiate_multipart_upload,
            initiate_kwargs
        )

        if initiate_response:
            print(f"Starting multipart upload for {file_count} files. Total size {total_size} bytes.")
            for i, file in enumerate(files, 1):
                with open(file.get("file_path"), "rb") as file_object:
                    upload_kwargs = {
                        "vaultName": self.vault_name,
                        "uploadId": initiate_response.get("uploadId"),
                        "range": file.get("range"),
                        "body": file_object,
                    }
                print(f"Uploading file {i}/{file_count}...")
                upload_response = self._execute_call(
                    self.client.upload_multipart_part,
                    upload_kwargs
                )
                # TODO HERE: Retry on failure?
                if upload_response:
                    file.update({"success": True})
                else:
                    file.update({"success": False})

            if all([file.get("success") for file in files]):
                complete_kwargs = {
                    "vaultName": self.vault_name,
                    "uploadId": initiate_response.get("uploadId"),
                    "archiveSize": total_size,
                    "checksum": total_hash
                }
            else:
                print("Upload for some archive parts failed.")
                print("Aborting multipart upload.")
                self._abort_multipart_upload()

    def _abort_multipart_upload(self, upload_id):
        pass

    def _execute_call(self, call, kwargs):
        response = None
        try:
            response = call(**kwargs)
        except self.client.exceptions.ResourceNotFoundException:
            print("No such vault found")
            raise
        except self.client.exceptions.InvalidParameterValueException:
            print("Invalid parameters")
            raise
        except self.client.exceptions.MissingParameterValueException:
            print("Missing needed parameter")
            raise
        except self.client.exceptions.RequestTimeoutException:
            print("Timeout")
            raise
        except self.client.exceptions.ServiceUnavailableException:
            print("Connection error")
            raise
        return response


if __name__ == "__main__":
    glacier = GlacierLib(vault_name='cute-kittens-glacier')
    glacier.upload(
        files=[
            {"file_path": "test.txt"},
            {"file_path": "test_file2.txt"}
        ],
        description='Test files'
        )
