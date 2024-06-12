bl_info = {
    "name": "Export Models as FBX",
    "blender": (2, 80, 0),
    "category": "Import-Export",
}

import bpy
from bpy.props import StringProperty
from bpy.types import Operator, Panel, AddonPreferences
from bpy_extras.io_utils import ExportHelper

class ExportSettings(AddonPreferences):
    bl_idname = __name__
    
    default_path: StringProperty(
        name="Default Export Path",
        subtype='DIR_PATH',
        default="//"
    )
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "default_path")

class ExportModelOperator(Operator, ExportHelper):
    bl_idname = "export_model.fbx"
    bl_label = "Export Model as FBX"
    
    filename_ext = ".fbx"
    
    filter_glob: StringProperty(
        default="*.fbx",
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        return bpy.ops.export_scene.fbx(filepath=self.filepath)
    
class ExportModelPanel(Panel):
    bl_idname = "VIEW3D_PT_export_model"
    bl_label = "Export Model"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Export'
    
    def draw(self, context):
        layout = self.layout
        layout.operator(ExportModelOperator.bl_idname, text="Export Model as FBX")

def menu_func_export(self, context):
    self.layout.operator(ExportModelOperator.bl_idname, text="Export Model as FBX")

def register():
    bpy.utils.register_class(ExportSettings)
    bpy.utils.register_class(ExportModelOperator)
    bpy.utils.register_class(ExportModelPanel)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.context.preferences.addons[__name__].preferences

def unregister():
    bpy.utils.unregister_class(ExportSettings)
    bpy.utils.unregister_class(ExportModelOperator)
    bpy.utils.unregister_class(ExportModelPanel)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
