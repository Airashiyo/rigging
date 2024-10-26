import maya.cmds as cmds

# Pre-defined list of bone names (replace with actual bone names in your scene)
bone_list = ["center_01", "right_01", "left_00"]  # Example bone names




# Function to create two NURBS circles and add control_tag attributes to their shape nodes
def create_and_tag_circles():
    # Create two NURBS circles
    circle1 = cmds.circle(name="circle1", normal=(0, 1, 0))[0]  # First circle facing Y-axis
    circle2 = cmds.circle(name="circle2", normal=(0, 1, 0))[0]  # Second circle, initially same orientation

    # Rotate the second circle by 90 degrees on the X-axis
    cmds.rotate(90, 0, 0, circle2)

    # Freeze transformations on the rotated circle to bake the rotation into its shape
    cmds.makeIdentity(circle2, apply=True, rotate=True)

    # Get the shape nodes for both circles
    shapes1 = cmds.listRelatives(circle1, shapes=True, fullPath=True)
    shapes2 = cmds.listRelatives(circle2, shapes=True, fullPath=True)

    # Add "control_tag" attribute to each shape node if it's a NURBS shape
    for shape in shapes1 + shapes2:
        if cmds.objectType(shape) == "nurbsCurve":
            # Set the line width to 2
            cmds.setAttr(f"{shape}.lineWidth", 2)

            if not cmds.attributeQuery("control_tag", node=shape, exists=True):
                cmds.addAttr(shape, longName="control_tag", dataType="string", keyable=True)
                cmds.setAttr(f"{shape}.control_tag", "control_shape", type="string")

    # Re-parent the shape of circle2 under circle1
    circle2_shape = shapes2[0]
    cmds.parent(circle2_shape, circle1, shape=True, relative=True)

    # Clean up by deleting the now-empty transform of circle2
    cmds.delete(circle2)

    # Rename the combined result for clarity
    combined_circle = cmds.rename(circle1, "combinedCircle")

    return combined_circle




# Main function to process predefined bones
def addControls(*args):  # Accept one or more arguments
    # Iterate over each bone in the predefined list
    for target in bone_list:
        if not cmds.objExists(target):
            cmds.warning(f"{target} does not exist in the scene.")
            continue

        # Create the combined circles
        combined_circle = create_and_tag_circles()

        # Get the shapes under the combined circle
        shapes = cmds.listRelatives(combined_circle, shapes=True, fullPath=True)

        if shapes:
            # Check if there are existing NURBS curves under the target
            existing_shapes = cmds.listRelatives(target, shapes=True, fullPath=True) or []
            existing_nurbs = [s for s in existing_shapes if cmds.objectType(s) == "nurbsCurve"]

            # Only parent new shapes if there are no existing NURBS curves
            if not existing_nurbs:
                for shape in shapes:
                    cmds.parent(shape, target, shape=True, relative=True)
                cmds.warning(f"Shapes parented under {target}.")
            else:
                cmds.warning(f"Not parenting shapes under {target} because existing NURBS curves are present.")

            # Clean up the now-empty combined circle transform
            cmds.delete(combined_circle)
        else:
            cmds.warning(f"No shapes found in the created combined circle for target {target}.")




# Function to delete all NURBS curve shapes with the control_tag attribute
def delete_curves_with_control_tag(*args):
    # Get all shape nodes in the scene
    all_shapes = cmds.ls(type="nurbsCurve", long=True)  # List all NURBS curve shapes

    # Iterate over all shapes and check for the control_tag attribute
    for shape in all_shapes:
        if cmds.attributeQuery("control_tag", node=shape, exists=True):
            # Delete the shape node
            cmds.delete(shape)
            print(f"Deleted shape: {shape}")




# Function to create a simple Maya window with text
def create_revRigUI():
    # Check if the window already exists and delete it if it does
    if cmds.window("revRigWindow", exists=True):
        cmds.deleteUI("revRigWindow")

    # Create a new window
    window = cmds.window("revRigWindow", title="Reverse Rig", widthHeight=(500, 350), sizeable=False)

    # Create a layout for the window
    cmds.columnLayout(adjustableColumn=True)

    # Add a text label
    cmds.text(label="Hello, this is a simple Maya window!")

    # Creating button_insertTargetChain
    button_addControls = cmds.button(label='Generate', w=35, h=25, command=addControls)

    # Creating button_insertTargetChain
    button_deleteControls = cmds.button(label='Scrub Shapes', w=35, h=25, command=delete_curves_with_control_tag)

    # Show the window
    cmds.showWindow(window)

# Run the function to create the window
create_revRigUI()
