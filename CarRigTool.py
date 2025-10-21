import maya.cmds as cmds
import json
import os

parts_attr = {}
parts = []
ctrls = []


def Create_UI(*args):
    # Delete window if it already exists
    if cmds.window('CarRigToolWindow', exists=True):
        cmds.deleteUI('CarRigToolWindow')
    
    # Create main window with better styling
    window = cmds.window('CarRigToolWindow', title='Car Rig Tool', width=520, height=700, sizeable=True)
    
    # Main scroll layout for better content management
    mainScroll = cmds.scrollLayout(childResizable=True, backgroundColor=[0.2, 0.2, 0.2])
    
    # Main column layout
    cmds.columnLayout('mainColumnLayout', adjustableColumn=True, rowSpacing=10, columnAttach=('both', 10))
    
    # Header section
    cmds.separator(height=10, style='none')
    cmds.text(label='CAR RIG TOOL', font='boldLabelFont', height=30, 
              backgroundColor=[0.3, 0.35, 0.4], align='center')
    cmds.separator(height=15, style='none')
    
    # Create Tab Layout
    tabs = cmds.tabLayout('mainTabLayout', innerMarginWidth=5, innerMarginHeight=5)
    
    # TAB 1: Parts
    tab1 = cmds.scrollLayout('partsTab', childResizable=True, backgroundColor=[0.22, 0.22, 0.22], height=550)
    Create_Parts_Tab()
    cmds.setParent('..')
    
    # TAB 2: Bone Data
    tab2 = cmds.scrollLayout('boneDataTab', childResizable=True, backgroundColor=[0.22, 0.22, 0.22], height=550)
    Create_Bone_Data_Tab()
    cmds.setParent('..')
    
    # TAB 3: Relations and Features
    tab3 = cmds.scrollLayout('relationsTab', childResizable=True, backgroundColor=[0.22, 0.22, 0.22], height=550)
    Create_Relations_Tab()
    cmds.setParent('..')
    
    # TAB 4: Actions
    tab4 = cmds.scrollLayout('actionsTab', childResizable=True, backgroundColor=[0.22, 0.22, 0.22], height=550)
    Create_Actions_Tab()
    cmds.setParent('..')
    
    # Set tab labels
    cmds.tabLayout(tabs, edit=True, 
                   tabLabel=((tab1, 'Parts'), (tab2, 'Bone Data'), 
                            (tab3, 'Relations & Features'), (tab4, 'Actions')))
    
    return window


def Create_Parts_Tab(*args):
    """Tab 1: Parts Management"""
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAttach=('both', 5))
    
    cmds.separator(height=5, style='none')
    
    # Add Custom Part Section
    cmds.frameLayout(label='Add Custom Part', collapsable=False, 
                    backgroundColor=[0.25, 0.25, 0.25],
                    marginWidth=5, marginHeight=10)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnAttach=('both', 5))
    cmds.separator(height=5, style='none')
    cmds.rowLayout(numberOfColumns=2, adjustableColumn=1,
                  columnAttach=[(1, 'both', 5), (2, 'both', 5)])
    cmds.textField('customPartNameField', placeholderText='Enter part name...', height=30)
    cmds.button(label='Add Part', 
               command=Add_Custom_Part,
               height=30,
               backgroundColor=[0.4, 0.6, 0.5],
               width=100)
    cmds.setParent('..')
    cmds.separator(height=5, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=10, style='none')
    
    # Parts List Section
    cmds.frameLayout(label='Parts List', collapsable=False,
                    backgroundColor=[0.25, 0.25, 0.25],
                    marginWidth=5, marginHeight=10)
    cmds.scrollLayout('partsListScroll', childResizable=True, height=450)
    Create_Parts_List()
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=10, style='none')
    cmds.setParent('..')


