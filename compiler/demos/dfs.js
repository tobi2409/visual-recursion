// work in progress, not yet fully functional

import RecursionLibrary from '../recursion-library.js';

function dfs(tree) {
    return {
        delta: function (node) {
            return ['#node.children[0]#']
        },
        
        combine: function (node) {
            return '#node.children[0].value#'
        },

        until: function (node) {
            return { condition: '#node.children.length === 0#', result: '#node.value#' }
        }
    }
}

const nativeModel = RecursionLibrary.createNativeModel(dfs)
console.log('Native Model:', nativeModel)
console.log('\nGenerated Code:\n')
const generatedCode = RecursionLibrary.generateCode(nativeModel)
console.log(generatedCode)
console.log('\nCall the generated function to test:')
eval(`${generatedCode}; console.log("dfs({ value: 1, children: [{ value: 2, children: [] }] }) =", dfs({ value: 1, children: [{ value: 2, children: [] }] })) `)