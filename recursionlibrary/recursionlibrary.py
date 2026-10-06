'''
Ziel ist es, einen WYSIWYG-Editor zu entwickeln
darin kann eine Rekursion in Form einer Baumstruktur modelliert werden
damit die Visualisierung gut verständlich ist, wird dort mit Beispiel-Nodes gearbeitet
diese Beispiel-Nodes haben aber keine Auswirkung auf den Algorithmus, sondern dienen lediglich der Visualisierung
wichtig ist, dass die deltas angegeben werden,
wobei man im Laufe der Entwicklung auch eine Mustererkennung entwickeln kann für die Übertragung von Beispiel-Nodes auf delta

Die Schwäche von appendChildren ist die Performance.

Dies soll in zwei Wegen gelöst werden.
1.) mehrere Abstraktionsschichten von appendChildren (angefangen von einem ganz minimalen Template bis zu diesem komplexen Template)
    inkl. Parametrisierungen, welche node-Attribute mitgeliefert werden sollen, ob im Node children erstellt werden sollen etc.
2.) (besonders für mathematische Funktionen wie fib, fak), bei denen die Liste sowie die Erstellung der delta-Liste nur eine visuelle Funktion hat,
    soll ein Compiler die Listenstruktur in eine "native" Struktur umwandeln
'''

def appendChildren(lst, delta, assignCallback = (lambda node: node['value']), combineCallback = (lambda node: node['value']),
        resultConditionCallback = (lambda node: node['children'] == []), resultNodeCallback = (lambda node: node), expandOnEmptyDelta = False,
        rootValue = None, assignResultStoreIn = '', combineResultStoreIn = ''):
        
    def factorNode(value, currentListIndex, lstSize, layer, children, parent):
        return {'value': value, 'currentListIndex': currentListIndex, 'listSize': lstSize, 'layer': layer, 'children': children, 'parent': parent}

    def setValue(node, storeIn, value):
        if storeIn == '':
            node['value'] = value
        else:
            if type(node['value']) != dict:
                node['value'] = {}

            node['value'][storeIn] = value

    def _appendChildren(_lst, delta, layer=1, parent=None, originalLst=lst):
        treeResult = []
        result = []

        if type(_lst) != list:
            return [], []

        _lstSize = len(_lst)

        for i, e in enumerate(_lst):
            node = factorNode(e, i, _lstSize, layer, [], parent)

            # das Value kann sich nochmal entscheidend verändern bzgl. delta und Child-Erzeugung
            setValue(node, assignResultStoreIn, assignCallback(node)) # Assign-Informationen beim Top-Down

            deltaed = delta(node, _lst, originalLst)

            if deltaed != [] or expandOnEmptyDelta: # Node aufnehmen, wenn Kinder existieren ODER wir auch Blätter erzwingen wollen
                childNodes, nextResult = _appendChildren(deltaed, delta, layer=layer + 1, parent=id(node), originalLst=lst)
                node['children'].extend(childNodes)

                setValue(node, combineResultStoreIn, combineCallback(node)) # für Bottom-Up-Rekursion

                treeResult.append(node)

                if resultConditionCallback(node):
                    resultNode = resultNodeCallback(node)
                    if resultNode != None:
                        result.append(resultNodeCallback(node))

                result.extend(nextResult)

        return treeResult, result

    root = factorNode(rootValue, -1, -1, 0, [], -1)
    children, result = _appendChildren(lst, delta, parent=id(root))
    root['children'].extend(children)
    return root, result

def getObject(id):
    if id == -1:
        return None

    import ctypes
    return ctypes.cast(id, ctypes.py_object).value