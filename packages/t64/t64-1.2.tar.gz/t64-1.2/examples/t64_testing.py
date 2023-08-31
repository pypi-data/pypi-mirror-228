# Test reading T64 files using t64 library: https://pypi.org/project/t64/

import math
from t64 import T64ImageReader

# Parameters (T64 files only)
mediaFolder = "C:/Commodore/AppMedia/c64/"
selectedFileName = "Qix.t64"
selectedProgram = b"QIX+"
read_contents = True

hostFile = T64ImageReader(mediaFolder + selectedFileName)
with hostFile as image:

    print("D64 Image properties and directory listing")
    print(f"hostFile size: {hostFile.filepath.stat().st_size}")
    print(f"Image full path: {hostFile.filepath}")
    print(f"Tape name: {hostFile.tape_name}")
    mylist = list(image.directory())  #Directory including disk name and blocks free
    print(mylist)

    print("Directory listing with entry details")
    for entry in image.iterdir():  #Directory with access to path entries
        size_blocks = math.ceil((entry.end_addr-entry.start_addr) / 254)
        print(f"name: {entry.name}, type: {entry.disk_type}, size blocks: {size_blocks}")

    print("Find specific program name on disk")
    for entry in image.iterdir():
        if entry.name == selectedProgram and entry.disk_type == "PRG":
            size_blocks = math.ceil((entry.end_addr-entry.start_addr) / 254)
            print(f"name: {entry.name}, type: {entry.disk_type}, size blocks: {size_blocks}")

            if read_contents:
                print(entry.contents())
