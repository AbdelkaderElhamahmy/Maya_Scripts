import maya.cmds as cmds

def baseRig(*args):
    #Create Spine
    cmds.joint(n = 'hip_jnt', p=(0, 15, 0))
    cmds.joint(n = 'spine01_jnt', p=(0, 19, 0))
    cmds.joint(n = 'spine02_jnt', p=(0, 22, 0))
    cmds.joint(n = 'spine03_jnt', p=(0, 25, 0))
    cmds.joint(n = 'chest_jnt', p=(0, 30, 0))
    
    #Create Neck and Head
    cmds.select('chest_jnt')
    cmds.joint(n = 'neck01_jnt', p=(0, 35, 0))
    cmds.joint(n = 'neck02_jnt', p=(0, 38, 0))
    cmds.joint(n = 'head_jnt', p=(0, 45, 0))

    #Create L_Arm
    cmds.select('chest_jnt')
    cmds.joint(n = 'l_shoulder_drv', p=(5, 33, 0))
    cmds.joint(n = 'l_elbow_drv', p=(10, 33, -1))
    cmds.joint(n = 'l_wrest_drv', p=(15, 33, 0))
    
    #Create R_Arm
    cmds.select('chest_jnt')
    cmds.joint(n = 'r_shoulder_drv', p=(-5, 33, 0))
    cmds.joint(n = 'r_elbow_drv', p=(-10, 33, -1))
    cmds.joint(n = 'r_wrest_drv', p=(-15, 33, 0))
    
    #Create L_Leg
    cmds.select('hip_jnt')
    cmds.joint(n = 'l_leg_drv', p=(5, 13, 0))
    cmds.joint(n = 'l_knee_drv', p=(5, 8, 1))
    cmds.joint(n = 'l_ankle_drv', p=(5, 0, 0))
    
    #Create R_Leg
    cmds.select('hip_jnt')
    cmds.joint(n = 'r_leg_drv', p=(-5, 13, 0))
    cmds.joint(n = 'r_knee_drv', p=(-5, 8, 1))
    cmds.joint(n = 'r_ankle_drv', p=(-5, 0, 0))
    
    # Create Left Hand Pinky Ring Middle Index Thumb 
    cmds.select('l_wrest_drv')
    cmds.joint(n = 'l_pinkey_01', p=(16, 33, 3))
    cmds.joint(n = 'l_pinkey_02', p=(17, 33, 0))
    cmds.joint(n = 'l_pinkey_03', p=(18, 33, 0))
    cmds.joint(n = 'l_pinkey_04', p=(19, 33, 0))
    cmds.joint(n = 'l_pinkey_05', p=(20, 33, 0))
    
def createFK(*args):
    #Create Fk LeftArm
    duplicated_root = cmds.duplicate('l_shoulder_drv', renameChildren=True)[0]
    duplicated_joints = cmds.listRelatives(duplicated_root, allDescendents=True, type='joint') or []
    duplicated_joints.append(duplicated_root)
    duplicated_joints.reverse() 
    for joint in duplicated_joints:
        new_name = joint.replace("_drv", "_jnt").replace("l_", "l_fk_")
        if new_name.endswith('1'):
           new_name = new_name[:-1]
        cmds.rename(joint, new_name)
        
    #Create Fk RightArm
    new_name = ''
    duplicated_root = cmds.duplicate('r_shoulder_drv', renameChildren=True)[0]
    duplicated_joints = cmds.listRelatives(duplicated_root, allDescendents=True, type='joint') or []
    duplicated_joints.append(duplicated_root)
    duplicated_joints.reverse() 
    for joint in duplicated_joints:
        new_name = joint.replace("_drv", "_jnt").replace('r_', "r_fk_", 1)
        if new_name.endswith('1'):
           new_name = new_name[:-1]
        cmds.rename(joint, new_name)
        
    #Create Fk Left Leg
    duplicated_root = cmds.duplicate('l_leg_drv', renameChildren=True)[0]
    duplicated_joints = cmds.listRelatives(duplicated_root, allDescendents=True, type='joint') or []
    duplicated_joints.append(duplicated_root)
    duplicated_joints.reverse() 
    for joint in duplicated_joints:
        new_name = joint.replace("_drv", "_jnt").replace("l_", "l_fk_")
        if new_name.endswith('1'):
           new_name = new_name[:-1]
        cmds.rename(joint, new_name)
        
    #Create Fk Right Leg
    new_name = ''
    duplicated_root = cmds.duplicate('r_leg_drv', renameChildren=True)[0]
    duplicated_joints = cmds.listRelatives(duplicated_root, allDescendents=True, type='joint') or []
    duplicated_joints.append(duplicated_root)
    duplicated_joints.reverse() 
    for joint in duplicated_joints:
        new_name = joint.replace("_drv", "_jnt").replace('r_', "r_fk_", 1)
        if new_name.endswith('1'):
           new_name = new_name[:-1]
        cmds.rename(joint, new_name) 
    
    
    
    
        
