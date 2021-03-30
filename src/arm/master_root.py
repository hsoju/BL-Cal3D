import bpy
import random
import re

from ..maps.bones.heads import HeadMap
from ..maps.bones.rolls import RollMap
from ..maps.bones.tails import TailMap


def add_bone(armature: bpy.types.Armature, bone_name: str, head: list, tail: list,
             roll: float, connect: bool, parent=None) -> bpy.types.EditBone:
    bone = armature.edit_bones.new(bone_name)
    bone.head[:] = head[0], head[1], head[2]
    bone.tail[:] = tail[0], tail[1], tail[2]
    bone.roll = roll
    bone.use_connect = connect
    if parent:
        bone.parent = armature.edit_bones[parent]
    return bone


def lock_bones(obj: bpy.types.Object):
    for bone in obj.pose.bones:
        bone.lock_scale = [True, True, True]
        name = bone.name
        if name != 'PelvisNode':
            bone.lock_location = [True, True, True]
            if 'meta' in name or 'Hip' in name:
                bone.lock_rotation = [True, True, True]
            elif '02' in name or '03' in name or 'Calf' in name or 'Toes' in name:
                if 'Spine' not in name and 'Neck' not in name:
                    bone.lock_rotation = [False, True, True]
            elif '01' in name or 'Hand' in name:
                if 'Spine' not in name and 'Neck' not in name:
                    bone.lock_rotation = [False, True, False]
            elif 'Bicep' in name or 'Wrist' in name:
                bone.lock_rotation = [True, False, True]
            elif 'Elbow' in name:
                bone.lock_rotation = [True, True, False]


def rand(num: int = 1) -> float:
    return random.uniform(-num, num)


def randomize_pelvis(bone: bpy.types.PoseBone) -> str:
    height = random.choice(['STAND', 'SIT'])
    if height == 'STAND':
        bone.location.z = 0
    else:
        bone.location.z = random.uniform(-2.5, -2.3)
    return height


def randomize_spine(bones: dict, pose_type: str):

    if pose_type == 'STRAIGHT':
        bones['Spine01'].rotation_euler[:] = random.uniform(-11, -9), rand(), rand(5)
        bones['Spine02'].rotation_euler[:] = rand(), rand(), random.uniform(-1, -0.5)
        bones['Spine03'].rotation_euler[:] = rand(), rand(), random.uniform(-7.5, -5)
        bones['Spine04'].rotation_euler[:] = rand(5), rand(), random.uniform(-18, -15)
    elif pose_type == 'LEAN':
        bones['Spine01'].rotation_euler[:] = random.uniform(-24, -16), rand(), rand(5)
        bones['Spine02'].rotation_euler[:] = rand(), rand(), random.uniform(-20, -15)
        bones['Spine03'].rotation_euler[:] = rand(), rand(), random.uniform(-20, -15)
        bones['Spine04'].rotation_euler[:] = rand(5), rand(), random.uniform(-32, -27)
    elif pose_type == 'SLOUCH':
        bones['Spine01'].rotation_euler[:] = random.uniform(-60, -50), rand(), rand(5)
        bones['Spine02'].rotation_euler[:] = rand(), rand(), random.uniform(-10, -5)
        bones['Spine03'].rotation_euler[:] = rand(), rand(), random.uniform(-10, -5)
        bones['Spine04'].rotation_euler[:] = rand(5), rand(), random.uniform(-30, -25)


def randomize_leg(bones: dict, side_name: str, pose_type: str):
    bones['Thigh'].rotation_euler.x = random.uniform(15, 25)
    if pose_type == 'STAND':
        bones['Thigh'].rotation_euler.y = random.uniform(10, 30) if side_name == 'rt' else random.uniform(-30, -10)
        bones['Thigh'].rotation_euler.z = random.uniform(0, 10) if side_name == 'rt' else random.uniform(-10, 0)
        bones['Calf'].rotation_euler[:] = random.uniform(4, 8), rand(), rand()
    elif pose_type == 'SIT':
        bones['Thigh'].rotation_euler.y = random.uniform(30, 60) if side_name == 'rt' else random.uniform(-60, -30)
        bones['Thigh'].rotation_euler.z = random.uniform(20, 50) if side_name == 'rt' else random.uniform(-50, -20)
        bones['Calf'].rotation_euler[:] = random.uniform(60, 120), rand(), rand()
    bones['Foot'].rotation_euler[:] = random.uniform(0, 4), random.uniform(-8, 8), random.uniform(-8, 8)


