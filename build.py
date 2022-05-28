from sys import platform
import shutil
import os
from time import sleep

filename = ""
dfilename = ""

print("Checking platform...")

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
    print(f"Create a bug report for your platform in the github repo\nPlatform: {platform}");
    exit(1)

print(f"found platform! {platform} \nStarting build in 5 seconds...")
sleep(5)

print("Starting Build!")
try:
    os.system("cd submodules/miscLib && cargo build -r && cd ../../")
    print("Build Successful!")
except Exception as e:
    print(f"Failed to build package: {e}")
    exit(2)

print("Moving file...")
shutil.move(f"submodules/miscLib/target/release/{filename}", f"libraries/{dfilename}")

print("Done! (NOTE: This needs to be run on every update!!!!)")
exit(0)