def createIK(*args):
    #Create IK LeftArm
    duplicated_root = cmds.duplicate('l_shoulder_drv', renameChildren=True)[0]
    duplicated_joints = cmds.listRelatives(duplicated_root, allDescendents=True, type='joint') or []
    duplicated_joints.append(duplicated_root)
    duplicated_joints.reverse() 
    for joint in duplicated_joints:
        new_name = joint.replace("_drv", "_jnt").replace("l_", "l_ik_")
        if new_name.endswith('1'):
           new_name = new_name[:-1]
        cmds.rename(joint, new_name)
    cmds.ikHandle( sj='l_ik_shoulder_jnt', ee='l_ik_wrest_jnt',n = "l_ik_arm_handle")
    
    #Create IK RightArm
    new_name = ''
    duplicated_root = cmds.duplicate('r_shoulder_drv', renameChildren=True)[0]
    duplicated_joints = cmds.listRelatives(duplicated_root, allDescendents=True, type='joint') or []
    duplicated_joints.append(duplicated_root)
    duplicated_joints.reverse() 
    for joint in duplicated_joints:
        new_name = joint.replace("_drv", "_jnt").replace('r_', "r_ik_", 1)
        if new_name.endswith('1'):
           new_name = new_name[:-1]
        cmds.rename(joint, new_name)
    cmds.ikHandle( sj='r_ik_shoulder_jnt', ee='r_ik_wrest_jnt',n = "r_ik_arm_handle")
    
    #Create IK Left Leg
    duplicated_root = cmds.duplicate('l_leg_drv', renameChildren=True)[0]
    duplicated_joints = cmds.listRelatives(duplicated_root, allDescendents=True, type='joint') or []
    duplicated_joints.append(duplicated_root)
    duplicated_joints.reverse() 
    for joint in duplicated_joints:
        new_name = joint.replace("_drv", "_jnt").replace("l_", "l_ik_")
        if new_name.endswith('1'):
           new_name = new_name[:-1]
        cmds.rename(joint, new_name)
    cmds.ikHandle( sj='l_ik_leg_jnt', ee='l_ik_ankle_jnt',n = "l_ik_leg_handle")
    
    #Create IK Right Leg
    new_name = ''
    duplicated_root = cmds.duplicate('r_leg_drv', renameChildren=True)[0]
    duplicated_joints = cmds.listRelatives(duplicated_root, allDescendents=True, type='joint') or []
    duplicated_joints.append(duplicated_root)
    duplicated_joints.reverse() 
    for joint in duplicated_joints:
        new_name = joint.replace("_drv", "_jnt").replace('r_', "r_ik_", 1)
        if new_name.endswith('1'):
           new_name = new_name[:-1]
        cmds.rename(joint, new_name) 
    cmds.ikHandle( sj='r_ik_leg_jnt', ee='r_ik_ankle_jnt',n = "r_ik_leg_handle")

