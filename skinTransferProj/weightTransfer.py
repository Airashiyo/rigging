import maya.cmds as cmds


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