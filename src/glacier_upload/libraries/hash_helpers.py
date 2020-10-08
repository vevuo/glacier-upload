import binascii
import hashlib
from botocore.utils import calculate_tree_hash


def add_hashes(files):
    """Updates the provided files with tree hashes using the
    calculate_tree_hash function from botocore.utils.

    Args:
        files (list): List of dicts with info on each file (i.e. file path)

    Returns:
        list: The original list of dicts updated with tree hash for each file
    """
    for file in files:
        tree_hash = get_hash(file)
        file.update({"hash": tree_hash})
    return files


def get_hash(file):
    with open(file.get("file_path"), "rb") as file_object:
        tree_hash = calculate_tree_hash(file_object)
    return tree_hash


def get_total_hash(files):
    """Calculates the total hash for all parts of the archive

    Args:
        files (list): List of dicts with info on each file (i.e. file path)

    Returns:
        string: Calculated total hash
    
    def calculate_total_tree_hash(list_of_checksums):
        tree = list_of_checksums[:]
        while len(tree) > 1:
            parent = []
            for i in range(0, len(tree), 2):
                if i < len(tree) - 1:
                    part1 = binascii.unhexlify(tree[i])
                    part2 = binascii.unhexlify(tree[i + 1])
                    parent.append(hashlib.sha256(part1 + part2).hexdigest())
                else:
                    parent.append(tree[i])
            tree = parent
        return tree[0]
    """
    tree = [file.get("hash") for file in files]
    while len(tree) > 1:
        parent = []
        for i in range(0, len(tree), 2):
            if i < len(tree) - 1:
                part1 = binascii.unhexlify(tree[i])
                part2 = binascii.unhexlify(tree[i + 1])
                parent.append(hashlib.sha256(part1 + part2).hexdigest())
            else:
                parent.append(tree[i])
        tree = parent
    return tree[0]


if __name__ == "__main__":
    files = [
        {"file_path": "data/random_2.zip.001"},
        {"file_path": "data/random_2.zip.002"},
        {"file_path": "data/random_2.zip.003"},
    ]
    total_hash = get_total_hash(files)
    print(total_hash)
