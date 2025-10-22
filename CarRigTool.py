import maya.cmds as cmds
import json
import os
import google.generativeai as genai

# --- (Global variables) ---
parts_attr = {}
parts = []
ctrls = []
relations = [] 


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
    
    # TAB 3: Relations
    tab3 = cmds.scrollLayout('relationsTab', childResizable=True, backgroundColor=[0.22, 0.22, 0.22], height=550)
    Create_Relations_Tab()
    cmds.setParent('..')
    
    # TAB 4: Actions
    tab4 = cmds.scrollLayout('actionsTab', childResizable=True, backgroundColor=[0.22, 0.22, 0.22], height=550)
    Create_Actions_Tab()
    cmds.setParent('..')
    
    # TAB 5: AI Generator
    tab5 = cmds.scrollLayout('aiTab', childResizable=True, backgroundColor=[0.22, 0.22, 0.22], height=550)
    Create_AI_Tab()
    cmds.setParent('..')
    
    
    # Set tab labels
    cmds.tabLayout(tabs, edit=True, 
                   tabLabel=((tab1, 'Parts'), (tab2, 'Bone Data'), 
                            (tab3, 'Relations'), 
                            (tab4, 'Actions'),
                            (tab5, 'AI Generator'))) 
    
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
    
    # --- NEW: Add a column layout to hold buttons AND scroll layout ---
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnAttach=('both', 5))
    
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(240, 240),
                  columnAttach=[(1, 'both', 5), (2, 'both', 5)],
                  height=30)
    cmds.button(label='Expand All', 
               command=lambda x: Toggle_All_Frames('ui_partFrame', False), # <-- Use key
               backgroundColor=[0.4, 0.5, 0.4])
    cmds.button(label='Collapse All', 
               command=lambda x: Toggle_All_Frames('ui_partFrame', True), # <-- Use key
               backgroundColor=[0.5, 0.4, 0.4])
    cmds.setParent('..') # Back to the new columnLayout
    
    cmds.separator(height=5, style='in')
    
    cmds.scrollLayout('partsListScroll', childResizable=True, height=450)
    Create_Parts_List() # This will populate parts_attr[part]['ui_partFrame']
    cmds.setParent('..') # Back to the new columnLayout
    
    cmds.setParent('..') # Back to the frameLayout
    cmds.setParent('..') # Back to the main tab layout
    
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
        # --- MODIFIED: Store frame name ---
        frame = cmds.frameLayout(label=part, collapsable=True, collapse=False, 
                                 backgroundColor=[0.28, 0.28, 0.28],
                                 marginWidth=5, marginHeight=5)
        parts_attr[part]['ui_partFrame'] = frame # <-- Store the frame name
        
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
    
    # --- NEW: Add a column layout to hold buttons AND scroll layout ---
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnAttach=('both', 5))

    cmds.rowLayout(numberOfColumns=2, columnWidth2=(240, 240),
                  columnAttach=[(1, 'both', 5), (2, 'both', 5)],
                  height=30)
    cmds.button(label='Expand All', 
               command=lambda x: Toggle_All_Frames('ui_boneFrame', False), # <-- Use key
               backgroundColor=[0.4, 0.5, 0.4])
    cmds.button(label='Collapse All', 
               command=lambda x: Toggle_All_Frames('ui_boneFrame', True), # <-- Use key
               backgroundColor=[0.5, 0.4, 0.4])
    cmds.setParent('..') # Back to the new columnLayout
    
    cmds.separator(height=5, style='in')

    cmds.scrollLayout('boneDataScroll', childResizable=True, height=500)
    Create_Bone_Transform_Controls() # This will populate parts_attr[part]['ui_boneFrame']
    cmds.setParent('..') # Back to the new columnLayout
    
    cmds.setParent('..') # Back to the frameLayout
    cmds.setParent('..') # Back to the main tab layout
    
    cmds.separator(height=10, style='none')
    cmds.setParent('..')


def Create_Bone_Transform_Controls(*args):
    """Create transform and orientation input fields for each part's bone"""
    cmds.columnLayout(adjustableColumn=True, rowSpacing=5, columnAttach=('both', 5))
    
    for part in parts:
        if part not in parts_attr:
            parts_attr[part] = {}
        
        # --- MODIFIED: Store frame name ---
        frame = cmds.frameLayout(label=f'{part} - Bone Data', collapsable=True, collapse=False,
                                backgroundColor=[0.28, 0.28, 0.28],
                                marginWidth=5, marginHeight=5)
        parts_attr[part]['ui_boneFrame'] = frame # <-- Store the frame name
        
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


# --- (No changes to Create_Relations_Tab) ---
def Create_Relations_Tab(*args):
    """Tab 3: Relations - Parent-child relationships and constraints"""
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
    
    cmds.separator(height=8, style='in')
    
    # Constraint Type Selection
    cmds.text(label='Constraint Type:', align='left', font='boldLabelFont')
    cmds.separator(height=3, style='none')
    
    cmds.radioCollection('constraintTypeCollection')
    cmds.radioButton('directParentRadio', label='Direct (Group under Controller)', 
                    select=True, annotation='Parent the child group directly under the parent controller')
    cmds.radioButton('parentConstraintRadio', label='Parent Constraint',
                    annotation='Use parent constraint (position and rotation)')
    cmds.radioButton('pointConstraintRadio', label='Point Constraint',
                    annotation='Use point constraint (position only)')
    cmds.radioButton('orientConstraintRadio', label='Orient Constraint',
                    annotation='Use orient constraint (rotation only)')
    cmds.radioButton('scaleConstraintRadio', label='Scale Constraint',
                    annotation='Use scale constraint (scale only)')
    cmds.radioButton('allConstraintsRadio', label='All Constraints (Parent + Scale)',
                    annotation='Use both parent and scale constraints')
    
    cmds.separator(height=8, style='in')
    
    # Maintain Offset Option
    cmds.checkBox('maintainOffsetCheck', label='Maintain Offset', value=True,
                 annotation='Keep the current position/rotation when creating constraint')
    
    cmds.separator(height=5, style='none')
    
    cmds.button(label='Apply Relation', height=35,
               command=Apply_Parent_Relation, 
               backgroundColor=[0.4, 0.6, 0.5],
               annotation='Apply the selected parent-child relationship')
    
    cmds.separator(height=5, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=10, style='none')
    
    # Current Relations Display
    cmds.frameLayout(label='Current Relations', collapsable=False,
                    backgroundColor=[0.25, 0.25, 0.25],
                    marginWidth=5, marginHeight=10)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8, columnAttach=('both', 5))
    cmds.separator(height=5, style='none')
    
    cmds.textScrollList('relationsListUI', height=200, 
                       allowMultiSelection=False,
                       backgroundColor=[0.2, 0.2, 0.2])
    Update_Relations_Display() 
    
    cmds.separator(height=5, style='none')
    
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(240, 240),
                  columnAttach=[(1, 'both', 5), (2, 'both', 5)])
    cmds.button(label='Remove Selected Relation', height=30,
               command=Remove_Selected_Relation, 
               backgroundColor=[0.6, 0.4, 0.3])
    cmds.button(label='Clear All Relations', height=30,
               command=Clear_All_Relations, 
               backgroundColor=[0.6, 0.3, 0.3])
    cmds.setParent('..')
    
    cmds.separator(height=5, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=10, style='none')
    cmds.setParent('..')

