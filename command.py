c_type = 1
pVec = [0,1,0]
# ^ you replace these two lines with your vector and type of transformation

import maya.cmds as cmds
import maya.mel as mel
import time

def scalarMaker(c_type):
    if (c_type == 1):
        # TRANSLATE SCALAR
        return 1
    elif (c_type == 2):
        # ROTATE SCALAR
        return 1
    elif (c_type == 3):
        # SCALE SCALAR
        return 1
    elif (c_type == 4) || (c_type == 5):
        # OBJECT CREATION
        return 1
    else:
        print "ERROR: cmd not found %d" % c_type 
        return 0

def command(c_type, pVec):
    k = scalarMaker(c_type)
    if c_type == 1:
        cmds.move(k*pVec[0], k*pVec[1], k*pVec[2], relative=True)
    elif c_type == 2:
        cmds.rotate(k*pVec[0], k*pVec[1], k*pVec[2], relative=True)
    elif c_type == 3:
        cmds.scale(k*pVec[0], k*pVec[1], k*pVec[2], relative=True)
    elif c_type == 4:
        cmds.polyCube(sx=8, sy=8, sz=8, w=16, h=16, d=16)
    elif c_type == 5:
        cmds.polyTorus(sx=32, sy=16, r=10, sr=4)
    elif c_type == 6:
        cmds.delete()
        #deletes selected item

