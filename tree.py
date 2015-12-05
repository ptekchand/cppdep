from depend import Depend
from depend import DependReport


if __name__ == "__main__":
  import sys
  file = sys.argv[1]
  lines = open(file).readlines()
  depend = Depend()
  depend.feed(lines)
  reporter = DependReport()
  print reporter.report(depend.getTree())
