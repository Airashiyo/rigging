import maya.cmds as cmds


# def findInfluenceJoint(countSourceMesh, countTargetMesh):
#     # just making sure this shit exists by looking for an object w matching name
#     if not cmds.objExists(countSourceMesh):
#         print(f"Source mesh '{countSourceMesh}' does not exist.")
#         return None
#     if not cmds.objExists(countTargetMesh):
#         print(f"Source mesh '{countTargetMesh}' does not exist.")
#         return None
#
#     usedMeshes = [countSourceMesh, countTargetMesh]
#
#     # using ls to return names and types of objects, it looks for skin cluster in mesh history
#     sortSkin = cmds.ls(cmds.listHistory(usedMeshes), type='skinCluster')
#     if not sortSkin:
#         print(f"bitch you thought, one of '{usedMeshes}' not skinned")
#         return None
#
#     # influence returns string array of the joints and transforms.
#     jointSourceInfluences = cmds.skinCluster(sortSkin[0], query=True, inf=True)
#     jointTargetInfluences = cmds.skinCluster(sortSkin[1], query=True, inf=True)
#     # "joint" is recognized by maya.
#     influencesSource_dict = {joint: index for index, joint in enumerate(jointSourceInfluences)}
#     influencesSource_count = len(influencesSource_dict)
#     influencesTarget_dict = {joint: index for index, joint in enumerate(jointTargetInfluences)}
#     influencesTarget_count = len(influencesTarget_dict)
#
#     return influencesSource_dict, influencesSource_count, influencesTarget_dict, influencesTarget_count


def findInfluencesInSource(countSourceMesh):
    # just making sure this shit exists by looking for an object w matching name
    if not cmds.objExists(countSourceMesh):
        print(f"Source mesh '{countSourceMesh}' does not exist.")
        return None

    # using ls to return names and types of objects, it looks for skin cluster in mesh history
    sourceInfluenceSkin = cmds.ls(cmds.listHistory(countSourceMesh), type='skinCluster')
    if not sourceInfluenceSkin:
        print(f"bitch you thought, '{countSourceMesh}' not skinned")
        return None

    sourceJoints = (cmds.skinCluster(sourceInfluenceSkin[0], query=True, inf=True))
    sourceJoints_dict = []
    for jnt in sourceJoints:
        sourceJoints_dict.append(jnt)
    sourceJoints_count = len(sourceJoints_dict)

    return sourceJoints_dict, sourceJoints_count


def findInfluencesInTarget(countTargetMesh):
    # just making sure this shit exists by looking for an object w matching name
    if not cmds.objExists(countTargetMesh):
        print(f"Source mesh '{countTargetMesh}' does not exist.")
        return None

    # using ls to return names and types of objects, it looks for skin cluster in mesh history
    targetInfluenceSkin = cmds.ls(cmds.listHistory(countTargetMesh), type='skinCluster')
    if not targetInfluenceSkin:
        print(f"bitch you thought, '{countTargetMesh}' not skinned")
        return None

    targetJoints = cmds.skinCluster(targetInfluenceSkin[0], query=True, inf=True)
    targetJoints_dict = []
    for jnt in targetJoints:
        targetJoints_dict.append(jnt)
    targetJoints_count = len(targetJoints_dict)

    return targetJoints_dict, targetJoints_count


# feeding it this fucker to check joints on
countSourceMesh = "src_shoulderGoober_00"
countTargetMesh = "trg_shoulderGoober_00"

# unpacking both functions, so their returns can be used individually
sourceJoints_dict, sourceJoints_count = findInfluencesInSource(countSourceMesh)
targetJoints_dict, targetJoints_count = findInfluencesInTarget(countTargetMesh)


print("Source joints found :)")
print(sourceJoints_dict)
print(sourceJoints_count)


print("Target joints found :)")
print(targetJoints_dict)
print(targetJoints_count)


# Retarget variables:
# reSourceMesh = []
# reTargetMesh = []
# reSourceJoint_00 = []
# reSourceJoint_01 = []
# reTargetJoint_00 = []
# reTargetJoint_01 = []

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


def apply_skin_weights_to_target_mesh(targetMesh, skinWeightsDict):
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


# Retarget variables:
sourceMesh = "source_mesh_name"
targetMesh = "target_mesh_name"
sourceChain = "source_jnt_chain_name_segment"
targetChain = "target_jnt_chain_name_segment"

# Store skin weights:
skinWeightsDict = storeRetargetWeights(sourceMesh, targetMesh, sourceChain, targetChain)
if skinWeightsDict:
    print("Skin weights stored successfully!")
    print(skinWeightsDict)

# Apply skin weights to target mesh
apply_skin_weights_to_target_mesh(targetMesh, skinWeightsDict)

# In this case, "bozo" and "haha" were simply my test objects.