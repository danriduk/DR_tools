'''
main class for rig controls
'''

import string
import maya.cmds as mc
from . import dictionaries
from . import overrides, checks, utils


class Control():

	def __init__(
		self,
		prefix='pre',
		name='name',
		suffix='con',
		scale=1.0,
		parent='',
		shape='circle',
		color='auto',
		lockChannels=[],
		translateTo='',
		rotateTo='',
		offsetLocs=1,
		offsetGrps=1
	):
		'''
		@param prefix: str, prefix name for control
		@param name: str, main name for control
		@param scale: float, scale size for control shape
		@param parent: str, parent for control
		@param shape: str, shape for the control
		@param lockChannels: list( str ), list of channels to lock on creation
		@param translateTo: str, object to match translation too
		@param rotateTo: str, object to match rotation too
		@param offsetLocs: int, number of offset locators to add too control
		@param offsetGrps: int, number of offset groups to add too control
		'''

		shapeDict = dictionaries.curveShapes()
		colorDict = dictionaries.colorDictionary()

		ctrlObject = None

		# check if shape is inside dictionary
		if shape not in shapeDict:
			mc.error('requested shape - {0} - not found'.format(shape))

		# get unique name
		fullName = checks.uniqueName(prefix, name, suffix)

		# create control
		ctrlObject = mc.curve(n=fullName, p=shapeDict[shape], d=1)

		# rename ctrlObject shape
		shape = checks.getShape(ctrlObject)
		mc.rename(shape, '{0}Shape'.format(ctrlObject))

		# control overrides
		overrides.lockAttrs(ctrlObject, channels=lockChannels)

		# scale control
		self.transformControlShape(ctrlObject, s=(scale, scale, scale))

		# color control based on prefix
		if color == 'auto':
			if prefix == 'l':
				overrides.override(ctrlObject, col='b')
			elif prefix == 'r':
				overrides.override(ctrlObject, col='r')
			elif prefix == 'c':
				overrides.override(ctrlObject, col='y')
			elif prefix == 'global':
				overrides.override(ctrlObject, col='g')
		# use specified color if not auto
		else:
			if color in colorDict.keys():
				overrides.override(ctrlObject, col=color)
			else:
				mc.error('{0} - does not exist in dictionary'.format(color))

		# translate and rotate too
		if mc.objExists(translateTo):
			mc.delete(mc.pointConstraint(translateTo, ctrlObject))
		if mc.objExists(rotateTo):
			mc.delete(mc.orientConstraint(rotateTo, ctrlObject))

		# parent control
		if mc.objExists(parent):
			mc.parent(ctrlGrp, parent)

		# offset locs and groups
		self.offsetLoc(ctrlObject, count=offsetLocs)
		self.offsetGrp(ctrlObject, count=offsetGrps)

		# global members
		self.con = ctrlObject

	def transformControlShape(self, ctrlObject, t=(0, 0, 0), ro=(0, 0, 0), s=(1, 1, 1)):

		# function to adject transforms of control shape
		shape = checks.getShape(ctrlObject)
		cluster = mc.cluster(shape)

		mc.xform(cluster, s=s, t=t, ro=ro, r=1)
		mc.delete(ctrlObject, ch=1)

	def parentShape(self, object, node):

		# parent shape under object
		shape = checks.getShape(node)
		mc.parent(shape, object, r=1, s=1)
		mc.delete(node)

	def offsetLoc(self, con, count=1):
		if count == 0:
			return

		locs = []
		# split name
		nameSplit = con.split('_')

		for num in range(count):
			if count == 1:
				letter = ''
			else:
				letter = string.ascii_lowercase[num]

			loc = mc.spaceLocator(n='{0}_{1}{2}_loc'.format(nameSplit[0], nameSplit[1],letter))
			mc.delete(mc.parentConstraint(con, loc[0]))

			locs.append(loc[0])

			# hide loc
			overrides.override(loc[0], v=0)

		# parenting
		mc.parent(con, locs[-1])

		if len(locs) > 1:
			utils.iterParenting(locs)

		# global members
		self.locs = locs

	def offsetGrp(self, con, count=1):
		if count == 0:
			return

		grps = []
		# split name
		nameSplit = con.split('_')

		for num in range(count):
			if count == 1:
				letter = ''
			else:
				letter = string.ascii_lowercase[num]

			grp = mc.group(n='{0}_{1}{2}_grp'.format(nameSplit[0], nameSplit[1],letter), em=1)
			mc.delete(mc.parentConstraint(con, grp))

			grps.append(grp)

		# parenting
		if len(grps) > 1:
			utils.iterParenting(grps)

		if self.locs:
			mc.parent(self.locs[-1], grps[0])
		else:
			mc.parent(con, grps[-1])

		# global members
		self.grps = grps
