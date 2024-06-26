import maya.cmds as cmds
import time

# import json
# import os
# import tempfile


# deprecated definition from testing phase - was used with a button command to insert selection into a text box.
# def insertFirstSelected(*args):
#     sel = cmds.selected()
#     if len(sel) > 0:
#         cmds.textField('input_sourceChain', edit=True, text=sel[0])
#     else:
#         cmds.warning("Nothing is selected.")





# definition for determining type of selection, getting its parent list, splitting the chain to find desired joint.
# if the item isn't a joint, it returns false as a failsafe.
# used to insert "clean" joint names into a text box.

srcFieldList = []
trgFieldList = []

srcJntList = []
trgJntList = []

def jntNameSplit(*args):
    # Get the current selection in Maya
    sel = cmds.ls(selection=True)

    if not sel:
        cmds.warning("No joint selected. Please select a joint.")
        return

    # Ensure that the selection is a joint
    if not cmds.objectType(sel[0], isType='joint'):
        cmds.warning("Selected object is not a joint. Please select a joint.")
        return

    # Get the name of the selected joint
    selJointName = sel[0]

    return selJointName


# definition for determining type of selection, getting its parent list, splitting the chain to find the desired shape.
# if the transform isn't a mesh or a skin cluster, it returns false as a failsafe.
# used to insert "clean" joint names into a text box.
def skinNameSplit(*args):
    sel = cmds.ls(selection=True, long=True)
    meshParent = cmds.listRelatives(sel, shapes=True, fullPath=True)
    meshName = meshParent[0].rsplit("|", 1)[-1]
    for item in sel:
        if not meshName or cmds.nodeType(meshParent[0]) != 'mesh':
            continue

        skinCluster = cmds.ls(cmds.listHistory(item), type='skinCluster')
        if skinCluster:
            return meshName

    return False


# fetching UI functions
def getInsertedInfo():
    sourceMesh = cmds.textField('input_sourceMesh', query=True, text=True)
    targetMesh = cmds.textField('input_targetMesh', query=True, text=True)
    sourceChain = cmds.textField('input_sourceChain', query=True, text=True)
    targetChain = cmds.textField('input_targetChain', query=True, text=True)
    sourceJoint = cmds.textField('source_text_field', query=True, text=True)
    targetJoint = cmds.textField('target_text_field', query=True, text=True)


    return sourceMesh, targetMesh, sourceChain, targetChain, sourceJoint, targetJoint

# fetching debug UI functions
def getDebugInfo():
    weightDictCheck = cmds.textField('field_weightDictCheck', query=True, text=True)

    return weightDictCheck

def getMessageInfo():
    stateMessage = cmds.text('text_jointsSection', query=True, label=True)

    return stateMessage


def deleteRowPanel(rowPanel):
    cmds.deleteUI(rowPanel, layout=True)

def createRowPanel(dummyArgument=None):
    rowPanel = cmds.rowLayout(width=330, numberOfColumns=5, columnWidth5=(25, 100, 25, 100, 25), columnAttach=[
        (1, 'left', 0), (2, 'left', 0), (3, 'left', 15), (4, 'left', 0), (5, 'left', 15)], parent="itemColumn")

    # Insert button for source joint
    cmds.button(label='>', w=25, h=25, parent=rowPanel, command=lambda x: insertSourceJoint(srcTextField))
    # Source joint text field
    srcTextField = cmds.textField(placeholderText='source?', w=100, h=25, parent=rowPanel)
    srcFieldList.append(srcTextField)

    # Insert button for target joint
    cmds.button(label='>', w=25, h=25, parent=rowPanel, command=lambda x: insertTargetJoint(trgTextField))
    # Target joint text field
    trgTextField = cmds.textField(placeholderText='target?', w=100, h=25, parent=rowPanel)
    trgFieldList.append(trgTextField)

    # Remove button
    cmds.button(label='X', w=25, h=25, parent=rowPanel, command=lambda x: deleteRowPanel(rowPanel))



