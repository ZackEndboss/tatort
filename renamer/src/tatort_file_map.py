#!/usr/bin/env python3
import os
from pathlib import Path
from renamer import Renamer
import argparse

# SOURCE_DIR = "../test-source"
# DEST_DIR = "../test-dest"
# DUPLICATE_DIR = "../test-dups"
# SYMLINK = True

# docker run -it --rm   --name tatortrenamer   -v /home/zack/docs/docker/tatort/test-src:/home/zack/docs/docker/tatort/test-src   -v /home/zack/docs/docker/tatort/test-dest:/home/zack/docs/docker/tatort/test-dest -v /home/zack/docs/docker/tatort/test-dups:/home/zack/docs/docker/tatort/test-dups  tatort.renamer python /usr/src/app/tatort_file_map.py /home/zack/docs/docker/tatort/test-src /home/zack/docs/docker/tatort/test-dest /home/zack/docs/docker/tatort/test-dups

parser = argparse.ArgumentParser(description="Script um manuell ein Source-Folder mit Tatort-Folgen umbenannt in ein Destination-Folder moved/linked um diese mit Plex-Agents erkennen zu koennen.")

# Erforderliche Argumente
parser.add_argument("source", type=str, help="Pfad zum Quellverzeichnis.")
parser.add_argument("dest", type=str, help="Pfad zum Zielpfad.")
parser.add_argument("duplicate", type=str, help="Pfad zum Duplicatedverzeichniss.")

# Optionale Argumente
parser.add_argument("--symlink", type=bool, default=True, help="Gibt an, ob ein symbolischer Link erstellt werden soll, statt die source zu verschieben.")

args = parser.parse_args()

# Zugriff auf die Argumente
SOURCE_DIR    = args.source
DEST_DIR      = args.dest
DUPLICATE_DIR = args.duplicate
SYMLINK       = args.symlink

def move(source, dest) :
    try :
        os.makedirs(os.path.dirname(dest))
    except :
        pass
    if SYMLINK is True:
        # os.symlink(source, dest)
        print(f"link: {source} -> {dest}")
    else:
        os.rename(source, dest)
        # print(f"move: {source} -> {dest}")

renamer = Renamer()

for f in Path(SOURCE_DIR).iterdir():
    if f.name in ["duplicate", "logs", "unknown"]:
        continue
    if f.is_file() or f.is_dir():
        new_name = renamer.rename(f.name)
        if new_name is not None :
            source = f"{f.parent}/{f.name}"
            dest = f"{DEST_DIR}/{new_name}"
            duplicate = f"{DUPLICATE_DIR}/{f.name}"
            if not os.path.isfile(dest) and not os.path.islink(dest) and not os.path.isdir(dest):
                print(f">>> {f.name} moved/linked")
                move(source, dest)
            else :
                print(f"*** {f.name} duplicate")
                move(source, duplicate)
        else :
            print(f"??? {f.name} not found")
