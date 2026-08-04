import RecursionLibrary from '../recursion-library.js'

function fib(n) {
    return {
        delta: function (node) {
            return ['#node.value# - 1', '#node.value# - 2']
        },

        combine: function (node) {
            return '#node.children[0].value# + #node.children[1].value#'
        },

        until: function (node) {
            return { condition: '#node.value# <= 1', result: '#node.value#' }
        }
    }
}

const nativeModel = RecursionLibrary.createNativeModel(fib)
console.log('Native Model:', nativeModel)
console.log('\nGenerated Code:\n')
const generatedCode = RecursionLibrary.generateCode(nativeModel)
console.log(generatedCode)
console.log('\nCall the generated function to test:')
eval(`${generatedCode}; console.log("fib(35) =", fib(35)) `)