def Create_Parts_List(*args):
    """Create list of parts with enable/disable, color, and controller transform controls"""
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnAttach=('both', 5))
    
    for part in parts:
        # Initialize part data if needed
        if part not in parts_attr:
            parts_attr[part] = {}
            parts_attr[part]['color'] = {'R': 0.5, 'G': 0.5, 'B': 0.5}
        
        # Create frame for each part
        frame = cmds.frameLayout(label=part, collapsable=True, collapse=False, 
                                 backgroundColor=[0.28, 0.28, 0.28],
                                 marginWidth=5, marginHeight=5)
        
        cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
        cmds.separator(height=5, style='none')
        
        # Enable checkbox - Always recreate to get fresh UI reference
        parts_attr[part]['isChecked'] = cmds.checkBox(label=f'Enable {part}', 
                                                      value=parts_attr[part].get('isCheckedValue', True),
                                                      backgroundColor=[0.3, 0.3, 0.3])
        
        cmds.separator(height=8, style='in')
        
        # Controller Transform Controls Section
        cmds.text(label='Controller Transform Controls', font='boldLabelFont', align='left',
                 backgroundColor=[0.3, 0.34, 0.38])
        
        # Translate Section
        cmds.text(label='Translation', align='left', height=20)
        cmds.rowLayout(numberOfColumns=3, columnWidth3=(140, 140, 140),
                      columnAttach=[(1, 'left', 5), (2, 'left', 5), (3, 'left', 5)])
        parts_attr[part]['tx'] = cmds.checkBox(label='Translate X', value=parts_attr[part].get('txValue', True))
        parts_attr[part]['ty'] = cmds.checkBox(label='Translate Y', value=parts_attr[part].get('tyValue', True))
        parts_attr[part]['tz'] = cmds.checkBox(label='Translate Z', value=parts_attr[part].get('tzValue', True))
        cmds.setParent('..')
        
        cmds.separator(height=5, style='none')
        
        # Rotate Section
        cmds.text(label='Rotation', align='left', height=20)
        cmds.rowLayout(numberOfColumns=3, columnWidth3=(140, 140, 140),
                      columnAttach=[(1, 'left', 5), (2, 'left', 5), (3, 'left', 5)])
        parts_attr[part]['rx'] = cmds.checkBox(label='Rotate X', value=parts_attr[part].get('rxValue', True))
        parts_attr[part]['ry'] = cmds.checkBox(label='Rotate Y', value=parts_attr[part].get('ryValue', True))
        parts_attr[part]['rz'] = cmds.checkBox(label='Rotate Z', value=parts_attr[part].get('rzValue', True))
        cmds.setParent('..')
        
        cmds.separator(height=5, style='none')
        
        # Scale Section
        cmds.text(label='Scale', align='left', height=20)
        cmds.rowLayout(numberOfColumns=3, columnWidth3=(140, 140, 140),
                      columnAttach=[(1, 'left', 5), (2, 'left', 5), (3, 'left', 5)])
        parts_attr[part]['sx'] = cmds.checkBox(label='Scale X', value=parts_attr[part].get('sxValue', False))
        parts_attr[part]['sy'] = cmds.checkBox(label='Scale Y', value=parts_attr[part].get('syValue', False))
        parts_attr[part]['sz'] = cmds.checkBox(label='Scale Z', value=parts_attr[part].get('szValue', False))
        cmds.setParent('..')
        
        cmds.separator(height=8, style='in')
        
        # Controller Orientation Section
        cmds.text(label='Controller Orientation Axis', font='boldLabelFont', align='left',
                 backgroundColor=[0.3, 0.34, 0.38])
        cmds.rowLayout(numberOfColumns=4, adjustableColumn=1,
                      columnAttach=[(1, 'both', 5), (2, 'both', 5), (3, 'both', 5), (4, 'both', 5)])
        cmds.text(label='Normal:', align='left')
        
        # Create radio collection for this part
        parts_attr[part]['axisCollection'] = cmds.radioCollection()
        parts_attr[part]['axis_x'] = cmds.radioButton(label='X', 
                                                      onCommand=lambda x, p=part: set_axis(p, 'x'))
        parts_attr[part]['axis_y'] = cmds.radioButton(label='Y',
                                                      onCommand=lambda x, p=part: set_axis(p, 'y'))
        parts_attr[part]['axis_z'] = cmds.radioButton(label='Z',
                                                      onCommand=lambda x, p=part: set_axis(p, 'z'))
        
        # Set the selected radio button based on saved value
        current_axis = parts_attr[part].get('axisValue', 'z')
        if current_axis == 'x':
            cmds.radioCollection(parts_attr[part]['axisCollection'], edit=True, select=parts_attr[part]['axis_x'])
        elif current_axis == 'y':
            cmds.radioCollection(parts_attr[part]['axisCollection'], edit=True, select=parts_attr[part]['axis_y'])
        else:
            cmds.radioCollection(parts_attr[part]['axisCollection'], edit=True, select=parts_attr[part]['axis_z'])
        
        cmds.setParent('..')
        
        cmds.separator(height=8, style='in')

        # --- START NEW SECTION ---
        
        # Controller Shape Section
        cmds.text(label='Controller Shape', font='boldLabelFont', align='left',
                 backgroundColor=[0.3, 0.34, 0.38])
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2,
                      columnAttach=[(1, 'right', 5), (2, 'both', 5)])
        cmds.text(label='Shape:', align='left')
        parts_attr[part]['shapeMenu'] = cmds.optionMenu(label='')
        cmds.menuItem(label='Circle')
        cmds.menuItem(label='Box')
        cmds.menuItem(label='Triangle')
        cmds.menuItem(label='Arrow (4-Point)')
        
        # Set the selected shape based on saved value
        current_shape = parts_attr[part].get('shapeValue', 'Circle')
        cmds.optionMenu(parts_attr[part]['shapeMenu'], edit=True, value=current_shape)
        
        cmds.setParent('..')
        
        cmds.separator(height=5, style='none')
        
        # Controller Size Section
        cmds.text(label='Controller Size', font='boldLabelFont', align='left',
                 backgroundColor=[0.3, 0.34, 0.38])
        cmds.rowLayout(numberOfColumns=2, columnWidth2=(80, 120),
                      columnAttach=[(1, 'left', 5), (2, 'left', 5)])
        cmds.text(label='Size:', align='left', width=70)
        parts_attr[part]['sizeField'] = cmds.floatField(
            value=parts_attr[part].get('sizeValue', 1.0), 
            precision=3, 
            minValue=0.01,
            width=115)
        cmds.setParent('..')

        cmds.separator(height=8, style='in')
        
        # --- END NEW SECTION ---
        
        # Color Section
        cmds.text(label='Controller Color', font='boldLabelFont', align='left',
                 backgroundColor=[0.3, 0.34, 0.38])
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=1,
                      columnAttach=[(1, 'both', 5), (2, 'both', 5)])
        
        cmds.button(label='Choose Color', 
                   command=lambda x, p=part: get_color_from_picker(p),
                   backgroundColor=[0.4, 0.4, 0.45],
                   height=30)
        
        # Always recreate color canvas
        parts_attr[part]['colorUI'] = cmds.canvas(
            rgbValue=(parts_attr[part]['color']['R'],
                     parts_attr[part]['color']['G'],
                     parts_attr[part]['color']['B']), 
            width=80, height=30)
        
        cmds.setParent('..')
        cmds.separator(height=5, style='none')
        cmds.setParent('..')
        cmds.setParent('..')
        
        parts_attr[part]['name'] = part
    
    cmds.setParent('..')


def Create_Bone_Data_Tab(*args):
    """Tab 2: Bone Data - Transform controls and orientation"""
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAttach=('both', 5))
    
    cmds.separator(height=5, style='none')
    
    # Bone Transform Controls
    cmds.frameLayout(label='Bone Transform Controls', collapsable=False,
                    backgroundColor=[0.25, 0.25, 0.25],
                    marginWidth=5, marginHeight=10)
    cmds.scrollLayout('boneDataScroll', childResizable=True, height=500)
    Create_Bone_Transform_Controls()
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=10, style='none')
    cmds.setParent('..')


