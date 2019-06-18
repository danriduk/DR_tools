'''
general utility functions
'''

import maya.cmds as mc



def iterParenting(nodes, rev=1):
	print nodes
	'''
	parents a given lists nodes under each other in an FK chain
	'''
	# sanity checks
	if not nodes:
		return

	if rev == 1:
		nodes.reverse()

	for i, node in reversed(list(enumerate(nodes))):
		if i == 0:
			break

		mc.parent(nodes[i - 1], nodes[i])