def randomize_head(bones: dict):
    bones['Neck01'].rotation_euler[:] = 0, 0, random.uniform(0, 5)
    bones['Neck02'].rotation_euler[:] = 0, 0, random.uniform(-10, -5)
    bones['Neck03'].rotation_euler[:] = 0, 0, random.uniform(0, 2)
    bones['Neck04'].rotation_euler[:] = 0, 0, random.uniform(5, 10)
    bones['Head'].rotation_euler[:] = random.uniform(-10, 10), random.uniform(-45, 45), random.uniform(-10, 0)


def randomize_arm(bones: dict, side_name: str):
    bones['Clavicle'].rotation_euler[:] = rand(), rand(), random.uniform(0, 10)
    bones['Shoulder'].rotation_euler = [random.uniform(20, 50), random.uniform(7, 10), random.uniform(10, 40)]
    bones['Wrist'].rotation_euler[:] = rand(), rand(), rand()
    bones['Elbow'].rotation_euler[:2] = rand(), rand()
    bones['Elbow'].rotation_euler.z = random.uniform(20, 100) if side_name == 'lf' else random.uniform(-100, -20)


def clench_finger(bones: dict, finger_name: str):
    bones['01'].rotation_euler.x = random.uniform(70, 90)
    bones['01'].rotation_euler[1:] = rand(), rand()
    bones['02'].rotatation_euler.x = random.uniform(80, 100) if finger_name != 'Index' else random.uniform(-100, -80)
    bones['02'].rotation_euler[1:] = rand(), rand()
    bones['03'].rotation_euler.x = random.uniform(-10, 0) if finger_name != 'Pinky' else random.uniform(0, 10)
    bones['03'].rotatation_euler[1:] = rand(), rand()


def curve_finger(bones: dict, finger_name: str):
    bones['01'].rotation_euler.x = random.uniform(5, 45)
    bones['01'].rotation_euler[1:] = rand(), rand()
    bones['02'].rotatation_euler.x = random.uniform(30, 40) if finger_name != 'Index' else random.uniform(-40, -30)
    bones['02'].rotation_euler[1:] = rand(), rand()
    bones['03'].rotation_euler.x = random.uniform(-15, -5) if finger_name != 'Pinky' else random.uniform(5, 15)
    bones['03'].rotatation_euler[1:] = rand(), rand()


def point_finger(bones: dict, finger_name: str):
    bones['01'].rotation_euler.x = random.uniform(-10, -5)
    bones['01'].rotation_euler[1:] = rand(), rand()
    bones['02'].rotatation_euler.x = random.uniform(-15, -10) if finger_name != 'Index' else -random.uniform(20, 30)
    bones['02'].rotation_euler[1:] = rand(), rand()
    bones['03'].rotation_euler.x = random.uniform(7, 12) if finger_name != 'Pinky' else random.uniform(-17, -12)
    bones['03'].rotatation_euler[1:] = rand(), rand()


def randomize_finger(bones: dict, finger_name: str):
    random.choice([clench_finger, curve_finger, point_finger])(bones, finger_name)


def isolate_fingers(bones: dict, finger_name: str) -> dict:
    fingers = {}
    for bone_name, bone in bones.items():
        if finger_name in bone_name:
            bone_num = re.findall('\d+', bone_name)[0]
            fingers[bone_num] = bone
    return fingers


def randomize_hand(bones: dict):
    index = isolate_fingers(bones, 'Index')
    middle = isolate_fingers(bones, 'Middle')
    ring = isolate_fingers(bones, 'Ring')
    pinky = isolate_fingers(bones, 'Pinky')
    # thumb = isolate_fingers(bones, 'Thumb')


def randomize_bones(obj: bpy.types.Object):
    bones = {bone.name: bone for bone in obj.pose.bones}
    pose_type = randomize_pelvis(bones['PelvisNode'])


