#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import sys

def parse_args():
    prog = sys.argv[0]
    description = "Import vcpkg packages into our custom registry."
    parser = argparse.ArgumentParser(prog = prog, description = description)

    parser.add_argument("--repo",
        default = "~/github/microsoft/vcpkg",
        help = "Path to an clone of vcpkg"
    )
    parser.add_argument("config",
        help = "Path to the vcpkg.json for TileDB."
    )

    return parser.parse_args()

def load_vcpkg_json(path):
    if not os.path.isfile(path):
        print("File not found: {}".format(path))
        exit(1)
    with open(path) as handle:
        return json.load(handle)

def vcpkg_dep_packages(vcpkg_json):
    for dep in vcpkg_json.get("dependencies", []):
        if isinstance(dep, str):
            yield dep
        elif isinstance(dep, dict):
            yield dep["name"]
    for feat in vcpkg_json.get("features", []):
        for dep in vcpkg_json["features"][feat].get("dependencies", []):
            if isinstance(dep, str):
                yield dep
            elif isinstance(dep, dict):
                yield dep["name"]

def import_package(pkg_name, repo, imported = None):
    if imported is None:
        imported = set()
    if pkg_name in imported:
        return
    print("Importing: {}".format(pkg_name))
    imported.add(pkg_name)

    port_dir = os.path.join(
        os.path.expanduser(repo),
        "ports",
        pkg_name
    )
    vcpkg_path = os.path.join(port_dir, "vcpkg.json")
    vcpkg_json = load_vcpkg_json(vcpkg_path)
    for dep in vcpkg_dep_packages(vcpkg_json):
        import_package(dep, repo, imported = imported)

    # Copy the port data over
    dst_path = os.path.join("ports", pkg_name)
    shutil.copytree(port_dir, dst_path, dirs_exist_ok=True)

    # Copy the version file
    version_path = os.path.join(
        os.path.expanduser(repo),
        "versions",
        "{}-".format(pkg_name[0]),
        "{}.json".format(pkg_name)
    )
    dst_dir = os.path.join(
        "versions",
        "{}-".format(pkg_name[0])
    )
    dst_path = os.path.join(dst_dir, "{}.json".format(pkg_name))
    if not os.path.isdir(dst_dir):
        os.mkdir(dst_dir)
    shutil.copy2(version_path, dst_path)

def main():
    args = parse_args()

    root = load_vcpkg_json(args.config)
    for pkg in vcpkg_dep_packages(root):
        import_package(pkg, args.repo)

if __name__ == "__main__":
    main()