# --- (No changes to Relation functions) ---

def Apply_Parent_Relation(*args):
    """Saves the selected parent-child relation to the global list and applies it to the scene."""
    
    # 1. Read values from UI
    child = cmds.optionMenu('childPartMenu', q=True, v=True)
    parent = cmds.optionMenu('parentPartMenu', q=True, v=True)
    
    if not child:
        cmds.warning("No child part selected.")
        return
        
    constraint_type_radio = cmds.radioCollection('constraintTypeCollection', q=True, select=True)
    constraint_type_label = cmds.radioButton(constraint_type_radio, q=True, label=True)
    maintain_offset = cmds.checkBox('maintainOffsetCheck', q=True, v=True)
    
    # 2. Translate label to key
    radio_map = {
        'Direct (Group under Controller)': 'direct',
        'Parent Constraint': 'parent',
        'Point Constraint': 'point',
        'Orient Constraint': 'orient',
        'Scale Constraint': 'scale',
        'All Constraints (Parent + Scale)': 'all'
    }
    constraint_type = radio_map.get(constraint_type_label, 'direct')
    
    # 3. Validation
    if child == parent:
        cmds.warning(f"Cannot parent a part to itself: {child}")
        return
        
    # 4. Find and remove any existing relation for this child
    existing_rel = None
    for rel in relations:
        if rel['child'] == child:
            existing_rel = rel
            break
    
    if existing_rel:
        Remove_Relation_In_Scene(existing_rel) # Remove from scene
        relations.remove(existing_rel)         # Remove from list
        
    # 5. Add new relation (if parent is not 'None')
    if parent == 'None':
        Update_Relations_Display()
        print(f"Removed relation for child: {child}")
        return
        
    new_relation = {
        'child': child,
        'parent': parent,
        'type': constraint_type,
        'maintain_offset': maintain_offset
    }
    
    relations.append(new_relation)
    Apply_Relation_In_Scene(new_relation) # Apply new one to scene
    Update_Relations_Display()
    print(f"Applied relation: {child} -> {parent} ({constraint_type})")

def Update_Relations_Display(*args):
    """Refreshes the 'relationsListUI' with data from the global 'relations' list."""
    if not cmds.textScrollList('relationsListUI', exists=True):
        return
        
    cmds.textScrollList('relationsListUI', e=True, removeAll=True)
    
    for rel in relations:
        child = rel['child']
        parent = rel['parent']
        rel_type = rel['type']
        mo = rel['maintain_offset']
        
        display_string = f"{child}  <-  {parent}  [{rel_type}, MO={mo}]"
        cmds.textScrollList('relationsListUI', e=True, append=display_string)

def Remove_Selected_Relation(*args):
    """Removes the selected relation from the UI, the global list, and the scene."""
    selected_indices = cmds.textScrollList('relationsListUI', q=True, selectIndexedItem=True)
    
    if not selected_indices:
        cmds.warning("No relation selected to remove.")
        return
        
    # Get 0-based index
    selected_index_0based = selected_indices[0] - 1
    
    if 0 <= selected_index_0based < len(relations):
        rel_to_remove = relations.pop(selected_index_0based)
        Remove_Relation_In_Scene(rel_to_remove)
        Update_Relations_Display()
        print(f"Removed relation: {rel_to_remove['child']} -> {rel_to_remove['parent']}")
    else:
        cmds.warning("Selected index out of bounds. Please refresh.")

def Clear_All_Relations(*args):
    """Removes ALL relations from the list and the scene after confirmation."""
    result = cmds.confirmDialog(title='Confirm Clear',
                                message='Are you sure you want to remove ALL relations?',
                                button=['Yes', 'No'], defaultButton='No',
                                cancelButton='No', dismissString='No')
    
    if result == 'Yes':
        # Use list() to create a copy so we can modify the original
        for rel in list(relations): 
            Remove_Relation_In_Scene(rel)
        
        relations.clear()
        Update_Relations_Display()
        print("All relations cleared.")

def Apply_Relation_In_Scene(relation_dict):
    """Applies a single relation to the live rig nodes in the scene."""
    child_part = relation_dict['child']
    parent_part = relation_dict['parent']
    rel_type = relation_dict['type']
    mo = relation_dict['maintain_offset']
    
    # Get node names from parts_attr
    child_grp = parts_attr.get(child_part, {}).get('grp')
    parent_ctrl = parts_attr.get(parent_part, {}).get('ctrl', [None])[0]
    
    # Check if nodes exist
    if not child_grp or not cmds.objExists(child_grp):
        print(f"Apply Relation: Child group for '{child_part}' not found. Skipping.")
        return
    if not parent_ctrl or not cmds.objExists(parent_ctrl):
        print(f"Apply Relation: Parent controller for '{parent_part}' not found. Skipping.")
        return

    # First, remove any existing relations on this child
    Remove_Relation_In_Scene(relation_dict)

    # Apply new relation
    print(f"Applying {rel_type} constraint: {parent_ctrl} -> {child_grp}")
    try:
        if rel_type == 'direct':
            cmds.parent(child_grp, parent_ctrl)
        elif rel_type == 'parent':
            cmds.parentConstraint(parent_ctrl, child_grp, mo=mo)
        elif rel_type == 'point':
            cmds.pointConstraint(parent_ctrl, child_grp, mo=mo)
        elif rel_type == 'orient':
            cmds.orientConstraint(parent_ctrl, child_grp, mo=mo)
        elif rel_type == 'scale':
            cmds.scaleConstraint(parent_ctrl, child_grp, mo=mo)
        elif rel_type == 'all':
            cmds.parentConstraint(parent_ctrl, child_grp, mo=mo)
            cmds.scaleConstraint(parent_ctrl, child_grp, mo=mo)
    except Exception as e:
        cmds.warning(f"Failed to apply relation {parent_ctrl} -> {child_grp}: {str(e)}")


