#!/bin/env python
import unittest
from dependencyBuilder import DependencyBuilder
from pmock import *

class TestDependencyBuilder(MockTestCase):
  def setUp(self):
    self.metrics = self.mock()
    self.builder = DependencyBuilder(self.metrics)
    self.builder.factory = self.mock()

  def treeFactoryExpects(self, param=None):
    if param is None:
      param = once()
    return self.builder.factory.expects(param)

  def getTree(self):
    return self.builder.getTree()
    
  def testNothing(self):
    assert(self.getTree() is None)

  def testOneLineOnly(self):
    self.builder.line()
    assert(self.getTree() is None)

  def testOneNode(self):
    node = self.mock()
    self.treeFactoryExpects().create(eq("./file.cpp"), eq("file.cpp"), same(None)).will(return_value(node))
    self.metrics.expects(once()).addFile(same(node))
    self.builder.node("./file.cpp", "file.cpp")
    assert(self.getTree() is node)

  def testTwoFiles(self):
    nodeA = self.mock()
    nodeB = self.mock()
    self.treeFactoryExpects().create(eq("./a.cpp"), eq("a.cpp"), same(None)).will(return_value(nodeA))
    self.treeFactoryExpects().create(eq("./b.cpp"), eq("b.cpp"), same(None)).will(return_value(nodeB))
    self.metrics.expects(once()).addFile(same(nodeA))
    self.metrics.expects(once()).addFile(same(nodeB))

    self.builder.node("./a.cpp", "a.cpp")
    self.builder.end()
    self.builder.node("./b.cpp", "b.cpp")
    assert(self.getTree() is nodeA)

  def testOneNodeFollowedByLine(self):
    node = self.mock()
    self.treeFactoryExpects().create(eq("./file.cpp"), eq("file.cpp"), same(None)).will(return_value(node))
    self.metrics.expects(once()).addFile(same(node))
    node.set_default_stub(return_value(None))
    self.builder.node("./file.cpp", "file.cpp")
    self.builder.line()
    assert(self.getTree() is node)

  def expectChildCreation(self, node, file, name):
    node.expects(once()).method("isMyParent").will(return_value(False))
    node.expects(once()).file().will(return_value("nomatch"))
    child = self.mock()
    self.treeFactoryExpects().create(eq(file), eq(name), same(node)).will(return_value(child))
    self.metrics.expects(once()).addFile(same(child))
    return child

  def testNesting(self):
    node = self.mock()
    self.treeFactoryExpects().create(eq("./file.cpp"), eq("file.cpp"), same(None)).will(return_value(node))
    self.metrics.expects(once()).addFile(same(node))

    child = self.expectChildCreation(node, "sys/time.h", "time.h")
    self.expectChildCreation(child, "sys/ctype.h", "ctype.h")

    self.builder.node("./file.cpp", "file.cpp")
    self.builder.node("sys/time.h", "time.h")
    self.builder.node("sys/ctype.h", "ctype.h")
    assert(self.getTree() is node)

  def testSiblings(self):
    node = self.mock()
    self.treeFactoryExpects().create(eq("./file.cpp"), eq("file.cpp"), same(None)).will(return_value(node))
    self.metrics.expects(once()).addFile(same(node))

    child = self.expectChildCreation(node, "sys/time.h", "time.h")
    child.expects(once()).isMyParent(eq("./file.cpp")).will(return_value(True))
    child.expects(once()).parent().will(return_value(node))
    self.expectChildCreation(node, "sys/ctype.h", "ctype.h")

    self.builder.node("./file.cpp", "file.cpp")
    self.builder.node("sys/time.h", "time.h")
    self.builder.node("./file.cpp", "file.cpp")
    self.builder.node("sys/ctype.h", "ctype.h")
    assert(self.getTree() is node)

if __name__ == "__main__":
  unittest.main()
