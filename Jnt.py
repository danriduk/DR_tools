'''
Super Joint class
'''

import maya.cmds as mc
from . import overrides


class Jnt():
    """
    main joint class used throughout
    @param side: (str), specify side for joint valid sides (c,l,r)
    @param name: (str), main name for created joint
    @param type: (str), type of joint to create valid types (jnt,bnd,env)
            type='jnt' : generic joint for rig functionality
            type='bnd' : any joint that is skinned anything but geometry
            type='env' : joints that will be driving geometry via skin clusters
    """

    def __init__(self,
            edit=None,
            side='c',
            name='joint',
            suffix='jnt',
            pos=(0, 0, 0),
            **kwargs):

        self.jnt = None
        self.type = type

        kwargs['name'] = '{0}_{1}_{2}'.format(side, name, suffix)
        for key in kwargs:
            kwargs[key] = kwargs[key]

        kwargs['radius'] = 1.0
        if not edit:
            self._create(flags=kwargs)
            mc.xform(self.jnt, t=pos)
        else:
            self.jnt = edit

    def _create(self, flags={}):
        # method to create joint
        self.jnt = mc.joint(**flags)
        mc.select(cl=1)

    def getJntChain(self):
        # returns list of child joints
        if not mc.objExists(self.jnt):
            return None

        chain = [ jnt for jnt in mc.listRelatives(self.jnt, type='joint', c=1, ad=1) ][::-1]
        chain.insert(0, self.jnt)
        return chain

    def _unparentChild(self, obj):
        children = mc.listRelatives(obj, c=1, pa=1) or []
        return [mc.parent(child, w=1)[0] for child in children]

    def _reparentChild(self, *args):
        for child in args[1]:
            mc.parent(child, args[0])

    def _orientPlanar(self, upVector=(0, 1, 0)):
        # orient the middle joint of a 3 joint chain too its plane
        chain = self.getJntChain()
        for jnt in chain:
            par = mc.listRelatives(jnt, p=1, pa=1)
            if not par:
                continue

            children = self._unparentChild(jnt)
            if not children:
                continue

            mc.delete(mc.aimConstraint(children[0], jnt,
                                       aim=(1, 0, 0), u=upVector,
                                       wut='object', wuo=par[0]))

            mc.makeIdentity(jnt, a=1)
            self._reparentChild(jnt, children)

    def _alignToChild(self):
        # orients the parent of a joint to its child if no parent is found
        chain = self.getJntChain()
        for jnt in chain:
            children = self._unparentChild(jnt)
            if children:
                mc.delete(mc.aimConstraint(children[0], jnt,
                                           aim=(1, 0, 0), u=(0, 1, 0), wu=(0, 1, 0),
                                           wut='objectrotation', wuo=children[0]))

                mc.makeIdentity(jnt, a=1)
                self._reparentChild(jnt, children)

    def _zeroEndOrients(self):
        # orients the end joint too its parent joint
        chain = self.getJntChain()
        if chain:
            mc.setAttr('{0}.jointOrient'.format(chain[-1]), 0, 0, 0)

    def orientChain(self, upVector=(0, 1, 0)):
        self._orientPlanar(upVector=upVector)
        self._zeroEndOrients()
        self._alignToChild()

    def stripName(self):
        # returns split name of joint [prefix, name, suffix]
        if not mc.objExists(self.jnt):
            return None

        return self.jnt.split('_')

    def addEnv(self):
        mc.select(cl=1)
        # adds env joint parented under self.jnt
        name = self.jnt.replace('jnt', 'env')

        children = self._unparentChild(self.jnt)

        self.env = mc.duplicate(self.jnt, n=name)[0]
        mc.parent(self.env, self.jnt)
        mc.setAttr('{0}.radius'.format(self.env), 2)
        overrides.override(self.env, col='env')

        self._reparentChild(self.jnt, children)
        mc.select(self.jnt)

    def addBnd(self):
        mc.select(cl=1)
        # adds bnd joint parented under self.jnt
        name = self.jnt.replace('jnt', 'bnd')

        children = self._unparentChild(self.jnt)

        self.env = mc.duplicate(self.jnt, n=name)[0]
        mc.parent(self.env, self.jnt)
        mc.setAttr('{0}.radius'.format(self.env), 1.5)
        overrides.override(self.env, col='bnd')

        self._reparentChild(self.jnt, children)
        mc.select(self.jnt)