def Remove_Relation_In_Scene(relation_dict):
    """Finds and removes any constraints or direct parenting on the child part's group."""
    child_part = relation_dict['child']
    child_grp = parts_attr.get(child_part, {}).get('grp')
    
    if not child_grp or not cmds.objExists(child_grp):
        # Child group doesn't exist, nothing to remove
        return

    # 1. Delete constraints
    # Find constraints targeting the child group
    constraints = cmds.listRelatives(child_grp, type='constraint', allDescendents=False)
    if constraints:
        print(f"Removing constraints from {child_grp}: {constraints}")
        try:
            cmds.delete(constraints)
        except Exception as e:
            cmds.warning(f"Could not delete constraints: {str(e)}")

    # 2. Unparent from direct parenting
    current_parent = cmds.listRelatives(child_grp, parent=True)
    if current_parent:
        # Check if parent is a known controller
        all_ctrl_names = [parts_attr[p]['ctrl'][0] for p in parts_attr if 'ctrl' in parts_attr[p] and parts_attr[p]['ctrl']]
        if current_parent[0] in all_ctrl_names:
            print(f"Unparenting {child_grp} from {current_parent[0]}")
            try:
                cmds.parent(child_grp, world=True)
            except Exception as e:
                # This might fail if it's locked, but we try
                cmds.warning(f"Could not unparent {child_grp}: {str(e)}")

def Apply_All_Relations_To_Scene(*args):
    """Loops through the global 'relations' list and applies each one."""
    print("Applying all stored relations...")
    for rel in relations:
        Apply_Relation_In_Scene(rel)
    print("Finished applying relations.")


# --- NEW FUNCTION ---
def Toggle_All_Frames(frame_key, collapse_state, *args):
    """
    Collapses or expands all frames stored in parts_attr under a specific key.
    frame_key (str): The key in parts_attr[part] holding the frame name (e.g., 'ui_partFrame')
    collapse_state (bool): True to collapse, False to expand.
    """
    for part in parts:
        if part in parts_attr and frame_key in parts_attr[part]:
            frame_name = parts_attr[part][frame_key]
            if frame_name and cmds.frameLayout(frame_name, exists=True):
                try:
                    cmds.frameLayout(frame_name, edit=True, collapse=collapse_state)
                except Exception as e:
                    print(f"Error toggling frame {frame_name}: {e}")
# --- END NEW FUNCTION ---


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


# --- (No changes to Create_AI_Tab and AI functions) ---

def Create_AI_Tab(*args):
    """Tab 5: AI Generator"""
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10, columnAttach=('both', 5))
    
    cmds.separator(height=5, style='none')
    
    # --- AI Configuration Section ---
    cmds.frameLayout(label='AI Settings', collapsable=False,
                     backgroundColor=[0.25, 0.25, 0.25],
                     marginWidth=5, marginHeight=10)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8, columnAttach=('both', 5))

    # Dropdown for AI provider
    cmds.text(label='Select AI Provider:', align='left')
    cmds.optionMenu('aiProviderMenu', label='', changeCommand=update_ai_provider_help)
    cmds.menuItem(label='Google Gemini')
    cmds.menuItem(label='OpenAI GPT')
    cmds.menuItem(label='Anthropic Claude')
    cmds.menuItem(label='Custom API')

    cmds.separator(height=5, style='none')

    # Help text for selected provider
    cmds.text('aiProviderHelpText', 
              label='Enter your Gemini API key and optionally specify a model (default: gemini-2.0-flash-exp)',
              align='left', wordWrap=True, height=40,
              backgroundColor=[0.2, 0.25, 0.3])

    cmds.separator(height=5, style='none')

    # Input for API key
    cmds.text(label='API Key:', align='left')
    cmds.textField('aiApiKeyField', placeholderText='Enter your API key here...', height=30)

    # Input for Model name
    cmds.text(label='Model Name / Endpoint:', align='left')
    cmds.textField('aiModelNameField', 
                   placeholderText='e.g., gemini-2.0-flash-exp or gpt-4o-mini', 
                   height=30)

    cmds.separator(height=10, style='in')
    cmds.setParent('..')
    cmds.setParent('..')

    # --- AI Prompt Section ---
    cmds.frameLayout(label='AI-Powered Configuration Generator', collapsable=False,
                     backgroundColor=[0.25, 0.25, 0.25],
                     marginWidth=5, marginHeight=10)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8, columnAttach=('both', 5))
    cmds.separator(height=5, style='none')
    
    cmds.text(label='Describe the vehicle you want to rig.\n'
                    'The AI will attempt to generate the parts list and default transforms.', 
              align='left')
    
    cmds.separator(height=5, style='in')
    
    cmds.scrollField('aiPromptField', 
                     text='e.g., "A simple 4-wheel car with a chassis and four wheels: Wheel_FL, Wheel_FR, Wheel_BL, Wheel_BR"',
                     wordWrap=True, height=150, font='plainLabelFont')
    
    cmds.separator(height=5, style='none')
    
    cmds.button(label='Generate and Load Configuration', 
                command=Generate_With_AI,
                height=40,
                backgroundColor=[0.3, 0.5, 0.7])
    
    cmds.separator(height=5, style='in')
    
    cmds.text('aiStatusText', 
              label='Status: Ready',
              align='left', height=30,
              backgroundColor=[0.2, 0.2, 0.2])
    
    cmds.separator(height=5, style='none')
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(height=10, style='none')
    cmds.setParent('..')


def update_ai_provider_help(*args):
    """Update help text based on selected provider"""
    try:
        provider = cmds.optionMenu('aiProviderMenu', q=True, value=True)
        
        help_texts = {
            'Google Gemini': 'Enter your Gemini API key and optionally specify a model (default: gemini-2.0-flash-exp)',
            'OpenAI GPT': 'Enter your OpenAI API key and optionally specify a model (default: gpt-4o-mini)',
            'Anthropic Claude': 'Enter your Anthropic API key and optionally specify a model (default: claude-3-5-sonnet-20241022)',
            'Custom API': 'For Hugging Face: Enter HF token as API key and model name (e.g., mistralai/Mistral-7B-Instruct-v0.2)\nFor other APIs: Enter full endpoint URL in Model Name field'
        }
        
        help_text = help_texts.get(provider, 'Select a provider and configure settings')
        
        if cmds.text('aiProviderHelpText', exists=True):
            cmds.text('aiProviderHelpText', edit=True, label=help_text)
            
    except Exception:
        pass

