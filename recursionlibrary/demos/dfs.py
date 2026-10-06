import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from recursionlibrary import appendChildren, getObject

from json import dumps

def dfs(tree):
    def delta(node, lst, originalLst):
        return node['value']['ch']

    def combineCallback(node):
        return node['value']['val']

    def resultNodeCallback(node):
        return None

    print(dumps(appendChildren([tree], delta, combineCallback=combineCallback, resultNodeCallback=resultNodeCallback, expandOnEmptyDelta=True, rootValue={'val': 0}), indent=2))

dfs({
    'val': 1,
    'ch': [
        {'val': 2, 'ch': []},
        {'val': 3, 'ch': [
            {'val': 4, 'ch': []}
        ]}
    ]
})