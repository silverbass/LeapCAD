import maya.cmds as cmds


#create generic polysphere (automatically selects it)
cmds.polySphere(sx=10, sy=15, r=20)
#create generic polycube (automatically selects it)
cmds.polyCube( sx=10, sy=15, sz=5, h=20)
#delete selected object
cmds.delete()
