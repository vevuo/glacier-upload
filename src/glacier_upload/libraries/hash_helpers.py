import binascii
import hashlib
from botocore.utils import calculate_tree_hash


def get_tree_hash(path_to_file):
    """Returns a tree hash for a single file."""
    with open(path_to_file, "rb") as file_object:
        tree_hash = calculate_tree_hash(file_object)
    return tree_hash


def get_part_hash(part_data):
    return hashlib.sha256(part_data).hexdigest()


def get_total_hash(hashes):
    """Calculates the total hash for all uploaded parts.

    Args:
        files (list): List of dicts with info on each part (tree hash)

    Returns:
        string: Calculated total hash
    """
    while len(hashes) > 1:
        parent = []
        for i in range(0, len(hashes), 2):
            if i < len(hashes) - 1:
                part1 = binascii.unhexlify(hashes[i])
                part2 = binascii.unhexlify(hashes[i + 1])
                parent.append(hashlib.sha256(part1 + part2).hexdigest())
            else:
                parent.append(hashes[i])
        hashes = parent
    return hashes[0]