def Create_Bone_Transform_Controls(*args):
    """Create transform and orientation input fields for each part's bone"""
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnAttach=('both', 5))
    
    for part in parts:
        if part not in parts_attr:
            parts_attr[part] = {}
        
        frame = cmds.frameLayout(label=f'{part} - Bone Data', collapsable=True, collapse=False,
                                backgroundColor=[0.28, 0.28, 0.28],
                                marginWidth=5, marginHeight=5)
        
        cmds.columnLayout(adjustableColumn=True, rowSpacing=5)
        cmds.separator(height=5, style='none')
        
        # Translate Values Section
        cmds.text(label='Translation (Position)', font='boldLabelFont', align='left', 
                 backgroundColor=[0.28, 0.32, 0.36])
        cmds.rowLayout(numberOfColumns=4, columnWidth4=(60, 120, 120, 120),
                      columnAttach=[(1, 'left', 5), (2, 'left', 5), (3, 'left', 5), (4, 'left', 5)])
        cmds.text(label='', width=60)
        cmds.text(label='X', align='center')
        cmds.text(label='Y', align='center')
        cmds.text(label='Z', align='center')
        cmds.setParent('..')
        
        cmds.rowLayout(numberOfColumns=4, columnWidth4=(60, 120, 120, 120),
                      columnAttach=[(1, 'left', 5), (2, 'left', 5), (3, 'left', 5), (4, 'left', 5)])
        cmds.text(label='Value:', align='left', width=60)
        parts_attr[part]['bone_tx'] = cmds.floatField(value=parts_attr[part].get('bone_txValue', 0.0), precision=3, width=115)
        parts_attr[part]['bone_ty'] = cmds.floatField(value=parts_attr[part].get('bone_tyValue', 0.0), precision=3, width=115)
        parts_attr[part]['bone_tz'] = cmds.floatField(value=parts_attr[part].get('bone_tzValue', 0.0), precision=3, width=115)
        cmds.setParent('..')
        
        cmds.separator(height=8, style='in')
        
        # Rotate Values Section
        cmds.text(label='Rotation (Degrees)', font='boldLabelFont', align='left',
                 backgroundColor=[0.28, 0.32, 0.36])
        cmds.rowLayout(numberOfColumns=4, columnWidth4=(60, 120, 120, 120),
                      columnAttach=[(1, 'left', 5), (2, 'left', 5), (3, 'left', 5), (4, 'left', 5)])
        cmds.text(label='', width=60)
        cmds.text(label='X', align='center')
        cmds.text(label='Y', align='center')
        cmds.text(label='Z', align='center')
        cmds.setParent('..')
        
        cmds.rowLayout(numberOfColumns=4, columnWidth4=(60, 120, 120, 120),
                      columnAttach=[(1, 'left', 5), (2, 'left', 5), (3, 'left', 5), (4, 'left', 5)])
        cmds.text(label='Value:', align='left', width=60)
        parts_attr[part]['bone_rx'] = cmds.floatField(value=parts_attr[part].get('bone_rxValue', 0.0), precision=3, width=115)
        parts_attr[part]['bone_ry'] = cmds.floatField(value=parts_attr[part].get('bone_ryValue', 0.0), precision=3, width=115)
        parts_attr[part]['bone_rz'] = cmds.floatField(value=parts_attr[part].get('bone_rzValue', 0.0), precision=3, width=115)
        cmds.setParent('..')
        
        cmds.separator(height=8, style='in')
        
        # Scale Values Section
        cmds.text(label='Scale', font='boldLabelFont', align='left',
                 backgroundColor=[0.28, 0.32, 0.36])
        cmds.rowLayout(numberOfColumns=4, columnWidth4=(60, 120, 120, 120),
                      columnAttach=[(1, 'left', 5), (2, 'left', 5), (3, 'left', 5), (4, 'left', 5)])
        cmds.text(label='', width=60)
        cmds.text(label='X', align='center')
        cmds.text(label='Y', align='center')
        cmds.text(label='Z', align='center')
        cmds.setParent('..')
        
        cmds.rowLayout(numberOfColumns=4, columnWidth4=(60, 120, 120, 120),
                      columnAttach=[(1, 'left', 5), (2, 'left', 5), (3, 'left', 5), (4, 'left', 5)])
        cmds.text(label='Value:', align='left', width=60)
        parts_attr[part]['bone_sx'] = cmds.floatField(value=parts_attr[part].get('bone_sxValue', 1.0), precision=3, width=115)
        parts_attr[part]['bone_sy'] = cmds.floatField(value=parts_attr[part].get('bone_syValue', 1.0), precision=3, width=115)
        parts_attr[part]['bone_sz'] = cmds.floatField(value=parts_attr[part].get('bone_szValue', 1.0), precision=3, width=115)
        cmds.setParent('..')
        
        cmds.separator(height=8, style='in')
        
        # Orientation Section
        cmds.text(label='Joint Orientation (Degrees)', font='boldLabelFont', align='left',
                 backgroundColor=[0.28, 0.32, 0.36])
        cmds.rowLayout(numberOfColumns=4, columnWidth4=(60, 120, 120, 120),
                      columnAttach=[(1, 'left', 5), (2, 'left', 5), (3, 'left', 5), (4, 'left', 5)])
        cmds.text(label='', width=60)
        cmds.text(label='X', align='center')
        cmds.text(label='Y', align='center')
        cmds.text(label='Z', align='center')
        cmds.setParent('..')
        
        cmds.rowLayout(numberOfColumns=4, columnWidth4=(60, 120, 120, 120),
                      columnAttach=[(1, 'left', 5), (2, 'left', 5), (3, 'left', 5), (4, 'left', 5)])
        cmds.text(label='Value:', align='left', width=60)
        parts_attr[part]['orient_x'] = cmds.floatField(value=parts_attr[part].get('orient_xValue', 0.0), precision=3, width=115)
        parts_attr[part]['orient_y'] = cmds.floatField(value=parts_attr[part].get('orient_yValue', 0.0), precision=3, width=115)
        parts_attr[part]['orient_z'] = cmds.floatField(value=parts_attr[part].get('orient_zValue', 0.0), precision=3, width=115)
        cmds.setParent('..')
        
        cmds.separator(height=5, style='none')
        cmds.setParent('..')
        cmds.setParent('..')
    
    cmds.setParent('..')


