import maya.mel as mel
import sys
sys.path.insert(0, "/Users/raychen/Library/Preferences/Autodesk/maya/2015-x64/prefs/scriptEditorTemp/")
import command
while True:
	reload(command)
	command.command(command.c_type, command.pVec)
	mel.eval("refresh -f")