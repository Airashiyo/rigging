import maya.cmds as cmds


def create_ui():
    if cmds.window("skinWeightWindow", exists=True):
        cmds.deleteUI("skinWeightWindow")

    cmds.window("skinWeightWindow", title="Skin Weight Tool", widthHeight=(300, 100))
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label="Enter Joint Name:")
    text_field = cmds.textField("jointNameField")
    cmds.button(label="Search", command=lambda x: search_joints(text_field))
    cmds.showWindow("skinWeightWindow")


def search_joints(text_field):
    joint_name = cmds.textField(text_field, query=True, text=True)
    matching_joints = find_matching_joints(skin_weights, joint_name)
    print("Matching joints:")
    for joint in matching_joints:
        print(joint)


def find_matching_joints(weights_dict, joint_name):
    return [joint for joint in weights_dict.keys() if joint_name in joint]


# Example dictionary containing skin cluster vertex weights
skin_weights = {
    "joint1": [0.1, 0.2, 0.3],
    "joint2": [0.4, 0.5, 0.6],
    "joint3": [0.7, 0.8, 0.9],
    # Add more data as needed
}

# Create the UI
create_ui()