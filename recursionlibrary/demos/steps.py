import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from recursionlibrary import appendChildren, getObject

from json import dumps

"""
Angenommen, ein Kind kann eine Treppe mit s Stufen erklimmen, indem es entweder 1, 2, ..., k
Stufen in einem einzigen Schritt nimmt. Berechnen Sie alle unterschiedlichen Schrittfolgen, mit
denen das Kind genau die s Stufen der Treppe erklimmt.
"""

#TODO: Parents müssen noch dereferenziert werden
def steps(s):
    def delta(node, lst, originalLst):
        return [i for i in range(1, s + 1)] if node['value'] <= s else []

    def assignCallback(node):
        return node['value'] + getObject(node['parent'])['value']
        
    print(dumps(appendChildren([i for i in range(1, s + 1)], delta, assignCallback=assignCallback, rootValue=0), indent=2))

steps(5)