# ===================== UI CREATION =========================
# definition for tool window incoming lol
def uiWindow():
    # kill window if it already exists
    if cmds.window("weightTransferUI", exists=True):
        cmds.deleteUI("weightTransferUI")

    # build window bozo
    toolWindow = cmds.window("weightTransferUI", t="Skin Weight Transfer", w=350, h=450, sizeable=False,
                             minimizeButton=True, maximizeButton=True)

    # setting window layout, form type
    # create tabLayout
    tabs = cmds.tabLayout(imw=5, imh=5)


    # create tabs
    form = cmds.formLayout(numberOfDivisions=100, w=340, h=400, parent=tabs)
    cmds.tabLayout(tabs, edit=True, tabLabel=(form, 'Retarget'))
    info = cmds.formLayout(numberOfDivisions=100, w=340, h=400, parent=tabs)
    cmds.tabLayout(tabs, edit=True, tabLabel=(info, 'Help'))
    debug = cmds.formLayout(numberOfDivisions=100, w=340, h=400, parent=tabs)
    cmds.tabLayout(tabs, edit=True, tabLabel=(debug, 'Debug'))
    picker = cmds.formLayout(numberOfDivisions=100, w=340, h=400, parent=tabs)
    cmds.tabLayout(tabs, edit=True, tabLabel=(picker, 'Compare'))

    # fill info tab
    cmds.setParent(info)

    # creating text to insert in scrField_infoText
    infoText = ('Skin Weights Transfer Tool \nVersion: 1.00 \nby Ketlin Riks. '
                '\n\nThis tool saves the skin weights of each vertex, alters the information, and applies it to the target mesh. '
                '\n\nUsed joints require keywords/prefixes. It is suggested to rename all joints in the desired chains with a prefix. Use said prefix in the inputs. '
                '\n\nUsed meshes require object names and a present skin cluster.'
                '\n\n\nDISCLAIMERS:'
                '\nThis tool relies on vertex ID matching, therefore it currently only works with identical source/target meshes and same-count joint chains.')

    # creating scrollable text field scrField_infoText
    scrField_infoText = cmds.scrollField(text=infoText, w=300, h=300, editable=False, wordWrap=True)
    cmds.formLayout(info, edit=True, attachForm=[(scrField_infoText, 'top', 10), (scrField_infoText, 'left', 20)])



    # fill picker tab
    cmds.setParent(picker)

    # scrollLayout = cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
    # cmds.formLayout(picker, edit=True, attachForm=[(scrollLayout, 'top', 10), (scrollLayout, 'left', 20)])

    # creating div_itemsTop separator, organising the UI
    div_itemsTop = cmds.separator(hr=True, style="in", h=15, w=340)
    cmds.formLayout(picker, edit=True,
                    attachForm=[(div_itemsTop, 'top', 0)])

    text_sourceLabel = cmds.text(label="SOURCE:", font="boldLabelFont")
    cmds.formLayout(picker, edit=True,
                    attachForm=[(text_sourceLabel, 'top', 20), (text_sourceLabel, 'left', 42)])

    text_targetLabel = cmds.text(label="TARGET:", font="boldLabelFont")
    cmds.formLayout(picker, edit=True,
                    attachForm=[(text_targetLabel, 'top', 20), (text_targetLabel, 'left', 189)])

    # Button to create new rowPanel
    button_addRow = cmds.button(label="+", w=25, h=25, command=createRowPanel)
    cmds.formLayout(picker, edit=True,
                    attachForm=[(button_addRow, 'top', 13), (button_addRow, 'right', 16)])

    # creating div_itemsTop separator, organising the UI
    div_itemsBottom = cmds.separator(hr=True, style="in", h=15, w=340)
    cmds.formLayout(picker, edit=True,
                    attachForm=[(div_itemsBottom, 'top', 35)])

    # creating div_itemsTop separator, organising the UI
    div_functTop = cmds.separator(hr=True, style="in", h=15, w=340)
    cmds.formLayout(picker, edit=True,
                    attachForm=[(div_functTop, 'bottom', 45)])

    # creating button_runRemap button, it runs function "remapCommand", which in turn runs all relevant functions.
    button_runDynRemap = cmds.button(l="Remap", w=150, h=25, command=dynRemapCommand)
    cmds.formLayout(picker, edit=True, attachForm=[(button_runDynRemap, 'bottom', 17), (button_runDynRemap, 'left', 95)])

    # creating div_itemsTop separator, organising the UI
    div_functBottom = cmds.separator(hr=True, style="in", h=15, w=340)
    cmds.formLayout(picker, edit=True,
                    attachForm=[(div_functBottom, 'bottom', 0)])

    # double-layer form to buffer space above the columns
    itemsForm = cmds.formLayout(numberOfDivisions=100, w=340, h=320)
    cmds.formLayout(picker, edit=True, attachForm=[(itemsForm, 'top', 50), (itemsForm, 'left', 0)])

    scroll = cmds.scrollLayout(width=340, height=320, childResizable=True)
    cmds.formLayout(itemsForm, edit=True, attachForm=[(scroll, 'top', 0), (scroll, 'left', 5)])

    # create column layout for stacking in the tab, nest it into the double-layer form
    itemColumn = cmds.columnLayout('itemColumn', columnWidth=330, columnAttach=('both', 5), rowSpacing=5, parent=scroll)


    createRowPanel()

    # fill debug tab
    cmds.setParent(debug)

    # creating text to insert in scrField_debug
    debugText = ('DEBUG CHECKLIST'
                 '\n\nCompilation of all checks that have been put in place as the functions run.'
                 '\n\nIf successful, it will return "TRUE".'
                 '\nIf failed, it will return "FALSE".'
                 '\n\nThis can help diagnose issues with the tool.')

    # creating scrollable field scrField_debug
    scrField_debug = cmds.scrollField(text=debugText, w=300, h=180, editable=False, wordWrap=True)
    cmds.formLayout(debug, edit=True, attachForm=[(scrField_debug, 'top', 10), (scrField_debug, 'left', 20)])




    # ================ EXPERIMENTAL ================
    # creating text_jointsSection text, clarifying focused object
    text_weightDictCheck = cmds.text(label="Skin Dictionary Storage:", font="boldLabelFont")
    cmds.formLayout(debug, edit=True,
                    attachForm=[(text_weightDictCheck, 'top', 200), (text_weightDictCheck, 'left', 20)])
    # ------------------------------------------------------
    # creating text_jointsSection text, clarifying focused object
    field_weightDictCheck = cmds.textField('field_weightDictCheck', placeholderText='N/A', w=50, h=25, editable=False)
    cmds.formLayout(debug, edit=True,
                    attachForm=[(field_weightDictCheck, 'top', 200), (field_weightDictCheck, 'right', 60)])


    # fill main utility tab
    cmds.setParent(form)

    # ====================== JOINTS ========================
    # ===================== DIVIDER ========================
    # creating div_jointsTop separator, organising the UI
    div_jointsTop = cmds.separator(hr=True, style="in", h=15, w=200)
    cmds.formLayout(form, edit=True,
                    attachForm=[(div_jointsTop, 'top', 3), (div_jointsTop, 'left', 60)])
    # ------------------------------------------------------
    # creating text_jointsSection text, clarifying focused object
    text_jointsSection = cmds.text(label="JOINT RETARGETING", font="boldLabelFont")
    cmds.formLayout(form, edit=True,
                    attachForm=[(text_jointsSection, 'top', 20), (text_jointsSection, 'left', 60)])
    # ------------------------------------------------------
    # creating img_jointIcon image, visual indicator. aligned with text_jointsSection
    img_jointSourceIcon = cmds.image('img_jointSourceIcon', w=25, h=30, image='kinJoint.png')
    cmds.formLayout(form, edit=True, attachForm=[(img_jointSourceIcon, 'top', 13), (img_jointSourceIcon, 'right', 75)])
    # ------------------------------------------------------
    # creating div_jointsTop separator, organising the UI
    div_jointsBottom = cmds.separator(hr=True, style="out", h=15, w=200)
    cmds.formLayout(form, edit=True,
                    attachForm=[(div_jointsBottom, 'top', 37), (div_jointsBottom, 'left', 60)])
    # ------------------------------------------------------
    # ===================== SOURCE =========================
    # creating button_insertSourceChain
    button_insertSourceChain = cmds.button(label='>', w=35, h=25, command=insertSourceChain)
    cmds.formLayout(form, edit=True,
                    attachForm=[(button_insertSourceChain, 'top', 50), (button_insertSourceChain, 'left', 60)])
    # ------------------------------------------------------
    # creating input_sourceChain text field, insert source jnt chain keyword
    input_sourceChain = cmds.textField('input_sourceChain', placeholderText='Source joint chain key.', w=180, h=25)
    cmds.formLayout(form, edit=True,
                    attachForm=[(input_sourceChain, 'top', 50), (input_sourceChain, 'left', 100)])
    # ------------------------------------------------------
    # ===================== TARGET =========================
    # creating button_insertTargetChain
    button_insertTargetChain = cmds.button(label='>', w=35, h=25, command=insertTargetChain)
    cmds.formLayout(form, edit=True,
                    attachForm=[(button_insertTargetChain, 'top', 90), (button_insertTargetChain, 'left', 60)])
    # ------------------------------------------------------
    # creating input_targetChain text field, insert source jnt chain keyword
    input_targetChain = cmds.textField('input_targetChain', placeholderText='Target joint chain key.', w=180, h=25)
    cmds.formLayout(form, edit=True, attachForm=[(input_targetChain, 'top', 90), (input_targetChain, 'left', 100)])

    # ======================= SKINS =========================
    # ===================== DIVIDER ========================
    # creating div_jointsTop separator, organising the UI
    div_skinsTop = cmds.separator(hr=True, style="in", h=15, w=200)
    cmds.formLayout(form, edit=True,
                    attachForm=[(div_skinsTop, 'top', 123), (div_skinsTop, 'left', 60)])
    # ------------------------------------------------------
    # creating text_jointsSection text, clarifying focused object
    text_skinsSection = cmds.text(label="SKIN RETARGETING", font="boldLabelFont")
    cmds.formLayout(form, edit=True,
                    attachForm=[(text_skinsSection, 'top', 140), (text_skinsSection, 'left', 60)])
    # ------------------------------------------------------
    # creating img_jointIcon image, visual indicator. aligned with text_jointsSection
    img_skinsIcon = cmds.image('img_skinsIcon', w=25, h=30, image='smoothSkin.png')
    cmds.formLayout(form, edit=True, attachForm=[(img_skinsIcon, 'top', 132), (img_skinsIcon, 'right', 75)])
    # ------------------------------------------------------
    # creating div_jointsTop separator, organising the UI
    div_skinsBottom = cmds.separator(hr=True, style="out", h=15, w=200)
    cmds.formLayout(form, edit=True,
                    attachForm=[(div_skinsBottom, 'top', 157), (div_skinsBottom, 'left', 60)])
    # ------------------------------------------------------
    # ===================== SOURCE =========================
    # creating button_insertSourceMesh
    button_insertSourceMesh = cmds.button(label='>', w=35, h=25, command=insertSourceSkin)
    cmds.formLayout(form, edit=True,
                    attachForm=[(button_insertSourceMesh, 'top', 170), (button_insertSourceMesh, 'left', 60)])
    # ------------------------------------------------------
    # creating input_sourceMesh text field, insert source jnt chain keyword
    input_sourceMesh = cmds.textField('input_sourceMesh', placeholderText='Source skinned mesh name.', w=180, h=25)
    cmds.formLayout(form, edit=True, attachForm=[(input_sourceMesh, 'top', 170), (input_sourceMesh, 'left', 100)])
    # ------------------------------------------------------
    # ===================== TARGET =========================
    # creating button_insertTargetMesh
    button_insertTargetMesh = cmds.button(label='>', w=35, h=25, command=insertTargetSkin)
    cmds.formLayout(form, edit=True,
                    attachForm=[(button_insertTargetMesh, 'top', 210), (button_insertTargetMesh, 'left', 60)])
    # ------------------------------------------------------
    # creating input_targetMesh text field, insert source jnt chain keyword
    input_targetMesh = cmds.textField('input_targetMesh', placeholderText='Target skinned mesh name.', w=180, h=25)
    cmds.formLayout(form, edit=True, attachForm=[(input_targetMesh, 'top', 210), (input_targetMesh, 'left', 100)])

    # ======================= EXECUTE =========================
    # creating button_runRemap button, it runs function "remapCommand", which in turn runs all relevant functions.
    button_runRemap = cmds.button(l="Remap", w=215, h=35, command=remapCommand)
    cmds.formLayout(form, edit=True, attachForm=[(button_runRemap, 'bottom', 110), (button_runRemap, 'left', 60)])
    # ------------------------------------------------------
    # creating div_jointsTop separator, organising the UI
    div_progressTop = cmds.separator(hr=True, style="in", h=15, w=230)
    cmds.formLayout(form, edit=True,
                    attachForm=[(div_progressTop, 'bottom', 90), (div_progressTop, 'left', 50)])
    # ------------------------------------------------------
    # creating text_jointsSection text, clarifying focused object
    text_progressTitle = cmds.text(label="PROGRESS:", font="boldLabelFont")
    cmds.formLayout(form, edit=True,
                    attachForm=[(text_progressTitle, 'bottom', 80), (text_progressTitle, 'left', 140)])
    # ------------------------------------------------------
    # creating text_jointsSection text, clarifying focused object
    item_progressBar = cmds.progressBar('item_progressBar', width=200)
    # text_jointsSection = cmds.text('text_jointsSection', label="sample text")
    cmds.formLayout(form, edit=True,
                    attachForm=[(item_progressBar, 'bottom', 55), (item_progressBar, 'left', 65)])
    # ------------------------------------------------------
    # creating img_jointIcon image, visual indicator. aligned with text_jointsSection
    # img_jointSourceIcon = cmds.image('img_jointSourceIcon', w=25, h=30, image='kinJoint.png')
    # cmds.formLayout(form, edit=True, attachForm=[(img_jointSourceIcon, 'top', 13), (img_jointSourceIcon, 'right', 75)])
    # ------------------------------------------------------
    # creating div_jointsTop separator, organising the UI
    div_progressBottom = cmds.separator(hr=True, style="out", h=15, w=230)
    cmds.formLayout(form, edit=True,
                    attachForm=[(div_progressBottom, 'bottom', 40), (div_progressBottom, 'left', 50)])
    # ------------------------------------------------------

    # ======================================================
    # execute window
    cmds.showWindow(toolWindow)


