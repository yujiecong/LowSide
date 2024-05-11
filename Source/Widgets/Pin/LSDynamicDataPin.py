import typing
from typing import List

from Source.Common import Func
from Source.Custom.Enums.LSPinEnum import PinFlow

from Source.Common.DataClass import LSSubPinInfo
from Source.Common.Obj import LSDictWrapper

from Source.Custom.LSObject import LSObject

from Source.Common.Func import OS
from Source.Widgets.Pin.LSDataPin import LSDataPin
from Source import Globs
from PySide2.QtWidgets import *

from Source.Widgets.Pin.LSDynamicDataSubPin import LSDynamicDataSubPin

qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss = open(qss_path, encoding="utf8").read()


class LSDynamicDataPin(LSDataPin):
    @classmethod
    def deserialize(cls,new_item_instance, wrapper: "LSDynamicDataPin") -> object:
        new_pin:"LSDynamicDataPin"=super().deserialize(new_item_instance,wrapper)
        new_pin.sub_pin_info=LSSubPinInfo(**wrapper.sub_pin_info)
        return new_pin

    def finished_init(self):
        for sub_pin_index,sub_pin_uuid in enumerate(self.sub_pin_info.sub_pins_uuid):
            sub_pin=self.node.find_pin_by_uuid(sub_pin_uuid)
            self.prepare_sub_pin(sub_pin, sub_pin_index)
            self.sub_pins.append(sub_pin)

    def __init__(self, *args, **kwargs):
        self.sub_pins:typing.List[LSDynamicDataSubPin]=[]
        with LSObject.Record(self, LSObject.RecordType.Serialize):
            self.sub_pin_info=LSSubPinInfo()

        super().__init__(*args, **kwargs)

    def init_attrs(self):
        super().init_attrs()

    def init_properties(self):
        super().init_properties()

    def init_ui(self):
        super().init_ui()

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet() + qss)

    def init_connection(self):
        super().init_connection()

    def get_sub_pins_uuid(self):
        print(self.sub_pins)
        return [sub_pin.uuid_ for sub_pin in self.sub_pins]

    def create_sub_pin(self,sub_pin_idx) -> LSDynamicDataSubPin:
        raise NotImplementedError

    def prepare_sub_pin(self,sub_pin,sub_pin_index):
        sub_pin.set_enabled(not self.is_in_connected)
        sub_pin.destroyed_signal.connect(self.sub_pin_destruct)
        sub_pin.set_title(f"arg{sub_pin_index}")

    def add_sub_pin(self, dynamic_idx=None):
        sub_pin_index = len(self.sub_pins)
        sub_pin_idx = dynamic_idx if dynamic_idx is not None else sub_pin_index
        sub_pin:LSDynamicDataSubPin = self.create_sub_pin(sub_pin_idx)
        self.prepare_sub_pin(sub_pin,sub_pin_index)
        sub_pin_row = self.row + sub_pin_idx + 1
        self.node.add_pin(sub_pin, row=sub_pin_row)
        self.sub_pins.append(sub_pin)
        self.sub_pin_info.sub_pins_uuid.append(sub_pin.uuid_)
        return sub_pin

    def sub_pin_destruct(self):
        sub_pin = self.sender()
        self.sub_pins.remove(sub_pin)
        self.sub_pin_info.sub_pins_uuid.remove(sub_pin.uuid_)

    def connect_finished(self, ):
        super().connect_finished()
        if self.get_flow()==PinFlow.In:
            for sub_pin in self.sub_pins:
                sub_pin.set_enabled(not self.is_in_connected)
                for line in sub_pin.out_lines:
                    line.update_pen_color()
                for line in sub_pin.in_lines:
                    line.update_pen_color()


    def disconnect_finished(self, ):
        super().disconnect_finished()
        if self.get_flow()==PinFlow.In:
            for sub_pin in self.sub_pins:
                sub_pin.set_enabled(not self.is_in_connected)
                for line in sub_pin.out_lines:
                    line.update_pen_color()
                for line in sub_pin.in_lines:
                    line.update_pen_color()



if __name__ == '__main__':
    app = QApplication()
    window = LSDynamicDataPin()
    window.show()
    app.exec_()
