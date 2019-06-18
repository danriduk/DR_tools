'''
module for node overrides'
'''

import maya.cmds as mc
from . import dictionaries
from . import checks


colDict = dictionaries.colorDictionary()
displayDict = dictionaries.displayDictionary()


def override(node, display='normal', col='default', v=1):
	# main function for overriding object displays
	# override shape node if object has one
	shape = checks.getShape(node)
	if shape != 'None':
		node = shape

	# enable drawing overrides
	if '{0}.overrideEnabled'.format(node) != 1:
		mc.setAttr('{0}.overrideEnabled'.format(node), 1)
	else:
		pass

	# set display type
	if '{0}.overrideDisplayType'.format(node) != displayDict[display]:
		mc.setAttr('{0}.overrideDisplayType'.format(node), displayDict[display])
	else:
		pass

	# set display color
	if '{0}.overrideColor'.format(node) != colDict[col]:
		mc.setAttr('{0}.overrideColor'.format(node), colDict[col])
	else:
		pass

	# set visibility
	if '{0}.overrideVisibility'.format(node) != v:
		mc.setAttr('{0}.overrideVisibility'.format(node), v)
	else:
		pass


def lockAttrs(object, channels=['t', 'r', 's', 'v'], attrs=['x', 'y', 'z']):
		# function to lock specified attributes, if none specified locks all
	# check if object exists
	if mc.objExists(object):

		# lock specified attributes
		for channel in channels:
			for attr in attrs:
				try:
					mc.setAttr('{0}.{1}{2}'.format(object, channel, attr), k=0, l=1)
				except:
					pass

			mc.setAttr('{0}.v'.format(object), k=0, l=1)

	else:
		mc.error('{0} does not exist'.format(object))


def unlockAttrs(object, channels=['t', 'r', 's'], attrs=['x', 'y', 'z'], v=1):
	# function to unlock specified attributes, if none specified locks all
	# check if object exists
	if mc.objExists(object):

		# unlock specified attributes
		for channel in channels:
			for attr in attrs:
				mc.setAttr('{0}.{1}{2}'.format(object, channel, attr), k=1, l=0)

		mc.setAttr('{0}.v'.format(object), k=1, l=0)

	else:
		mc.error('{0} does not exist'.format(object))
