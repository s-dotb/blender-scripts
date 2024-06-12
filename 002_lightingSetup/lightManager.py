bl_info = {
    "name": "Basic Lighting Setup",
    "blender": (3, 0, 0),
    "category": "Lighting",
}

import bpy
from bpy.props import EnumProperty

# Define the EnumProperty outside the class
light_type_items = [
    ('POINT', 'Point', 'Add a point light'),
    ('SPOT', 'Spot', 'Add a spot light'),
    ('SUN', 'Sun', 'Add a sun light'),
    ('AREA', 'Area', 'Add an area light')
]

# Operator class to add a light
class AddLightOperator(bpy.types.Operator):
    bl_idname = "light.add_light"  # Unique identifier for the operator
    bl_label = "Add Light"  # Display name in the UI
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operation

    # Property to choose the type of light to add
    light_type: EnumProperty(
        name="Light Type",
        description="Type of light to add",
        items=light_type_items,
        default='POINT'  # Default light type
    )

    # Function to execute the operator
    def execute(self, context):
        bpy.ops.object.light_add(type=self.light_type)  # Add the selected type of light
        return {'FINISHED'}  # Indicate successful completion

# Panel class to manage lights
class LightManagerPanel(bpy.types.Panel):
    bl_label = "Light Manager"  # Panel label in the UI
    bl_idname = "LIGHT_PT_manager"  # Unique identifier for the panel
    bl_space_type = 'VIEW_3D'  # Panel location: 3D View
    bl_region_type = 'UI'  # Panel region: UI
    bl_category = 'Lighting'  # Tab category

    # Function to draw the panel UI
    def draw(self, context):
        layout = self.layout  # Define the layout of the panel
        self.draw_light_buttons(layout)  # Draw buttons to add lights
        self.draw_light_properties(layout, context.object)  # Draw properties for selected light

    # Function to draw buttons to add different types of lights
    def draw_light_buttons(self, layout):
        row = layout.row()
        row.operator('light.add_light', text="Add Point Light").light_type = 'POINT'
        row.operator('light.add_light', text="Add Spot Light").light_type = 'SPOT'
        row.operator('light.add_light', text="Add Sun Light").light_type = 'SUN'
        row.operator('light.add_light', text="Add Area Light").light_type = 'AREA'

    # Function to draw properties of the selected light
    def draw_light_properties(self, layout, obj):
        if obj and obj.type == 'LIGHT':  # Check if the selected object is a light
            light = obj.data  # Get the light data
            col = layout.column()  # Create a column layout
            col.prop(obj, "location")  # Add control for light location
            col.prop(obj, "rotation_euler", text="Rotation")  # Add control for light rotation
            col.prop(obj, "scale", text="Scale")  # Add control for light scale
            col.prop(light, "color", text="Color")  # Add control for light color
            col.prop(light, "energy", text="Intensity")  # Add control for light intensity
            
            if light.type == 'SPOT':  # Additional properties for spotlights
                col.prop(light, "spot_size", text="Spot Size")  # Control for spot size
                col.prop(light, "spot_blend", text="Spot Blend")  # Control for spot blend

# List of classes to register
classes = [AddLightOperator, LightManagerPanel]

# Function to register classes
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

# Function to unregister classes
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

# Main check to run the register function
if __name__ == "__main__":
    register()
