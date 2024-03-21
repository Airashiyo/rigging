import maya.cmds as cmds


def getExclKeywords():
    exclKeyField = cmds.textField("excludeField", query=True, text=True)
    if exclKeyField.count(","): # count will give the amount of times that string (",") exists in the given text, if more than 0 times the if condition will be true and we can split
    # start of what you already had
        exclList = exclKeyField.split(",")
        newExcl = []
        for word in exclList:
            newExcl.append(word.strip())
        wordExcl = newExcl
    # end of what you already had
    elif exclKeyField == "": # if there is not a single instance of "," in the textfield, we go to the "else if" statement, here we check if the text field isn't just empty
        wordExcl = [] # if the textfield is empty the condition is true, and we make the wordExcl equal to an empty list
    else: # if the textfield isn't empty, and it doesn't have "," in the text, then we just turn the text in the textfield into a list of only that one piece of text
        wordExcl = [exclKeyField]

    return wordExcl






def getSelInfo():
    #isUnity = cmds.checkBox("unityCheck", query=True, value=True)
    useHierarchy = cmds.checkBox("hierarchyCheck", query=True, value=True)
    selection = cmds.ls(selection=True, type="joint", long=True)
    jntRescale = cmds.floatField("jntRescaleFloat", query=True, value=True)
    assignLayer = cmds.radioButton("existLayerButton", query=True, sl=True)
    createLayer = cmds.radioButton("newLayerButton", query=True, sl=True)
    dontLayer = cmds.radioButton("ignoreLayerButton", query=True, sl=True)
    unrealChoice = cmds.radioButton("unrealButton", query=True, sl=True)
    otherChoice = cmds.radioButton("otherButton", query=True, sl=True)
    #nameLayer = cmds.textField("layerName", query=True, text=True)
    

    #newSkelLayer = cmds.checkBox("newLayerCheck", query=True, value=True)
    #addSkelLayer = cmds.checkBox("existLayerCheck", query=True, value=True)

    return unrealChoice, otherChoice, useHierarchy, selection, jntRescale, assignLayer, createLayer, dontLayer
    






def createLayerFunc(newJoints):
    insertLayerName = cmds.textField("layerName", query=True, text=True)
    if insertLayerName:
        if not cmds.objExists(insertLayerName):
            crtLayer = cmds.createDisplayLayer(n=insertLayerName)
            cmds.editDisplayLayerMembers(crtLayer, newJoints)
        else:
            attentionWindow = cmds.confirmDialog(
                title="Attention!", message="A layer with this name already exists, joints will be assigned to that instead!", 
                messageAlign="center", button=['Continue'], defaultButton="Continue")
            assignLayerFunc(newJoints)

    else:
        warningWindow = cmds.confirmDialog(
            title="Warning!", message="No name provided, layer creation will be skipped!", 
            messageAlign="center", button=['Continue'], defaultButton="Continue")




def assignLayerFunc(newJoints):
    insertLayerName = cmds.textField("layerName", query=True, text=True) # // gets the dumbass text box
    if insertLayerName:
        if cmds.objExists(insertLayerName):  # // checks if this is in fact fr
            cmds.editDisplayLayerMembers(insertLayerName, newJoints) # // puts yo shit in yo layer
        else:
            attentionWindow = cmds.confirmDialog(
                title="Attention!", message="A layer with this name doesn't exist yet, it will be created!", 
                messageAlign="center", button=['Continue'], defaultButton="Continue")
            createLayerFunc(newJoints)
    else:
        warningWindow = cmds.confirmDialog(
            title="Warning!", message="No name provided, layer assignment will be skipped!", 
            messageAlign="center", button=['Continue'], defaultButton="Continue")




