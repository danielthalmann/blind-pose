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


def look_rotation(source, target, upwards = mathutils.Vector((0,0,1))):

    forward = target - source
    
    forward = forward.normalized()
    upwards = upwards.normalized()
    
    right = forward.cross(upwards).normalized()
    up = right.cross(forward)
    
    return mathutils.Matrix([right, forward, up]).transposed().to_euler()




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
                    try:
                        bones.get(points[id]).location.y = lm.z / 4
                        bones.get(points[id]).location.x = (0.5-lm.x) * 2 
                        bones.get(points[id]).location.z = ((0.2-lm.y) + 2 ) * 2
                        # bones.get(points[id]).keyframe_insert(data_path="location", frame=n)
                    except:
                        pass


            cv2.imshow("frame", frame)

            # the space ' ' button is set as the 
            # quitting button you may use any 
            # desired button of your choice 
            if cv2.waitKey(1) & 0xFF == ord(' '): 
                break
        

            n = n + 1
                       
            bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=2)
            

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

        import numpy as np
        frame = np.zeros((100,100,3), dtype=np.uint8)
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mpPose = mp.solutions.pose
        pose = mpPose.Pose()
        results = pose.process(imgRGB)
        print(results.pose_landmarks)
        if results.pose_landmarks:
            print (results.pose_landmarks )
                
        try:
            # switch in object mode
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        except:
            pass
        
        
        try:
            bpy.data.objects['BlindPoseArmature']
            return
        except KeyError:
            pass
                # create new armature
        bpy.ops.object.armature_add(enter_editmode=False)
        # obtaine selected object
        armature = bpy.context.object
        armature.select_set(True)

        bpy.context.object.data.display_type = 'STICK'


        # rename armature 
        armature.name = "BlindPoseArmature"

        # armature.dsplay_type = 'STICK'
        
        armature.data.name = "BlindPoseBody"

        # switch in edit mode
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

        # rename first bone
        armature.data.bones[0].name = "nose"
        
        #   bone = bpy.context.active_object.data.edit_bones["nose"]
        #   bone.tail.x = 0
        #   bone.tail.y = 0
        #   bone.tail.z = 0
        #   bone.head = bone.tail
        #   bone.head.y = 0.3
        #root = armature.data.bones[0]

        # add bones
        #self.add_bone(None, 'nose', (0, 0, 0))
        self.add_bone(None, 'nose',                      (0, 0.01, 0))

        self.add_bone(None, 'left eye',                  (0, 0.01, 0))
        self.add_bone(None, 'left eye inner',            (0, 0.02, 0))
        self.add_bone(None, 'left eye outer',            (0, 0.03, 0))
        
        self.add_bone(None, 'right eye',                 (0, 0.04, 0))
        self.add_bone(None, 'right eye inner',           (0, 0.04, 0))
        self.add_bone(None, 'right eye outer',           (0, 0.06, 0))
        
        self.add_bone(None, 'left ear',                  (0, 0.07, 0))
        self.add_bone(None, 'right ear',                 (0, 0.07, 0))
        
        self.add_bone(None, 'mouth left',                (0, 0.09, 0))
        self.add_bone(None, 'mouth right',               (0, 0.10, 0))

        shoulder = self.add_bone(None, 'left shoulder',  (0, 0.11, 0))
        elbow = self.add_bone(shoulder, 'left elbow',    (0, 0.12, 0))
        wrist = self.add_bone(elbow, 'left wrist',       (0, 0.13, 0))
        self.add_bone(wrist, 'left pinky',               (0, 0.14, 0))
        self.add_bone(wrist, 'left index',               (0, 0.15, 0))
        self.add_bone(wrist, 'left thumb',               (0, 0.16, 0))
        
        hip   = self.add_bone(None , 'left hip',         (-0.1, 0.17, 0))
        knee  = self.add_bone(hip  , 'left knee',        (-0.1, 0.18, 0))
        ankle = self.add_bone(knee , 'left ankle',       (-0.1, 0.19, 0))
        heel  = self.add_bone(ankle, 'left heel',        (-0.1, 0.21, 0))
        foot  = self.add_bone(ankle, 'left foot index',  (-0.1, 0.22, 0))
        
        
        shoulder = self.add_bone(None, 'right shoulder', (0, 0.23, 0))
        elbow = self.add_bone(None, 'right elbow',       (0, 0.24, 0))
        wrist = self.add_bone(None, 'right wrist',       (0, 0.25, 0))
        self.add_bone(None, 'right pinky',               (0, 0.26, 0))
        self.add_bone(None, 'right index',               (0, 0.27, 0))
        self.add_bone(None, 'right thumb',               (0, 0.28, 0))
        
        hip   = self.add_bone(None , 'right hip',        (0.1, 0.17, 0))
        knee  = self.add_bone(hip  , 'right knee',       (0.1, 0.18, 0))
        ankle = self.add_bone(knee , 'right ankle',      (0.1, 0.19, 0))
        heel  = self.add_bone(ankle, 'right heel',       (0.1, 0.21, 0))
        foot  = self.add_bone(ankle, 'right foot index', (0.1, 0.22, 0))        

        obj = bpy.context.object
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


    def add_bone(self, parent, bone_name, vect):

        bpy.ops.armature.bone_primitive_add(name=bone_name)
        bone = bpy.context.active_object.data.edit_bones[bone_name]
        
        bone.tail.x = vect[0]
        bone.tail.y = vect[1]
        bone.tail.z = vect[2]
        
        if parent != None :
            print ("parent")
            print (parent)
            bone.use_connect = True
            bone.parent = parent
        else :
            bone.head = bone.tail
            bone.head.y = vect[1] + 0.3
                
        return bone
        
    def execute(self, context):
        
        self.create_armature()
        ## run_full(file_dir)
        return{'FINISHED'}


class RunTestArmature(Operator):
    """Test armature for motion capture"""
    bl_idname = "run.test_armature"
    bl_label = "Test armature"
  
    def execute(self, context):
        
        mobile = bpy.data.objects["Cube"]
        cible  = bpy.data.objects["Cible"]

        mobile.rotation_euler = look_rotation(mobile.location, cible.location)

#        v = lookAt(mobile.location, cible.location)
        
#        mobile.rotation_mode = 'XYZ'
#        mobile.rotation_euler = (v[0], v[1], v[2])
        
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
        layout.row().operator(RunTestArmature.bl_idname, text="Test")
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
    RunTestArmature,
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