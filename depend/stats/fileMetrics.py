from lineCounter import LineCounter

class FileMetrics:
  def __init__(self):
    self.nodes = []
    self.lineCounter = LineCounter()
    self.__fileLineCountCache = None

  def addNode(self, node):
    self.nodes.append(node)

  def compiledLines(self):
    return sum(node.totalLines() for node in self.nodes)

  def file(self):
    return self.nodes[0].file()

  def name(self):
    return self.nodes[0].name()

  def fileLines(self):
    if len(self.nodes) != 0:
      if self.__fileLineCountCache is None:
        self.__fileLineCountCache = self.lineCounter.countLines(self.nodes[0].file())
      return self.__fileLineCountCache
    else:
      return 0

  def includedFrom(self):
    return len([node for node in self.nodes if node.parent() is not None])

class FileMetricsFactory:
  def create(self):
    return FileMetrics()

