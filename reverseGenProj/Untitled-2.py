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
def main():
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
            # Parent each shape of the combined circle under the target transform (bone)
            for shape in shapes:
                cmds.parent(shape, target, shape=True, relative=True)
            
            # Clean up the now-empty combined circle transform
            cmds.delete(combined_circle)
        else:
            cmds.warning(f"No shapes found in the created combined circle for target {target}.")

# Run the main function
main()
