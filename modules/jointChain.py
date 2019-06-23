'''
joint chain class
'''

## MAYA MODULES ##
import maya.cmds as mc

## CUSTOM MODULES ##
from ..utils import checks
from ..functionSets import jntFn
from ..utils import checks, hierarchy
reload(jntFn)


class JntChain(object):
    def __init__(
            self,
            prefix='c',
            name='joint',
            suffix='jnt',
            posList=[(0, 0, 0)]
    ):

        self.prefix = prefix
        self.name = name
        self.suffix = suffix
        self.posList = posList

        self.TMPLgrp = None
        self.locs = []
        self.jnts = []

    def createTemplate(self):
        # get unique name
        fullName = checks.uniqueName(self.prefix, self.name, 'TMPL')
        # create template top group
        self.TMPLgrp = mc.group(em=1, n=fullName)
        mc.xform(self.TMPLgrp, t=self.posList[0])

        # create locators from pos list
        for pos in self.posList:
            mc.select(cl=1)

            # get unique name
            fullName = checks.uniqueName(self.prefix, self.name, 'LOC')

            loc = mc.spaceLocator(n=fullName)[0]
            mc.xform(loc, t=pos)
            mc.parent(loc, self.TMPLgrp)

            self.locs.append(loc)

        hierarchy.iterParenting(self.locs)
        self.locs.sort()

    def build(self):
        # create joints from pos list from template locs
        if self.locs:
            self.posList = [mc.xform(loc, q=1, ws=1, t=1) for loc in self.locs]

        for pos in self.posList:
            # get unique name
            fullName = checks.uniqueName(self.prefix, self.name, self.suffix)

            # clear selection to create joints in root
            mc.select(cl=1)
            jnt = mc.joint(n=fullName, p=pos)

            self.jnts.append(jnt)

        hierarchy.iterParenting(self.jnts)

        # orient chain
        oriJnt = jntFn.JointFn(self.jnts[-1])
        oriJnt.orientChain()
