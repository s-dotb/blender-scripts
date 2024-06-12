"""
This script provides functions to calculate the center of an object based on the centers of its mesh children and place an empty object at the calculated center for visualization.

Functions:
- calculate_center_of_object(obj): Calculate the center of an object based on the centers of its mesh children.
- place_empty_at_center(name, location): Place an empty object at the specified location for visualization.
- main(): Main function to execute the script.
"""
import bpy
import mathutils

import bpy
import mathutils

def calculate_center_of_object(obj):
    """
    Calculate the center of an object based on the centers of its mesh children.
    
    :param obj: The parent object.
    :type obj: bpy.types.Object
    :return: The center of the object.
    :rtype: mathutils.Vector
    """
    if not obj.children:
        return obj.location

    total_location = mathutils.Vector((0.0, 0.0, 0.0))
    mesh_count = 0

    for child in obj.children:
        if child.type == 'MESH':
            total_location += child.location
            mesh_count += 1
        else:
            # Recursively handle non-mesh children
            child_center = calculate_center_of_object(child)
            if child_center:
                total_location += child_center
                mesh_count += 1

    if mesh_count > 0:
        return total_location / mesh_count
    else:
        return obj.location

def place_empty_at_center(name, location):
    """
    Place an empty object at the specified location for visualization.
    
    :param name: The name of the new empty object.
    :type name: str
    :param location: The location to place the empty object.
    :type location: mathutils.Vector
    """
    empty = bpy.data.objects.new(name, None)
    empty.location = location
    bpy.context.collection.objects.link(empty)

def main():
    """
    Main function to execute the script.
    """
    selected_objects = bpy.context.selected_objects

    for obj in selected_objects:
        if obj.type == 'EMPTY':
            center = calculate_center_of_object(obj)
            print(f'Center of object "{obj.name}" is at: {center}')
            place_empty_at_center(f"{obj.name}_center", center)

if __name__ == "__main__":
    main()
