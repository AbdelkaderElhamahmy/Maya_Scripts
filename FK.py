Sfrom pymel.core import *
import maya.cmds as cmd
win = window(title="My Window")
layout = columnLayout()

btn = button(label="FK", parent=layout)

myColorSlider = cmds.colorSliderGrp( label='Blue', rgb=(0, 0, 1),parent=layout)

def buttonPressed(*args):
    sel = cmds.ls(selection=True )
    for obj in sel:
        colorValue = cmds.colorSliderGrp(myColorSlider, q=True, rgb=True)

        d = cmds.circle( n= ((obj) + '_ctrl') )
        cmds.setAttr((obj) + "_ctrlShape.overrideEnabled",1)
        cmds.setAttr((obj) + "_ctrlShape.overrideRGBColors",1)
        cmds.setAttr ((obj) + "_ctrlShape.overrideColorRGB",colorValue[0], colorValue[1], colorValue[2])
        print(colorValue[1])
        cmds.group( em=False, name= (str(obj) + "_offsetB"))
        cmds.group( em=False, name= (str(obj) + "_offsetA"))
        cmds.group( em=False, name= (str(obj) + "_grp"))
        cmds.matchTransform(str(obj) + "_grp",str(obj))
        cmds.parentConstraint( (str(obj) + '_ctrl'),str(obj) )
    
    for i in range(len(sel)-1):
        print(str(sel[-1]),str(sel[-2]) )
        cmds.parent((str(sel[-1-i]) + '_grp'),(str(sel[-2-i]) + '_ctrl') )


btn.setCommand(buttonPressed)
btn.setCommand(buttonPressed)

win.show()

