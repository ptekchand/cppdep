import unittest
from pmock import *
from metrics import Metrics

class TestMetrics(MockTestCase):
  def setUp(self):
    self.metrics = Metrics()
    self.metrics.factory = self.mock()
    self.fileMetrics = self.mock()
    self.metrics.factory.expects(once()).create().will(return_value(self.fileMetrics))

  def node(self, name="test.cpp"):
    newNode = self.mock()
    newNode.expects(at_least_once()).file().will(return_value(name))
    return newNode

  def testAddFile(self):
    node = self.node()
    self.fileMetrics.expects(once()).addNode(same(node))
    self.metrics.addFile(node)
    assert(self.metrics.file("test.cpp") is self.fileMetrics)
    self.assertEqual(len(self.metrics.files()), 1)
    assert(self.metrics.files()[0] is self.fileMetrics)

  def testAddSameFileTwice(self):
    node = self.node()
    self.fileMetrics.expects(once()).addNode(same(node))
    self.fileMetrics.expects(once()).addNode(same(node))

    self.metrics.addFile(node)
    self.metrics.addFile(node)
    assert(self.metrics.file("test.cpp") is self.fileMetrics)
    self.assertEqual(len(self.metrics.files()), 1)

  def testTwoDifferentFiles(self):
    node1 = self.node("test1.h")
    node2 = self.node("test2.h")
    self.fileMetrics.expects(once()).addNode(same(node1))
    self.fileMetrics.expects(once()).addNode(same(node2))
    self.metrics.factory.expects(once()).create().will(return_value(self.fileMetrics))

    self.metrics.addFile(node1)
    self.metrics.addFile(node2)
    assert(self.metrics.file("test1.h") is self.fileMetrics)
    assert(self.metrics.file("test2.h") is self.fileMetrics)
    self.assertEqual(len(self.metrics.files()), 2)


if __name__ == "__main__":
  unittest.main()
