'''
ik creation class
'''

## MAYA MODULES ##
import maya.cmds as mc

## CUSTOM MODULES ##
from ..utils import checks


class IKHandle(object):
    def __init__(self,
                 prefix='c',
                 name='ik',
                 suffix='HDL',
                 start=None,
                 end=None,
                 type='RP'
                 ):

        self.prefix = prefix
        self.name = name
        self.suffix = suffix

        self.SJ = start
        self.EJ = end

        # solver type
        if type == 'RP':
            self.iktype = 'ikRPsolver'
        elif type == 'SC':
            self.iktype = 'ikSCsolver'
        else:
            mc.error('{0} is not a valid solver type'.format(type))

        self.handle = None
        self.effector = None

        self._sanityCheck(self.SJ)
        self._sanityCheck(self.EJ)

    def build(self):
        fullName = checks.uniqueName(self.prefix, self.name, self.suffix)

        # create ik handle
        self.handle = mc.ikHandle(n=fullName, sj=self.SJ, ee=self.EJ)

        # rename effector
        mc.rename(self.handle[1], '{0}eff'.format(fullName))

    def _sanityCheck(self, node):
        if not mc.objExists(node):
            mc.error('Joint {0} does not exist'.format(node))

        if not mc.objectType(node):
            mc.error('object {0} is not of type "JOINT"'.format(node))
