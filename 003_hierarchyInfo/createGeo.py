import bpy
import random

def create_random_object(name, location=(0, 0, 0)):
    """Creates a random mesh object with a given name and location."""
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    return obj

def create_complex_hierarchy(base_name, levels, children_per_level):
    """Creates a complex hierarchy of objects."""
    def create_children(parent, level):
        if level >= levels:
            return
        
        for i in range(children_per_level):
            child_name = f"{parent.name}_Child{level}_{i}"
            child_location = (
                parent.location.x + random.uniform(-2, 2),
                parent.location.y + random.uniform(-2, 2),
                parent.location.z - 2
            )
            child = create_random_object(child_name, child_location)
            child.parent = parent
            create_children(child, level + 1)
    
    root = create_random_object(base_name)
    create_children(root, 1)

def main():
    # Clear existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Create a complex hierarchy
    base_name = "Root"
    levels = 4  # Number of levels deep
    children_per_level = 3  # Number of children per level
    
    create_complex_hierarchy(base_name, levels, children_per_level)
    
    # Run the provided script to find parent and list children
    def get_parent_name(obj):
        if obj.parent:
            return obj.parent.name
        else:
            return "No parent"

    def get_all_children(obj, children_list=None):
        if children_list is None:
            children_list = []
        
        for child in obj.children:
            children_list.append(child.name)
            get_all_children(child, children_list)
        
        return children_list

    if bpy.context.active_object:
        active_object = bpy.context.active_object
        parent_name = get_parent_name(active_object)
        print(f"Parent Name: {parent_name}")
        children_names = get_all_children(active_object)
        print(f"Children Names: {children_names}")
    else:
        print("No active object selected.")

# Run the main function
if __name__ == "__main__":
    main()
