import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from recursionlibrary import appendChildren, getObject

from json import dumps

def flatten(lst):
    def delta(node, lst, originalLst):
        # klar kann man das auch in einem Einzeiler schreiben, aber es soll veranschaulicht werden, dass auch ein normales int als delta ausgegeben werden kann
        # -> in dem Fall findet einfach keine weitere Rekursion mehr statt und das int wird zum Blatt
        if type(node['value']) == list:
            return node['value']
        elif type(node['value']) == int:
            return node['value']

    def resultNodeCallback(node):
        return node['value']

    print(dumps(appendChildren(lst, delta, resultNodeCallback=resultNodeCallback), indent=2))

flatten([2, 5, 1, 7, [3, 8, [9, [4, 1], 0], 2], 6, 4])