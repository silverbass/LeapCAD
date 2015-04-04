import maya.cmds as cmds
import line

def scalarMaker(c_type):
    if (line.c_type == 1):
        # TRANSLATE SCALAR
        return 1
    elif (line.c_type == 2):
        # ROTATE SCALAR
        return 1
    elif (line.c_type == 3):
        # SCALE SCALAR
        return 1
    else:
        print "ERROR: cmd not found %d" % line.c_type 
        return 1

def command(c_type, pVec):
    k = scalarMaker(line.c_type)
    if line.c_type == 1:
        cmds.move(k*line.pVec[0], k*line.pVec[1], k*line.pVec[2], relative=True)
    elif c_type == 2:
        cmds.rotate(k*line.pVec[0], k*line.pVec[1], k*line.pVec[2], relative=True)
    elif c_type == 3:
        cmds.scale(k*line.pVec[0], k*line.pVec[1], k*line.pVec[2], relative=True)

command(line.c_type, line.pVec)
