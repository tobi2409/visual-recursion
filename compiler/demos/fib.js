import RecursionLibrary from '../recursion-library.js'

function fib(n) {
    return {
        delta: function (node) {
            return ['#node# - 1', '#node# - 2']
        },

        combine: function (node) {
            return '#node.children#[0] + #node.children#[1]'
        },

        until: function (node) {
            return { condition: '#node# <= 1', result: '#node#' }
        }
    }
}

const nativeModel = RecursionLibrary.createNativeModel(fib)
console.log('Native Model:', nativeModel)
console.log('\nGenerated Code:\n')
const generatedCode = RecursionLibrary.generateCode(nativeModel)
console.log(generatedCode)
console.log('\nCall the generated function to test:')
eval(`${generatedCode }; console.log("fib(35) =", fib(35)) `)