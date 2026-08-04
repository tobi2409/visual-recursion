import RecursionLibrary from '../recursion-library.js'

function fak(n) {
    return {
        delta: function (node) {
            return ['#node.value# - 1']
        },

        combine: function (node) {
            return '#node.value# * #node.children[0].value#'
        },

        until: function (node) {
            return { condition: '#node.value# === 1', result: '1' }
        }
    }
}

/* -> zu generierender Code:
function fak(n) {
    if (n === 1) {
        return 1
    }

    const deltaed = [fak(n - 1)] // resultiert aus delta: function (node) { return ['#node.value# - 1'] }

    // die Resultate von deltaed sind die Kinder des aktuellen Knotens, daher deltaed[0] für das erste Kind
    const combined = n * deltaed[0] // resultiert aus combine: function (node) { return '#node.value# * #node.children#[0].value' }

    return combined
}
*/

const nativeModel = RecursionLibrary.createNativeModel(fak)
console.log('Native Model:', nativeModel)
console.log('\nGenerated Code:\n')
const generatedCode = RecursionLibrary.generateCode(nativeModel)
console.log(generatedCode)
console.log('\nCall the generated function to test:')
eval(`${generatedCode}; console.log("fak(5) =", fak(5)) `)