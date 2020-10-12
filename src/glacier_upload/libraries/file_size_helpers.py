from pathlib import Path


def get_total_size(files):
    return sum(get_file_size(file.get("file_path")) for file in files)


def get_file_size(file_path):
    return Path(file_path).stat().st_size


def get_allowed_sizes():
    allowed = dict()
    mb = 1
    byte = 1048576
    for i in range(12):
        allowed.update({str(mb): byte})
        mb += mb
        byte += byte
    return allowed


def get_needed_parts(path_to_file, part_size_mb, total_size):
    allowed_sizes = get_allowed_sizes()
    part_size_bytes = allowed_sizes.get(str(part_size_mb))
    last_part_size = total_size % part_size_bytes
    amount_of_parts = (total_size - last_part_size) / part_size_bytes
    parts = list()
    for _ in range(int(amount_of_parts)):
        parts.append({"part_size": part_size_bytes})
    parts.append({"part_size": last_part_size})
    return parts


def add_range_string(parts):
    start = 0
    for part in parts:
        end = start + part.get("part_size")
        part.update({"range": f"bytes {start}-{end-1}/*"})
        start = end
    return parts
