import maya.mel as mel
import command as com
for i in range(0, 3000):
    command(com.c_type, com.pVec)
    mel.eval("refresh -f")