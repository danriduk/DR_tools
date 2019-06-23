'''
IK/FK limb class
'''

## MAYA MODULES ##
import maya.cmds as mc

## CUSTOM MODULES ##
from . import fkChain, ikChain, jointChain
reload(fkChain)
reload(ikChain)
reload(jointChain)


class Limb(object):
    def __init__(self,
                 prefix='c',
                 name='limb',
                 color='auto',
                 posList=([0, 0, 0])
                 ):

        self.prefix = prefix
        self.name = '{0}'.format(name)
        self.color = color
        self.posList = posList

        self.jntchain = None
        self.fkchain = None
        self.ikchain = None

    def createTemplate(self):
        self.jntchain = jointChain.JntChain(posList=self.posList,
                                            prefix=self.prefix, name=self.name)
        self.jntchain.createTemplate()

    def build(self):
        # create joints from pos list from template locs
        self.posList = [mc.xform(loc, q=1, ws=1, t=1)
                        for loc in self.jntchain.locs]

        # build chains
        # init fk and ik chains
        self.fkchain = fkChain.FKChain(
            posList=self.posList, prefix=self.prefix, name=self.name)
        self.ikchain = ikChain.IKChain(
            posList=self.posList, prefix=self.prefix, name=self.name)

        # build
        self.jntchain.build()
        self.fkchain.build()
        self.ikchain.build()
