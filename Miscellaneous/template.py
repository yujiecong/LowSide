from Source import Globs
from Source.Common.Func import OS

title_name="LSPinWrapper"

py=f"{Globs.source_dir}/Widgets/{title_name}.py"

if OS.exists(py):
    raise
with open(py,"w",encoding="utf8") as f:
    f.write(
        f'''
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from Source.Common.Func import OS
from Source.Custom.LSObject import LSObject



qss_path = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
qss=open(qss_path,encoding="utf8").read()
class {title_name}(QFrame,LSObject):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        "如果有父了 就不要调用了"
        LSObject.__init__(self)
        
    def init_attrs(self):
        super().init_attrs()

        
    def init_properties(self):
        super().init_properties()

        
    def init_ui(self):
        super().init_ui()

    def init_style(self):
        super().init_style()
        self.setStyleSheet(self.styleSheet()+qss)

        
    def init_connection(self):
        super().init_connection()
        pass
if __name__ == '__main__':
    app=QApplication()
    window={title_name}()
    window.show()
    app.exec_()
'''
    )
with open(f"{Globs.source_dir}/Widgets/Qss/{title_name}.qss",'w'):
    pass