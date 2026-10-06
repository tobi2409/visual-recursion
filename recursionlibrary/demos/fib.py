import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from recursionlibrary import appendChildren, getObject

from json import dumps

def fib(n):
    def delta(node, lst, originalLst):
        return [node['value'] - 1, node['value'] - 2] if node['value'] - 1 >= 0 else []

    def combineCallback(node):
        return node['children'][0]['value'] + node['children'][1]['value'] if len(node['children']) == 2 else 1

    def resultConditionCallback(node):
        return node['layer'] == 1

    def resultNodeCallback(node):
        return node['value']

    return appendChildren([n], delta, combineCallback=combineCallback, resultConditionCallback=resultConditionCallback, resultNodeCallback=resultNodeCallback)

import datetime
t = datetime.datetime.now()

print(fib(7)[1])

t = datetime.datetime.now() - t
print(t)