def Generate_With_AI(*args):
    """Get prompt, call AI, and load the resulting config data"""
    # 1. Get prompt from UI
    prompt = cmds.scrollField('aiPromptField', q=True, text=True)
    if not prompt:
        cmds.warning("Please enter a description in the AI prompt field.")
        cmds.text('aiStatusText', e=True, label='Status: Error - Prompt is empty.',
                  backgroundColor=[0.5, 0.2, 0.2])
        return
        
    cmds.text('aiStatusText', e=True, label='Status: Calling AI model... (Using placeholder)',
              backgroundColor=[0.6, 0.4, 0.2])
    
    try:
        # 2. Call the (placeholder) AI model
        #    This function returns a Python dictionary, not a JSON string
        ai_generated_data = call_ai_model(prompt)
        
        if not ai_generated_data:
            cmds.warning("AI (placeholder) returned no data.")
            cmds.text('aiStatusText', e=True, label='Status: Error - AI returned no data.',
                      backgroundColor=[0.5, 0.2, 0.2])
            return
            
        cmds.text('aiStatusText', e=True, label='Status: AI data received. Loading configuration...',
                  backgroundColor=[0.2, 0.5, 0.3])
                  
        # 3. Load the data into the tool
        #    This function is shared with the Import button
        Load_Config_Data(ai_generated_data)
        
        cmds.text('aiStatusText', e=True, label=f"Status: Success! Loaded {len(ai_generated_data.get('parts', []))} parts.",
                  backgroundColor=[0.2, 0.5, 0.3])
                  
    except Exception as e:
        cmds.text('aiStatusText', e=True, label=f"Status: Error - {str(e)}",
                  backgroundColor=[0.5, 0.2, 0.2])
        cmds.confirmDialog(
            title='AI Generation Error',
            message=f'Failed to generate or load AI configuration:\n{str(e)}',
            button=['OK'],
            defaultButton='OK'
        )

