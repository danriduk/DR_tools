'''
ik joint chain class
'''

import maya.cmds as mc
from . import jointChain, controls, utils


class ikChain(jointChain.jntChain):
	def __init__(
		self,
		prefix='c',
		name='ikChain',
		shape='cube',
		color='auto',
		posList=([0,0,0])
		):

		self.prefix = prefix
		self.name = '{0}IK'.format(name)
		self.shape = shape
		self.color = color
		self.posList = posList

		# init parent class
		jointChain.jntChain.__init__(
								self,
								prefix=self.prefix,
								name=self.name,
								suffix='jnt',
								posList=self.posList
								)

	def build(self):
		# call parent class build method
		jointChain.jntChain.build(self)

		# build control
		self._addControls()

	def _addControls(self):
		# add ik control to end joint
		ikCon = controls.Control(
						prefix=self.prefix,
						name=self.name,
						suffix='con',
						shape=self.shape,
						color=self.color,
						translateTo=self.jnts[-1]
						)
