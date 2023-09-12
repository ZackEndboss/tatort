#!/usr/bin/env python3
import os
from pathlib import Path
from renamer import Renamer

SOURCE_DIR = "/Users/haiko/Documents/Temp/Filme/Tatort"
DEST_DIR = "/Users/haiko/Documents/Temp/Tatort"
DUPLICATE_DIR = "/Users/haiko/Documents/Temp/Tatort-Doppelt"
SYMLINK = True

def move(source, dest) :
    try :
        os.makedirs(os.path.dirname(dest))
    except :
        pass
    if SYMLINK is True:
        os.symlink(source, dest)
        print(f"link: {source} -> {dest}")
    else:
        os.rename(source, dest)
        print(f"move: {source} -> {dest}")

renamer = Renamer()

for f in Path(SOURCE_DIR).iterdir():
    if f.is_file() :
        new_name = renamer.rename(f.name)
        if new_name is not None :
            source = f"{f.parent}/{f.name}"
            dest = f"{DEST_DIR}/{new_name}"
            duplicate = f"{DUPLICATE_DIR}/{f.name}"
            if not os.path.isfile(dest) and not os.path.islink(dest):
                print(f">>> {f.name} moved/linked")
                move(source, dest)
            else :
                print(f"*** {f.name} duplicate")
                move(source, duplicate)
        else :
            print(f"??? {f.name} not found")
