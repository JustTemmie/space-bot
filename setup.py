import json
import os
from os.path import exists

folderLocations = [
    "temp",
]

fileLocations = [
    ["data/yrIDs.json", "{}"],
]

for i in folderLocations:
    if not exists(i):
        print(f"created new folder at {i}")
        os.makedirs(i)
        

def checkAndWrite(file, contentIfEmpty):
    if not exists(file):
        with open(file, "w") as f:
            f.write(contentIfEmpty)
            print(f"created new file at {file} - containing {contentIfEmpty}")

for i in fileLocations:
    checkAndWrite(i[0], i[1])
