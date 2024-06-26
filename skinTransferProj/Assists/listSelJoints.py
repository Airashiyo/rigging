import maya.cmds as cmds


def listSelJoints():
    sel = cmds.ls(selection=True, type="joint")
    jointHierarchy = cmds.listRelatives(sel, type="joint", allDescendents=True)
    # creating an empty list
    wholeHierarchy = []

    # adding joints found through the relatives command to the list.
    wholeHierarchy.extend(jointHierarchy)
    # adding the selection itself, because listRelatives excludes the selection.
    wholeHierarchy.extend(sel)
    # reversing the list
    wholeHierarchy.reverse()

    #jointAmount = len(wholeHierarchy)

    return wholeHierarchy


def sortThroughJoints(*args):
    rawList = listSelJoints()




# def uiWindow():
#     # kill window if it already exists
#     if cmds.window("treeViewWin", exists=True):
#         cmds.deleteUI("treeViewWin")
#
#     # build window bozo
#     toolWindow = cmds.window("treeViewWin", t="Joint Tree", w=350, h=450, sizeable=False,
#                              minimizeButton=True, maximizeButton=True)
#
#     # setting window layout, form type
#     # create tabLayout
#     layout = cmds.formLayout()
#
#     treeControl = cmds.treeView(parent=layout, abr=False)
#     joint = "layer lol"
#
#     bozo = listSelJoints()
#
#     for joint in treeControl:
#         cmds.treeView(treeControl, e=True, addItem=(bozo, joint))
#
#     cmds.showWindow(toolWindow)
#
#
# tabAmount = listSelJoints()
# print(tabAmount)
#
# if __name__ == "__main__":
#     uiWindow()
