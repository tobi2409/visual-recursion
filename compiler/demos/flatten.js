// work in progress, not yet fully functional

import RecursionLibrary from '../recursion-library.js';

function flatten(list) {
    return {
        delta: function (node) {
            return '#node#'
        },
        
        combine: function (node) {
            return '#node.children#.flat()'
        },

        until: function (node) {
            return { condition: '!Array.isArray(#node#)', result: '#node#' }
        }
    }
}

const nativeModel = RecursionLibrary.createNativeModel(flatten)
console.log('Native Model:', nativeModel)
console.log('\nGenerated Code:\n')
const generatedCode = RecursionLibrary.generateCode(nativeModel)
console.log(generatedCode)
console.log('\nCall the generated function to test:')
eval(`${generatedCode}; console.log("flatten([1, 3, [4, 5, [6]], 8, [9]]) =", flatten([1, 3, [4, 5, [6]], 8, [9]])) `)