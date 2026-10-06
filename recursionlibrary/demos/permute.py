import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from recursionlibrary import appendChildren, getObject

from json import dumps

def permute():
    def delta(node, lst, originalLst):
        return [e for e in lst if e != node['value']]

    def resultNodeCallback(node):
        return None

    print(dumps(appendChildren([8,6,3,7], delta, resultNodeCallback=resultNodeCallback, expandOnEmptyDelta=True), indent=2))

permute()