def call_ai_model(prompt):
    """
    Unified AI caller that reads provider, api key, and model from the UI and returns a Python dict.

    Handles:
      - Google Gemini (google.generativeai as genai)
      - OpenAI (supports both pre-1.0 and post-1.0 openai-python interfaces)
      - Anthropic (claude)
      - Custom API (Hugging Face, local models, etc.)
    """
    # Read UI values (graceful fallbacks)
    try:
        provider = cmds.optionMenu('aiProviderMenu', q=True, value=True) if cmds.optionMenu('aiProviderMenu', exists=True) else 'Google Gemini'
    except Exception:
        provider = 'Google Gemini'
    try:
        API_KEY = cmds.textField('aiApiKeyField', q=True, text=True) if cmds.textField('aiApiKeyField', exists=True) else ''
    except Exception:
        API_KEY = ''
    try:
        model_name = cmds.textField('aiModelNameField', q=True, text=True) if cmds.textField('aiModelNameField', exists=True) else ''
    except Exception:
        model_name = ''

    if not API_KEY and 'custom' not in provider.lower():
        try:
            cmds.confirmDialog(title='API Key Missing',
                               message='No API key found. Please enter your API key in the AI Settings tab.',
                               button=['OK'], defaultButton='OK')
        except Exception:
            pass
        raise Exception('API key not provided in UI (aiApiKeyField).')

    # System prompt instructs models to return only JSON with the expected schema.
    system_prompt = """
    You are a technical rigging assistant for Autodesk Maya. Your task is to generate a JSON configuration for a car rig based on a user's prompt.
    You MUST return ONLY a valid JSON object, and nothing else. Do not wrap the JSON in markdown (```json ... ```).
    The JSON object must have two top-level keys: "parts" (a list of part names) and "parts_config" (an object mapping part names to their settings).

    The structure for each part in "parts_config" MUST be:
    {
        "enabled": true,
        "color": {"R": float, "G": float, "B": float},
        "axis": "x", "y", or "z",
        "shape": "Circle", "Box", "Triangle", or "Arrow (4-Point)",
        "size": float,
        "controller_transforms": {
            "tx": bool, "ty": bool, "tz": bool,
            "rx": bool, "ry": bool, "rz": bool,
            "sx": bool, "sy": bool, "sz": bool
        },
        "bone_data": {
            "translate": {"x": float, "y": float, "z": float},
            "rotate": {"x": float, "y": float, "z": float},
            "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
            "orientation": {"x": 0.0, "y": 0.0, "z": 0.0}
        }
    }

    - For wheels, the "axis" should typically be 'x'.
    - For a chassis or main body, "axis" can be 'z' or 'y'.
    - Guess reasonable translate values for standard car layout.
    - Set controller transform booleans appropriately (e.g., wheel: only rotation enabled).
    - Return a well-formed JSON object only.
    """

    # JSON extraction helper (tries a few heuristics)
    def extract_json_from_text(text):
        try:
            return json.loads(text)
        except Exception:
            pass

        # Remove markdown code blocks if present
        if '```json' in text:
            start = text.find('```json') + 7
            end = text.find('```', start)
            if end != -1:
                text = text[start:end].strip()
                try:
                    return json.loads(text)
                except Exception:
                    pass
        elif '```' in text:
            start = text.find('```') + 3
            end = text.find('```', start)
            if end != -1:
                text = text[start:end].strip()
                try:
                    return json.loads(text)
                except Exception:
                    pass

        # First/last braces heuristic
        first = text.find('{')
        last = text.rfind('}')
        if first != -1 and last != -1 and last > first:
            snippet = text[first:last+1]
            try:
                return json.loads(snippet)
            except Exception:
                pass

        # Balanced-braces scan for first valid JSON object
        stack = []
        start_idx = -1
        for i, ch in enumerate(text):
            if ch == '{':
                if start_idx == -1:
                    start_idx = i
                stack.append(i)
            elif ch == '}':
                if stack:
                    stack.pop()
                    if not stack:
                        candidate = text[start_idx:i+1]
                        try:
                            return json.loads(candidate)
                        except Exception:
                            start_idx = -1
                            continue
        raise Exception('Failed to parse JSON from AI response.')

    # Generic text extractor for provider responses (tries lots of shapes)
    def extract_text_from_response(resp_obj):
        # If it's already a string
        if isinstance(resp_obj, str):
            return resp_obj

        # Try attribute-style FIRST (new openai client responses >= 1.0)
        try:
            # e.g., resp.choices[0].message.content
            choices_attr = getattr(resp_obj, 'choices', None)
            if choices_attr:
                first_choice = choices_attr[0]
                # attribute message
                msg = getattr(first_choice, 'message', None)
                if msg is not None:
                    content = getattr(msg, 'content', None)
                    # content might be a list of fragments
                    if isinstance(content, str):
                        return content
                    try:
                        # try first element then its text
                        if isinstance(content, (list, tuple)) and len(content) > 0:
                            c0 = content[0]
                            txt = getattr(c0, 'text', None) or getattr(c0, 'content', None)
                            if isinstance(txt, str):
                                return txt
                    except Exception:
                        pass
                # old-style: first_choice.text
                text_attr = getattr(first_choice, 'text', None)
                if isinstance(text_attr, str):
                    return text_attr
        except Exception:
            pass

        # Try dict-like access (for older versions)
        try:
            # openai v0.x style dict
            if isinstance(resp_obj, dict):
                choices = resp_obj.get('choices')
                if choices and len(choices) > 0:
                    first = choices[0]
                    # try message.content
                    if isinstance(first, dict):
                        msg = first.get('message')
                        if isinstance(msg, dict):
                            content = msg.get('content')
                            if isinstance(content, str):
                                return content
                            # content might be list
                            if isinstance(content, list) and len(content) > 0:
                                candidate = content[0]
                                if isinstance(candidate, dict):
                                    return candidate.get('text') or candidate.get('content') or json.dumps(candidate)
                                else:
                                    return str(candidate)
                        # fallback: first.get('text')
                        if 'text' in first and isinstance(first.get('text'), str):
                            return first.get('text')
                    # fallback stringify
                    return json.dumps(first)
        except Exception:
            pass

        # As a last resort, stringify the entire response
        try:
            return str(resp_obj)
        except Exception:
            raise Exception('Unable to extract text from provider response.')

    provider_lower = provider.lower()

    # ----------------------------
    # Google Gemini branch
    # ----------------------------
    if 'google' in provider_lower or 'gemini' in provider_lower:
        try:
            genai.configure(api_key=API_KEY)
            if not model_name:
                model_name = 'gemini-2.0-flash-exp'
            model = genai.GenerativeModel(model_name)
            generation_config = genai.GenerationConfig(response_mime_type="application/json")
            full_prompt = [system_prompt, "USER PROMPT: " + prompt]
            response = model.generate_content(full_prompt, generation_config=generation_config)
            json_response_text = response.text
            ai_data = extract_json_from_text(json_response_text)
            return ai_data
        except Exception as e:
            raise Exception(f"Google Gemini error: {str(e)}")

    # ----------------------------
    # OpenAI branch (CHECK NEW API FIRST)
    # ----------------------------
    elif 'openai' in provider_lower or 'gpt' in provider_lower:
        try:
            try:
                import openai
            except Exception:
                raise Exception("openai package not installed. Install it (pip install openai).")

            # Choose defaults if none provided
            if not model_name:
                model_name = 'gpt-4o-mini'

            # NEW SDK FIRST (>=1.0) - Check for OpenAI class
            if hasattr(openai, 'OpenAI'):
                try:
                    client = openai.OpenAI(api_key=API_KEY)
                    
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                    
                    resp = client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        temperature=0.0,
                        max_tokens=1200
                    )
                    
                    text = extract_text_from_response(resp)
                    ai_data = extract_json_from_text(text)
                    return ai_data
                    
                except Exception as e:
                    # If new API fails, provide helpful error
                    raise Exception(f"OpenAI new API error: {str(e)}")
            
            # OLD SDK (pre-1.0) - Only check if new API not available
            elif hasattr(openai, 'ChatCompletion'):
                try:
                    openai.api_key = API_KEY
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                    resp = openai.ChatCompletion.create(
                        model=model_name,
                        messages=messages,
                        temperature=0.0,
                        max_tokens=1200
                    )
                    text = extract_text_from_response(resp)
                    ai_data = extract_json_from_text(text)
                    return ai_data
                except Exception as e:
                    raise Exception(f"OpenAI legacy API error: {str(e)}")
            
            else:
                raise Exception("Could not find compatible OpenAI API interface. Please ensure openai package is installed correctly.")

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    # ----------------------------
    # Anthropic (Claude) branch
    # ----------------------------
    elif 'anthropic' in provider_lower or 'claude' in provider_lower:
        try:
            try:
                import anthropic
            except ImportError:
                raise Exception("anthropic package not installed. Install it (pip install anthropic).")

            if not model_name:
                model_name = 'claude-3-5-sonnet-20241022'
            
            client = anthropic.Anthropic(api_key=API_KEY)
            
            response = client.messages.create(
                model=model_name,
                max_tokens=1200,
                temperature=0.0,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract text from response
            text = response.content[0].text if response.content else str(response)
            ai_data = extract_json_from_text(text)
            return ai_data

        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")

    # ----------------------------
    # Custom API branch (Hugging Face, local models, etc.)
    # ----------------------------
    elif 'custom' in provider_lower:
        try:
            # Try using requests for HTTP API calls
            try:
                import requests
            except ImportError:
                raise Exception("requests package not installed. Install it (pip install requests) to use Custom API.")
    
            # Check if we have an API endpoint in the model name field
            if not model_name:
                raise Exception("Please enter either:\n1. Hugging Face model name (e.g., mistralai/Mistral-7B-Instruct-v0.2)\n2. Full API endpoint URL")
            
            # Determine if it's a URL or a model name
            if model_name.startswith('http://') or model_name.startswith('https://'):
                # Full URL provided
                api_url = model_name
            else:
                # Hugging Face Inference API - use the correct endpoint
                # Remove any leading/trailing whitespace
                model_name = model_name.strip()
                api_url = f"https://api-inference.huggingface.co/models/{model_name}"
            
            print(f"Custom API: Calling {api_url}")
            
            # Prepare headers
            headers = {
                "Content-Type": "application/json"
            }
            
            if API_KEY:
                # Clean the API key
                api_key_clean = API_KEY.strip()
                headers["Authorization"] = f"Bearer {api_key_clean}"
            
            # Combine system prompt and user prompt for better results
            full_prompt = f"{system_prompt}\n\nUSER REQUEST:\n{prompt}\n\nRemember: Return ONLY the JSON object, no explanatory text before or after."
            
            # Hugging Face Inference API payload
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": 2000,
                    "temperature": 0.1,
                    "return_full_text": False,
                    "top_p": 0.95,
                    "do_sample": True
                },
                "options": {
                    "wait_for_model": True,
                    "use_cache": False
                }
            }
            
            print(f"Custom API: Sending request...")
            
            # Make the request with longer timeout
            response = requests.post(api_url, headers=headers, json=payload, timeout=180)
            
            # Handle different status codes
            if response.status_code == 404:
                raise Exception(f"Model not found: {model_name}\n\nMake sure:\n1. Model name is correct (check on huggingface.co)\n2. Model exists and is public\n3. Model supports text-generation task\n\nTry one of these tested models:\n- mistralai/Mistral-7B-Instruct-v0.2\n- meta-llama/Meta-Llama-3-8B-Instruct\n- google/flan-t5-xxl")
            
            elif response.status_code == 401:
                raise Exception("Invalid API token. Please check your Hugging Face token in the API Key field.")
            
            elif response.status_code == 403:
                raise Exception("Access forbidden. This model may require:\n1. Accepting the model's license on huggingface.co\n2. A Pro subscription\n3. Special permissions")
            
            elif response.status_code == 503:
                # Model is loading
                error_msg = response.json().get('error', 'Model is loading')
                estimated_time = response.json().get('estimated_time', 20)
                
                print(f"Custom API: Model is loading, estimated time: {estimated_time}s")
                cmds.text('aiStatusText', e=True, 
                         label=f'Status: Model loading, waiting {estimated_time}s...',
                         backgroundColor=[0.6, 0.4, 0.2])
                
                # Wait for the model to load
                import time
                time.sleep(max(estimated_time, 20))
                
                # Retry the request
                print(f"Custom API: Retrying after model load...")
                response = requests.post(api_url, headers=headers, json=payload, timeout=180)
            
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded. Please wait a few minutes or upgrade to HF Pro.")
            
            elif response.status_code != 200:
                error_detail = response.text
                try:
                    error_json = response.json()
                    error_detail = error_json.get('error', error_detail)
                except:
                    pass
                raise Exception(f"API request failed with status {response.status_code}:\n{error_detail}")
            
            # Parse response
            result = response.json()
            print(f"Custom API: Response received, type: {type(result)}")
            
            # Extract text from various response formats
            text = None
            
            # Hugging Face text-generation format (most common)
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], dict):
                    text = result[0].get('generated_text') or result[0].get('text')
                    if text:
                        print(f"Custom API: Extracted from HF list format")
            
            # Dict format
            elif isinstance(result, dict):
                # Check for error first
                if 'error' in result:
                    raise Exception(f"API returned error: {result['error']}")
                
                # Try various field names
                text = (result.get('generated_text') or 
                       result.get('text') or 
                       result.get('output') or
                       result.get('completion'))
                
                # OpenAI-compatible format
                if not text and 'choices' in result and len(result['choices']) > 0:
                    choice = result['choices'][0]
                    if 'message' in choice:
                        text = choice['message'].get('content')
                    elif 'text' in choice:
                        text = choice['text']
                
                if text:
                    print(f"Custom API: Extracted from dict format")
            
            if not text:
                # Last resort: stringify the whole response
                print(f"Custom API: Using full response as text")
                text = json.dumps(result) if isinstance(result, (dict, list)) else str(result)
            
            print(f"Custom API: Extracted text length: {len(text)} characters")
            print(f"Custom API: First 500 chars:\n{text[:500]}")
            
            # Extract JSON from the text
            ai_data = extract_json_from_text(text)
            
            if not ai_data:
                raise Exception(f"Could not extract valid JSON from response.\n\nReceived text preview:\n{text[:1000]}\n\nPlease try:\n1. A different model\n2. Simplifying your prompt\n3. Running the generation again")
            
            # Validate the structure
            if 'parts' not in ai_data or 'parts_config' not in ai_data:
                raise Exception(f"AI generated invalid structure. Missing 'parts' or 'parts_config' keys.\n\nReceived: {list(ai_data.keys())}")
            
            print(f"Custom API: Successfully parsed JSON with {len(ai_data.get('parts', []))} parts")
            
            return ai_data
    
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. The model may be too slow. Try:\n1. A smaller/faster model\n2. Waiting a moment and trying again")
        
        except requests.exceptions.ConnectionError:
            raise Exception("Connection error. Check your internet connection.")
        
        except Exception as e:
            # If it's already our custom exception, re-raise it
            if "Model not found" in str(e) or "API request failed" in str(e):
                raise e
            # Otherwise wrap it
            raise Exception(f"Custom API error: {str(e)}")

    else:
        raise Exception(f"Provider '{provider}' not supported. Choose Google Gemini, OpenAI GPT, Anthropic Claude, or Custom API.")