# ======================= EXTRA FUNCT =======================
def getSkinnedMeshes():
    """
    function for finding skinned meshes. sorts through relatives. makes sure the found obj is a skin cluster
    if the transform isn't a mesh or a skin cluster, it returns false as a failsafe.
    used to insert "clean" skin cluster names into text box
    """
    selected = cmds.ls(selection=True, long=True)

    for item in selected:
        shapes = cmds.listRelatives(item, shapes=True, fullPath=True)
        if not shapes or cmds.nodeType(shapes[0]) != 'mesh':
            continue

        skin_clusters = cmds.ls(cmds.listHistory(item), type='skinCluster')
        if skin_clusters:
            return True

    return False


def insertSourceChain(*args):
    """
    function for finding the source chain name keys. makes sure the selection is a joint.
    if the item isn't a joint or is empty, it returns as false (failsafe)
    used to insert "clean" joint names into the text box.
    """
    sel = cmds.ls(selection=True, type="joint", long=True)
    jointName = jntNameSplit()
    if len(sel) > 0:
        cmds.textField('input_sourceChain', edit=True, text=jointName)
    else:
        warningWindow = cmds.confirmDialog(
            title="Empty!", message="Selection was invalid! Please select a source joint.",
            messageAlign="center", button=['Continue'], defaultButton="Continue")


