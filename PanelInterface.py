from bpy.types import Panel
#from .Operators.RunFileSelector import RunFileSelector

class PanelInterface(Panel):
    bl_label = "Blind Pose"
    bl_category = "BlindPose"
    bl_idname = "VIEW3D_blindpose_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):

        settings = context.scene.blindposesettings
        layout = self.layout

        box = layout.box()
        column_flow = box.column_flow()
        column = column_flow.column(align=True)
        column.label(text="Capture Mode:", icon='MOD_ARMATURE')
        column.prop(settings, 'body_tracking', text='Body', icon='ARMATURE_DATA')
        column.prop(settings, 'hand_tracking', text='Hands', icon='VIEW_PAN')
        column.prop(settings, 'face_tracking', text='Face', icon='MONKEY')



    #    box = layout.box()
    #    column_flow = box.column_flow()
    #    column = column_flow.column(align=True)
    #    column.label(text="Process from file:", icon='FILE_MOVIE')
    #    column.operator(RunFileSelector.bl_idname, text="Load Video File", icon='FILE_BLANK')

