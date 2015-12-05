#!/bin/env python

class Tree:
  def __init__(self, file, name, parent):
    self.__name = name
    self.__file = file
    self.__parent = parent
    self.__lines = []
    self.__children = []

  def isMyParent(self, file):
    if self.parent() is None:
      return False
    else:
      return file == self.parent().file()

  def parent(self):
    return self.__parent

  def name(self):
    return self.__name

  def file(self):
    return self.__file

  def addLine(self, line):
    self.__lines.append(line)

  def addChild(self, subTree):
    self.__children.append(subTree)

  def lines(self):
    return self.__lines

  def children(self):
    return self.__children

  def totalLines(self):
    total = len(self.__lines)
    for subTree in self.__children:
      total += subTree.totalLines()
    return total

class TreeFactory:
  def create(self, file, name, parent=None):
    newTree = Tree(file, name, parent)
    if parent is not None:
      parent.addChild(newTree)
    return newTree

class TreeBuilder:
  def __init__(self):
    self.root = None
    self.current = None
    self.factory = TreeFactory()

  def createRoot(self, file, name):
    self.current = self.factory.create(file, name)
    self.root = self.current

  def addChild(self, file, name):
    self.current = self.factory.create(file, name, self.current)

  def node(self, file, name):
    if self.root is None:
      self.createRoot(file, name)
    else:
      if self.current.isMyParent(file):
        self.current = self.current.parent()
      elif file != self.current.file():
        self.addChild(file, name)

  def line(self, line):
    if self.current is not None:
      self.current.addLine(line)

  def getTree(self):
    return self.root

