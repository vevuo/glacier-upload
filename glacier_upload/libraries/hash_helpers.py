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
    """
    tree_hashes = [file.get("hash") for file in files]
    parent = []
    for i in range(0, len(tree_hashes), 2):
        if i < len(tree_hashes) - 1:
            part1 = binascii.unhexlify(tree_hashes[i])
            part2 = binascii.unhexlify(tree_hashes[i + 1])
            parent.append(hashlib.sha256(part1 + part2).hexdigest())
        else:
            parent.append(tree_hashes[i])
    return parent[0]
