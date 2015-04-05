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

command(c_type, pVec)
mel.eval("refresh -f")