def CreateSpineCtrls(*args):
    # Create Base Controls
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "Global_ctrl", r = 10)
    cmds.group(name='Global_grp' )
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "Offset_ctrl", r = 8)
    cmds.group(name='Offset_grp' )
    cmds.parent('Offset_grp', 'Global_ctrl')
    
    # Create Spine Controls
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "hip_ctrl", r = 5)
    cmds.group(name='hip_grp')
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "spine01_ctrl", r = 5)
    cmds.group(name='spine01_grp')
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "spine02_ctrl", r = 5)
    cmds.group(name='spine02_grp')
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "spine03_ctrl", r = 5)
    cmds.group(name='spine03_grp')
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "chest_ctrl", r = 5)
    cmds.group(name='chest_grp')    
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "neck01_ctrl", r = 3)
    cmds.group(name='neck01_grp')  
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "neck02_ctrl", r = 3)
    cmds.group(name='neck02_grp')  
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "head_ctrl", r = 5)
    cmds.group(name='head_grp')  
    
    cmds.matchTransform('hip_grp','hip_jnt')
    cmds.matchTransform('spine01_grp','spine01_jnt')
    cmds.matchTransform('spine02_grp','spine02_jnt')
    cmds.matchTransform('spine03_grp','spine03_jnt')
    cmds.matchTransform('chest_grp','chest_jnt')
    
    cmds.matchTransform('neck01_grp','neck01_jnt')
    cmds.matchTransform('neck02_grp','neck02_jnt')
    cmds.matchTransform('head_grp','head_jnt')
    
    cmds.parent('neck01_grp', 'chest_ctrl')
    cmds.parent('neck02_grp', 'neck01_ctrl')
    cmds.parent('head_grp', 'neck02_ctrl')
    
    cmds.parent('spine01_grp', 'hip_ctrl')
    cmds.parent('spine02_grp', 'spine01_ctrl')
    cmds.parent('spine03_grp', 'spine02_ctrl')
    cmds.parent('chest_grp', 'spine03_ctrl')
    cmds.parent('hip_grp', 'Offset_ctrl')

