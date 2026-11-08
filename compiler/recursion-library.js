// Simple marker-based transformation (new markers: #node# and #node.children[n]#)
function transformNodeToParam(expr, paramName) {
    // Replace '#node#' (the node's value) with the function parameter
    return expr.replace(/#node#/g, paramName);
}

function transformNodeChildrenToDeltaed(expr) {
    // Replace generic '#node.children#' -> 'deltaed'
    return expr.replace(/#node\.children#/g, 'deltaed');
}

function wrapWithFunctionCall(expr, fnName) {
    return `${fnName}(${expr})`;
}

//TODO: USE PARSER!
const RecursionLibrary = (function() {
    function createNativeModel(fn) {
        const fnName = fn.name
        
        // Extract parameter name from function
        const fnString = fn.toString()
        const paramMatch = fnString.match(/function\s*\w*\s*\(([^)]*)\)/)
        const paramName = paramMatch && paramMatch[1].trim() ? paramMatch[1].trim() : 'n'

        const recursionInput = fn()

        const deltaDescription = recursionInput.delta()
        // Arrays describe fixed recursive arguments; a string describes a dynamic collection.
        const nativeDelta = Array.isArray(deltaDescription)
            ? deltaDescription.map((delta) => {
                const transformed = transformNodeToParam(delta, paramName)
                return wrapWithFunctionCall(transformed, fnName)
            })
            : transformNodeToParam(deltaDescription, paramName)
        
        const combineDescription = recursionInput.combine()
        // Transform combine: indexed children first, then generic children, then node param
        let nativeCombine = transformNodeChildrenToDeltaed(combineDescription)
        nativeCombine = transformNodeToParam(nativeCombine, paramName)

        const untilDescription = recursionInput.until()
        // Transform until: #node.value# -> paramName in both condition and result
        const nativeUntilCondition = transformNodeToParam(untilDescription.condition, paramName)
        const nativeUntilResult = transformNodeToParam(untilDescription.result, paramName)
        const nativeUntil = {
            condition: nativeUntilCondition,
            result: nativeUntilResult
        }
        
        return {
            fnName,
            paramName,
            nativeDelta,
            nativeCombine,
            nativeUntil
        }
    }

    function generateCode(nativeModel) {
        const { fnName, paramName, nativeDelta, nativeCombine, nativeUntil } = nativeModel
        
        let code = `function ${fnName}(${paramName}) {\n`
        
        // Add until condition (base case)
        code += `    if (${nativeUntil.condition}) {\n`
        code += `        return ${nativeUntil.result}\n`
        code += `    }\n\n`
        
        // Add delta (recursive calls)
        if (Array.isArray(nativeDelta)) {
            code += `    const deltaed = [${nativeDelta.join(', ')}]\n\n`
        } else {
            code += `    const deltaed = ${nativeDelta}.map((${paramName}) => ${fnName}(${paramName}))\n\n`
        }
        
        // Add combine
        code += `    const combined = ${nativeCombine}\n\n`
        
        // Return combined result
        code += `    return combined\n`
        code += `}`

        return code
    }

    return {
        createNativeModel,
        generateCode
    }
})()

export default RecursionLibrary