def Create_Relations_Tab(*args):
    """Tab 3: Relations and Features"""
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAttach=('both', 5))
    
    cmds.separator(height=5, style='none')
    
    # Parent-Child Relations
    cmds.frameLayout(label='Parent-Child Relations', collapsable=False,
                    backgroundColor=[0.25, 0.25, 0.25],
                    marginWidth=5, marginHeight=10)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8, columnAttach=('both', 5))
    cmds.separator(height=5, style='none')
    
    cmds.text(label='Set parent relationships between parts', align='left')
    cmds.separator(height=5, style='in')
    
    cmds.rowLayout(numberOfColumns=3, adjustableColumn=2,
                  columnAttach=[(1, 'both', 5), (2, 'both', 5), (3, 'both', 5)])
    cmds.text(label='Child:', width=60)
    cmds.optionMenu('childPartMenu', label='')
    for part in parts:
        cmds.menuItem(label=part)
    cmds.setParent('..')
    
    cmds.separator(height=5, style='none')
    
    cmds.rowLayout(numberOfColumns=3, adjustableColumn=2,
                  columnAttach=[(1, 'both', 5), (2, 'both', 5), (3, 'both', 5)])
    cmds.text(label='Parent:', width=60)
    cmds.optionMenu('parentPartMenu', label='')
    cmds.menuItem(label='None')
    for part in parts:
        cmds.menuItem(label=part)
    cmds.setParent('..')
    
    cmds.separator(height=5, style='none')
    
    cmds.button(label='Set Parent Relation', height=30,
               backgroundColor=[0.4, 0.5, 0.6])
    
    cmds.separator(height=5, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=10, style='none')
    
    # Constraint Features
    cmds.frameLayout(label='Constraint Features', collapsable=False,
                    backgroundColor=[0.25, 0.25, 0.25],
                    marginWidth=5, marginHeight=10)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8, columnAttach=('both', 5))
    cmds.separator(height=5, style='none')
    
    cmds.checkBox('useParentConstraint', label='Use Parent Constraint', value=True)
    cmds.checkBox('usePointConstraint', label='Use Point Constraint', value=False)
    cmds.checkBox('useOrientConstraint', label='Use Orient Constraint', value=False)
    cmds.checkBox('useScaleConstraint', label='Use Scale Constraint', value=False)
    
    cmds.separator(height=5, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=10, style='none')
    
    # Additional Features
    cmds.frameLayout(label='Additional Features', collapsable=False,
                    backgroundColor=[0.25, 0.25, 0.25],
                    marginWidth=5, marginHeight=10)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8, columnAttach=('both', 5))
    cmds.separator(height=5, style='none')
    
    cmds.checkBox('autoOrient', label='Auto Orient Bones', value=True)
    cmds.checkBox('createIK', label='Create IK Handles', value=False)
    cmds.checkBox('createFK', label='Create FK Controls', value=True)
    cmds.checkBox('mirrorRig', label='Mirror Rig (Left/Right)', value=False)
    
    cmds.separator(height=5, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=10, style='none')
    cmds.setParent('..')


def Create_Actions_Tab(*args):
    """Tab 4: Actions"""
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAttach=('both', 5))
    
    cmds.separator(height=5, style='none')
    
    # Build Actions
    cmds.frameLayout(label='Build Actions', collapsable=False,
                    backgroundColor=[0.25, 0.25, 0.25],
                    marginWidth=5, marginHeight=10)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAttach=('both', 10))
    cmds.separator(height=10, style='none')
    
    cmds.button(label='Create Bones Only', 
               command=Create_Bones,
               height=40,
               backgroundColor=[0.4, 0.5, 0.6])
    
    cmds.button(label='Create Controllers Only', 
               command=Create_Ctrls,
               height=40,
               backgroundColor=[0.5, 0.6, 0.5])
    
    cmds.button(label='Build Complete Rig', 
               command=Build_Full_Rig,
               height=40,
               backgroundColor=[0.5, 0.7, 0.4])
    
    cmds.separator(height=10, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=10, style='none')
    
    # Utility Actions
    cmds.frameLayout(label='Utility Actions', collapsable=False,
                    backgroundColor=[0.25, 0.25, 0.25],
                    marginWidth=5, marginHeight=10)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAttach=('both', 10))
    cmds.separator(height=10, style='none')
    
    cmds.button(label='Select All Controllers', 
               height=35,
               backgroundColor=[0.45, 0.45, 0.5])
    
    cmds.button(label='Reset Controllers', 
               height=35,
               backgroundColor=[0.5, 0.5, 0.4])
    
    cmds.button(label='Delete Rig', 
               command=Delete_Rig,
               height=35,
               backgroundColor=[0.6, 0.3, 0.3])
    
    cmds.separator(height=10, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=10, style='none')
    
    # Export/Import
    cmds.frameLayout(label='Export/Import', collapsable=False,
                    backgroundColor=[0.25, 0.25, 0.25],
                    marginWidth=5, marginHeight=10)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAttach=('both', 10))
    cmds.separator(height=10, style='none')
    
    cmds.button(label='Export Rig Configuration', 
               command=Export_Rig_Config,
               height=35,
               backgroundColor=[0.4, 0.5, 0.5])
    
    cmds.button(label='Import Rig Configuration', 
               command=Import_Rig_Config,
               height=35,
               backgroundColor=[0.5, 0.5, 0.5])
    
    cmds.separator(height=10, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=10, style='none')
    cmds.setParent('..')


def set_axis(part, axis, *args):
    """Set the controller orientation axis for a part"""
    parts_attr[part]['axisValue'] = axis
    print(f"{part} - Controller axis set to: {axis.upper()}")

# --- START NEW CONTROLLER SHAPE FUNCTIONS ---

def create_circle_ctrl(name, size, normal):
    """Creates a circle controller"""
    # cmds.circle returns [transform, makeNode]
    return cmds.circle(n=name, r=size, nr=normal)[0]

