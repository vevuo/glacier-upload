from pathlib import Path


class Packager:
    def __init__(self, args):
        self.setup = args

    def compress(self):
        """Validates that there are files to compress and then proceeds to
        zip them to chunks with size specified in the self.setup.
        """
        file_list = list()
        try:
            file_list = self.validate_folder_and_get_files()
        except AssertionError as e:
            return {'success': False, 'msg': str(e)}

        try:
            chunks = self.chunkify(file_list)
        except RuntimeError as e:
            return {'success': False, 'msg': str(e)}

        return {
            'success': True,
            'msg': f'{len(file_list)} files found which were compressed to {len(chunks)} archives.',
            'original_file_list': file_list,
            'chunks': chunks
        }

    def validate_folder_and_get_files(self):
        """Validates that the folder is okay for the Packager to compress. Returns
        a list of found files and folders.
        """
        folder = Path(self.setup['folder'])
        file_list = []
        assert folder.exists(), f'Could not find {folder} folder.'
        # Check that folder is not empty. Create a list of all files.
        for item in folder.rglob("*"):
            if item.is_file():
                file_list.append(item)
        assert file_list, f'No files found in {folder} folder.'
        return file_list

    def chunkify(self):
        pass


if __name__ == "__main__":
    pc = Packager({'folder': 'test'})
    result = pc.compress()
    print(result)
