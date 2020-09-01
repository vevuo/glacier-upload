import os.path
import boto3
from botocore.utils import calculate_tree_hash
from response_storage import Storage

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
        if self.ready_for_upload(files):
            if len(files) > 1:
                pass
            else:
                self._start_upload(files, description)

    def ready_for_upload(self, files):
        """Checks that everything is ready for the upload to begin."""
        status = [
            self._check_if_all_files_exist(files),
            # self._check_if_vault_exists(self.vault_name),
        ]
        return all(status)

    def _check_if_all_files_exist(self, files):
        files_found = []
        for file in files:
            if os.path.exists(file.get("file_path")):
                files_found.append(True)
            else:
                print(f"File {file.get("file_path")} can't be found. Canceling upload process.")
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
            assert exists, f"Seems like a vault with the name \"{vault_name}\" doesn\'t exist."
        except AssertionError as e:
            print(e)
            print("Canceling upload process.")
        return exists

    def _calculate_hashes(self, files):
        for file in files  # FIX
            with open(file, "rb") as file_object:
                tree_hash = calculate_tree_hash(file_object)
                print(tree_hash)

    def _start_upload(self, files, description):
        """When only one file is provided it will be uploaded using the upload_archive()
        method from boto3.
        """
        response = None
        with open(files[0], "rb") as file_object:
            try:
                response = self.client.upload_archive(
                    vaultName=self.vault_name,
                    archiveDescription=description,
                    body=file_object
                )
                self.storage.save(response)
            except Exception as e:
                print(e)
        return response

    def _start_multipart_upload(self, archive, description, part_size):
        """When there are multiple files (multiple parts of an archive) we use specific
        initiate, upload and complete methods from the boto3 library.
        """
        initiate_kwargs = {
            "vaultName": self.vault_name,
            "archiveDescription": description,
            "partSize": part_size,
        }
        initiate_response = self._execute_call(
            self.client.initiate_multipart_upload,
            initiate_kwargs
        )

        if initiate_response:
            for archive_part in archive:
                with open(archive_part, "rb") as file_object:
                    upload_kwargs = {
                        "vaultName": self.vault_name,
                        "uploadId": initiate_response.get("uploadId"),
                        "range": archive_part.get("range"),
                        "body": file_object,
                    }
                upload_response = self._execute_call(
                    self.client.upload_multipart_part,
                    upload_kwargs
                )
                if not upload_response:
                    # TODO: Needs to have retry option
                    break
            
            if all([True if archive_part.get("status") is 1 else False for archive_part in archive]):
                complete_kwargs = {
                    "vaultName": self.vault_name,
                    "uploadId": initiate_response.get("uploadId"),
                    "archiveSize": ,
                    "body": file_object,                    
                }
            else:
                # TODO: So something has failed. Not all of the parts got uploaded.
                # Need to _abort_multipart_upload().
                pass

    def _abort_multipart_upload(self, upload_id):
        pass

    def _execute_call(self, func, kwargs):
        response = None
        try:
            response = func(**kwargs)
        except ResourceNotFoundException:
            raise
        except InvalidParameterValueException:
            raise
        except MissingParameterValueException:
            raise
        except RequestTimeoutException:
            print("Timeout")
            raise
        except ServiceUnavailableException:
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
