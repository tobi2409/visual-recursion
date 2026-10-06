import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from recursionlibrary import appendChildren, getObject

from json import dumps

def sum(n):
    def delta(node, lst, originalLst):
        return [node['value'] - 1] if node['value'] >= 1 else []

    def combineCallback(node):
        return node['value'] + node['children'][0]['value'] if len(node['children']) != 0 else node['value']

    def resultConditionCallback(node):
        return node['layer'] == 1

    def resultNodeCallback(node):
        return node['value']

    print(dumps(appendChildren([n], delta, combineCallback=combineCallback, resultConditionCallback=resultConditionCallback, resultNodeCallback=resultNodeCallback), indent=2))

sum(5)