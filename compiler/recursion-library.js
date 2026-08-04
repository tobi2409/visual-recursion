// Simple marker-based transformation
function transformNodeValueToParam(expr, paramName) {
    return expr.replace(/#node\.value#/g, paramName);
}

function transformNodeChildrenToDeltaed(expr) {
    // Replace #node.children[i].value# -> deltaed[i]
    return expr.replace(/#node\.children(\[\d+\])\.value#/g, 'deltaed$1');
}

function wrapWithFunctionCall(expr, fnName) {
    return `${fnName}(${expr})`;
}

const RecursionLibrary = (function() {
    function createNativeModel(fn) {
        const fnName = fn.name
        
        // Extract parameter name from function
        const fnString = fn.toString()
        const paramMatch = fnString.match(/function\s*\w*\s*\(([^)]*)\)/)
        const paramName = paramMatch && paramMatch[1].trim() ? paramMatch[1].trim() : 'n'

        const recursionInput = fn()

        const deltaDescription = recursionInput.delta()
        // Transform each delta expression: #node.value# -> paramName, then wrap with function call
        const nativeDelta = deltaDescription.map((d) => {
            const transformed = transformNodeValueToParam(d, paramName)
            return wrapWithFunctionCall(transformed, fnName)
        })
        
        const combineDescription = recursionInput.combine()
        // Transform combine: #node.value# -> paramName, #node.children# -> deltaed
        let nativeCombine = transformNodeChildrenToDeltaed(combineDescription)
        nativeCombine = transformNodeValueToParam(nativeCombine, paramName)

        const untilDescription = recursionInput.until()
        // Transform until: #node.value# -> paramName in both condition and result
        const nativeUntilCondition = transformNodeValueToParam(untilDescription.condition, paramName)
        const nativeUntilResult = transformNodeValueToParam(untilDescription.result, paramName)
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
        code += `    const deltaed = [${nativeDelta.join(', ')}]\n\n`
        
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