def createExpSkel(wordExcl,unrealChoice, otherChoice, useHierarchy,selection,jntRescale, assignLayer, createLayer, dontLayer):
    selection = cmds.ls(selection=True, type="joint", long=True) # // variable to define our selection throughout
        # // Start of function for creating the export skeleton. Parameters are set // isUnity determines if the rig is meant for Unity, if it isn't, it defaults to Unreal Engine //
        # // useHierarchy determines whether to create the rig based on the hierarchy of the bones - if False, it defaults to user's selection. //
    exclusionKeywords = (wordExcl) # // list of key words based on which the tool will later ignore certain joints
    if not selection: # // condition for if there's nothing selected or it doesn't meet the requirements set by the line that defines selection at the bottom
        return "Nope!", [], "No constraints :(", "Try again next time!"

    cmds.select(clear=True)
    if not cmds.objExists("ConstraintsSet"):
        cmds.sets(name="ConstraintsSet")
    if not cmds.objExists("ExpJntSet"):
        cmds.sets(name="ExpJntSet")
        # This checks if the sets with the corresponding names already exists - if they don't, it creates them.

    if useHierarchy:
        relatives_list = [] # // named variable with empty selection
        for jnt in selection: # // for loop start that targets every "joint" within the selection ("selection" is referenced at the bottom)
            relatives_list.append(jnt) # // adds the selected joints into a list under the given name
            relatives_paths = cmds.listRelatives(jnt, allDescendents=True, type="joint", fullPath=True) # // finds the entire hierarchy of the object, has to be a joint.
            if relatives_paths:
                relatives_paths.reverse() # // reverses the hierarchy cus maya is a retard that starts with the egg
                relatives_list.extend(relatives_paths) # // adds all the found joint relatives into a list from earlier (line 21)
        relatives_list = list(dict.fromkeys(relatives_list)) # // dict will avoid duplicate keys, this is to ensure that an EXP joint isn't generated twice from 1 joint.
        selection = relatives_list # // empties the selection

    new_list = []
    for item in selection: # // for loop start that checks every item in the joint relative list for keywords in order to exclude certain joints
        ignore_jnt = False # // by default, it won't ignore joints but conditions are set below:
        for key in exclusionKeywords: # // loop that checks for the key words from exclusion_keywords list on line 5
            if key in item: # // conditions if there's a keyword present in the targeted joint
                ignore_jnt = True # // it will ignore the joint
        if ignore_jnt: # // if the joint doesn't need to be ignored, it'll skip over the conditions
            continue
        new_list.append(item) # // adds all the joints that passed the keyword check into a list
    selection = new_list



    newJoints = [] # // new empty variable so we can assign shit to it later
    newConstraints = [] # // new empty variable so we can assign shit to it later

    for jnt in selection: # // for every joint in the defined selection
        cmds.select(cl=1) # // clears the selection
        jnt_name = jnt.rsplit("|", 1)[-1] # // splits the selected strong from the right, into a list, and separates it by parent division. -1 makes it choose the last item on the list
        nJnt = cmds.joint(n="%s_EXP" % jnt_name) # // variable for creating a joint which inherits the first part of the name, adding _EXP
        if otherChoice: # // if isUnity is enabled, then
            sJnt = cmds.joint(n="%s_sEXP" % jnt_name) # // variable for creating a joint which inherits the first part of the name, adding _sEXP (meaning scaleExport)
            newJoints.append(sJnt) # // adds sJnts into a list with the determined name
        cmds.matchTransform(nJnt, jnt, pos=1, rot=1) # // matches the position and rotation transformations of the newer joints to the previously selected joints
        cmds.makeIdentity(nJnt, apply=1) # // applies transforms to the selected item and all of its children down to shape level, apply=1 means the world space position is preserved and the shape doesnt move
        pc = cmds.parentConstraint(jnt, nJnt, mo=0)[0] # // creates a parent constraint between the original joint and the new joint, maintain offset is turned off
        newJoints.append(nJnt) # // adds nJnts into a list with the determined name

        if otherChoice: # // if the tool is used for exporting to unity
            sc = cmds.scaleConstraint(jnt, sJnt, mo=0)[0] # // creates a scale constraint between the original joint and the new joint, maintain offset is turned off
            for new_made_jnt in [nJnt, sJnt]: # // for loop start that targets the newly made and scale joints
                cmds.setAttr("%s.segmentScaleCompensate" % new_made_jnt, 0) # // disconnects the segmentscalecomp attribute
                
        if unrealChoice: # // if it's not meant for unity
            sc = cmds.scaleConstraint(jnt, nJnt, mo=0)[0] # // creates a scale constraint between the original joint and the new joint, maintain offset is turned off
            cmds.disconnectAttr("%s.parentInverseMatrix[0]" % nJnt, "%s.constraintParentInverseMatrix" % sc) # // disconnects the parentInvMatr attribute in the new joint, from the constraintParent attribute in the scale constraint

        newConstraints.extend([pc, sc]) # // adds the new attributes into a list

        cmds.disconnectAttr("%s.parentMatrix[0]" % jnt, "%s.target[0].targetParentMatrix" % sc) # // disconnects parentmatrix attribute in the original joint from the targetparentmatrix in the scale constraint

    for Constraint in newConstraints: # // for every constraint in the newConstraints list
        cmds.sets(Constraint, include="ConstraintsSet") # // adds all the constraints from the list of constraints into a set
    for Jnt in newJoints: # // for every joint in the newJoints list
        cmds.sets(Jnt, include="ExpJntSet") # // adds all the joints from the list of export joints into a set



    if createLayer:
        createLayerFunc(newJoints)

    if assignLayer:
        assignLayerFunc(newJoints)

    if dontLayer:
        pass



    for jnt in selection: # // for every item in defined selection
        jnt_name = jnt.rsplit("|", 1)[-1] # // splits the selected strong from the right, into a list, and separates it by parent division. -1 makes it choose the last item on the list
        parent = cmds.listRelatives(jnt, parent=True, type="joint", fullPath=True) # // variable which lists all relatives including parents, has to be a joint, and finds the entire hierarchy/path
        if not parent: # // if it doesn't meet the requirements, then skips
            continue
        parent_name = parent[0].rsplit("|", 1)[-1] # // takes the first parent selection and splits the selected string from the right, into a list, and separates it by parent division. //
                                                   # // -1 makes it choose the last item on the list//
        if not cmds.objExists("%s_EXP" % parent_name): # // checks to make sure the object actually exists, if not then it skips
            continue
        cmds.parent("%s_EXP" % jnt_name, "%s_EXP" % parent_name) # // parents one joint to the other

    for jnt in newJoints:
        print(str(jnt) + ' %s'%int(jntRescale))
        changeRadius = cmds.setAttr(jnt+".radius", jntRescale)

    return "Baby!", len(newConstraints), "ConstraintsSet", "ExpJntSet"




