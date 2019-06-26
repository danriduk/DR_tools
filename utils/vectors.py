'''
utility function for vectors
'''

## MAYA MODULES ##
import maya.cmds as mc
import maya.OpenMaya as om

## CUSTOM MODULES ##
from . import checks


def createVector(pos, buildLoc=False):
    name = checks.uniqueName('v', '', 'loc')

    vector = om.MVector(pos[0], pos[1], pos[2])

    if buildLoc:
        loc = mc.spaceLocator(n=name)[0]
        grp = mc.group(em=1, n=name.replace('loc', 'grp'))
        mc.xform(loc, t=(vector.x, vector.y, vector.z))
        mc.parent(loc, grp)

        return vector, loc

    return vector


def addVectors(vec1, vec2, buildLoc=False):
    name = checks.uniqueName('v', 'AplusB', 'loc')

    vector = vec1 + vec2

    if buildLoc:
        loc = mc.spaceLocator(n=name)[0]
        grp = mc.group(em=1, n=name.replace('loc', 'grp'))
        mc.xform(loc, t=(vector.x, vector.y, vector.z))
        mc.parent(loc, grp)

        return vector, loc

    return vector


def subVectors(vec1, vec2, buildLoc=False):
    name = checks.uniqueName('v', 'AplusB', 'loc')

    vector = vec1 - vec2

    if buildLoc:
        loc = mc.spaceLocator(n=name)[0]
        grp = mc.group(em=1, n=name.replace('loc', 'grp'))
        mc.xform(loc, t=(vector.x, vector.y, vector.z))
        mc.parent(loc, grp)

        return vector, loc

    return vector
