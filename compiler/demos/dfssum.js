// work in progress, not yet fully functional

import RecursionLibrary from '../recursion-library.js';

function dfssum(tree) {
    return {
        delta: function (node) {
            return '#node#.children'
        },
        
        combine: function (node) {
            return '#node#.value + #node.children#.reduce((sum, child) => sum + child, 0)'
        },

        until: function (node) {
            return { condition: '#node#.children.length === 0', result: '#node#.value' }
        }
    }
}

const nativeModel = RecursionLibrary.createNativeModel(dfssum)
console.log('Native Model:', nativeModel)
console.log('\nGenerated Code:\n')
const generatedCode = RecursionLibrary.generateCode(nativeModel)
console.log(generatedCode)
console.log('\nCall the generated function to test:')
const tree = {
    value: 1,
    children: [
        { value: 2, children: [] },
        {
            value: 3,
            children: [
                { value: 4, children: [] },
                { value: 5, children: [] }
            ]
        },
        { value: 6, children: [] }
    ]
}
eval(`${generatedCode}; console.log("dfssum(tree) =", dfssum(tree))`)