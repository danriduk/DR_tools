'''
utility function for vectors
'''

## MAYA MODULES ##
import maya.cmds as mc
import maya.OpenMaya as om


def createVector(node):
    if not mc.objectType(node) == 'transform':
        mc.error('{0} not of type, transform'.format(node))

    pos = mc.xform(node, q=1, ws=1, t=1)
    vector = om.MVector(pos[0], pos[1], pos[2])

    return vector
