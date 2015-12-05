class Tree:
  def __init__(self, file, name, parent):
    self.__name = name
    self.__file = file
    self.__parent = parent
    self.__lines = 0
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

  def addLine(self):
    self.__lines += 1

  def addChild(self, subTree):
    self.__children.append(subTree)

  def lines(self):
    return self.__lines

  def children(self):
    return self.__children

  def totalLines(self):
    total = self.__lines
    for subTree in self.__children:
      total += subTree.totalLines()
    return total
