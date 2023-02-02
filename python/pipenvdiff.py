import argparse
import json
import re

parser = argparse.ArgumentParser(description="Compare two Pipfile.lock files.")
parser.add_argument("base", type=str, help="The base lock file to be compared.")
parser.add_argument("head", type=str, help="The head lock file to be compared.")

args = parser.parse_args()

with open(args.base) as base_file, open(args.head) as head_file:
    base, head = json.load(base_file), json.load(head_file)

changes = []

for group in (set(base.keys()) | set(head.keys())) - {"_meta"}:
    base_packages, head_packages = base[group], head[group]

    for name, info in base_packages.items():
        if name not in head_packages.keys():
            changes.append(f"{name} removed")
            continue
        base_version = re.sub(r"[=]", "", info.get("version", ""))
        head_version = re.sub(r"[=]", "", head_packages[name].get("version", ""))
        if not base_version == head_version:
            changes.append(f"{name}: {base_version} -> {head_version}")

    for name, info in head_packages.items():
        if name not in base_packages.keys():
            changes.append(f"{name} added")

print("\n".join(sorted(set(changes))))
