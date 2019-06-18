'''
joint chain class
'''

import maya.cmds as mc
<<<<<<< HEAD
from . import checks, utils, Jnt
reload(utils)



class jntChain():
	def __init__(
		self,
		prefix='c',
		name='joint',
		suffix='jnt',
		posList=[(0,0,0)]
		):

		self.prefix = prefix
		self.name = name
		self.suffix = suffix
		self.posList = posList

		self.jnts = []

	def build(self):
		# create joints from pos list
		for p in self.posList:
			# clear selection to create joints in root
			mc.select(cl=1)

			# get unique name
			fullName = checks.uniqueName(self.prefix, self.name, self.suffix)
			nameSplit = fullName.split('_')
			jnt = Jnt.Jnt(side=nameSplit[0],
						name=nameSplit[1],
						suffix=nameSplit[-1],
						pos=p)
			# jnt = mc.joint(name=fullName, p=p)
			self.jnts.append(jnt.jnt)

		utils.iterParenting(self.jnts)
		# orient chain
		jnt.orientChain()

	def displayAxis(self, jnts=[]):
		# toggle display axis
		for jnt in jnts:
			attr = mc.getAttr('{0}.displayLocalAxis'.format(jnt))
			mc.setAttr('{0}.displayLocalAxis'.format(jnt), not attr)

	def _unparentChild(self, jnt):
		# list children of joint
		children = mc.listRelatives(jnt, c=1, pa=1) or []
		# return unparented child joint
		return [ mc.parent(child, w=1)[0] for child in children ]

	def _reparentChild(self, jnt, children):
		# reparent child joint too given joint
		for child in children:
			mc.parent(child, jnt)
=======
from . import checks, utils


class JntChain():
    def __init__(
            self,
            prefix='c',
            name='joint',
            suffix='jnt'
    ):

        self.prefix = prefix
        self.name = name
        self.suffix = suffix

        self.jnts = []

    def build(self, pos=[(0, 0, 0)]):
        # create joints from pos list
        for p in pos:
            # clear selection to create joints in root
            mc.select(cl=1)

            # get unique name
            fullName = checks.uniqueName(self.prefix, self.name, self.suffix)
            jnt = mc.joint(name=fullName, p=p)
            self.jnts.append(jnt)

        utils.iterParenting(self.jnts)

    def displayAxis(self, jnts=[]):
        # toggle display axis
        for jnt in jnts:
            attr = mc.getAttr('{0}.displayLocalAxis'.format(jnt))
            mc.setAttr('{0}.displayLocalAxis'.format(jnt), not attr)
>>>>>>> vscode test
