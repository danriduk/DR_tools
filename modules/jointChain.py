'''
joint chain class
'''

## MAYA MODULES ##
import maya.cmds as mc

## CUSTOM MODULES ##
from ..utils import checks
from ..functionSets import jntFn
from ..utils import checks, hierarchy


class JntChain():
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

        self.jnts = []

    def build(self):
        # create joints from pos list
        for pos in self.posList:
            # clear selection to create joints in root
            mc.select(cl=1)

            # get unique name
            fullName = checks.uniqueName(self.prefix, self.name, self.suffix)
            nameSplit = fullName.split('_')
            jntName = '{0}_{1}_{2}'.format(
                nameSplit[0], nameSplit[1], nameSplit[-1])

            jnt = mc.joint(n=jntName, p=pos)

            self.jnts.append(jnt)

        hierarchy.iterParenting(self.jnts)

        # orient chain
        oriJnt = jntFn.Jnt(edit=self.jnts[-1])
        oriJnt.orientChain()