def CreateArmCtrls(*args):
    # Create Left FK Arm Controls
    cmds.circle( nr=(1, 0, 0), c=(0, 0, 0), n = "l_fk_shoulder_ctrl", r = 3)
    cmds.group(name='l_fk_shoulder_grp')
    cmds.circle( nr=(1, 0, 0), c=(0, 0, 0), n = "l_fk_elbow_ctrl", r = 3)
    cmds.group(name='l_fk_elbow_grp')
    cmds.circle( nr=(1, 0, 0), c=(0, 0, 0), n = "l_fk_wrest_ctrl", r = 3)
    cmds.group(name='l_fk_wrest_grp')
    
    cmds.matchTransform('l_fk_shoulder_grp','l_fk_shoulder_jnt')
    cmds.matchTransform('l_fk_elbow_grp','l_fk_elbow_jnt')
    cmds.matchTransform('l_fk_wrest_grp','l_fk_wrest_jnt')
        
    cmds.parent('l_fk_elbow_grp', 'l_fk_shoulder_ctrl')
    cmds.parent('l_fk_wrest_grp', 'l_fk_elbow_ctrl')
    cmds.parent('l_fk_shoulder_grp', 'chest_ctrl')
    
    # Create Left FK Arm Controls
    cmds.circle( nr=(1, 0, 0), c=(0, 0, 0), n = "r_fk_shoulder_ctrl", r = 3)
    cmds.group(name='r_fk_shoulder_grp')
    cmds.circle( nr=(1, 0, 0), c=(0, 0, 0), n = "r_fk_elbow_ctrl", r = 3)
    cmds.group(name='r_fk_elbow_grp')
    cmds.circle( nr=(1, 0, 0), c=(0, 0, 0), n = "r_fk_wrest_ctrl", r = 3)
    cmds.group(name='r_fk_wrest_grp')
    
    cmds.matchTransform('r_fk_shoulder_grp','r_fk_shoulder_jnt')
    cmds.matchTransform('r_fk_elbow_grp','r_fk_elbow_jnt')
    cmds.matchTransform('r_fk_wrest_grp','r_fk_wrest_jnt')
        
    cmds.parent('r_fk_elbow_grp', 'r_fk_shoulder_ctrl')
    cmds.parent('r_fk_wrest_grp', 'r_fk_elbow_ctrl')
    cmds.parent('r_fk_shoulder_grp', 'chest_ctrl')
    

    # Create Right IK Arm Controls
    cmds.circle( nr=(0, 0, 0), c=(0, 0, 0), n = "r_ik_pv_ctrl", r = 1)
    cmds.group(name='r_ik_pv_grp')
    cmds.circle( nr=(1, 0, 0), c=(0, 0, 0), n = "r_ik_wrest_ctrl", r = 3)
    cmds.group(name='r_ik_wrest_grp')
    
    cmds.circle( nr=(0, 0, 0), c=(0, 0, 0), n = "r_arm_options_ctrl", r = 2)
    cmds.group(name='r_arm_options_grp')
    
    cmds.addAttr( "r_arm_options_ctrl",longName='FK_IK', attributeType='float',min =0, max = 1,keyable=True)
    
    cmds.matchTransform('r_ik_pv_grp','r_ik_elbow_jnt')
    cmds.move( 0, 0, -8, 'r_ik_pv_grp', relative=True, objectSpace=True, worldSpaceDistance=True)
    cmds.matchTransform('r_ik_wrest_grp','r_ik_wrest_jnt')
    
    cmds.matchTransform('r_arm_options_grp','r_ik_wrest_jnt')
    cmds.move( 0, 8, -8, 'r_arm_options_grp', relative=True, objectSpace=True, worldSpaceDistance=True)
    
    cmds.parent('r_ik_pv_grp', 'chest_ctrl')
    cmds.parent('r_ik_wrest_grp', 'chest_ctrl')
    cmds.parent('r_arm_options_grp', 'chest_ctrl')
    
    # Create Left IK Arm Controls
    cmds.circle( nr=(0, 0, 0), c=(0, 0, 0), n = "l_ik_pv_ctrl", r = 1)
    cmds.group(name='l_ik_pv_grp')
    cmds.circle( nr=(1, 0, 0), c=(0, 0, 0), n = "l_ik_wrest_ctrl", r = 3)
    cmds.group(name='l_ik_wrest_grp')
    
    cmds.circle( nr=(0, 0, 0), c=(0, 0, 0), n = "l_arm_options_ctrl", r = 2)
    cmds.group(name='l_arm_options_grp')

    cmds.addAttr( "l_arm_options_ctrl",longName='FK_IK', attributeType='float',max = 1, min = 0,keyable=True)
    
    cmds.matchTransform('l_ik_pv_grp','l_ik_elbow_jnt')
    cmds.move( 0, 0, -8, 'l_ik_pv_grp', relative=True, objectSpace=True, worldSpaceDistance=True)
    cmds.matchTransform('l_ik_wrest_grp','l_ik_wrest_jnt')
    
    cmds.matchTransform('l_arm_options_grp','l_ik_wrest_jnt')
    cmds.move( 0, 8, -8, 'l_arm_options_grp', relative=True, objectSpace=True, worldSpaceDistance=True)
    
    cmds.parent('l_ik_pv_grp', 'chest_ctrl')
    cmds.parent('l_ik_wrest_grp', 'chest_ctrl')
    cmds.parent('l_arm_options_grp', 'chest_ctrl')
    
