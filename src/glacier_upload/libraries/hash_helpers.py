import binascii
import hashlib
from botocore.utils import calculate_tree_hash


def get_tree_hash(path_to_file):
    with open(path_to_file, "rb") as file_object:
        tree_hash = calculate_tree_hash(file_object)
    return tree_hash


def get_part_hash(part_data):
    return hashlib.sha256(part_data).hexdigest()


def get_total_hash(hash_list):
    """As implemented in another similar project here:
    https://github.com/tbumi/glacier-upload/
    """
    tree = hash_list[:]
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


def get_total_hash_alt(hash_list):
    tree = iter(hash_list)
    trees_in_pairs = [h + next(ini_list, '') for h in ini_list]


    return
