import maya.cmds as O

window = cmds.window()
O.columnLayout()
mo = O.radioButtonGrp( label='Option', labelArray2=['Selection', 'All'], numberOfRadioButtons=2,select = 1)
O.rowColumnLayout( numberOfRows=1)
O.button( l='Hide Joint',w=150, c=(HJNT) )
O.button( l='Show Joint',w=150, c=(SHJNT) )
O.showWindow( window )
O.rowColumnLayout( numberOfRows=1)
O.setParent( '..' )
window = O.window()

def erroro(*args):
    window = cmds.window()
    O.columnLayout()
    no = O.confirmDialog(message="Error, No selected Joints", button=["ok"])
    window = O.window()
    
def HJNT(*args):
        moq = O.radioButtonGrp(mo, q = True,select=True )
        if moq == 1:
            if moq:
                Joints=O.ls(type="joint",selection =True)
                for i in range(len(Joints)):
                    O.setAttr((Joints[i]+".drawStyle"),2)
            else:
                erroro()
        elif moq == 2:
            Joints=O.ls(type="joint")
            for i in range(len(Joints)):
                O.setAttr((Joints[i]+".drawStyle"),2)

def SHJNT(*args):
        moq = O.radioButtonGrp(mo, q = True,select=True )
        if moq == 1:
           if moq == 0:
                erroro()
           else:
               Joints=O.ls(type="joint",selection =True)
               for i in range(len(Joints)):
                   O.setAttr((Joints[i]+".drawStyle"),0) 
        elif moq == 2:
            Joints=O.ls(type="joint")
            for i in range(len(Joints)):
                O.setAttr((Joints[i]+".drawStyle"),0)