#!/bin/env python
import re
from include import DependencyBuilder
from stats import Metrics

class Depend:
  def __init__(self):
    self.__pattern = re.compile('^( |\t)*#(line)? [0-9]+ "(?P<file>.*)"')
    self.__WindowsFilePattern = re.compile('.*\\\\(?P<name>.*)')
    self.__UnixFilePattern = re.compile('.*/(?P<name>.*)')
    self.metrics = Metrics()
    self.builder = DependencyBuilder(self.metrics)

  def __getName(self, file):
    match = self.__WindowsFilePattern.match(file)
    if match is None:
      match = self.__UnixFilePattern.match(file)
    if match is None:
      return file
    else:
      return match.group("name")

  def notBogus(self, file):
    """In g++ the first couple of lines in the pre-processed output
       look like this:
       # 1 "<built-in>"

       These lines should be ignored; they don't refer to real include files."""
    return file[0] != '<' and file[-1] != '>'

  def feed(self, lines):
    for line in lines:
      match = self.__pattern.match(line)
      if match is not None:
        file = match.group('file')
        name = self.__getName(file)
        if self.notBogus(file):
          self.builder.node(file, name)
      else:
        self.builder.line()
    self.builder.end()

  def getTree(self):
    return self.builder.getTree()

  def getTrees(self):
    return self.builder.getTrees()

  def getStats(self):
    return self.metrics
