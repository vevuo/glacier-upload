from botocore.utils import calculate_tree_hash


def get_hashes(files):
    """Updates the provided files with tree hashes using the
    calculate_tree_hash function from botocore.utils. Also returns
    a total hash for all files.

    Args:
        files (list): List of dicts. Each containing path to the specific file.

    Returns:
        tuple: Updated files list and the total hash as a string
    """
    for file in files:
        tree_hash = _get_hash(file)
        file.update({"hash": tree_hash})
    total_hash = _get_total_hash(files)
    return files, total_hash


def _get_hash(file):
    with open(file.get("file_path"), "rb") as file_object:
        tree_hash = calculate_tree_hash(file_object)
    return tree_hash


def _get_total_hash(files):
    tree_hashes = [file.get("hash") for file in files]
    total_hash = "".join(tree_hashes)
    return total_hash


if __name__ == "__main__":
    files = [
        {"file_path": "test.txt"},
        {"file_path": "test_file2.txt"}
    ]
    updated_files, total_hash = get_hashes(files)
    print(updated_files)
    print(total_hash)
