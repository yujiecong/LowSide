from PySide2.QtWidgets import QApplication, QLineEdit

# 创建应用程序实例
app = QApplication([])

# 创建一个 QLineEdit
line_edit = QLineEdit()
line_edit.setText("Hello, World!")  # 设置文本内容

# 设置光标位置到第一个字符后面
line_edit.setCursorPosition(1)

# 显示 QLineEdit
line_edit.show()

# 运行应用程序
app.exec_()
