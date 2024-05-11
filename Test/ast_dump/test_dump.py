import ast
import pprint

r=ast.parse(open("./a.py","r",encoding="utf8").read())
# for i in ast.dump(r).body:
def f(node, depth=0):
    fields = [(k, getattr(node, k, [])) for k in node._fields]
    node_info = f"{node.__class__.__name__}: {fields}"
    print("\t" * depth, ast.dump(node))

    for k, values in fields:
        if isinstance(values, list):
            for i in values:
                if isinstance(i, ast.AST):
                    f(i, depth + 1)
        # elif isinstance(values, ast.AST):
        #     f(values, depth + 1)
    # else:
    #     print("\t"*depth,ast.dump(node))
f(r)
ast.If
# pprint.pprint(ast.dump(r))
r=ast.unparse(r)
print(r)