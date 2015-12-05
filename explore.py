#!/bin/env python
import os
from gui import Tree
from Tkinter import *

def formatNodeText(node):
        return "%s,    lines(%d),    total_lines(%d),    nested_included(%d)" % (node.name(), 
		node.lines(), node.totalLines(), len(node.children()))

class get:
  def __init__(self, dependTree):
    self.dependTree = dependTree

  def findChild(self, children, id):
    for child in children:
      if id == child.file():
        return child
    return None
  
  def getCurrent(self, node):
    currentNode = self.dependTree
    for id in node.full_id()[1:]:
      if currentNode is not None:
        currentNode = self.findChild(currentNode.children(), id)
    return currentNode

  def __call__(self, node):
    currentNode = self.getCurrent(node)
    if currentNode is None: return
    children = currentNode.children()
    children.sort(key=lambda k:k.totalLines())
    for child in currentNode.children():
        flag = 0
        if len(child.children()) == 0:
          flag = 0
        else:
          flag = 1
        t.add_node(name=formatNodeText(child), id=child.file(), flag=flag)

root=Tk()
root.title(os.path.basename(sys.argv[0]))

import sys
from depend import Depend
file = sys.argv[1]
lines = open(file).xreadlines()
depend = Depend()
depend.feed(lines)
dependTree = depend.getTree()
if dependTree is None:
  print "Error reading dependancy information from %s" % file
  sys.exit(0)

# create the control
t=Tree.Tree(master=root,
            root_id=dependTree.file(),
            root_label=formatNodeText(dependTree),
            get_contents_callback=get(dependTree), 
            width=300)
t.grid(row=0, column=0, sticky='nsew')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

sb=Scrollbar(root)
sb.grid(row=0, column=1, sticky='ns')
t.configure(yscrollcommand=sb.set)
sb.configure(command=t.yview)

sb=Scrollbar(root, orient=HORIZONTAL)
sb.grid(row=1, column=0, sticky='ew')
t.configure(xscrollcommand=sb.set)
sb.configure(command=t.xview)

t.focus_set()
t.root.expand()

root.mainloop()
