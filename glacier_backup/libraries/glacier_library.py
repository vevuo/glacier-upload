import os.path
import boto3
# from botocore.utils import calculate_tree_hash, calculate_sha256
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
            if os.path.exists(file):
                files_found.append(True)
            else:
                print(f"File {file} can't be found. Cancelling upload process.")
                files_found.append(False)
                break
        return all(files_found)

    def _check_if_vault_exists(self, vault_name):
        response = self.client.list_vaults()
        try:
            vault_list = response.get('VaultList')
        except Exception as e:
            print(e)  # What will the error be?
            raise
        exists = any([True for vault in vault_list if vault['VaultName'] == vault_name])
        try:
            assert exists, f"Seems like a vault with the name \"{vault_name}\" doesn\'t exist."
        except AssertionError as e:
            print(e)
            print("Cancelling upload process.")
        return exists

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

    def _start_multipart_upload(self, files, description, part_size):
        """When there are multiple files (multiple parts of an archive) we use specific
        initate, upload and completion methods from the boto3 library.
        """
        try:
            response = self.client.initiate_multipart_upload(
                vaultName=self.vault_name,
                archiveDescription=description,
                partSize=part_size
            )
        except Exception as e:
            print(e)

        try:
            response = self.client.upload_multipart_part(

            )
        except Exception as e:
            print(e)

        try:
            response = self.client.complete_multipart_upload(

            )
        except Exception as e:
            print(e)

    def _execute_call(self, func, **kwargs):
        response = None
        try:
            response = func(**kwargs)
        except Exception as e:
            print(e)
        return response


if __name__ == "__main__":
    glacier = GlacierLib(vault_name='cute-kittens-glacier')
    glacier.upload(files=['test.txt'], description='Test files')