def create_box_ctrl(name, size, normal):
    """Creates a box controller"""
    s = size * 0.5
    points = []
    if normal == (1, 0, 0): # X-axis normal
        points = [(0, -s, -s), (0, s, -s), (0, s, s), (0, -s, s), (0, -s, -s)]
    elif normal == (0, 1, 0): # Y-axis normal
        points = [(-s, 0, -s), (s, 0, -s), (s, 0, s), (-s, 0, s), (-s, 0, -s)]
    else: # Z-axis normal (0, 0, 1) or default
        points = [(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0), (-s, -s, 0)]
    # cmds.curve returns transform name
    return cmds.curve(n=name, d=1, p=points)

def create_triangle_ctrl(name, size, normal):
    """Creates a triangle controller"""
    s = size * 0.5
    points = []
    if normal == (1, 0, 0): # X-axis normal
        points = [(0, 0, s), (0, s, -s), (0, -s, -s), (0, 0, s)]
    elif normal == (0, 1, 0): # Y-axis normal
        points = [(0, 0, s), (s, 0, -s), (-s, 0, -s), (0, 0, s)]
    else: # Z-axis normal (0, 0, 1) or default
        points = [(0, s, 0), (s, -s, 0), (-s, -s, 0), (0, s, 0)]
    return cmds.curve(n=name, d=1, p=points)
    
def create_arrow_ctrl(name, size, normal):
    """Creates a 4-point arrow controller"""
    s = size * 0.5
    s2 = size * 0.2 # inner point
    points = []
    if normal == (1, 0, 0): # X-axis normal
        points = [(0, 0, s), (0, s2, s2), (0, s, 0), (0, s2, -s2), (0, 0, -s), (0, -s2, -s2), (0, -s, 0), (0, -s2, s2), (0, 0, s)]
    elif normal == (0, 1, 0): # Y-axis normal
        points = [(0, 0, s), (s2, 0, s2), (s, 0, 0), (s2, 0, -s2), (0, 0, -s), (-s2, 0, -s2), (-s, 0, 0), (-s2, 0, s2), (0, 0, s)]
    else: # Z-axis normal (0, 0, 1) or default
        points = [(0, s, 0), (s2, s2, 0), (s, 0, 0), (s2, -s2, 0), (0, -s, 0), (-s2, -s2, 0), (-s, 0, 0), (-s2, s2, 0), (0, s, 0)]
    return cmds.curve(n=name, d=1, p=points)

def create_controller_shape(shape_type, name, size, normal):
    """Dispatcher function to create controller shapes."""
    if shape_type == 'Box':
        return create_box_ctrl(name, size, normal)
    elif shape_type == 'Triangle':
        return create_triangle_ctrl(name, size, normal)
    elif shape_type == 'Arrow (4-Point)':
        return create_arrow_ctrl(name, size, normal)
    elif shape_type == 'Circle':
        return create_circle_ctrl(name, size, normal)
    else:
        # Default to circle if shape_type is unknown
        print(f"Warning: Unknown shape '{shape_type}'. Defaulting to Circle.")
        return create_circle_ctrl(name, size, normal)

# --- END NEW CONTROLLER SHAPE FUNCTIONS ---


def Create_Bones(*args):
    # Save UI values before using them
    Save_UI_Values()
    
    for part in parts:
        # Part Check - use saved value if UI element doesn't exist
        is_enabled = parts_attr[part].get('isCheckedValue', True)
        if 'isChecked' in parts_attr[part] and cmds.checkBox(parts_attr[part]['isChecked'], exists=True):
            is_enabled = cmds.checkBox(parts_attr[part]['isChecked'], q=True, v=True)
        
        if is_enabled:
            parts_attr[part]['relative_bone'] = cmds.joint(n= part + '_jnt', p=(0, 0, 0))
            
            # Apply translation - use saved values or query UI
            tx = parts_attr[part].get('bone_txValue', 0.0)
            ty = parts_attr[part].get('bone_tyValue', 0.0)
            tz = parts_attr[part].get('bone_tzValue', 0.0)
            if 'bone_tx' in parts_attr[part] and cmds.floatField(parts_attr[part]['bone_tx'], exists=True):
                tx = cmds.floatField(parts_attr[part]['bone_tx'], q=True, value=True)
                ty = cmds.floatField(parts_attr[part]['bone_ty'], q=True, value=True)
                tz = cmds.floatField(parts_attr[part]['bone_tz'], q=True, value=True)
            cmds.setAttr(parts_attr[part]['relative_bone'] + '.translate', tx, ty, tz)
            
            # Apply rotation
            rx = parts_attr[part].get('bone_rxValue', 0.0)
            ry = parts_attr[part].get('bone_ryValue', 0.0)
            rz = parts_attr[part].get('bone_rzValue', 0.0)
            if 'bone_rx' in parts_attr[part] and cmds.floatField(parts_attr[part]['bone_rx'], exists=True):
                rx = cmds.floatField(parts_attr[part]['bone_rx'], q=True, value=True)
                ry = cmds.floatField(parts_attr[part]['bone_ry'], q=True, value=True)
                rz = cmds.floatField(parts_attr[part]['bone_rz'], q=True, value=True)
            cmds.setAttr(parts_attr[part]['relative_bone'] + '.rotate', rx, ry, rz)
            
            # Apply scale
            sx = parts_attr[part].get('bone_sxValue', 1.0)
            sy = parts_attr[part].get('bone_syValue', 1.0)
            sz = parts_attr[part].get('bone_szValue', 1.0)
            if 'bone_sx' in parts_attr[part] and cmds.floatField(parts_attr[part]['bone_sx'], exists=True):
                sx = cmds.floatField(parts_attr[part]['bone_sx'], q=True, value=True)
                sy = cmds.floatField(parts_attr[part]['bone_sy'], q=True, value=True)
                sz = cmds.floatField(parts_attr[part]['bone_sz'], q=True, value=True)
            cmds.setAttr(parts_attr[part]['relative_bone'] + '.scale', sx, sy, sz)
            
            # Apply orientation
            orient_x = parts_attr[part].get('orient_xValue', 0.0)
            orient_y = parts_attr[part].get('orient_yValue', 0.0)
            orient_z = parts_attr[part].get('orient_zValue', 0.0)
            if 'orient_x' in parts_attr[part] and cmds.floatField(parts_attr[part]['orient_x'], exists=True):
                orient_x = cmds.floatField(parts_attr[part]['orient_x'], q=True, value=True)
                orient_y = cmds.floatField(parts_attr[part]['orient_y'], q=True, value=True)
                orient_z = cmds.floatField(parts_attr[part]['orient_z'], q=True, value=True)
            cmds.setAttr(parts_attr[part]['relative_bone'] + '.jointOrient', 
                       orient_x, orient_y, orient_z)
        cmds.select(clear=True)
    
    print("Bones created successfully!")


