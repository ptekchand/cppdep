import unittest
from dependReport import DependReport

class MockTree:
  def __init__(self, name, numLines, totalLines, child=[]):
    self.mockName = name
    self.mockLines = ["line %d" %i for i in xrange(0,numLines)]
    self.mockTotalLines = totalLines
    self.mockChild = child

  def name(self):
    return self.mockName

  def lines(self):
    return len(self.mockLines)

  def totalLines(self):
    return self.mockTotalLines

  def children(self):
    return self.mockChild


class TestDependReport(unittest.TestCase):
  def testReportOneNode(self):
    reporter = DependReport()
    tree = MockTree("test.cpp", 1, 3)
    report = reporter.report(tree)
    self.assertEqual(report, "test.cpp directly included lines(1), all included lines(3)\n")

  def testReportOneInclude(self):
    reporter = DependReport()
    tree1 = MockTree("test.cpp", 1, 3)
    tree = MockTree("test.cpp", 1, 3, [tree1])
    report = reporter.report(tree)
    self.assertEqual(report, 
    """test.cpp directly included lines(1), all included lines(3)
    test.cpp directly included lines(1), all included lines(3)\n""")

if __name__ == "__main__":
  unittest.main()
