'''
module for general util checks
'''

import maya.cmds as mc

def uniqueName(side, name, suffix):
	security = 100

	i = 1
	fullName = '{0}_{1}{2:02d}_{3}'.format(side, name,i, suffix)

	while mc.objExists(fullName):
		if i < security:
			i += 1

			fullName = '{0}_{1}{2:02d}_{3}'.format(side, name,i, suffix)

	return fullName

def isGeometry(node):

	if not mc.nodeType(node) == 'transform':
		return False

	validTypes = ['mesh']
	children = mc.listRelatives(node, c=True, s=True, f=True) or []
	validChildren = [shape for shape in children if mc.nodeType(shape) in validTypes]

	if validChildren:
		return True

	return False


def isSkinned(object):

	hist = mc.listHistory(object, pdo=True) or []
	sclusters = [node for node in hist if mc.nodeType(node) == 'skinCluster']
	if sclusters:
		return True

	return False


def getShape(node):

	if not mc.nodeType(node) == 'transform':
		return 'None'

	validTypes = ['nurbsCurve', 'locator']
	children = mc.listRelatives(node, c=True, s=True, f=True) or []
	validChildren = [shape for shape in children if mc.nodeType(shape) in validTypes]

	if validChildren:
		return validChildren[0]
