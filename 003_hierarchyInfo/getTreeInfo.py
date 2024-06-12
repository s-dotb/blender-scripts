import bpy

def get_parent_name(obj):
    """Returns the name of the parent object if it exists."""
    return obj.parent.name if obj.parent else "No parent"

def collect_children_names(obj, children_names=None):
    """Recursively collects the names of all children of the given object."""
    if children_names is None:
        children_names = []
    
    for child in obj.children:
        children_names.append(child.name)
        collect_children_names(child, children_names)  # Recursive call
    
    return children_names

def print_hierarchy_info(obj):
    """Prints the parent name and all children's names of the given object."""
    parent_name = get_parent_name(obj)
    children_names = collect_children_names(obj)
    
    print(f"Parent Name: {parent_name}")
    print(f"Children Names: {children_names}")

def main():
    """Main function to execute the hierarchy information retrieval."""
    active_object = bpy.context.view_layer.objects.active
    if active_object:
        print_hierarchy_info(active_object)
    else:
        print("No active object selected.")

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
