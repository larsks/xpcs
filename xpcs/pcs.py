import subprocess
from lxml import etree

from xpcs.exc import *


class Clone(dict):
    def __init__(self, clone):
        assert(clone.tag == 'clone')
        super(Clone, self).__init__(clone.items())
        self._resources = clone.findall('resource')

    @property
    def resources(self):
        return (Resource(rsc, parent=self)
                for rsc in self._resources)


class Group(dict):
    def __init__(self, group):
        assert(group.tag == 'group')
        super(Group, self).__init__(group.items())
        self._resources = group.findall('resource')

    @property
    def resources(self):
        return (Resource(rsc, parent=self)
                for rsc in self._resources)


class Resource(dict):
    def __init__(self, rsc, parent=None):
        assert(rsc.tag == 'resource')
        super(Resource, self).__init__(rsc.items())
        if parent is not None:
            self['parent'] = parent

        self._nodes = rsc.findall('node')

    @property
    def nodes(self):
        return (Node(node) for node in self._nodes)


class Node(dict):
    def __init__(self, node):
        super(Node, self).__init__(node.items())


def to_object(thing):
    if thing.tag == 'resource':
        return Resource(thing)
    elif thing.tag == 'clone':
        return Clone(thing)
    elif thing.tag == 'group':
        return Group(thing)
    else:
        raise ValueError(thing.tag)


class PCS(object):
    def __init__(self, statusfile=None):
        self._status = None
        self._status_file = None

        if statusfile is not None:
            if hasattr(statusfile, 'read'):
                self._status = statusfile.read()
            else:
                self._status_file = statusfile

    @property
    def status(self):
        if self._status:
            status = self._status
        elif self._status_file:
            with open(self._status_file) as fd:
                status = fd.read()
        else:
            status = subprocess.check_output(
                ['pcs', 'status', 'xml'])

        return etree.fromstring(status)

    @property
    def resources(self):
        return (to_object(x) for x in
                self.status.xpath('/crm_mon/resources/*'))

    @property
    def nodes(self):
        return (Node(x) for x in
                self.status.xpath('/crm_mon/nodes/node'))

    def resource(self, name):
        rsc = self.status.xpath(
            '/crm_mon/resources/*[@id="%s"]' % name)
        if not len(rsc):
            raise ResourceNotFound(name)

        return to_object(rsc[0])

    def node(self, name):
        node = self.status.xpath(
            '/crm_mon/nodes/node[@name="%s"]' % name)
        if not len(node):
            raise NodeNotFound(name)

        return Node(node[0])
