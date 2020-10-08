from pathlib import Path


def get_total_size(files):
    return sum(get_file_size(file.get("file_path")) for file in files)


def get_file_size(file_path):
    return Path(file_path).stat().st_size


def add_file_size(files):
    updated_files = []
    for file in files:
        size = get_file_size(file.get("file_path"))
        file_size = {"file_size": size}
        updated_files.append({**file, **file_size})
    return updated_files


def add_ranges(files):
    updated_files = []
    start = 0
    for file in files:
        end = start + file.get("file_size")
        file_range = {"range": f"bytes {start}-{end-1}/*"}
        updated_files.append({**file, **file_range})
        start = end
    return updated_files
