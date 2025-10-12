import maya.cmds as cmds


def getSkinCluster(*args):
    skinCluster = []
    sel = cmds.ls(selection=True )
    for obj in sel:
     objHist = cmds.listHistory(obj, pdo=True)
     skinCluster += cmds.ls(objHist, type="skinCluster") or [None]
    return skinCluster
    
def copySkinToAll(*args):
    skinCluster = getSkinCluster()
    for i in range(len(sel)-1):
         cmds.copySkinWeights( ss=skinCluster[0], ds=skinCluster[i+1], ia="oneToOne", sa="rayCast",uvSpace = ("map1" ,"map1"))
         
copySkinToAll()