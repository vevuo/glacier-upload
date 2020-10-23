from pathlib import Path


def get_file_size(path_to_file):
    return Path(path_to_file).stat().st_size


def get_allowed_sizes():
    allowed = dict()
    mb = 1
    byte = 1048576
    for i in range(12):
        allowed.update({str(mb): byte})
        mb += mb
        byte += byte
    return allowed


def get_needed_parts(path_to_file, part_size_bytes, total_size):
    last_part_size = total_size % part_size_bytes
    amount_of_parts = (total_size - last_part_size) / part_size_bytes
    parts = list()
    for _ in range(int(amount_of_parts)):
        parts.append({"part_size": part_size_bytes})
    if last_part_size > 0:
        parts.append({"part_size": last_part_size})
    return parts


def add_byte_ranges(parts):
    start = 0
    for part in parts:
        end = start + part.get("part_size")
        part.update(
            {
                "range": f"bytes {start}-{end-1}/*",
                "range_start": start,
                "range_end": end,
            }
        )
        start = end
    return parts
