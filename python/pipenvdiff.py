# https://gist.github.com/ddahan/215472a4aa1805160aba0a77902e40da
import argparse
import json
import re

parser = argparse.ArgumentParser(description="Compare two Pipfile.lock files")
parser.add_argument(
    "file1", type=str, nargs="+", help="File 1 (the old one) to be compared"
)
parser.add_argument(
    "file2", type=str, nargs="+", help="File 2 (the new one) to be compared"
)

args = parser.parse_args()
file_1, file_2 = args.file1[0], args.file2[0]

with open(file_1) as data_file_1, open(file_2) as data_file_2:
    data_1_loaded, data_2_loaded = json.load(data_file_1), json.load(data_file_2)

packages_1, packages_2 = data_1_loaded["default"], data_2_loaded["default"]

for package_name, package_info in packages_1.items():
    if package_name in packages_2.keys():
        p1_version = re.sub("[=]", "", package_info.get("version", ""))
        p2_version = re.sub("[=]", "", packages_2[package_name].get("version", ""))
        if not p1_version == p2_version:
            print(f"{package_name}: {p1_version} -> {p2_version}")
