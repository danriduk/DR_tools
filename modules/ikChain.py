'''
ik joint chain class
'''

## MAYA MODULES ##
import maya.cmds as mc

## CUSTOM MODULES ##
from . import jointChain
from ..functionSets import controlFn
from ..utils import hierarchy, vectors
from ..base import ikhandle
reload(jointChain)


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

        self.ikCon = None
        self.elbowCon = None
        self.hdl = None

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

        # create ikhandle
        self.hdl = ikhandle.IKHandle(prefix=self.prefix, name=self.name,
                                     start=self.jnts[0], end=self.jnts[-1])
        self.hdl.build()

        # build control
        self._addControls()
        mc.parent(self.hdl.handle[0], self.ikCon.con)

        # print self.jnts

    def _addControls(self):
        # add ik control to end joint
        self.ikCon = controlFn.Control(
            prefix=self.prefix,
            name=self.name,
            suffix='con',
            shape=self.shape,
            color=self.color,
            translateTo=self.jnts[-1]
        )

        # build pole vector con
        self._poleVectorPos()
        self.elbowCon = controlFn.Control(
            prefix=self.prefix,
            name='{0}PV'.format(self.name),
            suffix='con',
            shape='sphere',
            color=self.color,
            scale=0.5
        )

        mc.xform(self.elbowCon.grps[0], t=(self.poleVectorPos))
        mc.poleVectorConstraint(self.elbowCon.con, self.hdl.handle[0])

    def _poleVectorPos(self):
        rootVec = vectors.createVector(mc.xform(self.jnts[0], q=1, t=1, ws=1))
        midVec = vectors.createVector(mc.xform(self.jnts[1], q=1, t=1, ws=1))
        endVec = vectors.createVector(mc.xform(self.jnts[2], q=1, t=1, ws=1))

        rootToEndVec = (endVec - rootVec)
        rootToMidVec = (midVec - rootVec)

        scaleVal = (rootToEndVec * rootToMidVec) / \
            (rootToEndVec * rootToEndVec)

        rootToEndElbowVec = rootToEndVec * scaleVal + rootVec

        self.poleVectorPos = ((midVec - rootToEndElbowVec) *
                              (rootToEndVec.length() / 2)) + midVec
