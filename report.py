from depend import Depend
from depend import DependReport


if __name__ == "__main__":
  import sys
  files = sys.argv[1:]
  depend = Depend()
  for file in files:
    lines = open(file).readlines()
    depend.feed(lines)
  reporter = DependReport()
  print reporter.reportStats(depend.getStats())
