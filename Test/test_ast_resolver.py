import ast
import dataclasses
import pprint

#
filename = r"C:\repo\_USDQ\LowSide\Test\resolve_dirs\a.py"


f=ast.parse(open(r"C:\repo\_USDQ\LowSide\Test\ast_dump\a.py",encoding="utf8").read())
d=ast.dump(f)
print(d)
unparse=ast.unparse(f)
# print(unparse)
# Module(body=[Expr(value=Constant(value='开始运行')), Expr(value=Call(func=Name(id='print', ctx=Load()), args=[], keywords=[keyword(arg='a', value=Name(id='NewVar', ctx=Load())), keyword(arg='c', value=Name(id='NewVar', ctx=Load()))]))], type_ignores=[])
# Module(body=[Expr(value=Constant(value='开始运行')), Expr(value=Call(func=Name(id='print_', ctx=Load()), args=[Name(id='NewVar'), Name(id='NewVar')]))])