def insertSourceJoint(textField):
    """
    function for finding the source chain name keys. makes sure the selection is a joint.
    if the item isn't a joint or is empty, it returns as false (failsafe)
    used to insert "clean" joint names into the text box.
    """
    sel = cmds.ls(selection=True, type="joint", long=True)
    jointName = jntNameSplit()
    if jointName:
        cmds.textField(textField, edit=True, text=jointName)
        srcJntList.append(jointName)
    else:
        warningWindow = cmds.confirmDialog(
            title="Empty!", message="Selection was invalid! Please select a source joint.",
            messageAlign="center", button=['Continue'], defaultButton="Continue")


def insertTargetChain(*args):
    """
    function for finding the target chain name keys. makes sure the selection is a joint.
    if the item isn't a joint or is empty, it returns as false (failsafe)
    used to insert "clean" joint names into the text box.
    """
    sel = cmds.ls(selection=True, type="joint", long=True)
    jointName = jntNameSplit()
    if len(sel) > 0:
        cmds.textField('input_targetChain', edit=True, text=jointName)
    else:
        warningWindow = cmds.confirmDialog(
            title="Empty!", message="Selection was invalid! Please select a target joint.",
            messageAlign="center", button=['Continue'], defaultButton="Continue")


def insertTargetJoint(textField):
    """
    function for finding the source chain name keys. makes sure the selection is a joint.
    if the item isn't a joint or is empty, it returns as false (failsafe)
    used to insert "clean" joint names into the text box.
    """
    sel = cmds.ls(selection=True, type="joint", long=True)
    jointName = jntNameSplit()
    if jointName:
        cmds.textField(textField, edit=True, text=jointName)
        trgJntList.append(jointName)
    else:
        warningWindow = cmds.confirmDialog(
            title="Empty!", message="Selection was invalid! Please select a source joint.",
            messageAlign="center", button=['Continue'], defaultButton="Continue")

