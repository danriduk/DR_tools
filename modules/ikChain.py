'''
ik joint chain class
'''

## MAYA MODULES ##
import maya.cmds as mc

## CUSTOM MODULES ##
from . import jointChain
from ..functionSets import controlFn
from ..utils import hierarchy


class IKChain(jointChain.JntChain, object):
    def __init__(
            self,
            prefix='c',
            name='ikChain',
            shape='cube',
            color='auto',
            posList=([0, 0, 0])
    ):

        self.prefix = prefix
        self.name = '{0}IK'.format(name)
        self.shape = shape
        self.color = color
        self.posList = posList

        # init parent class
        super(IKChain, self).__init__(
            prefix=self.prefix,
            name=self.name,
            suffix='jnt',
            posList=self.posList
        )

    def build(self):
        # call parent class build method
        super(IKChain, self).build()

        # build control
        self._addControls()

    def _addControls(self):
        # add ik control to end joint
        ikCon = controlFn.Control(
            prefix=self.prefix,
            name=self.name,
            suffix='con',
            shape=self.shape,
            color=self.color,
            translateTo=self.jnts[0]
        )
