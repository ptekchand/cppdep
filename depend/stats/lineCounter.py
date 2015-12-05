
class FileOpener:
  def open(self, filename):
    return open(filename)

class LineCounter:
  def __init__(self):
    self.fileOpener = FileOpener()

  def countLines(self, file):
    file = self.fileOpener.open(file)
    count = 0
    for line in file.xreadlines():
      count += 1
    return count