# --- END NEW AI TAB FUNCTIONS ---


# --- (No changes to set_axis) ---
def set_axis(part, axis, *args):
    """Set the controller orientation axis for a part"""
    parts_attr[part]['axisValue'] = axis
    print(f"{part} - Controller axis set to: {axis.upper()}")

# --- (No changes to controller shape functions) ---
def create_circle_ctrl(name, size, normal):
    """Creates a circle controller"""
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
        print(f"Warning: Unknown shape '{shape_type}'. Defaulting to Circle.")
        return create_circle_ctrl(name, size, normal)

# --- (No changes to Create_Bones) ---
def Create_Bones(*args):
    Save_UI_Values()
    
    for part in parts:
        is_enabled = parts_attr[part].get('isCheckedValue', True)
        if 'isChecked' in parts_attr[part] and cmds.checkBox(parts_attr[part]['isChecked'], exists=True):
            is_enabled = cmds.checkBox(parts_attr[part]['isChecked'], q=True, v=True)
        
        if is_enabled:
            parts_attr[part]['relative_bone'] = cmds.joint(n= part + '_jnt', p=(0, 0, 0))
            
            tx = parts_attr[part].get('bone_txValue', 0.0)
            ty = parts_attr[part].get('bone_tyValue', 0.0)
            tz = parts_attr[part].get('bone_tzValue', 0.0)
            if 'bone_tx' in parts_attr[part] and cmds.floatField(parts_attr[part]['bone_tx'], exists=True):
                tx = cmds.floatField(parts_attr[part]['bone_tx'], q=True, value=True)
                ty = cmds.floatField(parts_attr[part]['bone_ty'], q=True, value=True)
                tz = cmds.floatField(parts_attr[part]['bone_tz'], q=True, value=True)
            cmds.setAttr(parts_attr[part]['relative_bone'] + '.translate', tx, ty, tz)
            
            rx = parts_attr[part].get('bone_rxValue', 0.0)
            ry = parts_attr[part].get('bone_ryValue', 0.0)
            rz = parts_attr[part].get('bone_rzValue', 0.0)
            if 'bone_rx' in parts_attr[part] and cmds.floatField(parts_attr[part]['bone_rx'], exists=True):
                rx = cmds.floatField(parts_attr[part]['bone_rx'], q=True, value=True)
                ry = cmds.floatField(parts_attr[part]['bone_ry'], q=True, value=True)
                rz = cmds.floatField(parts_attr[part]['bone_rz'], q=True, value=True)
            cmds.setAttr(parts_attr[part]['relative_bone'] + '.rotate', rx, ry, rz)
            
            sx = parts_attr[part].get('bone_sxValue', 1.0)
            sy = parts_attr[part].get('bone_syValue', 1.0)
            sz = parts_attr[part].get('bone_szValue', 1.0)
            if 'bone_sx' in parts_attr[part] and cmds.floatField(parts_attr[part]['bone_sx'], exists=True):
                sx = cmds.floatField(parts_attr[part]['bone_sx'], q=True, value=True)
                sy = cmds.floatField(parts_attr[part]['bone_sy'], q=True, value=True)
                sz = cmds.floatField(parts_attr[part]['bone_sz'], q=True, value=True)
            cmds.setAttr(parts_attr[part]['relative_bone'] + '.scale', sx, sy, sz)
            
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


