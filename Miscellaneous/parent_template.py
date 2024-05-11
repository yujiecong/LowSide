from Source import Globs
from Source.Common.Func import OS

title_name="LSObject"

py=f"{Globs.main_dir}/Widgets/Custom/{title_name}.py"
if OS.exists(py):
    raise
with open(py,"w") as f:
    f.write(
        f'''
from Source import Globs
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from Common.Func import OS
from Widgets.Custom.LSObject import LSObject

class {title_name}(QFrame,LSObject):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        LSObject.__init__(self)
        
        self.init_ui()
        self.init_attrs()
        self.init_connection()
        self.init_style()
        self.init_properties()
        
    def init_attrs(self):
        pass
        
    def init_properties(self):
        pass
        
    def init_ui(self):
        pass
        
    def init_style(self):
        qss = OS.join(Globs.qss_dir, OS.basename(__file__) + ".qss")
        self.setStyleSheet(open(qss,encoding="utf8").read())
        
    def init_connection(self):
        pass
        
if __name__ == '__main__':
    app=QApplication()
    window={title_name}()
    window.show()
    app.exec_()
'''
    )
with open(f"{Globs.main_dir}/Widgets/Custom/Qss/{title_name}.qss",'w'):
    pass