import bpy
import subprocess
import sys

from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

from bpy.types import Panel

from bpy.types import PropertyGroup

import cv2
import mediapipe as mp


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



class BlindPoseSettings(PropertyGroup):

    face_tracking: bpy.props.BoolProperty(default=False)
    hand_tracking: bpy.props.BoolProperty(default=False)
    body_tracking: bpy.props.BoolProperty(default=True)
    

class RunCapture(Operator):

    bl_idname = "blindpose.capture"
    bl_label = "Capture camera"
     
    def capture_motion(self) :
        
        vid = cv2.VideoCapture(0)

        # img = cv2.imread("p:\\3D\\wall.png")

        while (True):
            
            ret, frame = vid.read() 
            cv2.imshow("frame", frame)
            # the space ' ' button is set as the 
            # quitting button you may use any 
            # desired button of your choice 
            
            if cv2.waitKey(1) & 0xFF == ord(' '): 
                break

        vid.release()

        cv2.destroyAllWindows()
        
    def execute(self, context):
        
        self.capture_motion()

        return{'FINISHED'}
    


    
class RunFileSelector(Operator, ImportHelper):
    bl_idname = "blindpose.capture_from_file"
    bl_label = "Select Video File"
    filename_ext = ""

    def execute(self, context):
        file_dir = self.properties.filepath
        ## run_full(file_dir)
        return{'FINISHED'}


class RunCreateArmature(Operator):
    """Create a base armature for motion capture"""
    bl_idname = "run.create_armature"
    bl_label = "Select Video File"
        
    def create_armature(self) :

    
        if (bpy.ops.object.armature["BlindPoseArmature"])
            return 

        # create new armature
        bpy.ops.object.armature_add(enter_editmode=False)
        # obtaine selected object
        armature = bpy.context.object
        # rename armature 
        armature.name = "BlindPoseArmature"
            
        # switch in edit mode
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        # rename first bone
        armature.data.bones[0].name = "Head"
        
    
        for id, lm in enumerate(self.body_point()):
            eb = armature.data.edit_bones.new("Bone_" + str(id))
            eb.parent = armature.data.edit_bones["Head"]
            cx, cy, cz = lm.x * 4, lm.y, lm.z
            eb.head = (cz, cx, cy) # if the head and tail are the same, the bone is deleted
            eb.tail = (cz + 1, cx, cy) # upon returning to object mode
        
        
        obj = bpy.context.object
        
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        

    def body_point(self)
        # https://developers.google.com/mediapipe/solutions/vision/pose_landmarker
        return [
            'nose',
            'left eye inner',
            'left eye',
            'left eye outer',
            'right eye inner',
            'right eye',
            'right eye outer',
            'left ear',
            'right ear',
            'mouth left',
            'mouth right',
            'left shoulder',
            'right shoulder',
            'left elbow',
            'right elbow',
            'left wrist',
            'right wrist',
            'left pinky',
            'right pinky',
            'left index',
            'right index',
            'left thumb',
            'right thumb',
            'left hip',
            'right hip',
            'left knee',
            'right knee',
            'left ankle',
            'right ankle',
            'left heel',
            'right heel',
            'left foot index',
            'right foot index'
        ]

        
    def execute(self, context):
        
        self.create_armature()
        ## run_full(file_dir)
        return{'FINISHED'}

        



class PanelInterface(Panel):
    bl_idname = "VIEW3D_PT_Pose" # Notice the ‘CATEGORY_PT_name’ Panel.bl_idname, this is a naming convention for panels.
    bl_label = "My Blind Pose" # title on the panel tools
    bl_category = "BlindPose" # text on tab
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI'

    def draw(self, context):

        settings = context.scene.blindPoseSettings
        layout = self.layout

        layout.row().operator(RunCreateArmature.bl_idname, text="Armature", icon='MOD_ARMATURE')
        layout.row().operator(RunCapture.bl_idname, text="Capture")
#        layout.row().operator(RunFileSelector.bl_idname, text="From file")

        box = layout.box()
        column_flow = box.column_flow()
        column = column_flow.column(align=True)
        column.label(text="Capture Mode:", icon='MOD_ARMATURE')
        column.prop(settings, 'body_tracking', text='Body', icon='ARMATURE_DATA')
#        column.prop(settings, 'hand_tracking', text='Hands', icon='VIEW_PAN')
        column.prop(settings, 'face_tracking', text='Face', icon='MONKEY')



_classes = [
    RunFileSelector,
    RunCapture,
    RunCreateArmature,
    PanelInterface
]


# start registring class in blender
def register():
    
    bpy.utils.register_class(BlindPoseSettings)

    # subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "mediapipe"])
    for c in _classes: 
        try:
            bpy.utils.register_class(c)
        except RuntimeError:
            pass
    
    # add settings to Scene
    bpy.types.Scene.blindPoseSettings = bpy.props.PointerProperty(type=BlindPoseSettings)

        


def unregister():
    for c in _classes: 
        try:
            bpy.utils.unregister_class(c)
        except RuntimeError:
            pass
    


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    unregister()
    register()