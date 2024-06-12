import bpy
import os
import random

# Path to the folder containing textures
texture_folder = "//path_to_your_texture_folder/"  # Replace with your folder path

# Function to create a new material with random color and a specific texture
def create_material(texture_path):
    mat = bpy.data.materials.new(name=os.path.basename(texture_path))
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    
    # Random color
    color = (random.random(), random.random(), random.random(), 1)
    bsdf.inputs['Base Color'].default_value = color
    
    # Add texture
    tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex_image.image = bpy.data.images.load(texture_path)
    mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])
    
    return mat

# Get the list of textures
texture_files = [f for f in os.listdir(bpy.path.abspath(texture_folder)) if f.endswith(('.png', '.jpg', '.jpeg', '.tga', '.bmp'))]
texture_paths = [os.path.join(bpy.path.abspath(texture_folder), f) for f in texture_files]

# Ensure there are enough textures for all instances
if len(texture_paths) < 16:
    raise ValueError("Not enough textures in the specified folder")

# Get the selected object
selected_obj = bpy.context.selected_objects[0]

# Set grid size
grid_size = 4
spacing = 2

# Shuffle the texture paths to ensure random assignment
random.shuffle(texture_paths)

# Iterate over the grid positions
for row in range(grid_size):
    for col in range(grid_size):
        # Duplicate the object
        new_obj = selected_obj.copy()
        new_obj.data = selected_obj.data.copy()
        new_obj.animation_data_clear()
        
        # Set the new object's location
        new_obj.location = (col * spacing, row * spacing, 0)
        
        # Create and assign a new material with a unique texture
        texture_path = texture_paths.pop()
        material = create_material(texture_path)
        if new_obj.data.materials:
            new_obj.data.materials[0] = material
        else:
            new_obj.data.materials.append(material)
        
        # Link the new object to the collection
        bpy.context.collection.objects.link(new_obj)
