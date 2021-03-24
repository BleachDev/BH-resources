import os
import sys
import time
import uuid
import zipfile
import requests
import shutil
from clint.textui import progress

if len(sys.argv) != 3:
    print("Invalid argument size")
    print("Syntax: installer.py [old-mod] [new-mod-url]")
    time.sleep(10)
    sys.exit()

#url = "https://nightly.link/BleachDrinker420/BleachHack/workflows/gradle/master/BleachHack-1.16.5.zip"

oldmodfile = sys.argv[1]
url = sys.argv[2]
tempfile = "bh-" + str(uuid.uuid4())

print("Downloading latest build..")

# stackoverflow momento
r = requests.get(url, stream=True)
with open(tempfile, "wb") as f:
    header = r.headers.get("content-length")

    try:
        total_length = int(header)
    except:
        total_length = 2_600_000

    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
        if chunk:
            f.write(chunk)
            f.flush()

print()

if url.endswith(".zip"):
    print("Extracting jar..")
    with zipfile.ZipFile(tempfile, 'r') as zp:
        files = zipfile.ZipFile.infolist(zp)
        if len(files) > 0:
            unzippedfile = "bh-" + str(uuid.uuid4())

            with open(unzippedfile, 'wb') as f:
                f.write(zp.read(files[0].filename))
        else:
            print("No files in zipfile, Aborting!")
            time.sleep(10)
            sys.exit()

    os.remove(tempfile)
    tempfile = unzippedfile

print("Replacing jar..")

firstLine = False
while True:
    try:
        os.remove(oldmodfile)

        if firstLine:
            print();

        break;
    except Exception as e:
        if not os.path.exists(oldmodfile):
            print("- File already deleted??")
            break;

        if firstLine:
            print(".", end="")
        else:
            print("- Waiting for Minecraft to close.", end="")
            firstLine = True

        time.sleep(1)

try:
    shutil.move(tempfile, oldmodfile)
except Exception as e:
    print("Unable to move jar to mod directory, Aborting!")
    time.sleep(10)
    sys.exit()

print("\nInstalled Successfully!")
time.sleep(10)