def CreateLegCtrls(*args):
    # Create Left FK Leg Controls
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "l_fk_leg_ctrl", r = 3)
    cmds.group(name='l_fk_leg_grp')
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "l_fk_knee_ctrl", r = 3)
    cmds.group(name='l_fk_knee_grp')
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "l_fk_ankle_ctrl", r = 3)
    cmds.group(name='l_fk_ankle_grp')
    
    cmds.matchTransform('l_fk_leg_grp','l_fk_leg_jnt')
    cmds.matchTransform('l_fk_knee_grp','l_fk_knee_jnt')
    cmds.matchTransform('l_fk_ankle_grp','l_fk_ankle_jnt')
        
    cmds.parent('l_fk_knee_grp', 'l_fk_leg_ctrl')
    cmds.parent('l_fk_ankle_grp', 'l_fk_knee_ctrl')
    cmds.parent('l_fk_leg_grp', 'hip_ctrl')
    
    # Create Left FK Leg Controls
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "r_fk_leg_ctrl", r = 3)
    cmds.group(name='r_fk_leg_grp')
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "r_fk_knee_ctrl", r = 3)
    cmds.group(name='r_fk_knee_grp')
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "r_fk_ankle_ctrl", r = 3)
    cmds.group(name='r_fk_ankle_grp')
    
    cmds.matchTransform('r_fk_leg_grp','r_fk_leg_jnt')
    cmds.matchTransform('r_fk_knee_grp','r_fk_knee_jnt')
    cmds.matchTransform('r_fk_ankle_grp','r_fk_ankle_jnt')
        
    cmds.parent('r_fk_knee_grp', 'r_fk_leg_ctrl')
    cmds.parent('r_fk_ankle_grp', 'r_fk_knee_ctrl')
    cmds.parent('r_fk_leg_grp', 'hip_ctrl')
    
    # Create Right IK Leg Controls
    cmds.circle( nr=(0, 0, 0), c=(0, 0, 0), n = "r_ik_leg_pv_ctrl", r = 1)
    cmds.group(name='r_ik_leg_pv_grp')
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "r_ik_ankle_ctrl", r = 3)
    cmds.group(name='r_ik_ankle_grp')
    
    cmds.circle( nr=(0, 0, 0), c=(0, 0, 0), n = "r_leg_options_ctrl", r = 2)
    cmds.group(name='r_leg_options_grp')
    
    cmds.addAttr( "r_leg_options_ctrl",longName='FK_IK', attributeType='float',min =0, max = 1,keyable=True)
    
    cmds.matchTransform('r_leg_options_grp','hip_jnt')
    cmds.move( -8, 0, 0, 'r_leg_options_grp', relative=True, objectSpace=True, worldSpaceDistance=True)
    
    cmds.matchTransform('r_ik_leg_pv_grp','r_ik_knee_jnt')
    cmds.move( 0, 0, 8, 'r_ik_leg_pv_grp', relative=True, objectSpace=True, worldSpaceDistance=True)
    
    cmds.matchTransform('r_ik_ankle_grp','r_ik_ankle_jnt')
        
    cmds.parent('r_ik_leg_pv_grp', 'hip_ctrl')
    cmds.parent('r_ik_ankle_grp', 'hip_ctrl')
    cmds.parent('r_leg_options_grp', 'hip_ctrl')
    
    # Create Left IK Leg Controls
    cmds.circle( nr=(0, 0, 0), c=(0, 0, 0), n = "l_ik_leg_pv_ctrl", r = 1)
    cmds.group(name='l_ik_leg_pv_grp')
    cmds.circle( nr=(0, 1, 0), c=(0, 0, 0), n = "l_ik_ankle_ctrl", r = 3)
    cmds.group(name='l_ik_ankle_grp')
    
    cmds.circle( nr=(0, 0, 0), c=(0, 0, 0), n = "l_leg_options_ctrl", r = 2)
    cmds.group(name='l_leg_options_grp')
    
    cmds.addAttr( "l_leg_options_ctrl",longName='FK_IK', attributeType='float',min =0, max = 1,keyable=True)
    
    cmds.matchTransform('l_leg_options_grp','hip_jnt')
    cmds.move( 8, 0, 0, 'l_leg_options_grp', relative=True, objectSpace=True, worldSpaceDistance=True)
    
    cmds.matchTransform('l_ik_leg_pv_grp','l_ik_knee_jnt')
    cmds.move( 0, 0, 8, 'l_ik_leg_pv_grp', relative=True, objectSpace=True, worldSpaceDistance=True)
    cmds.matchTransform('l_ik_ankle_grp','l_ik_ankle_jnt')
        
    cmds.parent('l_ik_leg_pv_grp', 'hip_ctrl')
    cmds.parent('l_ik_ankle_grp', 'hip_ctrl')
    cmds.parent('l_leg_options_grp', 'hip_ctrl')
    
