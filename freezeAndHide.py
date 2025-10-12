import maya.cmds as cmds

dictTransform = {
    "Translation": [".translateX",".translateY",".translateZ"],
    "Rotate": [".rotateX",".rotateY",".rotateZ"],
    "Scale": [".scaleX",".scaleY",".scaleZ"],
}

def UI(*args):
    global checkTrans, checkRotate, checkScale, checklock, checkHide
    if cmds.window("myWindow", exists=True):
        cmds.deleteUI("myWindow", window=True)
    window = cmds.window("myWindow", title='Tool', widthHeight=(200, 100))
    cmds.columnLayout( adjustableColumn=True )
    checkTrans = cmds.checkBox( label='Translate' )
    checkRotate = cmds.checkBox( label='Rotate')
    checkScale = cmds.checkBox( label='Scale')
    checklock = cmds.checkBox( label='Lock_Unlock')
    checkHide = cmds.checkBox( label='Hide_unHide')
    cmds.button( l='Lock_unLock',w=150, c=(lock_unlock_Attr) )
    cmds.button( l='Hide_unHide',w=150, c=(hide_unhide_Attr) )
    cmds.showWindow( window )

def lock_unlock_Attr(*args):
    sel = cmds.ls(selection =True)
    lo = cmds.checkBox(checklock, q = True, value = True )
    print(lo)
    if cmds.checkBox(checkTrans, q = True, value = True ):
        for x in sel:
            for i in dictTransform["Translation"]:
                cmds.setAttr(x + i, lock=lo)
    if cmds.checkBox(checkRotate, q = True, value = True ):
        for x in sel:
            for i in dictTransform["Rotate"]:
                cmds.setAttr(x + i, lock=lo)
    if cmds.checkBox(checkScale, q = True, value = True ):
        for x in sel:
            for i in dictTransform["Scale"]:
                cmds.setAttr(x + i, lock=lo)

def hide_unhide_Attr(*args):
    sel = cmds.ls(selection =True)
    hid = cmds.checkBox(checkHide, q = True, value = True )
    if cmds.checkBox(checkTrans, q = True, value = True ):
        for x in sel:
            for i in dictTransform["Translation"]:
                cmds.setAttr(x + i, keyable =hid )
    if cmds.checkBox(checkRotate, q = True, value = True ):
        for x in sel:
            for i in dictTransform["Rotate"]:
                cmds.setAttr(x + i, keyable =hid )
    if cmds.checkBox(checkScale, q = True, value = True ):
        for x in sel:
            for i in dictTransform["Scale"]:
                cmds.setAttr(x + i, keyable =hid )     

UI()