def insertSourceSkin(*args):
    """
    function for finding the target skin cluster name. makes sure the selection is a skinned mesh.
    if it's not a skinned mesh, it returns false (failsafe)
    used to insert "clean" skin names into the text box.
    """
    skinnedSourceMesh = getSkinnedMeshes()
    if skinnedSourceMesh:
        cmds.textField('input_sourceMesh', edit=True, text=skinNameSplit())
    else:
        warningWindow = cmds.confirmDialog(
            title="Empty!", message="Selection was invalid! Please select a skinned source mesh.",
            messageAlign="center", button=['Continue'], defaultButton="Continue")


def insertTargetSkin(*args):
    """
    function for finding the target skin cluster name. makes sure the selection is a skinned mesh.
    if it's not a skinned mesh, it returns false (failsafe)
    used to insert "clean" skin names into the text box.
    """
    skinnedTargetMesh = getSkinnedMeshes()
    if skinnedTargetMesh:
        cmds.textField('input_targetMesh', edit=True, text=skinNameSplit())
    else:
        warningWindow = cmds.confirmDialog(
            title="Empty!", message="Selection was invalid! Please select a skinned target mesh.",
            messageAlign="center", button=['Continue'], defaultButton="Continue")


taggedFunctions = []



def storeRetargetWeights(sourceMesh, targetMesh, sourceChain, targetChain):
    """
    Store skin weight values of each vertex in the specified source mesh in a dictionary.
    Convert the joint names from the source chain to the target chain.

    Args:
        sourceMesh (str): Name of the source mesh.
        targetMesh (str): Name of the target mesh.
        sourceChain (str): Prefix of the source chain joint names.
        targetChain (str): Prefix of the target chain joint names.

    Returns:
        dict: Dictionary containing skin weight values for each vertex.
              Keys are vertex names and values are dictionaries with target chain influence names as keys and skin weights as values.
              Example: {'pCube1.vtx[0]': {'target_joint1': 0.5, 'target_joint2': 0.3, ...}, ...}
    """
    # Check if the meshes exist
    if not cmds.objExists(sourceMesh):
        print(f"Source mesh '{sourceMesh}' does not exist.")
        return None
    if not cmds.objExists(targetMesh):
        print(f"Target mesh '{targetMesh}' does not exist.")
        return None

    # Get the skin cluster of the source mesh
    sourceSkin = cmds.ls(cmds.listHistory(sourceMesh), type='skinCluster')
    if not sourceSkin:
        print(f"Source mesh '{sourceMesh}' is not skinned.")
        return None

    # Get the influence list from the source chain
    # sourceInfluence = cmds.skinCluster(sourceSkin[0], query=True, inf=True) [OLD, BEFORE SOURCEJOINTS]
    sourceJoints = (cmds.skinCluster(sourceSkin[0], query=True, inf=True))
    sourceJoints_dict = []
    for jnt in sourceJoints:
        sourceJoints_dict.append(jnt)

    # Get the influence list from the target chain
    targetInfluence = [targetChain + influence[len(sourceChain):] for influence in sourceJoints_dict]

    # Get vertex positions from the source mesh
    vertex_count = cmds.polyEvaluate(sourceMesh, vertex=True)

    # Dictionary to store skin weight values with target chain influence names
    skinWeightsDict = {}

    for i in range(vertex_count):
        vertex = sourceMesh + ".vtx[" + str(i) + "]"
        # Get skin weight for each influence for the current vertex
        skin_weights = cmds.skinPercent(sourceSkin[0], vertex, query=True, value=True)
        vertex_weights = {}
        for influence, weight in zip(targetInfluence, skin_weights):
            vertex_weights[influence] = weight
        skinWeightsDict[vertex] = vertex_weights

    return skinWeightsDict


