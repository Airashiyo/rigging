import maya.cmds as cmds


def get_immediate_children():
    """
    Get immediate children of the given joint that are also joints.
    Returns a list of immediate children.
    """
    sel = cmds.ls(selection=True, type="joint", long=True)
    chainParent = cmds.listRelatives(sel, children=True, type='joint', fullPath=True)
    chainParent = chainParent[0] if chainParent else None

    jointName = chainParent[0].rsplit("|", 1)[-1]
    children = []

    for jointName in sel:  # // for loop start that targets every "joint" within the selection ("selection" is referenced at the bottom)
        children.append(jointName)  # // adds the selected joints into a list under the given name
        relatives_paths = cmds.listRelatives(jointName, allDescendents=True, type="joint",
                                             fullPath=True)  # // finds the entire hierarchy of the object, has to be a joint.
        if relatives_paths:
            relatives_paths.reverse()  # // reverses the hierarchy cus maya is a retard that starts with the egg
            children.extend(
                relatives_paths)


    return children



def populate_tree_view(tree_view, parent_joint):
    """
    Populate the tree view widget with the immediate children of the parent_joint.
    """
    # Clear existing items in the tree view
    cmds.treeView(tree_view, edit=True, removeAll=True)

    # Get immediate children of the parent_joint
    children = get_immediate_children(parent_joint)

    # Add each child to the tree view
    for child in children:
        cmds.treeView(tree_view, edit=True, addItem=(child, parent_joint))


def create_joint_hierarchy_ui():
    """
    Create a UI window with a tree view displaying the immediate children of a selected joint.
    """
    # Check if the window already exists
    if cmds.window("jointHierarchyWindow", exists=True):
        cmds.deleteUI("jointHierarchyWindow", window=True)

    # Create a new window
    window = cmds.window("jointHierarchyWindow", title="Joint Hierarchy", widthHeight=(300, 400))
    cmds.columnLayout(adjustableColumn=True)

    # Create the tree view widget
    tree_view = cmds.treeView(allowMultiSelection=False, numberOfButtons=0, abr=True)

    # Get the selected joint
    selected_joint = cmds.ls(selection=True, type='joint')
    if not selected_joint:
        cmds.warning("Please select a joint to display its immediate children.")
        return

    selected_joint = selected_joint[0]

    # Populate the tree view with the immediate children of the selected joint
    populate_tree_view(tree_view, selected_joint)

    # Show the window
    cmds.showWindow(window)

jointChildren = get_immediate_children(joint)

# Example usage
create_joint_hierarchy_ui()
