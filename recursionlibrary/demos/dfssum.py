import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from recursionlibrary import appendChildren, getObject

from json import dumps

def dfssum(tree):
    def delta(node, lst, originalLst):
        return node['value']['ch']

    def assignCallback(node):
        return node['value']['val'] + getObject(node['parent'])['value']['val']

    def combineCallback(node):
        return node['value']['val']

    def resultConditionCallback(node):
        return True

    def resultNodeCallback(node):
        return node['value']

    print(dumps(appendChildren([tree], delta, assignCallback=assignCallback, combineCallback=combineCallback,
        resultConditionCallback=resultConditionCallback, resultNodeCallback=resultNodeCallback,
        expandOnEmptyDelta=True, rootValue={'val': 0}, assignResultStoreIn='val'), indent=2))

dfssum({
    'val': 1,
    'ch': [
        {'val': 2, 'ch': []},
        {'val': 3, 'ch': [
            {'val': 4, 'ch': [
                {'val': 2, 'ch': []}
            ]}
        ]}
    ]
})