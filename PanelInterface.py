from bpy.types import Panel

class PanelInterface(Panel):
    bl_idname = "VIEW3D_PT_Pose" # Notice the ‘CATEGORY_PT_name’ Panel.bl_idname, this is a naming convention for panels.
    bl_label = "My Blind Pose"
    bl_category = "BlindPose"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):

        settings = context.scene.settings
        layout = self.layout

        row = layout.row()
        row.operator("mesh.primitive_cube_add", text="add cube")

        box = layout.box()
        column_flow = box.column_flow()
        column = column_flow.column(align=True)
        column.label(text="Capture Mode:", icon='MOD_ARMATURE')
        column.prop(settings, 'body_tracking', text='Body', icon='ARMATURE_DATA')
        column.prop(settings, 'hand_tracking', text='Hands', icon='VIEW_PAN')
        column.prop(settings, 'face_tracking', text='Face', icon='MONKEY')

