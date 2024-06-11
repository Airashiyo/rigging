import maya.cmds as cmds


def insertFirstSelected(*args):
    sel = cmds.selected()
    if len(sel) > 0:
        cmds.textField('input_sourceChain', edit=True, text=sel[0])
    else:
        cmds.warning("Nothing is selected.")


def jntNameSplit(*args):
    sel = cmds.ls(selection=True, type="joint", long=True)
    chainParent = cmds.listRelatives(sel, parent=True, type="joint", fullPath=True)
    jointName = chainParent[0].rsplit("|", 1)[-1]
    for jnt in sel:
        if not jointName or cmds.nodeType(chainParent[0]) != 'joint':
            continue

        if jointName:
            return jointName
    return False


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


def getInsertedInfo():
    sourceMesh = cmds.textField('input_sourceMesh', query=True, text=True)
    targetMesh = cmds.textField('input_targetMesh', query=True, text=True)
    sourceChain = cmds.textField('input_sourceChain', query=True, text=True)
    targetChain = cmds.textField('input_targetChain', query=True, text=True)

    return sourceMesh, targetMesh, sourceChain, targetChain


def uiWindow():
    # kill window if it already exists
    if cmds.window("weightTransferUI", exists=True):
        cmds.deleteUI("weightTransferUI")

    # build window
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

    cmds.setParent(info)

    infoText = ('Skin Weights Transfer Tool \nVersion: 1.00 \nby Ketlin Riks. '
                '\n\nThis tool saves the skin weights of each vertex, alters the information, and applies it to the target mesh. '
                '\n\nUsed joints require keywords/prefixes. It is suggested to rename all joints in the desired chains with a prefix. Use said prefix in the inputs. '
                '\n\nUsed meshes require object names and a present skin cluster.'
                '\n\n\nDISCLAIMERS:'
                '\nThis tool relies on vertex ID matching, therefore it currently only works with identical source/target meshes and same-count joint chains.')

    scrollField_infoText = cmds.scrollField(text=infoText, w=300, h=300, editable=False, wordWrap=True)
    cmds.formLayout(info, edit=True, attachForm=[(scrollField_infoText, 'top', 10), (scrollField_infoText, 'left', 20)])

    cmds.setParent(form)
    # ===================== FUCK AROUND FIND OUT =========================
    # random shit test

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
    button_runRemap = cmds.button(l="Remap", w=215, h=35, command=remapCommand)
    cmds.formLayout(form, edit=True, attachForm=[(button_runRemap, 'bottom', 90), (button_runRemap, 'left', 65)])

    # ======================================================
    # execute window
    cmds.showWindow(toolWindow)


def getSkinnedMeshes():
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
    sel = cmds.ls(selection=True, type="joint", long=True)
    # srcChainParent = cmds.listRelatives(sel, parent=True, type="joint", fullPath=True)
    # srcJntName = srcChainParent[0].rsplit("|", 1)[-1]
    if len(sel) > 0:
        cmds.textField('input_sourceChain', edit=True, text=jntNameSplit())
    else:
        warningWindow = cmds.confirmDialog(
            title="Empty!", message="Selection was invalid! Please select a source joint.",
            messageAlign="center", button=['Continue'], defaultButton="Continue")


def insertTargetChain(*args):
    sel = cmds.ls(selection=True, type="joint", long=True)
    if len(sel) > 0:
        cmds.textField('input_targetChain', edit=True, text=jntNameSplit())
    else:
        warningWindow = cmds.confirmDialog(
            title="Empty!", message="Selection was invalid! Please select a target joint.",
            messageAlign="center", button=['Continue'], defaultButton="Continue")


def insertSourceSkin(*args):
    sel = cmds.ls(selection=True, long=True)
    skinnedSourceMesh = getSkinnedMeshes()
    if skinnedSourceMesh:
        cmds.textField('input_sourceMesh', edit=True, text=skinNameSplit())
    else:
        warningWindow = cmds.confirmDialog(
            title="Empty!", message="Selection was invalid! Please select a skinned source mesh.",
            messageAlign="center", button=['Continue'], defaultButton="Continue")


def insertTargetSkin(*args):
    sel = cmds.ls(selection=True, long=True)
    skinnedTargetMesh = getSkinnedMeshes()
    if skinnedTargetMesh:
        cmds.textField('input_targetMesh', edit=True, text=skinNameSplit())
    else:
        warningWindow = cmds.confirmDialog(
            title="Empty!", message="Selection was invalid! Please select a skinned target mesh.",
            messageAlign="center", button=['Continue'], defaultButton="Continue")


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
    sourceInfluence = cmds.skinCluster(sourceSkin[0], query=True, inf=True)

    # Get the influence list from the target chain
    targetInfluence = [targetChain + influence[len(sourceChain):] for influence in sourceInfluence]

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


def remapCommand(*args):
    sourceMesh, targetMesh, sourceChain, targetChain = getInsertedInfo()

    # Store skin weights:
    skinWeightsDict = storeRetargetWeights(sourceMesh, targetMesh, sourceChain, targetChain)
    if skinWeightsDict:
        print("Skin weights stored successfully!")
        print(skinWeightsDict)

    # Apply skin weights to target mesh
    applySkinWeightsToTarget(sourceMesh, targetMesh, skinWeightsDict)


if __name__ == "__main__":
    uiWindow()