def allConstraint(*args):
    # Spine Constraints
    cmds.parentConstraint( 'hip_ctrl', 'hip_jnt')
    cmds.parentConstraint( 'spine01_ctrl', 'spine01_jnt')
    cmds.parentConstraint( 'spine02_ctrl', 'spine02_jnt')
    cmds.parentConstraint( 'spine03_ctrl', 'spine03_jnt')
    cmds.parentConstraint( 'chest_ctrl', 'chest_jnt')
    cmds.parentConstraint( 'neck01_ctrl', 'neck01_jnt')
    cmds.parentConstraint( 'neck02_ctrl', 'neck02_jnt')
    cmds.parentConstraint( 'head_ctrl', 'head_jnt')
    
    # Left/Right FK Arm Constraints
    cmds.parentConstraint( 'r_fk_shoulder_ctrl', 'r_fk_shoulder_jnt')
    cmds.parentConstraint( 'r_fk_elbow_ctrl', 'r_fk_elbow_jnt')
    cmds.parentConstraint( 'r_fk_wrest_ctrl', 'r_fk_wrest_jnt')
    
    cmds.parentConstraint( 'l_fk_shoulder_ctrl', 'l_fk_shoulder_jnt')
    cmds.parentConstraint( 'l_fk_elbow_ctrl', 'l_fk_elbow_jnt')
    cmds.parentConstraint( 'l_fk_wrest_ctrl', 'l_fk_wrest_jnt')
    
    # Left/Right FK Leg Constraints
    cmds.parentConstraint( 'r_fk_leg_ctrl', 'r_fk_leg_jnt')
    cmds.parentConstraint( 'r_fk_knee_ctrl', 'r_fk_knee_jnt')
    cmds.parentConstraint( 'r_fk_ankle_ctrl', 'r_fk_ankle_jnt')
    
    cmds.parentConstraint( 'l_fk_leg_ctrl', 'l_fk_leg_jnt')
    cmds.parentConstraint( 'l_fk_knee_ctrl', 'l_fk_knee_jnt')
    cmds.parentConstraint( 'l_fk_ankle_ctrl', 'l_fk_ankle_jnt')
    
    # Left/Right IK Arm Constraints
    cmds.parentConstraint( 'r_ik_wrest_ctrl', 'r_ik_arm_handle')
    cmds.poleVectorConstraint( 'r_ik_pv_ctrl', 'r_ik_arm_handle')
    
    cmds.parentConstraint( 'l_ik_wrest_ctrl', 'l_ik_arm_handle')
    cmds.poleVectorConstraint( 'l_ik_pv_ctrl', 'l_ik_arm_handle')
    
    # Left/Right IK Leg Constraints
    cmds.parentConstraint( 'r_ik_ankle_ctrl', 'r_ik_leg_handle')
    cmds.poleVectorConstraint( 'r_ik_leg_pv_ctrl', 'r_ik_leg_handle')
    
    cmds.parentConstraint( 'l_ik_ankle_ctrl', 'l_ik_leg_handle')
    cmds.poleVectorConstraint( 'l_ik_leg_pv_ctrl', 'l_ik_leg_handle')
    
    # Left/Right Arm Joints Constraints
    cmds.parentConstraint( 'l_ik_shoulder_jnt', 'l_fk_shoulder_jnt', 'l_shoulder_drv')
    cmds.parentConstraint( 'l_ik_elbow_jnt', 'l_fk_elbow_jnt', 'l_elbow_drv')
    cmds.parentConstraint( 'l_ik_wrest_jnt', 'l_fk_wrest_jnt', 'l_wrest_drv')
    
    cmds.parentConstraint( 'r_ik_shoulder_jnt', 'r_fk_shoulder_jnt', 'r_shoulder_drv')
    cmds.parentConstraint( 'r_ik_elbow_jnt', 'r_fk_elbow_jnt', 'r_elbow_drv')
    cmds.parentConstraint( 'r_ik_wrest_jnt', 'r_fk_wrest_jnt', 'r_wrest_drv')
    
    # Left/Right Leg Joints Constraints
    cmds.parentConstraint( 'l_ik_leg_jnt', 'l_fk_leg_jnt', 'l_leg_drv')
    cmds.parentConstraint( 'l_ik_knee_jnt', 'l_fk_knee_jnt', 'l_knee_drv')
    cmds.parentConstraint( 'l_ik_ankle_jnt', 'l_fk_ankle_jnt', 'l_ankle_drv')
    
    cmds.parentConstraint( 'r_ik_leg_jnt', 'r_fk_leg_jnt', 'r_leg_drv')
    cmds.parentConstraint( 'r_ik_knee_jnt', 'r_fk_knee_jnt', 'r_knee_drv')
    cmds.parentConstraint( 'r_ik_ankle_jnt', 'r_fk_ankle_jnt', 'r_ankle_drv')

