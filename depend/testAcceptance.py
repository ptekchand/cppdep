#!/bin/env python
import unittest
from depend import Depend

precompWithLinesTemplate="""#line 1 "%s"

int main(int argc, char** argv)
{
  return 0;
}

"""

precompWithLines=precompWithLinesTemplate % "test.cpp"

precompOneInclude="""#line 1 "test.cpp"
#line 1 "test.h"
struct t;
#line 2 "test.cpp"
int main(int argc, char** argv)
{
  return 0;
}

"""

precompNestedInclude="""#line 1 "test.cpp"
#line 1 "test2.h"
#line 1 "test.h"
struct t;
#line 2 "test2.h"
struct h;
#line 2 "test.cpp"
int main(int argc, char** argv)
{
  return 0;
}

"""

precompTwoIncludes="""#line 1 "test.cpp"
#line 1 "testa.h"
struct a;
#line 2 "test.cpp"
#line 1 "testb.h"
struct b;
#line 3 "test.cpp"
int main(int argc, char** argv)
{
  return 0;
}

"""

precompGnuCpp="""# 1 "test.cpp"
# 1 "<built-in>"
# 1 "<command line>"
# 1 "test.cpp"
# 1 "testa.h" 1
struct a;
# 2 "test.cpp" 2
# 1 "testb.h" 1
struct b;
# 3 "test.cpp" 2
int main(int argc, char** argv)
{
  return 0;
}
"""

precompNestedIncludeSameName="""#line 1 "test.cpp"
#line 1 "C:\\libs\\test.h"
#line 1 "C:\\sys\\libs\\test.h"
struct t;
#line 2 "C:\\libs\\test.h"
struct h;
#line 2 "test.cpp"
int main(int argc, char** argv)
{
  return 0;
}

"""

class TestAcceptance(unittest.TestCase):
  def setUp(self):
    self.depend = Depend()

  def feed(self, precomp):
    lines = precomp.splitlines()
    self.depend.feed(lines)
  
  def getStats(self, precomp):
    self.feed(precomp)
    return self.depend.getStats()

  def getTree(self, precomp):
    self.feed(precomp)
    return self.depend.getTree()

  def testNoNothing(self):
    tree = self.getTree("")
    assert(tree is None)

  def testNoNothingStats(self):
    stats = self.getStats("")
    self.assertEqual(len(stats.files()), 0)

  def testNoLineInfo(self):
    tree = self.getTree("/*nothing to see here*/")
    assert(tree is None)

  def testFirstNode(self):
    precomp='''#line 1 "test.cpp"'''
    tree = self.getTree(precomp)
    self.assertEqual(tree.name(), "test.cpp")

  def testWonkyLine(self):
    precomp='''   #line 1 "test.cpp"'''
    tree = self.getTree(precomp)
    self.assertEqual(tree.name(), "test.cpp")

  def testFirstNodeWithAnnoyingName(self):
    precomp='''#line 1 "C:\\blahblah\\overhere\\overthere\\test.cpp"'''
    tree = self.getTree(precomp)
    self.assertEqual(tree.name(), "test.cpp")

  def testFirstNodeWithLines(self):
    tree = self.getTree(precompWithLines)
    self.assertEqual(tree.name(), "test.cpp")
    self.assertEqual(tree.lines(), 6)

  def testTwoRootLevelFiles(self):
    self.feed(precompWithLinesTemplate % "a.cpp")
    self.feed(precompWithLinesTemplate % "b.cpp")
    trees = self.depend.getTrees()
    self.assertEqual(len(trees), 2)
    self.assertEqual(trees[0].name(), "a.cpp")
    self.assertEqual(trees[0].lines(), 6)
    self.assertEqual(trees[0].totalLines(), 6)
    self.assertEqual(trees[1].name(), "b.cpp")
    self.assertEqual(trees[1].lines(), 6)
    self.assertEqual(trees[1].totalLines(), 6)

  def testOneInclude(self):
    tree = self.getTree(precompOneInclude)
    self.assertEqual(tree.name(), "test.cpp")
    self.assertEqual(tree.lines(), 5)
    self.assertEqual(len(tree.children()), 1)
    self.assertEqual(tree.children()[0].name(), "test.h")
    self.assertEqual(tree.children()[0].lines(), 1)
    self.assertEqual(len(tree.children()[0].children()), 0)

  def testNestedInclude(self):
    tree = self.getTree(precompNestedInclude)
    self.assertEqual(tree.name(), "test.cpp")
    self.assertEqual(tree.lines(), 5)
    self.assertEqual(len(tree.children()), 1)
    self.assertEqual(tree.children()[0].name(), "test2.h")
    self.assertEqual(tree.children()[0].lines(), 1)
    self.assertEqual(len(tree.children()[0].children()), 1)
    self.assertEqual(tree.children()[0].children()[0].name(), "test.h")
    

  def testNestedIncludeSameNames(self):
    tree = self.getTree(precompNestedIncludeSameName)
    self.assertEqual(tree.name(), "test.cpp")
    self.assertEqual(tree.lines(), 5)
    self.assertEqual(len(tree.children()), 1)
    self.assertEqual(tree.children()[0].name(), "test.h")
    self.assertEqual(tree.children()[0].lines(), 1)
    self.assertEqual(len(tree.children()[0].children()), 1)
    self.assertEqual(tree.children()[0].children()[0].name(), "test.h")

  def testTwoIncludes(self):
    tree = self.getTree(precompTwoIncludes)
    self.assertEqual(tree.name(), "test.cpp")
    self.assertEqual(tree.lines(), 5)
    self.assertEqual(len(tree.children()), 2)
    self.assertEqual(tree.children()[0].name(), "testa.h")
    self.assertEqual(tree.children()[1].name(), "testb.h")

  def testTotalLines(self):
    tree = self.getTree(precompWithLines)
    self.assertEqual(tree.totalLines(), 6)

  def testTotalLinesWithNestedChildren(self):
    tree = self.getTree(precompNestedInclude)
    self.assertEqual(tree.totalLines(), 7)

  def testTotalLinesWithChildren(self):
    tree = self.getTree(precompTwoIncludes)
    self.assertEqual(tree.totalLines(), 7)

  def testTwoGnuCppIncludes(self):
    tree = self.getTree(precompGnuCpp)
    self.assertEqual(tree.name(), "test.cpp")
    self.assertEqual(tree.lines(), 4)
    self.assertEqual(len(tree.children()), 2)
    self.assertEqual(tree.children()[0].name(), "testa.h")
    self.assertEqual(tree.children()[1].name(), "testb.h")

if __name__ == "__main__":
  unittest.main()
