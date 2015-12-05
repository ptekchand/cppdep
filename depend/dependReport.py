from depend import Depend

class DependReport:
  def report(self, tree, indentlevel=0):
    text = "%s%s directly included lines(%d), all included lines(%d)\n" % ("    "*indentlevel, tree.name(), tree.lines(), tree.totalLines())
    for child in tree.children():
      text += self.report(child, indentlevel+1)
    return text

  def reportStats(self, stats):
    report = ""
    files = stats.files()
    files.sort(key=lambda k:k.compiledLines())
    for file in files:
      report += "%s lines in file(%d), all included lines(%d), places included from(%d)\n" % (file.file(), file.fileLines(), file.compiledLines(),
                file.includedFrom())
    return report


if __name__ == "__main__":
  import sys
  file = sys.argv[1]
  lines = open(file).readlines()
  depend = Depend()
  tree = depend.getTree(lines)
  reporter = DependReport()
  print reporter.report(tree)
