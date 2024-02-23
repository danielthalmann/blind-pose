import bpy
import subprocess
import sys
from .Operators.ObjectMove import ObjectMove
from .Operators.RunFileSelector import RunFileSelector
from .PanelInterface import PanelInterface


bl_info = {
    "name": "Blind Pose",
    "author": "Daniel Thalmann",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
#    "location": "",
    "description": "Motion capture with your web camera",
    "category": "3D View",
#    "wiki_url": "",
#    "tracker_url": ""
}

_classes = [
    ObjectMove,
    RunFileSelector,
    PanelInterface
]


    

#def menu_func(self, context):
#    self.layout.operator(ObjectMove.bl_idname)


#
def register():
    # subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "mediapipe"])
    for c in _classes: 
        try:
            bpy.utils.register_class(c)
        except RuntimeError:
            pass
        


def unregister():
    for c in _classes: 
        try:
            bpy.utils.unregister_class(c)
        except RuntimeError:
            pass
        


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
#if __name__ == "__main__":
#    register()