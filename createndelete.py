import maya.cmds as cmds

#create generic polycube (automatically selects it)
cmds.polyCube(sx=10, sy=10, sz=10, w=20, h=20, d=20, n="generic_cube")
#create generic polytorus (automatically selects it)
cmds.polyTorus(sx=8, sy=16, r=10, sr=1, n="generic_torus")
#delete selected object
cmds.delete()