# --- (No changes to Create_Ctrls) ---
def Create_Ctrls(*args):
    Save_UI_Values()
    
    for part in parts:
        is_enabled = parts_attr[part].get('isCheckedValue', True)
        if 'isChecked' in parts_attr[part] and cmds.checkBox(parts_attr[part]['isChecked'], exists=True):
            is_enabled = cmds.checkBox(parts_attr[part]['isChecked'], q=True, v=True)
        
        if is_enabled:
            axis = parts_attr[part].get('axisValue', 'z')
            normal = (1, 0, 0) if axis == 'x' else (0, 1, 0) if axis == 'y' else (0, 0, 1)
            shape = parts_attr[part].get('shapeValue', 'Circle')
            size = parts_attr[part].get('sizeValue', 1.0)
            ctrl_name = part + '_ctrl'
            new_ctrl_name = create_controller_shape(shape, ctrl_name, size, normal)
            
            parts_attr[part]['ctrl'] = [new_ctrl_name] 
            parts_attr[part]['grp'] = cmds.group(str(parts_attr[part]['ctrl'][0]), name=part + '_grp')
            
            ctrls.append(str(parts_attr[part]['ctrl'][0]))
            
            r = parts_attr[part]['color']['R']
            g = parts_attr[part]['color']['G']
            b = parts_attr[part]['color']['B']
            
            cmds.setAttr(parts_attr[part]['ctrl'][0] + '.overrideEnabled', 1)
            cmds.setAttr(parts_attr[part]['ctrl'][0] + '.overrideRGBColors', 1)
            cmds.setAttr(parts_attr[part]['ctrl'][0] + '.overrideColorRGB', r, g, b)
            
            attrs_to_check = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
            
            if 'relative_bone' in parts_attr[part] and cmds.objExists(parts_attr[part]['relative_bone']):
                cmds.matchTransform(parts_attr[part]['grp'], parts_attr[part]['relative_bone'])
            
            for attr in attrs_to_check:
                attr_enabled = parts_attr[part].get(attr + 'Value', True if attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz'] else False)
                if attr in parts_attr[part] and cmds.checkBox(parts_attr[part][attr], exists=True):
                    attr_enabled = cmds.checkBox(parts_attr[part][attr], q=True, v=True)
                
                if not attr_enabled:
                    cmds.setAttr(f"{parts_attr[part]['ctrl'][0]}.{attr}", 
                               lock=True, keyable=False, channelBox=False)
    
    print("Controllers created successfully!")


# --- (No changes to get_color_from_picker) ---
def get_color_from_picker(part, *args):
    result = cmds.colorEditor()
    values = result.split()
    
    if len(values) == 4:
        r = float(values[0])
        g = float(values[1])
        b = float(values[2])
        confirmed = int(values[3])
        
        if confirmed:
            parts_attr[part]['color']['R'] = r
            parts_attr[part]['color']['G'] = g
            parts_attr[part]['color']['B'] = b
            print(f"{part} - Selected color: R={r}, G={g}, B={b}")
            if 'colorUI' in parts_attr[part] and cmds.canvas(parts_attr[part]['colorUI'], exists=True):
                cmds.canvas(parts_attr[part]['colorUI'], edit=True, rgbValue=(r, g, b))


# --- (No changes to Add_Custom_Part) ---
def Add_Custom_Part(*args):
    custom_name = cmds.textField('customPartNameField', query=True, text=True).strip()
    
    if not custom_name:
        cmds.confirmDialog(title='Error', 
                          message='Please enter a part name!',
                          button=['OK'],
                          defaultButton='OK')
        return
    
    if custom_name in parts:
        cmds.confirmDialog(title='Error', 
                          message=f'Part "{custom_name}" already exists!',
                          button=['OK'],
                          defaultButton='OK')
        return
    
    parts.append(custom_name)
    cmds.textField('customPartNameField', edit=True, text='')
    Refresh_All_Tabs()
    print(f"Added custom part: {custom_name}")


# --- (No changes to Refresh_All_Tabs) ---
def Refresh_All_Tabs(*args):
    """Refresh all tabs to show new parts"""
    Save_UI_Values()
    
    if cmds.scrollLayout('partsListScroll', exists=True):
        cmds.deleteUI('partsListScroll', control=True)
    # Find the parent of 'partsListScroll' - it's the column layout inside the frame
    parent_col = cmds.frameLayout('partsTab|mainColumnLayout|partsTab|partsList|columnLayout', q=True, fullPathName=True) # This path might be fragile
    
    # Let's try to make the parent structure more robust in Create_Parts_Tab
    # For now, let's assume the hierarchy is correct.
    
    # Re-find parent layout more robustly
    if cmds.scrollLayout('partsTab', exists=True):
        cmds.setParent('partsTab')
        
        # Need to delete the old scroll layout AND its container
        if cmds.frameLayout('partsListFrame', exists=True): # Let's name the frame
            cmds.deleteUI('partsListFrame')
        
        # --- This part is tricky. Let's rebuild the *contents* of the tabs
        
        # Delete old UI content
        if cmds.scrollLayout('partsTab', exists=True):
            children = cmds.scrollLayout('partsTab', q=True, childArray=True)
            if children:
                for child in children:
                    cmds.deleteUI(child)
        
        if cmds.scrollLayout('boneDataTab', exists=True):
            children = cmds.scrollLayout('boneDataTab', q=True, childArray=True)
            if children:
                for child in children:
                    cmds.deleteUI(child)

        if cmds.scrollLayout('relationsTab', exists=True):
            children = cmds.scrollLayout('relationsTab', q=True, childArray=True)
            if children:
                for child in children:
                    cmds.deleteUI(child)

        # Re-create tab content
        cmds.setParent('partsTab')
        Create_Parts_Tab()
        
        cmds.setParent('boneDataTab')
        Create_Bone_Data_Tab()
        
        cmds.setParent('relationsTab')
        Create_Relations_Tab() # This already handles dropdowns
        
        # Update dropdowns in Relations Tab (which is now rebuilt, so this is redundant)
        # But Create_Relations_Tab reads the global 'parts' list, so it's fine.
    
    print("UI Refreshed.")


# --- (No changes to Save_UI_Values) ---
def Save_UI_Values(*args):
    """Save current UI values before refreshing"""
    for part in parts:
        if part in parts_attr:
            # Check if UI elements exist before querying
            if 'isChecked' in parts_attr[part] and cmds.checkBox(parts_attr[part]['isChecked'], exists=True):
                parts_attr[part]['isCheckedValue'] = cmds.checkBox(parts_attr[part]['isChecked'], q=True, v=True)
            
            for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']:
                if attr in parts_attr[part] and cmds.checkBox(parts_attr[part][attr], exists=True):
                    parts_attr[part][attr + 'Value'] = cmds.checkBox(parts_attr[part][attr], q=True, v=True)
            
            if 'shapeMenu' in parts_attr[part] and cmds.optionMenu(parts_attr[part]['shapeMenu'], exists=True):
                parts_attr[part]['shapeValue'] = cmds.optionMenu(parts_attr[part]['shapeMenu'], q=True, v=True)
            
            if 'sizeField' in parts_attr[part] and cmds.floatField(parts_attr[part]['sizeField'], exists=True):
                parts_attr[part]['sizeValue'] = cmds.floatField(parts_attr[part]['sizeField'], q=True, v=True)

            bone_attrs = ['bone_tx', 'bone_ty', 'bone_tz', 'bone_rx', 'bone_ry', 'bone_rz', 
                         'bone_sx', 'bone_sy', 'bone_sz', 'orient_x', 'orient_y', 'orient_z']
            for attr in bone_attrs:
                if attr in parts_attr[part] and cmds.floatField(parts_attr[part][attr], exists=True):
                    parts_attr[part][attr + 'Value'] = cmds.floatField(parts_attr[part][attr], q=True, value=True)


# --- (No changes to Delete_Rig) ---
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
                if parts_attr[part]['ctrl'] and cmds.objExists(str(parts_attr[part]['ctrl'][0])):
                    cmds.delete(str(parts_attr[part]['ctrl'][0]))
            if 'grp' in parts_attr[part]:
                if cmds.objExists(parts_attr[part]['grp']):
                    cmds.delete(parts_attr[part]['grp'])
            if 'relative_bone' in parts_attr[part]:
                if cmds.objExists(parts_attr[part]['relative_bone']):
                    cmds.delete(parts_attr[part]['relative_bone'])
        
        ctrls.clear()
        for part in parts_attr:
            parts_attr[part].pop('ctrl', None)
            parts_attr[part].pop('grp', None)
            parts_attr[part].pop('relative_bone', None)
            # --- NEW: Clear stale UI references ---
            parts_attr[part].pop('ui_partFrame', None)
            parts_attr[part].pop('ui_boneFrame', None)
            
        print("Rig deleted successfully!")


# --- (No changes to Build_Full_Rig) ---
def Build_Full_Rig(*args):
    Create_Bones()
    Create_Ctrls()
    Apply_All_Relations_To_Scene() 
    print("Rig created successfully!")
    print(parts_attr)
    cmds.confirmDialog(title='Success', 
                      message='Rig has been created successfully!',
                      button=['OK'],
                      defaultButton='OK')


# --- (No changes to Export_Rig_Config) ---
def Export_Rig_Config(*args):
    """Export rig configuration to JSON file"""
    print("Export function called!")
    Save_UI_Values()
    
    export_data = {
        'parts': parts,
        'parts_config': {},
        'relations': relations 
    }
    
    for part in parts:
        if part in parts_attr:
            part_config = {
                'enabled': parts_attr[part].get('isCheckedValue', True),
                'color': parts_attr[part].get('color', {'R': 0.5, 'G': 0.5, 'B': 0.5}),
                'axis': parts_attr[part].get('axisValue', 'z'),
                'shape': parts_attr[part].get('shapeValue', 'Circle'),
                'size': parts_attr[part].get('sizeValue', 1.0),
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
    
    print(f"Data prepared for export: {len(export_data['parts'])} parts, {len(export_data['relations'])} relations")
    
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
            
            if not file_path.endswith('.json'):
                file_path += '.json'
            
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


# --- (No changes to Import_Rig_Config) ---

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
            
            # Call the refactored loading function
            Load_Config_Data(import_data)
            
            print(f"Rig configuration imported from: {file_path}")
            cmds.confirmDialog(
                title='Import Successful',
                message=f'Rig configuration imported successfully!\n\nLoaded {len(parts)} parts and {len(relations)} relations.',
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

# --- (No changes to Load_Config_Data) ---
def Load_Config_Data(import_data):
    """
    Loads configuration data from a dictionary (from file or AI)
    into the tool's global variables and refreshes the UI.
    """
    global parts, parts_attr, relations 
    
    try:
        # Clear existing data
        parts = import_data.get('parts', [])
        parts_attr = {} 
        relations = import_data.get('relations', []) 
        
        # Load part configurations
        parts_config = import_data.get('parts_config', {})
        
        for part in parts:
            if part not in parts_attr:
                parts_attr[part] = {}
            
            if part in parts_config:
                config = parts_config[part]
                
                parts_attr[part]['isCheckedValue'] = config.get('enabled', True)
                parts_attr[part]['color'] = config.get('color', {'R': 0.5, 'G': 0.5, 'B': 0.5})
                
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
                
                parts_attr[part]['axisValue'] = config.get('axis', 'z')
                parts_attr[part]['shapeValue'] = config.get('shape', 'Circle')
                parts_attr[part]['sizeValue'] = config.get('size', 1.0)
                
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
        
        # --- MODIFIED: Re-create the entire UI to apply changes ---
        # This is more robust than trying to patch the existing UI
        if cmds.window('CarRigToolWindow', exists=True):
            cmds.deleteUI('CarRigToolWindow')
        global window
        window = Create_UI()
        cmds.showWindow(window)
        
    except Exception as e:
        # Re-raise the exception so the calling function can handle it
        raise Exception(f'Error while parsing config data: {str(e)}')

# --- END REFACTORED IMPORT FUNCTIONS ---


# --- (No changes to UI creation call) ---
# Create and show UI
window = Create_UI()
cmds.showWindow(window)