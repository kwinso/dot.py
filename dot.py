#!/usr/bin/env python3
import fnmatch
import os
import re
import shutil
from typing import List


# =============================
# Settings, feel free to edit
# =============================
class Settings:
    # Will copy files instead of sym-linking them (not VCS-friendly)
    use_copy = False
    use_gitignore = True  # Ignore files from .gitignore

    # Syntax:
    #  ("path to source file / dir", "path to destination file / dir")
    # NOTE:
    #  - Specifying directory as a source will copy <src>/* to <dst dir>/*
    #  - Copying file to directory follows the same logic as the `cp` command
    #  - Copying directory to file is not allowed
    paths = [
        (".", "~/.config"),
        (".bashrc", "~"),
    ]
    # Patters to ignore (relative to source directories, follows gitignore format)
    ignored: List[str] = []


# =============================
# EDIT ANYTHING BELOW CAREFULLY
# =============================
ignore_pattern = None


def main():
    print("This script replaces old dotfiles, make sure you have backups!")
    try:
        input("To stop, press <Ctrl + C>. To continue, press <Enter>: ")
    except KeyboardInterrupt:
        exit(0)

    if Settings.use_gitignore and os.path.exists(".gitignore"):
        Settings.ignored += list(
            set(open(".gitignore", "r").read().strip().split("\n"))
        )

    if len(Settings.ignored) > 0:
        global ignore_pattern
        ignore_pattern = "|".join(fnmatch.translate(pat) for pat in Settings.ignored)

    for src, dst in Settings.paths:
        src = normalize_path(src)
        dst = normalize_path(dst)

        if os.path.isdir(src) and os.path.isfile(dst):
            raise Exception(f"Cannot copy dir {src} to file {dst}")

        perform_copy(src, dst)

    print("Done copying files.")


def normalize_path(path):
    return os.path.abspath(os.path.expanduser(path))


def perform_copy(src, dst):
    if os.path.isfile(src):
        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))

        copy_file(src, dst)
        return

    children = os.walk(src)

    for d, subs, files in children:
        if len(subs) != 0:
            continue

        dst_path = d.replace(src, dst)
        os.makedirs(dst_path, exist_ok=True)

        for f in files:
            copy_file(
                os.path.join(d, f),
                os.path.join(dst_path, f),
            )


def copy_file(src_path, dst_path):
    """
    Fill either link or copy file based on settings.

    @param src_path: Source file absolute path
    @param dst_path: Destination absolute file path
    """

    if src_path == dst_path:
        print(f"Warn: cannot copy {src_path} to itself, skipping")
        return

    if bool(ignore_pattern) and bool(re.search(str(ignore_pattern), src_path.strip())):
        return

    # Make sure we're creating new file
    if os.path.exists(dst_path) or os.path.islink(dst_path):
        os.remove(dst_path)

    if Settings.use_copy:
        shutil.copyfile(src_path, dst_path)
    else:
        os.symlink(src_path, dst_path)


if __name__ == "__main__":
    main()