def Create_Ctrls(*args):
    # Save UI values before using them
    Save_UI_Values()
    
    for part in parts:
        # Check if this part should be created - use saved value if UI element doesn't exist
        is_enabled = parts_attr[part].get('isCheckedValue', True)
        if 'isChecked' in parts_attr[part] and cmds.checkBox(parts_attr[part]['isChecked'], exists=True):
            is_enabled = cmds.checkBox(parts_attr[part]['isChecked'], q=True, v=True)
        
        if is_enabled:
            # Get selected axis
            axis = parts_attr[part].get('axisValue', 'z')
            
            # Create normal vector based on selected axis
            normal = (1, 0, 0) if axis == 'x' else (0, 1, 0) if axis == 'y' else (0, 0, 1)
            
            # --- START MODIFIED SECTION ---
            
            # Get selected shape
            shape = parts_attr[part].get('shapeValue', 'Circle')
            
            # Get selected size
            size = parts_attr[part].get('sizeValue', 1.0)
            
            # Create controller based on shape and size
            ctrl_name = part + '_ctrl'
            new_ctrl_name = create_controller_shape(shape, ctrl_name, size, normal)
            
            # Store in list to match original structure
            parts_attr[part]['ctrl'] = [new_ctrl_name] 
            parts_attr[part]['grp'] = cmds.group(str(parts_attr[part]['ctrl'][0]), name=part + '_grp')
            
            # --- END MODIFIED SECTION ---
            
            ctrls.append(str(parts_attr[part]['ctrl'][0]))
            
            # Get color from parts_attr
            r = parts_attr[part]['color']['R']
            g = parts_attr[part]['color']['G']
            b = parts_attr[part]['color']['B']
            
            # Apply color override
            cmds.setAttr(parts_attr[part]['ctrl'][0] + '.overrideEnabled', 1)
            cmds.setAttr(parts_attr[part]['ctrl'][0] + '.overrideRGBColors', 1)
            cmds.setAttr(parts_attr[part]['ctrl'][0] + '.overrideColorRGB', r, g, b)
            
            attrs_to_check = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
            
            if 'relative_bone' in parts_attr[part] and cmds.objExists(parts_attr[part]['relative_bone']):
                cmds.matchTransform(parts_attr[part]['grp'], parts_attr[part]['relative_bone'])
            
            for attr in attrs_to_check:
                # Get value from saved data or UI
                attr_enabled = parts_attr[part].get(attr + 'Value', True if attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz'] else False)
                if attr in parts_attr[part] and cmds.checkBox(parts_attr[part][attr], exists=True):
                    attr_enabled = cmds.checkBox(parts_attr[part][attr], q=True, v=True)
                
                # If checkbox is NOT checked, lock and hide the attribute
                if not attr_enabled:
                    cmds.setAttr(f"{parts_attr[part]['ctrl'][0]}.{attr}", 
                               lock=True, keyable=False, channelBox=False)
    
    print("Controllers created successfully!")


def get_color_from_picker(part, *args):
    # Open color picker
    result = cmds.colorEditor()
    
    # Parse the result string
    values = result.split()
    
    if len(values) == 4:
        r = float(values[0])
        g = float(values[1])
        b = float(values[2])
        confirmed = int(values[3])
        
        # If user confirmed the selection
        if confirmed:
            parts_attr[part]['color']['R'] = r
            parts_attr[part]['color']['G'] = g
            parts_attr[part]['color']['B'] = b
            print(f"{part} - Selected color: R={r}, G={g}, B={b}")
            if 'colorUI' in parts_attr[part] and cmds.canvas(parts_attr[part]['colorUI'], exists=True):
                cmds.canvas(parts_attr[part]['colorUI'], edit=True, rgbValue=(r, g, b))


def Add_Custom_Part(*args):
    # Get the custom part name from text field
    custom_name = cmds.textField('customPartNameField', query=True, text=True).strip()
    
    # Validate input
    if not custom_name:
        cmds.confirmDialog(title='Error', 
                          message='Please enter a part name!',
                          button=['OK'],
                          defaultButton='OK')
        return
    
    # Check if part already exists
    if custom_name in parts:
        cmds.confirmDialog(title='Error', 
                          message=f'Part "{custom_name}" already exists!',
                          button=['OK'],
                          defaultButton='OK')
        return
    
    # Add to parts list
    parts.append(custom_name)
    
    # Clear the text field
    cmds.textField('customPartNameField', edit=True, text='')
    
    # Refresh all tabs
    Refresh_All_Tabs()
    
    print(f"Added custom part: {custom_name}")


def Refresh_All_Tabs(*args):
    """Refresh all tabs to show new parts"""
    # Save current values before refreshing
    Save_UI_Values()
    
    # Refresh Parts List
    if cmds.scrollLayout('partsListScroll', exists=True):
        cmds.deleteUI('partsListScroll', control=True)
    cmds.setParent('partsTab')
    cmds.scrollLayout('partsListScroll', childResizable=True, height=450)
    Create_Parts_List()
    cmds.setParent('..')
    
    # Refresh Bone Data
    if cmds.scrollLayout('boneDataScroll', exists=True):
        cmds.deleteUI('boneDataScroll', control=True)
    cmds.setParent('boneDataTab')
    cmds.scrollLayout('boneDataScroll', childResizable=True, height=500)
    Create_Bone_Transform_Controls()
    cmds.setParent('..')
    
    # Refresh Relations dropdowns
    if cmds.optionMenu('childPartMenu', exists=True):
        items = cmds.optionMenu('childPartMenu', query=True, itemListLong=True)
        if items:
            for item in items:
                cmds.deleteUI(item)
        for part in parts:
            cmds.menuItem(label=part, parent='childPartMenu')
    
    if cmds.optionMenu('parentPartMenu', exists=True):
        items = cmds.optionMenu('parentPartMenu', query=True, itemListLong=True)
        if items:
            for item in items:
                cmds.deleteUI(item)
        cmds.menuItem(label='None', parent='parentPartMenu')
        for part in parts:
            cmds.menuItem(label=part, parent='parentPartMenu')


def Save_UI_Values(*args):
    """Save current UI values before refreshing"""
    for part in parts:
        if part in parts_attr:
            # Save checkbox states
            if 'isChecked' in parts_attr[part] and cmds.checkBox(parts_attr[part]['isChecked'], exists=True):
                parts_attr[part]['isCheckedValue'] = cmds.checkBox(parts_attr[part]['isChecked'], q=True, v=True)
            
            # Save transform control checkboxes
            for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']:
                if attr in parts_attr[part] and cmds.checkBox(parts_attr[part][attr], exists=True):
                    parts_attr[part][attr + 'Value'] = cmds.checkBox(parts_attr[part][attr], q=True, v=True)
            
            # --- START MODIFIED SECTION ---
            
            # Save controller shape
            if 'shapeMenu' in parts_attr[part] and cmds.optionMenu(parts_attr[part]['shapeMenu'], exists=True):
                parts_attr[part]['shapeValue'] = cmds.optionMenu(parts_attr[part]['shapeMenu'], q=True, v=True)
            
            # Save controller size
            if 'sizeField' in parts_attr[part] and cmds.floatField(parts_attr[part]['sizeField'], exists=True):
                parts_attr[part]['sizeValue'] = cmds.floatField(parts_attr[part]['sizeField'], q=True, v=True)

            # --- END MODIFIED SECTION ---
            
            # Save bone transform values
            bone_attrs = ['bone_tx', 'bone_ty', 'bone_tz', 'bone_rx', 'bone_ry', 'bone_rz', 
                         'bone_sx', 'bone_sy', 'bone_sz', 'orient_x', 'orient_y', 'orient_z']
            for attr in bone_attrs:
                if attr in parts_attr[part] and cmds.floatField(parts_attr[part][attr], exists=True):
                    parts_attr[part][attr + 'Value'] = cmds.floatField(parts_attr[part][attr], q=True, value=True)


def Delete_Rig(*args):
    """Delete all rig elements"""
    result = cmds.confirmDialog(title='Confirm Delete', 
                                message='Are you sure you want to delete the entire rig?',
                                button=['Yes', 'No'],
                                defaultButton='No',
                                cancelButton='No',
                                dismissString='No')
    
    if result == 'Yes':
        for part in parts:
            if 'ctrl' in parts_attr[part]:
                # Check if the list is not empty and the object exists
                if parts_attr[part]['ctrl'] and cmds.objExists(str(parts_attr[part]['ctrl'][0])):
                    cmds.delete(str(parts_attr[part]['ctrl'][0]))
            if 'grp' in parts_attr[part]:
                if cmds.objExists(parts_attr[part]['grp']):
                    cmds.delete(parts_attr[part]['grp'])
            if 'relative_bone' in parts_attr[part]:
                if cmds.objExists(parts_attr[part]['relative_bone']):
                    cmds.delete(parts_attr[part]['relative_bone'])
        
        ctrls.clear()
        # Clear the saved object names from parts_attr
        for part in parts_attr:
            parts_attr[part].pop('ctrl', None)
            parts_attr[part].pop('grp', None)
            parts_attr[part].pop('relative_bone', None)
            
        print("Rig deleted successfully!")


def Build_Full_Rig(*args):
    Create_Bones()
    Create_Ctrls()
    print("Rig created successfully!")
    print(parts_attr)
    cmds.confirmDialog(title='Success', 
                      message='Rig has been created successfully!',
                      button=['OK'],
                      defaultButton='OK')


def Export_Rig_Config(*args):
    """Export rig configuration to JSON file"""
    print("Export function called!")
    
    # Save current UI values
    Save_UI_Values()
    
    # Prepare data for export
    export_data = {
        'parts': parts,
        'parts_config': {}
    }
    
    # Collect all part configurations
    for part in parts:
        if part in parts_attr:
            part_config = {
                'enabled': parts_attr[part].get('isCheckedValue', True),
                'color': parts_attr[part].get('color', {'R': 0.5, 'G': 0.5, 'B': 0.5}),
                'axis': parts_attr[part].get('axisValue', 'z'),
                'shape': parts_attr[part].get('shapeValue', 'Circle'), # --- NEW ---
                'size': parts_attr[part].get('sizeValue', 1.0),       # --- NEW ---
                'controller_transforms': {
                    'tx': parts_attr[part].get('txValue', True),
                    'ty': parts_attr[part].get('tyValue', True),
                    'tz': parts_attr[part].get('tzValue', True),
                    'rx': parts_attr[part].get('rxValue', True),
                    'ry': parts_attr[part].get('ryValue', True),
                    'rz': parts_attr[part].get('rzValue', True),
                    'sx': parts_attr[part].get('sxValue', False),
                    'sy': parts_attr[part].get('syValue', False),
                    'sz': parts_attr[part].get('szValue', False)
                },
                'bone_data': {
                    'translate': {
                        'x': parts_attr[part].get('bone_txValue', 0.0),
                        'y': parts_attr[part].get('bone_tyValue', 0.0),
                        'z': parts_attr[part].get('bone_tzValue', 0.0)
                    },
                    'rotate': {
                        'x': parts_attr[part].get('bone_rxValue', 0.0),
                        'y': parts_attr[part].get('bone_ryValue', 0.0),
                        'z': parts_attr[part].get('bone_rzValue', 0.0)
                    },
                    'scale': {
                        'x': parts_attr[part].get('bone_sxValue', 1.0),
                        'y': parts_attr[part].get('bone_syValue', 1.0),
                        'z': parts_attr[part].get('bone_szValue', 1.0)
                    },
                    'orientation': {
                        'x': parts_attr[part].get('orient_xValue', 0.0),
                        'y': parts_attr[part].get('orient_yValue', 0.0),
                        'z': parts_attr[part].get('orient_zValue', 0.0)
                    }
                }
            }
            export_data['parts_config'][part] = part_config
    
    print(f"Data prepared for export: {len(export_data['parts'])} parts")
    
    # Get file path from user
    try:
        file_path = cmds.fileDialog2(
            fileMode=0,
            caption='Export Rig Configuration',
            fileFilter='JSON Files (*.json)',
            okCaption='Export'
        )
        
        print(f"File dialog result: {file_path}")
        
        if file_path and len(file_path) > 0:
            file_path = file_path[0]
            
            # Ensure .json extension
            if not file_path.endswith('.json'):
                file_path += '.json'
            
            # Write to file
            with open(file_path, 'w') as f:
                json.dump(export_data, f, indent=4)
            
            print(f"Rig configuration exported to: {file_path}")
            cmds.confirmDialog(
                title='Export Successful',
                message='Rig configuration exported successfully!\n\n' + file_path,
                button=['OK'],
                defaultButton='OK'
            )
        else:
            print("Export cancelled by user")
            
    except Exception as e:
        print(f"Export error: {str(e)}")
        cmds.confirmDialog(
            title='Export Error',
            message='Failed to export configuration:\n' + str(e),
            button=['OK'],
            defaultButton='OK'
        )


def Import_Rig_Config(*args):
    """Import rig configuration from JSON file"""
    # Get file path from user
    file_path = cmds.fileDialog2(
        fileMode=1,
        caption='Import Rig Configuration',
        fileFilter='JSON Files (*.json)'
    )
    
    if file_path:
        file_path = file_path[0]
        try:
            with open(file_path, 'r') as f:
                import_data = json.load(f)
            
            # Clear existing parts (keep only imported ones)
            global parts
            parts = import_data.get('parts', [])
            global parts_attr
            parts_attr = {} # Clear existing attributes to avoid merging issues
            
            # Load part configurations
            parts_config = import_data.get('parts_config', {})
            
            for part in parts:
                if part not in parts_attr:
                    parts_attr[part] = {}
                
                if part in parts_config:
                    config = parts_config[part]
                    
                    # Load basic settings
                    parts_attr[part]['isCheckedValue'] = config.get('enabled', True)
                    parts_attr[part]['color'] = config.get('color', {'R': 0.5, 'G': 0.5, 'B': 0.5})
                    
                    # Load controller transform settings
                    ctrl_trans = config.get('controller_transforms', {})
                    parts_attr[part]['txValue'] = ctrl_trans.get('tx', True)
                    parts_attr[part]['tyValue'] = ctrl_trans.get('ty', True)
                    parts_attr[part]['tzValue'] = ctrl_trans.get('tz', True)
                    parts_attr[part]['rxValue'] = ctrl_trans.get('rx', True)
                    parts_attr[part]['ryValue'] = ctrl_trans.get('ry', True)
                    parts_attr[part]['rzValue'] = ctrl_trans.get('rz', True)
                    parts_attr[part]['sxValue'] = ctrl_trans.get('sx', False)
                    parts_attr[part]['syValue'] = ctrl_trans.get('sy', False)
                    parts_attr[part]['szValue'] = ctrl_trans.get('sz', False)
                    
                    # Load controller axis
                    parts_attr[part]['axisValue'] = config.get('axis', 'z')
                    
                    # --- START MODIFIED SECTION ---
                    
                    # Load controller shape and size
                    parts_attr[part]['shapeValue'] = config.get('shape', 'Circle')
                    parts_attr[part]['sizeValue'] = config.get('size', 1.0)
                    
                    # --- END MODIFIED SECTION ---
                    
                    # Load bone data
                    bone_data = config.get('bone_data', {})
                    
                    translate = bone_data.get('translate', {})
                    parts_attr[part]['bone_txValue'] = translate.get('x', 0.0)
                    parts_attr[part]['bone_tyValue'] = translate.get('y', 0.0)
                    parts_attr[part]['bone_tzValue'] = translate.get('z', 0.0)
                    
                    rotate = bone_data.get('rotate', {})
                    parts_attr[part]['bone_rxValue'] = rotate.get('x', 0.0)
                    parts_attr[part]['bone_ryValue'] = rotate.get('y', 0.0)
                    parts_attr[part]['bone_rzValue'] = rotate.get('z', 0.0)
                    
                    scale = bone_data.get('scale', {})
                    parts_attr[part]['bone_sxValue'] = scale.get('x', 1.0)
                    parts_attr[part]['bone_syValue'] = scale.get('y', 1.0)
                    parts_attr[part]['bone_szValue'] = scale.get('z', 1.0)
                    
                    orientation = bone_data.get('orientation', {})
                    parts_attr[part]['orient_xValue'] = orientation.get('x', 0.0)
                    parts_attr[part]['orient_yValue'] = orientation.get('y', 0.0)
                    parts_attr[part]['orient_zValue'] = orientation.get('z', 0.0)
            
            # Refresh UI with imported data
            Refresh_All_Tabs()
            
            print(f"Rig configuration imported from: {file_path}")
            cmds.confirmDialog(
                title='Import Successful',
                message=f'Rig configuration imported successfully!\n\nLoaded {len(parts)} parts.',
                button=['OK'],
                defaultButton='OK'
            )
        except Exception as e:
            cmds.confirmDialog(
                title='Import Error',
                message=f'Failed to import configuration:\n{str(e)}',
                button=['OK'],
                defaultButton='OK'
            )


# Create and show UI
window = Create_UI()
cmds.showWindow(window)