import os
import maya.cmds as cmds
from os.path import isfile, join

from functools import partial


def saveFile(name,*args):
    filename = cmds.textField(name,q= True, tx = True)
    fileExtension = cmds.optionMenu( 'Extension', q= True,v=True )
    filepath = os.path.expanduser("~/ITI/")+filename+ "."+fileExtension
    
    print(filepath)
    cmds.file(rename = filepath)
    if fileExtension == "mb":
        cmds.file(s=True,f=True, type="mayaBinary")
    elif fileExtension == "ma":
        cmds.file(s=True,f=True, type="mayaAscii")

def doubleClick(normal, *args):
    sll = cmds.textScrollList( "scrollList", q= True,si=True )
    file_path = os.path.expanduser("~/ITI/")+sll[0]
    if normal == True:
        cmds.file(new=True, force=True) 
        cmds.file(file_path, open=True)
    else:
        cmds.file( file_path, r=True, ns='ref' )
def GUI():
    if cmds.window("SaveTool", exists=True):
        cmds.deleteUI("SaveTool")
    window = cmds.window("SaveTool", title="Save Tool", widthHeight=(300, 50))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
    cmds.text( label='Name' )
    name = cmds.textField()    
    cmds.button(label="Save File", command=partial(saveFile,name))
    cmds.optionMenu( "Extension", label='Extension' )
    cmds.menuItem( label='ma' )
    cmds.menuItem( label='mb' )
    mypath = os.path.expanduser("~/ITI/")
    onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    scrollList = cmds.textScrollList("scrollList",numberOfRows=8,showIndexedItem=4,dcc=partial(doubleClick,True),append = onlyfiles )
    cmds.button(label="Import Ref", command=partial(doubleClick,False))
    cmds.setParent("..")
    cmds.showWindow(window)

GUI()