def applySkinWeightsToTarget(sourceMesh, targetMesh, skinWeightsDict):
    """
    Apply skin weight values to the specified target mesh.

    Args:
        targetMesh (str): Name of the target mesh.
        skinWeightsDict (dict): Dictionary containing skin weight values for each vertex.
                                  Keys are vertex names and values are dictionaries with target chain influence names as keys and skin weights as values.
    """
    # Check if the target mesh exists
    if not cmds.objExists(targetMesh):
        print(f"Target mesh '{targetMesh}' does not exist.")
        return

    # Get the skin cluster of the target mesh
    target_skin_cluster = cmds.ls(cmds.listHistory(targetMesh), type='skinCluster')
    if not target_skin_cluster:
        print(f"Target mesh '{targetMesh}' is not skinned.")
        return

    # Apply skin weight values to the corresponding vertices
    for vertex, weights in skinWeightsDict.items():
        # Convert vertex name to use target mesh vertex name
        target_vertex = vertex.replace(sourceMesh, targetMesh)
        for influence, weight in weights.items():
            cmds.skinPercent(target_skin_cluster[0], target_vertex, transformValue=[(influence, weight)])


def perItemApplication(sourceMesh, targetMesh, skinWeightsDict):

    target_skin_cluster = cmds.ls(cmds.listHistory(targetMesh), type='skinCluster')

    for vertex, weights in skinWeightsDict.items():
        target_vertex = vertex.replace(sourceMesh, targetMesh)
        for influence, weight in weights.items():
            cmds.skinPercent(target_skin_cluster[0], target_vertex, transformValue=[(influence, weight)])


