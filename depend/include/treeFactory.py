from tree import Tree

class TreeFactory:
  def create(self, file, name, parent=None):
    newTree = Tree(file, name, parent)
    if parent is not None:
      parent.addChild(newTree)
    return newTree