def uiWindow():
    if cmds.window("ExportJointCreatorWindow", exists=True):
        cmds.deleteUI("ExportJointCreatorWindow")


    toolWindow = cmds.window("ExportJointCreatorWindow", t="Export Joint Generator", w=450, h=450)

    mainLayout = cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, 450)], rowSpacing=[(1, 10)])

    cmds.frameLayout(label='Target Engine')
    testRowLayout = cmds.rowLayout( numberOfColumns=3, columnWidth3=(270, 10, 170), columnAlign=(1, 'center'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)])
    
    cmds.text(
        label="This setting affects whether \"Segment Scale Compensation\" is disabled. If Unreal Engine is not your target, choose \"Other\".",
        ww=True, parent=testRowLayout)
    
    cmds.separator(hr=False, style="single", h=50, parent=testRowLayout)
    
    collectionColumnLayout = cmds.columnLayout(parent=testRowLayout)
    engineOptionCollection = cmds.radioCollection(parent=collectionColumnLayout)
    unrealButton = cmds.radioButton("unrealButton", label='Unreal Engine')
    otherButton = cmds.radioButton("otherButton", label='Other')
    cmds.radioCollection(engineOptionCollection, edit=True, sl=unrealButton)


    #unityCheck = cmds.checkBox("unityCheck", l="Export for Unity? (Leave off for Unreal)", v=0)
    

    cmds.separator(hr=True, style="single", h=10, p=mainLayout)

    
    testRowLayout2 = cmds.rowLayout( numberOfColumns=2, columnWidth2=(220, 220), columnAttach=[(1, 'both', 0), (2, 'both', 0)], p=mainLayout)
    collectionColumnLayout2 = cmds.columnLayout(parent=testRowLayout2)
    cmds.frameLayout(label='Layer Assignment', w=200, p=collectionColumnLayout2)
    layerOptionCollection = cmds.radioCollection(p=collectionColumnLayout2)
    existLayerButton = cmds.radioButton("existLayerButton", label='Assign to Existing Layer')
    newLayerButton = cmds.radioButton("newLayerButton", label='Assign to New Layer')
    ignoreLayerButton = cmds.radioButton("ignoreLayerButton", label='Do Not Sort')
    cmds.radioCollection(layerOptionCollection, edit=True, sl=ignoreLayerButton)

    layerName = cmds.textField("layerName", w=200, h=20, pht="Specify Layer Name")

    columnLayoutPatch = cmds.columnLayout(parent=testRowLayout2, adj=True)
    cmds.frameLayout(label='Hierarchy', w=200, p=columnLayoutPatch)
    hierarchyCheck = cmds.checkBox("hierarchyCheck", l="Use hierarchy?", v=0)

    cmds.separator(hr=True, style="single", h=12)

    cmds.frameLayout(label="Joint Radius", w=200)
    jntRescaleFloat = cmds.floatField("jntRescaleFloat", v=1)

    

    cmds.separator(hr=True, style="single", h=10, p=mainLayout)

    cmds.frameLayout(label="Excluded Words", p=mainLayout)
    exclField = cmds.textField("excludeField", w=300, h=20, pht="Keywords will be separated with a comma [,]")

    cmds.separator(hr=True, style="single", h=20)

    cmds.button(l="Generate!", w=300, h=50, command=buttonCommand)

    cmds.showWindow(toolWindow)


def buttonCommand(buttonval):
    jntDuplicate = [jnt for jnt in cmds.ls(type="joint") if "|" in jnt]
    if jntDuplicate:
        errorWindow = cmds.confirmDialog(
            title="Error!", message="Joints with identical names found - this tool won't work if joints with identical names exist.", 
            messageAlign="center", button=['Continue'], defaultButton="Continue")
        return
    
    
    wordExcl = getExclKeywords()
    unrealChoice, otherChoice, useHierarchy, selection, jntRescale, assignLayer, createLayer, dontLayer = getSelInfo()
    
    createExpSkel(wordExcl, unrealChoice, otherChoice, useHierarchy, selection, jntRescale, assignLayer, createLayer, dontLayer)


if __name__ == "__main__":
    uiWindow()


# note to self: don't forget to add bee movie script