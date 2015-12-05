#!/bin/env python
import unittest
from depend import Depend
from pmock import *

class TestDepend(MockTestCase):
  def setUp(self):
    self.depend = Depend()
    self.builder = self.mock()
    self.depend.builder = self.builder

  def expects(self):
    return self.builder.expects(once())

  def expectEnd(self):
    self.expects().end()

  def expectNode(self, file, name):
    return self.expects().node(eq(file), eq(name))

  def expectLine(self):
    return self.expects().line()

  def feed(self, text):
    self.depend.feed([text])
    
  def testOneNode(self):
    self.expectNode("test.cpp", "test.cpp")
    self.expectEnd()
    self.feed('#line 1 "test.cpp"')

  def testTwoFeeds(self):
    self.expectNode("a.cpp", "a.cpp")
    self.expectEnd()
    self.expectNode("b.cpp", "b.cpp")
    self.expectEnd()
    self.feed('#line 1 "a.cpp"')
    self.feed('#line 1 "b.cpp"')

  def testWindowsFilenameWithPath(self):
    self.expectNode("C:\\doodaa\\day\\test.cpp", "test.cpp")
    self.expectEnd()
    self.feed('#line 2 "C:\\doodaa\\day\\test.cpp"')

  def testUnixFilenameWithPath(self):
    self.expectNode("/home.chris/src/test.cpp", "test.cpp")
    self.expectEnd()
    self.feed('#line 2 "/home.chris/src/test.cpp"')

  def testGnuCppNode(self):
    self.expectNode("test.cpp", "test.cpp")
    self.expectEnd()
    self.feed('# 1 "test.cpp"')

  def testGnuCppNodeType2(self):
    self.expectEnd()
    self.feed('# 1 "<built-in>"')

  def testGnuCppNodeType3(self):
    self.expectNode("testa.h", "testa.h")
    self.expectEnd()
    self.feed('# 1 "testa.h" 1')

  def testOneLine(self):
    self.expectLine()
    self.expectEnd()
    self.feed("struct a;")

  def testEmptyLine(self):
    self.expectLine()
    self.expectEnd()
    self.feed("")

  def testGetTree(self):
    self.expects().getTree()
    self.depend.getTree()


if __name__ == "__main__":
  unittest.main()
