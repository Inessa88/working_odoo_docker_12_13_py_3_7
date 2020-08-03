"""
Module to recursively find Odoo addon directories and requirements.
"""

# Stdlib:
import glob
import os
import sys
from pathlib import Path

MODULE_FILES = ("__manifest__.py", "__openerp__.py", "__odoo__.py", "__terp__.py")
REQUIREMENTS_FILE_NAME = "requirements.txt"


def is_module_directory(directory):
    for module_file in MODULE_FILES:
        pattern = os.path.join(directory, module_file)
        found_files = glob.glob(pattern)
        if found_files:
            return True
    return False


def is_modules_root_directory(directory):
    if is_module_directory(directory):
        return False
    for path in directory.iterdir():
        if is_module_directory(path):
            return True
    return False


# flake8: noqa: B006
def find_path_modules_root_directories(root_path, module_directories=set()):
    if is_module_directory(root_path):
        return module_directories
    for file in root_path.iterdir():
        if not file.is_dir() or file.name in [".git", ".github"]:
            continue
        if is_modules_root_directory(file):
            module_directories.add(str(file))
        find_path_modules_root_directories(file)
    return module_directories


# flake8: noqa: B006
def find_path_module_directories(root_path, module_directories=set()):
    if is_module_directory(root_path):
        return module_directories
    for file in root_path.iterdir():
        if not file.is_dir() or file.name in [".git", ".github"]:
            continue
        if is_module_directory(file) and not is_modules_root_directory(file):
            module_directories.add(str(file))
        find_path_module_directories(file)
    return module_directories


def find_requirements(root_path, requirements_list=set()):
    for file in root_path.iterdir():
        if not file.is_dir() or file.name in [".git", ".github"]:
            continue
        if is_module_directory(file) or file.name == "requirements":
            pattern = os.path.join(file.absolute(), REQUIREMENTS_FILE_NAME)
            requirements_file_path = Path(pattern)
            if requirements_file_path.exists() and requirements_file_path.is_file():
                requirements_list.add(str(requirements_file_path))
        find_requirements(file)
    return requirements_list


def get_path_directories_for_addons_path(path):
    print(
        ",".join(
            [
                module_directory
                for module_directory in find_path_modules_root_directories(Path(path))
            ]
        )
    )


def get_command_for_links_addons(path):
    with open("/tmp/set_links.sh", "w+") as f:
        f.write("#!/bin/sh\n\n")
        f.write(
            "\n".join(
                [
                    "ln -s {}/".format(os.environ.get("PWD"))
                    + module_directory
                    + "/* {}".format(os.environ.get("MAIN_ADDONS_PATH"))
                    for module_directory in find_path_modules_root_directories(
                        Path(path)
                    )
                ]
            )
        )


def get_command_for_install_requirements(path):
    with open("/tmp/set_requirements.sh", "w+") as f:
        f.write("#!/bin/sh\n\n")
        f.write(
            "\n".join(
                [
                    "pip3.7 install -r " + requirement
                    for requirement in find_requirements(Path(path))
                ]
            )
        )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "get_command_for_links_addons":
            get_command_for_links_addons(os.environ.get("PROJECT_PATH"))
        elif sys.argv[1] == "get_command_for_install_requirements":
            get_command_for_install_requirements(os.environ.get("PROJECT_PATH"))
    else:
        get_path_directories_for_addons_path(os.environ.get("PROJECT_PATH"))
