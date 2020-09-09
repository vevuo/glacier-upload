import os.path
import boto3
from botocore.utils import calculate_tree_hash
from response_storage import Storage
from helpers import get_total_size


class GlacierLib:
    def __init__(self, vault_name, region_name="eu-west-1", storage_file="uploaded.json"):
        """Uploads files to the specified AWS Glacier vault.

        Args:
            vault_name (str): Name of the target vault
            region_name (str, optional): AWS region that is used. Defaults to "eu-west-1".
        """
        self.client = boto3.client('glacier', region_name=region_name)
        self.vault_name = vault_name
        self.storage = Storage(file_name=storage_file)

    def upload(self, files, description):
        """Initiates the upload process for the provided files.

        Args:
            files (list): Path to each file
            description (str): Description of what is being uploaded
        """
        if self._is_ready_for_upload(files):
            if len(files) > 1:
                files = self._calculate_hashes(files)
                total_size = get_total_size(files)
            else:
                self._start_upload(files, description)

    def _is_ready_for_upload(self, files):
        status = [
            self._check_if_all_files_exist(files),
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
            self.client.list_vaults(),
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

    def _calculate_hashes(self, files):
        for file in files:
            with open(file.get("file_path"), "rb") as file_object:
                tree_hash = calculate_tree_hash(file_object)
            file.update({"hash": tree_hash})
        return files

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
            print("Starting single file upload")
            response = self._execute_call(
                self.client.upload_archive,
                upload_kwargs
            )
            print("Upload completed. Saving response.")
            self.storage.save(response)
        return response

    def _start_multipart_upload(self, files, description, part_size, total_size):
        """When there are multiple files (multiple parts of an archive) we use specific
        initiate, upload and complete methods from the boto3 library.
        """
        file_count = len(files)
        initiate_kwargs = {
            "vaultName": self.vault_name,
            "archiveDescription": description,
            "partSize": part_size,
        }
        print("Initiating multipart upload")
        initiate_response = self._execute_call(
            self.client.initiate_multipart_upload,
            initiate_kwargs
        )

        if initiate_response:
            print(f"Starting multipart upload for {file_count} files")
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
                # if not upload_response:
                # TODO HERE: Retry on failure?
                if upload_response:
                    file.update({"success": True})
                else:
                    file.update({"success": False})

            if all([file.get("success") for file in files]):
                complete_kwargs = {
                    "vaultName": self.vault_name,
                    "uploadId": initiate_response.get("uploadId"),
                    "archiveSize": "",
                    "body": file_object,
                }
            else:
                print("Upload process has failed. Aborting multipart upload.")
                self._abort_multipart_upload()

    def _abort_multipart_upload(self, upload_id):
        pass

    def _execute_call(self, func, kwargs):
        response = None
        try:
            response = func(**kwargs)
        except self.client.exceptions.ResourceNotFoundException:
            raise
        except self.client.exceptions.InvalidParameterValueException:
            raise
        except self.client.exceptions.MissingParameterValueException:
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
            {"file_path": "test.txt"}
        ],
        description='Test files'
        )
