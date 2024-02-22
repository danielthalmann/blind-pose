from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator

class RunFileSelector(Operator, ImportHelper):
    bl_idname = "run.capture_from_file"
    bl_label = "Select Video File"
    filename_ext = ""

    def execute(self, context):
        file_dir = self.properties.filepath
        ## run_full(file_dir)
        return{'FINISHED'}