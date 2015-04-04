import maya.cmds as cmds
cmd = 0
pVec = [0,0,0]

def scalarMaker(n):
	if n == 1:
		# TRANSLATE SCALAR
		return 1
	elif n == 2:
		# ROTATE SCALAR
		return 1
	elif n == 3:
		# SCALE SCALAR
		return 1
	else:
		print "ERROR: cmd not found %d" % n 
		return 1


def command(cmd,pVec):
	k = scalarMaker(cmd)
	if cmd == 1:
		cmds.move(k*pVec[0], k*pVec[1], k*pVec[2])
	elif cmd == 2:
		cmds.rotate(k*pVec[0], k*pVec[1], k*pVec[2])
	elif cmd =- 3:
		cmds.scale(k*pVec[0], k*pVec[1], k*pVec[2])
command(1,[1,2,3])


