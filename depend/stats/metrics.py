from fileMetrics import FileMetricsFactory

class Metrics:
  def __init__(self):
    self.factory = FileMetricsFactory()
    self.map = {}

  def addFile(self, node):
    fileMetrics = self.map.get(node.file(), None)
    if fileMetrics is None:
      fileMetrics = self.factory.create()
      self.map[node.file()] = fileMetrics
    fileMetrics.addNode(node)
    
  def file(self, name):
    return self.map[name]

  def files(self):
    return self.map.values()
