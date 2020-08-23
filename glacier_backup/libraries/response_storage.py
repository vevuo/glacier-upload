import os.path
import json


class Storage:
    def __init__(self, file_name="uploaded.json"):
        """By default a json file is used to store archive ids and other
        information related to the uploaded file(s). This can then be used
        to retrieve the archives later on. A proper database based setup
        could be used instead.

        Args:
            file_name (str, optional): Where the data is saved.
                Defaults to "uploaded.json".
        """
        self.file_name = file_name
        self._create_json_file()

    def _create_json_file(self):
        """Creates a json file structure if a file with the specified
        name doesn't already exist.
        """
        json_file_structure = {
            "archives": []
        }
        if not os.path.exists(self.file_name):
            self._write_json(json_file_structure)

    def _write_json(self, data):
        """Write given json formatted data to the file."""
        with open(self.file_name, "w") as file_object:
            json.dump(data, file_object, indent=4)

    def save(self, response):
        """Writes the given response dict to a json file.

        Args:
            response (dict): Response received from the AWS Glacier.
        """
        with open(self.file_name) as file_object:
            file_content = json.load(file_object)
            file_content['archives'].append(response)
        self._write_json(file_content)


if __name__ == "__main__":
    store = Storage()
    store.save({'moie': 'moi'})
