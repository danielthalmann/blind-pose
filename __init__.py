import bpy
import mathutils
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

        try:
            armature = bpy.data.objects['BlindPoseArmature']
            armature.select_set(True)
        except KeyError:
            return

        # switch in pose mode
        bpy.ops.object.mode_set(mode='POSE', toggle=False)

        bones = bpy.context.object.pose.bones
        
        vid = cv2.VideoCapture(0)
        mpPose = mp.solutions.pose
        mpDraw = mp.solutions.drawing_utils
        pose = mpPose.Pose()

        # img = cv2.imread("p:\\3D\\wall.png")


        points = self.body_points()
        n = 0

        while (True):
            
            ret, frame = vid.read() 
            frame = cv2.flip(frame, 1)
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)

            if results.pose_landmarks:
                mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    #try:
                    bones.get(points[id]).location.y = lm.z / 4
                    bones.get(points[id]).location.x = (0.5-lm.x)
                    bones.get(points[id]).location.z = (0.2-lm.y) + 2
                        #bones[points[id]].keyframe_insert(data_path="location", frame=n)
                    #except:
                    #    pass


            cv2.imshow("frame", frame)

            # the space ' ' button is set as the 
            # quitting button you may use any 
            # desired button of your choice 
            if cv2.waitKey(1) & 0xFF == ord(' '): 
                break
        

            n = n + 1
                       
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            

        vid.release()

        cv2.destroyAllWindows()


    def body_points(self):
        # https://developers.google.com/mediapipe/solutions/vision/pose_landmarker
        return [
            # head
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
            # body,
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

    
        try:
            bpy.data.objects['BlindPoseArmature']
            return
        except KeyError:
            pass
        
        # create new armature
        bpy.ops.object.armature_add(enter_editmode=False)
        # obtaine selected object
        armature = bpy.context.object
        # rename armature 
        armature.name = "BlindPoseArmature"

        # armature.dsplay_type = 'STICK'
        
        armature.data.name = "BlindPoseBody"

        # switch in edit mode
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

        # rename first bone
        armature.data.bones[0].name = "head"
        root = bpy.context.active_object.data.edit_bones["head"]
        #root = armature.data.bones[0]

        # add bones
        self.add_bone(None, 'nose', (0.0, 5.0, 0.0))

        left_eye = self.add_bone(None, 'left eye', (-2.5, 7.0, -0.1))
        self.add_bone(left_eye, 'left eye inner', (-1.5, 7.0, -0.1))
        self.add_bone(left_eye, 'left eye outer', (-3.5, 7.0, -0.1))
        
        right_eye = self.add_bone(None, 'right eye', (2.5, 7.0, -0.1))
        self.add_bone(right_eye, 'right eye inner', (1.5, 7.0, -0.1))
        self.add_bone(right_eye, 'right eye outer', (3.5, 7.0, -0.1))
        
        self.add_bone(None, 'left ear', (-5.0, 6.5, -0.1))
        self.add_bone(None, 'right ear', (5.0, 6.5, -0.1))
        
        self.add_bone(None, 'mouth left', (-1.5, 3.0, -0.1))
        self.add_bone(None, 'mouth right', (1.5, 3.0, -0.1))

        self.add_bone(None, 'left shoulder', (0, 0, 0))
        self.add_bone(None, 'right shoulder', (0, 0, 0))
        self.add_bone(None, 'left elbow', (0, 0, 0))
        self.add_bone(None, 'right elbow', (0, 0, 0))
        self.add_bone(None, 'left wrist', (0, 0, 0))
        self.add_bone(None, 'right wrist', (0, 0, 0))
        self.add_bone(None, 'left pinky', (0, 0, 0))
        self.add_bone(None, 'right pinky', (0, 0, 0))
        self.add_bone(None, 'left index', (0, 0, 0))
        self.add_bone(None, 'right index', (0, 0, 0))
        self.add_bone(None, 'left thumb', (0, 0, 0))
        self.add_bone(None, 'right thumb', (0, 0, 0))
        self.add_bone(None, 'left hip', (0, 0, 0))
        self.add_bone(None, 'right hip', (0, 0, 0))
        self.add_bone(None, 'left knee', (0, 0, 0))
        self.add_bone(None, 'right knee', (0, 0, 0))
        self.add_bone(None, 'left ankle', (0, 0, 0))
        self.add_bone(None, 'right ankle', (0, 0, 0))
        self.add_bone(None, 'left heel', (0, 0, 0))
        self.add_bone(None, 'right heel', (0, 0, 0))
        self.add_bone(None, 'left foot index', (0, 0, 0))
        self.add_bone(None, 'right foot index', (0, 0, 0))        

        obj = bpy.context.object
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


    def add_bone(self, parent, bone_name, vect):

        bpy.ops.armature.bone_primitive_add(name=bone_name)
        bone = bpy.context.active_object.data.edit_bones[bone_name]
        bone.tail.x = vect[0]
        bone.tail.y = vect[2]
        bone.tail.z = vect[1]
        bone.head = bone.tail
        bone.head.y = vect[2] + 0.3
        if parent != None :
            bone.head = parent.tail
            bone.parent = parent
        return bone
        
    def execute(self, context):
        
        self.create_armature()
        ## run_full(file_dir)
        return{'FINISHED'}

        



class PanelInterface(Panel):
    bl_idname = "VIEW3D_PT_Pose" # Notice the �CATEGORY_PT_name� Panel.bl_idname, this is a naming convention for panels.
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
#        column.prop(settings, 'face_tracking', text='Face', icon='MONKEY')



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