def add_master_root():
    """Generates the default armature for imvu skeleton rig.

    """
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.armature_add()
    bpy.ops.object.editmode_toggle()
    bpy.ops.armature.select_all(action='SELECT')
    bpy.ops.armature.delete()

    obj = bpy.context.active_object
    arm = obj.data

    root = add_bone(arm, "Female03MasterRoot", HeadMap.lookup("Female03MasterRoot"),
                    TailMap.lookup("Female03MasterRoot"), RollMap.lookup("Female03MasterRoot"), False)
    root.use_deform = False
    add_bone(arm, "PelvisNode", HeadMap.lookup("PelvisNode"), TailMap.lookup("PelvisNode"),
             RollMap.lookup("PelvisNode"), False, "Female03MasterRoot")
    add_bone(arm, "lfHip", HeadMap.lookup("lfHip"), TailMap.lookup("lfHip"),
             RollMap.lookup("lfHip"), False, "PelvisNode")
    add_bone(arm, "lfThigh", HeadMap.lookup("lfThigh"), TailMap.lookup("lfThigh"),
             RollMap.lookup("lfThigh"), True, "lfHip")
    add_bone(arm, "lfCalf", HeadMap.lookup("lfCalf"), TailMap.lookup("lfCalf"),
             RollMap.lookup("lfCalf"), True, "lfThigh")
    add_bone(arm, "lfFoot", HeadMap.lookup("lfFoot"), TailMap.lookup("lfFoot"),
             RollMap.lookup("lfFoot"), True, "lfCalf")
    add_bone(arm, "lfToes", HeadMap.lookup("lfToes"), TailMap.lookup("lfToes"),
             RollMap.lookup("lfToes"), True, "lfFoot")
    add_bone(arm, "rtHip", HeadMap.lookup("rtHip"), TailMap.lookup("rtHip"),
             RollMap.lookup("rtHip"), False, "PelvisNode")
    add_bone(arm, "rtThigh", HeadMap.lookup("rtThigh"), TailMap.lookup("rtThigh"),
             RollMap.lookup("rtThigh"), True, "rtHip")
    add_bone(arm, "rtCalf", HeadMap.lookup("rtCalf"), TailMap.lookup("rtCalf"),
             RollMap.lookup("rtCalf"), True, "rtThigh")
    add_bone(arm, "rtFoot", HeadMap.lookup("rtFoot"), TailMap.lookup("rtFoot"),
             RollMap.lookup("rtFoot"), True, "rtCalf")
    add_bone(arm, "rtToes", HeadMap.lookup("rtToes"), TailMap.lookup("rtToes"),
             RollMap.lookup("rtToes"), True, "rtFoot")
    add_bone(arm, "Spine01", HeadMap.lookup("Spine01"), TailMap.lookup("Spine01"),
             RollMap.lookup("Spine01"), False, "PelvisNode")
    add_bone(arm, "Spine02", HeadMap.lookup("Spine02"), TailMap.lookup("Spine02"),
             RollMap.lookup("Spine02"), False, "Spine01")
    add_bone(arm, "Spine03", HeadMap.lookup("Spine03"), TailMap.lookup("Spine03"),
             RollMap.lookup("Spine03"), True, "Spine02")
    add_bone(arm, "Spine04", HeadMap.lookup("Spine04"), TailMap.lookup("Spine04"),
             RollMap.lookup("Spine04"), True, "Spine03")
    add_bone(arm, "Neck01", HeadMap.lookup("Neck01"), TailMap.lookup("Neck01"),
             RollMap.lookup("Neck01"), False, "Spine04")
    add_bone(arm, "Neck02", HeadMap.lookup("Neck02"), TailMap.lookup("Neck02"),
             RollMap.lookup("Neck02"), False, "Neck01")
    add_bone(arm, "Neck03", HeadMap.lookup("Neck03"), TailMap.lookup("Neck03"),
             RollMap.lookup("Neck03"), True, "Neck02")
    add_bone(arm, "Neck04", HeadMap.lookup("Neck04"), TailMap.lookup("Neck04"),
             RollMap.lookup("Neck04"), True, "Neck03")
    add_bone(arm, "Head", HeadMap.lookup("Head"), TailMap.lookup("Head"),
             RollMap.lookup("Head"), True, "Neck04")
    add_bone(arm, "lfClavicle", HeadMap.lookup("lfClavicle"), TailMap.lookup("lfClavicle"),
             RollMap.lookup("lfClavicle"), False, "Spine04")
    add_bone(arm, "lfShoulder", HeadMap.lookup("lfShoulder"), TailMap.lookup("lfShoulder"),
             RollMap.lookup("lfShoulder"), False, "lfClavicle")
    add_bone(arm, "lfBicep", HeadMap.lookup("lfBicep"), TailMap.lookup("lfBicep"),
             RollMap.lookup("lfBicep"), True, "lfShoulder")
    add_bone(arm, "lfElbow", HeadMap.lookup("lfElbow"), TailMap.lookup("lfElbow"),
             RollMap.lookup("lfElbow"), True, "lfBicep")
    add_bone(arm, "lfWrist", HeadMap.lookup("lfWrist"), TailMap.lookup("lfWrist"),
             RollMap.lookup("lfWrist"), False, "lfElbow")
    add_bone(arm, "lfHand", HeadMap.lookup("lfHand"), TailMap.lookup("lfHand"),
             RollMap.lookup("lfHand"), True, "lfWrist")
    add_bone(arm, "lfmetaCarpal03", HeadMap.lookup("lfmetaCarpal03"), TailMap.lookup("lfmetaCarpal03"),
             RollMap.lookup("lfmetaCarpal03"), False, "lfHand")
    add_bone(arm, "lfFingerMiddle01", HeadMap.lookup("lfFingerMiddle01"), TailMap.lookup("lfFingerMiddle01"),
             RollMap.lookup("lfFingerMiddle01"), True, "lfmetaCarpal03")
    add_bone(arm, "lfFingerMiddle02", HeadMap.lookup("lfFingerMiddle02"), TailMap.lookup("lfFingerMiddle02"),
             RollMap.lookup("lfFingerMiddle02"), False, "lfFingerMiddle01")
    add_bone(arm, "lfFingerMiddle03", HeadMap.lookup("lfFingerMiddle03"), TailMap.lookup("lfFingerMiddle03"),
             RollMap.lookup("lfFingerMiddle03"), False, "lfFingerMiddle02")
    add_bone(arm, "lfmetaCarpal01", HeadMap.lookup("lfmetaCarpal01"), TailMap.lookup("lfmetaCarpal01"),
             RollMap.lookup("lfmetaCarpal01"), False, "lfHand")
    add_bone(arm, "lfThumb01", HeadMap.lookup("lfThumb01"), TailMap.lookup("lfThumb01"),
             RollMap.lookup("lfThumb01"), True, "lfmetaCarpal01")
    add_bone(arm, "lfThumb02", HeadMap.lookup("lfThumb02"), TailMap.lookup("lfThumb02"),
             RollMap.lookup("lfThumb02"), False, "lfThumb01")
    add_bone(arm, "lfThumb03", HeadMap.lookup("lfThumb03"), TailMap.lookup("lfThumb03"),
             RollMap.lookup("lfThumb03"), True, "lfThumb02")
    add_bone(arm, "lfmetaCarpal05", HeadMap.lookup("lfmetaCarpal05"), TailMap.lookup("lfmetaCarpal05"),
             RollMap.lookup("lfmetaCarpal05"), False, "lfHand")
    add_bone(arm, "lfFingerPinky01", HeadMap.lookup("lfFingerPinky01"), TailMap.lookup("lfFingerPinky01"),
             RollMap.lookup("lfFingerPinky01"), False, "lfmetaCarpal05")
    add_bone(arm, "lfFingerPinky02", HeadMap.lookup("lfFingerPinky02"), TailMap.lookup("lfFingerPinky02"),
             RollMap.lookup("lfFingerPinky02"), False, "lfFingerPinky01")
    add_bone(arm, "lfFingerPinky03", HeadMap.lookup("lfFingerPinky03"), TailMap.lookup("lfFingerPinky03"),
             RollMap.lookup("lfFingerPinky03"), True, "lfFingerPinky02")
    add_bone(arm, "lfmetaCarpal02", HeadMap.lookup("lfmetaCarpal02"), TailMap.lookup("lfmetaCarpal02"),
             RollMap.lookup("lfmetaCarpal02"), False, "lfHand")
    add_bone(arm, "lfFingerIndex01", HeadMap.lookup("lfFingerIndex01"), TailMap.lookup("lfFingerIndex01"),
             RollMap.lookup("lfFingerIndex01"), True, "lfmetaCarpal02")
    add_bone(arm, "lfFingerIndex02", HeadMap.lookup("lfFingerIndex02"), TailMap.lookup("lfFingerIndex02"),
             RollMap.lookup("lfFingerIndex02"), False, "lfFingerIndex01")
    add_bone(arm, "lfFingerIndex03", HeadMap.lookup("lfFingerIndex03"), TailMap.lookup("lfFingerIndex03"),
             RollMap.lookup("lfFingerIndex03"), True, "lfFingerIndex02")
    add_bone(arm, "lfmetaCarpal04", HeadMap.lookup("lfmetaCarpal04"), TailMap.lookup("lfmetaCarpal04"),
             RollMap.lookup("lfmetaCarpal04"), False, "lfHand")
    add_bone(arm, "lfFingerRing01", HeadMap.lookup("lfFingerRing01"), TailMap.lookup("lfFingerRing01"),
             RollMap.lookup("lfFingerRing01"), True, "lfmetaCarpal04")
    add_bone(arm, "lfFingerRing02", HeadMap.lookup("lfFingerRing02"), TailMap.lookup("lfFingerRing02"),
             RollMap.lookup("lfFingerRing02"), True, "lfFingerRing01")
    add_bone(arm, "lfFingerRing03", HeadMap.lookup("lfFingerRing03"), TailMap.lookup("lfFingerRing03"),
             RollMap.lookup("lfFingerRing03"), True, "lfFingerRing02")
    add_bone(arm, "rtClavicle", HeadMap.lookup("rtClavicle"), TailMap.lookup("rtClavicle"),
             RollMap.lookup("rtClavicle"), False, "Spine04")
    add_bone(arm, "rtShoulder", HeadMap.lookup("rtShoulder"), TailMap.lookup("rtShoulder"),
             RollMap.lookup("rtShoulder"), False, "rtClavicle")
    add_bone(arm, "rtBicep", HeadMap.lookup("rtBicep"), TailMap.lookup("rtBicep"),
             RollMap.lookup("rtBicep"), True, "rtShoulder")
    add_bone(arm, "rtElbow", HeadMap.lookup("rtElbow"), TailMap.lookup("rtElbow"),
             RollMap.lookup("rtElbow"), True, "rtBicep")
    add_bone(arm, "rtWrist", HeadMap.lookup("rtWrist"), TailMap.lookup("rtWrist"),
             RollMap.lookup("rtWrist"), False, "rtElbow")
    add_bone(arm, "rtHand", HeadMap.lookup("rtHand"), TailMap.lookup("rtHand"),
             RollMap.lookup("rtHand"), True, "rtWrist")
    add_bone(arm, "rtmetaCarpal03", HeadMap.lookup("rtmetaCarpal03"), TailMap.lookup("rtmetaCarpal03"),
             RollMap.lookup("rtmetaCarpal03"), True, "rtHand")
    add_bone(arm, "rtFingerMiddle01", HeadMap.lookup("rtFingerMiddle01"), TailMap.lookup("rtFingerMiddle01"),
             RollMap.lookup("rtFingerMiddle01"), True, "rtmetaCarpal03")
    add_bone(arm, "rtFingerMiddle02", HeadMap.lookup("rtFingerMiddle02"), TailMap.lookup("rtFingerMiddle02"),
             RollMap.lookup("rtFingerMiddle02"), True, "rtFingerMiddle01")
    add_bone(arm, "rtFingerMiddle03", HeadMap.lookup("rtFingerMiddle03"), TailMap.lookup("rtFingerMiddle03"),
             RollMap.lookup("rtFingerMiddle03"), True, "rtFingerMiddle02")
    add_bone(arm, "rtmetaCarpal01", HeadMap.lookup("rtmetaCarpal01"), TailMap.lookup("rtmetaCarpal01"),
             RollMap.lookup("rtmetaCarpal01"), True, "rtHand")
    add_bone(arm, "rtThumb01", HeadMap.lookup("rtThumb01"), TailMap.lookup("rtThumb01"),
             RollMap.lookup("rtThumb01"), False, "rtmetaCarpal01")
    add_bone(arm, "rtThumb02", HeadMap.lookup("rtThumb02"), TailMap.lookup("rtThumb02"),
             RollMap.lookup("rtThumb02"), False, "rtThumb01")
    add_bone(arm, "rtThumb03", HeadMap.lookup("rtThumb03"), TailMap.lookup("rtThumb03"),
             RollMap.lookup("rtThumb03"), True, "rtThumb02")
    add_bone(arm, "rtmetaCarpal05", HeadMap.lookup("rtmetaCarpal05"), TailMap.lookup("rtmetaCarpal05"),
             RollMap.lookup("rtmetaCarpal05"), True, "rtHand")
    add_bone(arm, "rtFingerPinky01", HeadMap.lookup("rtFingerPinky01"), TailMap.lookup("rtFingerPinky01"),
             RollMap.lookup("rtFingerPinky01"), True, "rtmetaCarpal05")
    add_bone(arm, "rtFingerPinky02", HeadMap.lookup("rtFingerPinky02"), TailMap.lookup("rtFingerPinky02"),
             RollMap.lookup("rtFingerPinky02"), False, "rtFingerPinky01")
    add_bone(arm, "rtFingerPinky03", HeadMap.lookup("rtFingerPinky03"), TailMap.lookup("rtFingerPinky03"),
             RollMap.lookup("rtFingerPinky03"), False, "rtFingerPinky02")
    add_bone(arm, "rtmetaCarpal02", HeadMap.lookup("rtmetaCarpal02"), TailMap.lookup("rtmetaCarpal02"),
             RollMap.lookup("rtmetaCarpal02"), True, "rtHand")
    add_bone(arm, "rtFingerIndex01", HeadMap.lookup("rtFingerIndex01"), TailMap.lookup("rtFingerIndex01"),
             RollMap.lookup("rtFingerIndex01"), True, "rtmetaCarpal02")
    add_bone(arm, "rtFingerIndex02", HeadMap.lookup("rtFingerIndex02"), TailMap.lookup("rtFingerIndex02"),
             RollMap.lookup("rtFingerIndex02"), True, "rtFingerIndex01")
    add_bone(arm, "rtFingerIndex03", HeadMap.lookup("rtFingerIndex03"), TailMap.lookup("rtFingerIndex03"),
             RollMap.lookup("rtFingerIndex03"), True, "rtFingerIndex02")
    add_bone(arm, "rtmetaCarpal04", HeadMap.lookup("rtmetaCarpal04"), TailMap.lookup("rtmetaCarpal04"),
             RollMap.lookup("rtmetaCarpal04"), True, "rtHand")
    add_bone(arm, "rtFingerRing01", HeadMap.lookup("rtFingerRing01"), TailMap.lookup("rtFingerRing01"),
             RollMap.lookup("rtFingerRing01"), False, "rtmetaCarpal04")
    add_bone(arm, "rtFingerRing02", HeadMap.lookup("rtFingerRing02"), TailMap.lookup("rtFingerRing02"),
             RollMap.lookup("rtFingerRing02"), False, "rtFingerRing01")
    add_bone(arm, "rtFingerRing03", HeadMap.lookup("rtFingerRing03"), TailMap.lookup("rtFingerRing03"),
             RollMap.lookup("rtFingerRing03"), True, "rtFingerRing02")

    bpy.ops.object.editmode_toggle()
    # lock_bones(obj)
    bpy.ops.object.posemode_toggle()
    obj.pose.bones['Female03MasterRoot'].bone.select = True
    bpy.ops.pose.hide()
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

    return obj
