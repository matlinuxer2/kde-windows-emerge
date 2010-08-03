#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# copyright 2010 by Intevation GmbH
#
"""Tool to generate Graphviz DOT file of the package dependencies
   for a given emerge package. Doubles as a library for explict
   dependency graph traverals.

   Usage:

   Precondition: Set the environment variables needed by emerge.

   $ python bin/dependencies.py -t <type of output> <emerge package> > deps.dot

   with <type of output> being the kind of output send to stdout.
   Possible values: 'dot' and 'xml'. Defaults to 'dot'

   The output is send to stdout. Piped into a file you may use
   dot to generate a graphical version.

   $ dot -T svg -o deps.svg deps.dot
"""

__author__  = "Sascha L. Teichmann <sascha.teichmann@intevation.de>"
__license__ = "GNU General Public License (GPL)"

import portage
import sys
import os
import getopt

OUTPUT_DOT = 0
OUTPUT_XML = 1

class Visitor(object):
    """Visitor applied to a node in the 
       dependency graph during traversal
    """

    CONTINUE_CHILDREN = 1
    IGNORE_CHILDREN   = 2

    def beforeChildren(self, node, context):
        """Called before the children of the node are visited."""
        return Visitor.CONTINUE_CHILDREN

    def afterChildren(self, node, context):
        """Called after the children  of the node are visited."""
        return Visitor.CONTINUE_CHILDREN

def nlSeparated(node):
    """Replace ':' by newlines to make target look better in dot output.""" 
    return str(node).replace(":", r"\n")

class GraphvizCreator(Visitor):
    """Visitor to create DOT files from dependency graphs."""

    def afterChildren(self, node, context):
        visited, out, ranks = context
        if not node.children: max_depth = 666
        else:                 max_depth = node.maxDepth()
        ranks.setdefault(max_depth, set()).add(node)
        for child in node.children:
            link = '"%s" -> "%s"' % (
                nlSeparated(node), nlSeparated(child))
            if link not in visited:
                visited.add(link)
                out.append(link)
        return Visitor.CONTINUE_CHILDREN

    def createOutput(self, tree):
        visited = set()
        out = [
            'digraph "dependencies" {', 
            'ranksep=2;',
            'size="6,6";' ]
        ranks = {}
        tree.visit(self, (visited, out, ranks))

        for k, v in ranks.iteritems():
            out.append("{ rank=same; ")
            for n in v: out.append('"%s";' % nlSeparated(n))
            out.append("}")

        out.append("}")

        return "\n".join(out)

class XMLCreator(Visitor):
    """Visitor to create an XML representation of the dependency graph."""

    def __init__(self):
        self.nodes_so_far = {}
        self.ignored      = False

    def beforeChildren(self, node, out):
        if not isinstance(node, DependenciesNode):
            return Visitor.CONTINUE_CHILDREN
        node_name = str(node)
        node_id = self.nodes_so_far.get(node_name)
        if node_id is not None:
            out.append('<dep ref="n%d"/>' % node_id)
            self.ignored = True
            return Visitor.IGNORE_CHILDREN

        new_id = len(self.nodes_so_far)

        self.nodes_so_far[node_name] = new_id
        out.append('<dep id="n%d" cat="%s" pgk="%s" ver="%s" tag="%s"'% (
            new_id,
            node.category, node.package, node.version, node.tag))
        if hasattr(node, "children") and not node.children:
            out.append("/>")
            self.ignored = True
            return Visitor.IGNORE_CHILDREN
        out.append(">")
        return Visitor.CONTINUE_CHILDREN

    def afterChildren(self, node, out):
        if self.ignored: self.ignored = False
        else:            out.append("</dep>")
        return Visitor.CONTINUE_CHILDREN

    def createOutput(self, tree):
        out = ['<?xml version="1.0" encoding="UTF-8" ?>\n']
        out.append("<deps>")
        tree.visit(self, out)
        out.append("</deps>")
        return ''.join(out)

