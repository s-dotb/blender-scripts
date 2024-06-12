import bpy
import json
import os
import math

# Define a helper function to get object data
def get_object_data(obj):
    return {
        'name': obj.name,
        'location': list(obj.location),
        'rotation': [math.degrees(angle) for angle in obj.rotation_euler],  # Manually convert radians to degrees
        'scale': list(obj.scale),
        'parent_name': obj.parent.name if obj.parent else None,
        'children_count': len(obj.children)
    }

# Define the operator class
class OBJECT_OT_ExportSelectedToJSON(bpy.types.Operator):
    bl_idname = "object.export_selected_to_json"
    bl_label = "Export Selected to JSON"
    bl_description = "Export data of selected objects to a JSON file"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        selected_objects = context.selected_objects
        data = [get_object_data(obj) for obj in selected_objects]
        
        # Write the data to the JSON file
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)
        
        self.report({'INFO'}, f"Data exported to {self.filepath}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Define the panel class
class OBJECT_PT_CustomPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_custom_panel"
    bl_label = "Export Selected Objects"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'
    
    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_ExportSelectedToJSON.bl_idname)

# Registration
classes = [OBJECT_OT_ExportSelectedToJSON, OBJECT_PT_CustomPanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass

if __name__ == "__main__":
    unregister()
    register()
