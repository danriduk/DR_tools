'''
fk joint chain class
'''

import maya.cmds as mc
from . import jointChain, controls, utils


class fkChain(jointChain.jntChain):
	def __init__(
		self,
		prefix='c',
		name='fkChain',
		shape='circle',
		color='auto',
		posList=[(0,0,0)]
		):

		self.prefix = prefix
		self.name = '{0}FK'.format(name)
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

		# global members
		self.cons = []
		self.consClass = []

	def build(self):
		# call parent class build method
		jointChain.jntChain.build(self)

		# build
		self._addControls()
		self._fkParenting()

	def _addControls(self):
		if len(self.jnts) < 1:
			return

		for jnt in self.jnts:
			fkCon = controls.Control(
						prefix=self.prefix,
						name=self.name,
						suffix='con',
						shape=self.shape,
						translateTo=jnt,
						rotateTo=jnt,
						color=self.color
						)

			fkCon.transformControlShape(fkCon.con, ro=(0,0,90))

			self.cons.append(fkCon.con)
			self.consClass.append(fkCon)

			# constrain joint too control
			mc.parentConstraint(fkCon.con, jnt)

	def _fkParenting(self):
		# fk parenting
		for i in reversed(range(len(self.consClass))):
			# check if not last control in list
			if i != (len(self.consClass)-1):
				mc.parent(self.consClass[i+1].grps[0], self.consClass[i].con)
