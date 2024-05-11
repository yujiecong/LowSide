import ast

from Source.Custom.Enums.LSPinEnum import PinType, PinFlow

from Source.Common.Logger import ls_print
from Source.Custom.LSAstData import LSAstCodeFragmentName
from Source.Widgets.NodeItem.Event.LSEventNodeItem_ProgramStart import LSEventNodeItem_ProgramStart
from Source.Widgets.Pin.LSExecPin import LSExecPin

keys = {"body", "orelse"}


class LSGraphicsViewParser:

    def __init__(self):
        pass

    def parse(self, start_item: LSEventNodeItem_ProgramStart, start_ast: ast.Module):
        self.recursive_parse(start_item, start_ast.body, start_ast.body)
        # ls_print(ast.dump(start_ast))
        # ls_print(ast.unparse(start_ast))
        return start_ast

    def recursive_parse(self, item, cur_body, last_body):
        item_ast = item.to_ast()
        cur_body.append(item_ast)
        for pin in item.pins:
            pin: LSExecPin
            if pin.flow == PinFlow.Out and pin.get_type() == PinType.Exec:
                for to_pin in pin.to_:
                    to_node = to_pin.node
                    "不同的pin会对应不同的scope"
                    if pin.code_fragment == LSAstCodeFragmentName.last:
                        item_body = last_body
                    else:
                        item_body = getattr(item_ast, pin.code_fragment, cur_body)
                    self.recursive_parse(to_node, item_body, cur_body)
