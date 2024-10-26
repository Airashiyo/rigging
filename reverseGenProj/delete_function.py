import maya.cmds as cmds

# Function to delete all NURBS curve shapes with the control_tag attribute
def delete_curves_with_control_tag():
    # Get all shape nodes in the scene
    all_shapes = cmds.ls(type="nurbsCurve", long=True)  # List all NURBS curve shapes

    # Iterate over all shapes and check for the control_tag attribute
    for shape in all_shapes:
        if cmds.attributeQuery("control_tag", node=shape, exists=True):
            # Delete the shape node
            cmds.delete(shape)
            print(f"Deleted shape: {shape}")

# Run the function to delete the curves
delete_curves_with_control_tag()