def remapCommand(*args):
    sourceMesh, targetMesh, sourceChain, targetChain, sourceJoint, targetJoint = getInsertedInfo()
    weightDictCheck = getDebugInfo()
    tasks = [storeRetargetWeights, applySkinWeightsToTarget]
    countTasks = len(tasks)

    cmds.progressBar('item_progressBar', edit=True, maxValue=countTasks, progress=0)

    for i, task in enumerate(tasks):
        cmds.progressBar('item_progressBar', edit=True, step=1)

    # Store skin weights:
    skinWeightsDict = storeRetargetWeights(sourceMesh, targetMesh, sourceChain, targetChain)
    if skinWeightsDict:
        cmds.textField("field_weightDictCheck", edit=True, text="True", backgroundColor=[0.49, 0.702, 0.192])
        print("Skin weights stored successfully!")
        print(skinWeightsDict)
    else:
        cmds.textField("field_weightDictCheck", edit=True, text="False", backgroundColor=[0.788, 0.282, 0.341])


    # Apply skin weights to target mesh
    applySkinWeightsToTarget(sourceMesh, targetMesh, skinWeightsDict)

def dynRemapCommand(*args):
    print("Source Joint Names:")
    for jnt in srcJntList:
        print(f"Joint Name: {jnt}")

    print("Target Joint Names:")
    for jnt in trgJntList:
        print(f"Joint Name: {jnt}")

# # Define the file path in the temp directory
# file_path = os.path.join(tempfile.gettempdir(), "skin_weights.json")
#
# # Save the dictionary to a file
# def save_skin_weights(skinWeightsDict, file_path):
#     with open(file_path, "w") as f:
#         json.dump(skinWeightsDict, f)
#     print(f"Skin weights saved to: {file_path}")
#
#     # Save the skin weights dictionary to the file
#     save_skin_weights(skinWeightsDict, file_path)
#
# # Delete the file when Maya is closed
# def delete_skin_weights_file(file_path):
#     if os.path.exists(file_path):
#         os.remove(file_path)
#         print(f"Deleted file: {file_path}")
#
# # Create a scriptJob to delete the file when Maya exits
# cmds.scriptJob(event=["quitApplication", lambda: delete_skin_weights_file(file_path)])








if __name__ == "__main__":
    uiWindow()
