from typing import *

from PySide2.QtCore import *

from Source import Globs


class LSCommand:
    def undo(self):
        raise NotImplementedError

    def __repr__(self):
        return f"{self.__class__.__name__}"

class LSAddItemCommand(LSCommand):
    def __init__(self, view, items):
        self.view = view
        self.items = items

    def undo(self):
        with Globs.DisableRecordCommandContext():
            self.view.remove_items(self.items,is_force=True)

    def __repr__(self):
        return f"add {self.items}"

class LSDestroyedCommand(LSCommand):
    def __init__(self,view ,items):
        self.view:AbsLSGraphicsView=view
        self.items=items
        self.uuid_2_item={item.uuid_:item for item in self.view.ls_items}
        self.items_pin_connect_info=[item.get_pin_connect_info() for item in items]

    def undo(self):
        """
        要记住所有的 连接关系,恢复之后要重新连接
        删除一个item  就代表要记住 所有 pin 连接的 node item
        首先是 out pin 的 connect info
        然后  in  pin 的 connect info

        :return:
        """

        with Globs.DisableRecordCommandContext():
            for item_connect_info in self.items_pin_connect_info:
                for connect_info in item_connect_info:
                    item=self.uuid_2_item[connect_info.node_uuid]
                    to_item=self.uuid_2_item[connect_info.to_node_uuid]
                    pin=item.find_pin_by_uuid(connect_info.pin_uuid)
                    to_pin=to_item.find_pin_by_uuid(connect_info.to_pin_uuid)
                    pin.connect_pin(to_pin)

            for item in self.items:
                self.view.add_item(item)
                item.show()

    def __repr__(self):
        return f"destroyed {self.items}"

class LSMoveCommand(LSCommand):
    def __init__(self, items,poses:List[QPoint]):
        self.items = items
        self.poses = poses

    def undo(self):
        for item, pos in zip(self.items, self.poses):
            item.proxy.setPos(pos)

    def __repr__(self):
        return f"move {self.items}"


class LSPinConnectCommand(LSCommand):
    def __init__(self, out_pin):
        self.out_pin = out_pin

    def undo(self):
        with Globs.DisableRecordCommandContext():
            self.out_pin.disconnect_pin(self.out_pin.to_[-1])

    def __repr__(self):
        return f"connect {self.out_pin} {self.out_pin.to_[-1]}"


class LSPinDisconnectCommand(LSCommand):
    def __init__(self,out_pin,in_pin):
        self.in_pin = in_pin
        self.out_pin = out_pin

    def undo(self):
        with Globs.DisableRecordCommandContext():
            self.out_pin.connect_pin(self.in_pin)

    def __repr__(self):
        return f"disconnect {self.out_pin} {self.in_pin}"

class LSDuplicateCommand(LSAddItemCommand):

    def __repr__(self):
        return f"duplicate {self.items}"


class LSAddPropertyCommand(LSCommand):
    def __init__(self, item,property_tree):
        self.item = item
        self.property_tree:AbsLSPropertyTreeWidget = property_tree

    def undo(self):
        with Globs.DisableRecordCommandContext():
            self.property_tree.remove_variable(self.item)

    def __repr__(self):
        return f"add property {self.item}"



