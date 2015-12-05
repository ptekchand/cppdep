from pmock import *
import unittest
from lineCounter import LineCounter

class TestLineCounter(MockTestCase):
  def setUp(self):
    self.counter = LineCounter()
    self.file = self.mock()
    self.counter.fileOpener = self.mock()
    self.counter.fileOpener.expects(once()).open(eq("test.h")).will(return_value(self.file))

  def loadLines(self, lines):
    self.file.expects(once()).xreadlines().will(return_value(lines))

  def testCountEmptyFile(self):
    self.loadLines([])
    self.assertEqual(self.counter.countLines("test.h"), 0)

  def testOneLine(self):
    self.loadLines(["a line"])
    self.assertEqual(self.counter.countLines("test.h"), 1)

  def testTwoLines(self):
    self.loadLines(["a line", "another"])
    self.assertEqual(self.counter.countLines("test.h"), 2)

if __name__ == "__main__":
  unittest.main()
