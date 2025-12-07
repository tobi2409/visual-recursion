module fak(n)
    delta(node)
        return node["value"] - 1
    end

    bound(node)
        if node["value"] < 2
            return 1
        end
    end

    combine(node)
        return node["value"] * node["childs"][0]["value"]
    end
end