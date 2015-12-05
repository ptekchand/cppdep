from treeFactory import TreeFactory

class DependencyBuilder:
  def __init__(self, metrics=None):
    self.root = None
    self.current = None
    self.factory = TreeFactory()
    self.metrics = metrics
    self.roots = []

  def setCurrent(self, current):
    self.current = current
    if self.current is not None:
      self.line = self.addLine
    else:
      self.line = self.ignoreLine

  def createNode(self, file, name, parent=None):
    self.setCurrent(self.factory.create(file, name, self.current))
    if self.metrics is not None:
      self.metrics.addFile(self.current)
    
  def createRoot(self, file, name):
    self.createNode(file, name)
    self.root = self.current

  def end(self):
    if self.root is not None:
      self.roots.append(self.root)
    self.root = None
    self.setCurrent(None)

  def node(self, file, name):
    if self.root is None:
      self.createRoot(file, name)
    else:
      if self.current.isMyParent(file):
        self.setCurrent(self.current.parent())
      elif file != self.current.file():
        self.createNode(file, name)


  def addLine(self):
      self.current.addLine()

  def ignoreLine(self, line): pass
  def line(self): pass

  def getTrees(self):
    return self.roots

  def getTree(self):
    self.end()
    if len(self.roots) != 0:
      return self.roots[0]
    else:
      return None

