import subprocess
from lxml import etree

from xpcs.exc import *


class Resource(dict):
    def __init__(self, rsc):
        super(Resource, self).__init__(rsc.items())
        self['nodes'] = (x.get('name') for x in rsc.findall('node'))


class Node(dict):
    def __init__(self, node):
        super(Node, self).__init__(node.items())


class PCS(object):
    @property
    def status(self):
        status = subprocess.check_output(
            ['pcs', 'status', 'xml'])
        return etree.fromstring(status)

    @property
    def resources(self):
        return (Resource(x) for x in
                self.status.xpath('/crm_mon/resources/resource'))

    @property
    def nodes(self):
        return (Node(x) for x in
                self.status.xpath('/crm_mon/nodes/node'))

    def resource(self, rid):
        rsc = self.status.xpath(
            '/crm_mon/resources/resource[@id="%s"]' % rid)
        if not len(rsc):
            raise ResourceNotFound(rid)

        return Resource(rsc[0])

    def node(self, name):
        node = self.status.xpath(
            '/crm_mon/nodes/node[@name="%s"]' % rid)
        if not len(node):
            raise NodeNotFound(name)

        return Node(node[0])
