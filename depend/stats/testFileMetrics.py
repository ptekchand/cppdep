import unittest
from pmock import *
from fileMetrics import FileMetrics

class TestFileMetrics(MockTestCase):
  def setUp(self):
    self.lineCounter = self.mock()
    self.fileMetrics = FileMetrics()
    self.fileMetrics.lineCounter = self.lineCounter
    self.node = self.mock()
    self.node.stubs().file().will(return_value("./test.cpp"))
    self.node.stubs().name().will(return_value("test.cpp"))

  def expectCounts(self, counts):
    for count in counts:
      self.node.expects(once()).totalLines().will(return_value(count))
      self.fileMetrics.addNode(self.node)

  def expectFileLineCount(self, count):
    self.lineCounter.expects(once()).countLines(eq("./test.cpp")).will(return_value(count))

  def testLinesCompiled(self):
    self.expectCounts([1])
    self.assertEqual(self.fileMetrics.compiledLines(), 1)

  def testLinesCompiledTwoNodes(self):
    self.expectCounts([100, 25])
    self.assertEqual(self.fileMetrics.compiledLines(), 125)

  def testCountFileLinesNoFile(self):
    self.assertEqual(self.fileMetrics.fileLines(), 0)

  def testCountFileLines(self):
    self.fileMetrics.addNode(self.node)
    self.expectFileLineCount(26)
    self.assertEqual(self.fileMetrics.fileLines(), 26)
    self.assertEqual(self.fileMetrics.name(), "test.cpp")
    self.assertEqual(self.fileMetrics.file(), "./test.cpp")

  def testFileLineCountCache(self):
    self.fileMetrics.addNode(self.node)
    self.expectFileLineCount(26)
    self.assertEqual(self.fileMetrics.fileLines(), 26)
    self.assertEqual(self.fileMetrics.fileLines(), 26)

  def testCountFileLinesTwoNodes(self):
    self.fileMetrics.addNode(self.node)
    self.fileMetrics.addNode(self.node)
    self.expectFileLineCount(26)
    self.assertEqual(self.fileMetrics.fileLines(), 26)

  def createNode(self, parent):
    node = self.mock()
    node.expects(once()).parent().will(return_value(parent))
    return node

  def testCountIncludedFrom(self):
    self.fileMetrics.addNode(self.createNode(self.mock()))
    self.fileMetrics.addNode(self.createNode(self.mock()))
    self.assertEqual(self.fileMetrics.includedFrom(), 2)

  def testCountIncludedFromWithoutParent(self):
    self.fileMetrics.addNode(self.createNode(self.mock()))
    self.fileMetrics.addNode(self.createNode(parent=None))
    self.assertEqual(self.fileMetrics.includedFrom(), 1)

if __name__ == "__main__":
  unittest.main()
