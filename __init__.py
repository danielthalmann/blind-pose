import subprocess
import sys

bl_info = {
    "name": "CamPose",
    "author": "Daniel Thalmann",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
#    "location": "",
    "description": "Motion capture with your web camera",
    "category": "3D View",
#    "wiki_url": "",
#    "tracker_url": ""
}

###
def register():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
    


def unregister():
    print("Goodbye World")