class DependenciesNode(object):
    """A node in the dependency graph."""

    def __init__(self, category, package, version, tag = "1", children = None):
        if children is None: children = []
        self.category = category
        self.package  = package
        self.version  = version
        self.tag      = tag
        self.children = children
        self.parents  = []

    def __str__(self):
        return "%s:%s:%s:%s" % (
            self.category, self.package, self.version, self.tag)

    def visit(self, visitor, context):
        """Apply a visitor to this node."""
        if visitor.beforeChildren(self, context) == Visitor.CONTINUE_CHILDREN:
            for child in self.children:
                child.visit(visitor, context)
        visitor.afterChildren(self, context)

    def maxDepth(self):
        """Calculates the maximum depth of this node."""
        if not self.parents:
            return 0
        pdepth = -1
        for p in self.parents:
            d = p.maxDepth()
            if d > pdepth: pdepth = d
        return pdepth + 1

class DependenciesTree(object):
    """A dependency tree. More a kind of DAG (directed acyclic graph)."""

    def __init__(self):
        self.roots    = []
        self.key2node = {}

    def addDependencies(self, category, package, version = ""):
        """Add a new root dependency tree to this graph."""

        pi = portage.PortageInstance

        if portage.platform.isCrossCompilingEnabled() \
        or os.getenv("EMERGE_SOURCEONLY") == "True" or os.getenv("EMERGE_SOURCEONLY") == "1":
            sp = pi.getCorrespondingSourcePackage(package)
            if sp:
                # we found such a package and we're allowed to replace it
                category = sp[0]
                package = sp[1]
                version = pi.getNewestVersion(category, package)

        if category == "":
            category = pi.getCategory(package)

        if version == "":
            version = pi.getNewestVersion(category, package)

        try:
            tag = pi.getAllTargets(category, package, version ).keys()[0]
        except:
            tag = "1"

        node = self.buildDepNode(category, package, version, tag)

        if not node in self.roots:
            self.roots.append(node)

    def buildDepNode(self, category, package, version, tag):
        """Recursive method to construct the nodes of the dependency tree."""
        key = "%s-%s-%s-%s" % (category, package, version, tag)
        try:
            node = self.key2node[key]
            return node
        except KeyError:
            pass

        children = []

        for t in portage.getDependencies(category, package, version):
            sub_node = self.buildDepNode(t[0], t[1], t[2], tag)
            children.append(sub_node)

        node = DependenciesNode(category, package, version, tag, children)
        for child in children:
            child.parents.append(node)

        self.key2node[key] = node

        return node

    def visit(self, visitor, context):
        """Apply a visitor to all parts of this graph."""
        for root in self.roots:
            root.visit(visitor, context)

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:", ["type="])
    except getopt.GetoptError, err:
        print >> sys.stderr, str(err)
        sys.exit(1)

    if len(args) < 1:
        print >> sys.stderr, "missing package"
        sys.exit(1)

    output_type = OUTPUT_DOT

    for o, a in opts:
        if o in ("-t", "--type"):
            if a == "xml": output_type = OUTPUT_XML
            else:          output_type = OUTPUT_DOT

    # little workaround to not display debug infos in generated output
    old_emerge_verbose = os.environ.get('EMERGE_VERBOSE')
    os.environ['EMERGE_VERBOSE'] = '0'

    packageList, categoryList = portage.getPackagesCategories(args[0])

    dep_tree = DependenciesTree()

    for catagory, package in zip(categoryList, packageList):
        dep_tree.addDependencies(catagory, package)

    if old_emerge_verbose is not None:
        os.environ['EMERGE_VERBOSE'] = old_emerge_verbose

    if   output_type == OUTPUT_XML: creator = XMLCreator()
    elif output_type == OUTPUT_DOT: creator = GraphvizCreator()

    output = creator.createOutput(dep_tree)

    print output

if __name__ == '__main__':
    main()