def connectAttributes(*args):
    # Left Arm
    ctrl_attr = 'l_arm_options_ctrl.FK_IK'
    connections = [
        ('l_wrest_drv_parentConstraint*', 'l_fk_wrest_jntW1', 'l_ik_wrest_jntW0'),
        ('l_elbow_drv_parentConstraint*', 'l_fk_elbow_jntW1', 'l_ik_elbow_jntW0'),
        ('l_shoulder_drv_parentConstraint*', 'l_fk_shoulder_jntW1', 'l_ik_shoulder_jntW0')
    ]
    for i, (constraint_pattern, fk_weight, ik_weight) in enumerate(connections):
        matches = cmds.ls(constraint_pattern)
        if not matches:
            continue
        constraint = matches[-1]
        blend_node = cmds.shadingNode('blendColors', asUtility=True, name=f'{constraint}_blendWeight')
        cmds.connectAttr(ctrl_attr, f'{blend_node}.blender', force=True)
        cmds.setAttr(f'{blend_node}.color1R', 1)  
        cmds.setAttr(f'{blend_node}.color2R', 0) 
        cmds.connectAttr(f'{blend_node}.outputR', f'{constraint}.{fk_weight}', force=True)
        blend_node_ik = cmds.shadingNode('blendColors', asUtility=True, name=f'{constraint}_blendWeightIK')
        cmds.connectAttr(ctrl_attr, f'{blend_node_ik}.blender', force=True)
        cmds.setAttr(f'{blend_node_ik}.color1R', 0)  
        cmds.setAttr(f'{blend_node_ik}.color2R', 1) 
        cmds.connectAttr(f'{blend_node_ik}.outputR', f'{constraint}.{ik_weight}', force=True)
        
    # Right Arm
    ctrl_attr = 'r_arm_options_ctrl.FK_IK'
    connections = [
        ('r_wrest_drv_parentConstraint*', 'r_fk_wrest_jntW1', 'r_ik_wrest_jntW0'),
        ('r_elbow_drv_parentConstraint*', 'r_fk_elbow_jntW1', 'r_ik_elbow_jntW0'),
        ('r_shoulder_drv_parentConstraint*', 'r_fk_shoulder_jntW1', 'r_ik_shoulder_jntW0')
    ]
    for i, (constraint_pattern, fk_weight, ik_weight) in enumerate(connections):
        matches = cmds.ls(constraint_pattern)
        if not matches:
            continue
        constraint = matches[-1]
        blend_node = cmds.shadingNode('blendColors', asUtility=True, name=f'{constraint}_blendWeight')
        cmds.connectAttr(ctrl_attr, f'{blend_node}.blender', force=True)
        cmds.setAttr(f'{blend_node}.color1R', 1)  
        cmds.setAttr(f'{blend_node}.color2R', 0) 
        cmds.connectAttr(f'{blend_node}.outputR', f'{constraint}.{fk_weight}', force=True)
        blend_node_ik = cmds.shadingNode('blendColors', asUtility=True, name=f'{constraint}_blendWeightIK')
        cmds.connectAttr(ctrl_attr, f'{blend_node_ik}.blender', force=True)
        cmds.setAttr(f'{blend_node_ik}.color1R', 0)  
        cmds.setAttr(f'{blend_node_ik}.color2R', 1) 
        cmds.connectAttr(f'{blend_node_ik}.outputR', f'{constraint}.{ik_weight}', force=True)
    
    # Right Leg
    ctrl_attr = 'r_leg_options_ctrl.FK_IK'
    connections = [
        ('r_leg_drv_parentConstraint*', 'r_fk_leg_jntW1', 'r_ik_leg_jntW0'),
        ('r_knee_drv_parentConstraint*', 'r_fk_knee_jntW1', 'r_ik_knee_jntW0'),
        ('r_ankle_drv_parentConstraint*', 'r_fk_ankle_jntW1', 'r_ik_ankle_jntW0')
    ]
    for i, (constraint_pattern, fk_weight, ik_weight) in enumerate(connections):
        matches = cmds.ls(constraint_pattern)
        if not matches:
            continue
        constraint = matches[-1]
        blend_node = cmds.shadingNode('blendColors', asUtility=True, name=f'{constraint}_blendWeight')
        cmds.connectAttr(ctrl_attr, f'{blend_node}.blender', force=True)
        cmds.setAttr(f'{blend_node}.color1R', 1)  
        cmds.setAttr(f'{blend_node}.color2R', 0) 
        cmds.connectAttr(f'{blend_node}.outputR', f'{constraint}.{fk_weight}', force=True)
        blend_node_ik = cmds.shadingNode('blendColors', asUtility=True, name=f'{constraint}_blendWeightIK')
        cmds.connectAttr(ctrl_attr, f'{blend_node_ik}.blender', force=True)
        cmds.setAttr(f'{blend_node_ik}.color1R', 0)  
        cmds.setAttr(f'{blend_node_ik}.color2R', 1) 
        cmds.connectAttr(f'{blend_node_ik}.outputR', f'{constraint}.{ik_weight}', force=True)
        
    # Left Leg
    ctrl_attr = 'l_leg_options_ctrl.FK_IK'
    connections = [
        ('l_leg_drv_parentConstraint*', 'l_fk_leg_jntW1', 'l_ik_leg_jntW0'),
        ('l_knee_drv_parentConstraint*', 'l_fk_knee_jntW1', 'l_ik_knee_jntW0'),
        ('l_ankle_drv_parentConstraint*', 'l_fk_ankle_jntW1', 'l_ik_ankle_jntW0')
    ]
    for i, (constraint_pattern, fk_weight, ik_weight) in enumerate(connections):
        matches = cmds.ls(constraint_pattern)
        if not matches:
            continue
        constraint = matches[-1]
        blend_node = cmds.shadingNode('blendColors', asUtility=True, name=f'{constraint}_blendWeight')
        cmds.connectAttr(ctrl_attr, f'{blend_node}.blender', force=True)
        cmds.setAttr(f'{blend_node}.color1R', 1)  
        cmds.setAttr(f'{blend_node}.color2R', 0) 
        cmds.connectAttr(f'{blend_node}.outputR', f'{constraint}.{fk_weight}', force=True)
        blend_node_ik = cmds.shadingNode('blendColors', asUtility=True, name=f'{constraint}_blendWeightIK')
        cmds.connectAttr(ctrl_attr, f'{blend_node_ik}.blender', force=True)
        cmds.setAttr(f'{blend_node_ik}.color1R', 0)  
        cmds.setAttr(f'{blend_node_ik}.color2R', 1) 
        cmds.connectAttr(f'{blend_node_ik}.outputR', f'{constraint}.{ik_weight}', force=True)
        
def FullRig(*args):
    createFK()
    createIK()
    CreateSpineCtrls()
    CreateArmCtrls()
    CreateLegCtrls()
    allConstraint()
    connectAttributes()
    
def GUI():
    if cmds.window("HumenGUI", exists=True):
        cmds.deleteUI("HumenGUI")
    window = cmds.window("HumenGUI", title="Humen Rig Builder", widthHeight=(300, 50))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=8)
    cmds.button(label="Create Base Rig", command=lambda *_: baseRig())
    cmds.button(label="Create Full Rig", command=lambda *_: FullRig())
    cmds.setParent("..")
    cmds.showWindow(window)
    
GUI()