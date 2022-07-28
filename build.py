
# Code by github user @Radiicall
 
# # Import necessary libraries
from sys import platform, stdout
import shutil
import os
from time import sleep

# Set filename and dfilename to make them global vars
filename = ""
dfilename = ""

print("Checking platform...")

# Check platform and set filenames appropriately
if platform == "linux":
    filename = "libRSmiscLib.so"
    dfilename = "RSmiscLib.so"
elif platform == "darwin":
    filename = "libRSmiscLib.dylib"
    dfilename = "RSmiscLib.so"
elif platform == "win32":
    filename = "RSmiscLib.dll"
    dfilename = "RSmiscLib.pyd"
else:
    # If platform is not supported, exit with error code 1
    print(f"Create a bug report for your platform in the github repo\nPlatform: {platform}");
    exit(101)

print(f"found platform! {platform}")
for i in range(5):
    if i != 4:
        print(f"Starting build in {5-i} seconds...", end="\r")
    else:
        print("Starting build in 1 second... ", end="\r")
    sleep(1)

print("Starting Build!                 ")
try:
    os.system("cd submodules/miscLib && cargo build --release && cd ../../")
    print("Build Successful!")
except Exception as e:
    print(f"Failed to build package: {e}")
    exit(102)

print("Moving file...")
shutil.move(f"submodules/miscLib/target/release/{filename}", f"libraries/{dfilename}")

print("Done! (NOTE: This needs to be run on every update!!!!)")
exit(0)
