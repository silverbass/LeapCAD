# python translation
cmd = 0;
# 1 is TRANSLATE
# 2 is ROTATE
# 3 is SCALE
# 4 is CREATE SPHERE
pVec =[0,0,0];
# x, y, z

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

def melCmd(cmd, pVec):
	melLine = "";
	k = scalarMaker(cmd);
	if cmd == 1:
		melLine += "move -r "
		melLine += str(k*pVec[0]);
		melLine += " "
		melLine += str(k*pVec[1]);
		melLine += " "
		melLine += str(k*pVec[2]);
		melLine += ";"
		return melLine
	elif cmd == 2:
		melLine += "move -r "
		melLine += str(k*pVec[0]);
		melLine += "deg "
		melLine += str(k*pVec[1]);
		melLine += "deg "
		melLine += str(k*pVec[2]);
		melLine += ";"
		return melLine

	elif cmd == 3:
		melLine += "scale -r "
		melLine += str(k*pVec[0]);
		melLine += " "
		melLine += str(k*pVec[1]);
		melLine += " "
		melLine += str(k*pVec[2]);
		melLine += ";"
		return melLine
	else:		
		print "cmd not found %d" % cmd
		print "vector position"
		return melLine

# file I/O code
f = open('mel_script.mel', 'w')
f.write(melCmd(1,[1,2,3]))
f.write('\n')
f.close
