# -*- coding: utf-8 -*-
# @Time : 2024/11/15 22:02
# @Author : Yuzhou Zhuang
# @Email : 605540375@qq.com


import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton,  QLabel, QFileDialog, QGraphicsView,
    QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import yaml

class Window1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗口 1")
        self.resize(1024, 720)
        self.center()

        # 创建一个中心部件来布局其他组件
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # 用于放置文件选择相关组件的水平布局
        file_choose_layout = QHBoxLayout()

        # 左右边距，可根据实际情况调整
        margin_size = 20

        # 用于显示文件路径的文本框
        self.file_path_edit = QLineEdit(self)
        file_choose_layout.addWidget(self.file_path_edit)

        # 按钮 "YAML配置文件选择"
        select_button = QPushButton("YAML配置文件选择", self)
        select_button.clicked.connect(self.choose_yaml_file)
        file_choose_layout.addWidget(select_button)

        # 设置水平布局的左右边距
        file_choose_layout.setContentsMargins(margin_size, 0, margin_size, 0)
        main_layout.addLayout(file_choose_layout)

        # 按钮 "下一界面"，放置在右上角
        next_button = QPushButton("下一界面", self)
        next_button.setGeometry(1024 - 100, 20, 80, 40)  # 右上角位置
        next_button.clicked.connect(self.open_window2)

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(screen.center())
        self.move(frame.topLeft())

    def choose_yaml_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择YAML配置文件", "", "YAML Files (*.yaml)")
        if file_path:
            self.file_path_edit.setText(file_path)

    def open_window2(self):
        # # 这里可以添加逻辑，比如根据获取到的文件路径读取config.yaml文件内容并传递给下一个窗口
        # file_path = self.file_path_edit.text()
        # if file_path:
        #     try:
        #         with open(file_path, 'r') as file:
        #             data = yaml.safe_load(file)
        #             print(data)  # 这里简单打印读取到的数据，可根据需求处理
        #     except FileNotFoundError:
        #         print(f"文件 {file_path} 不存在")

        self.window2 = Window2()
        self.window2.show()
        self.close()

class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗口 2")
        self.resize(1024, 720)
        self.center()

        # 按钮 "进入" 放在左上角
        button1 = QPushButton("上一界面", self)
        button1.setGeometry(20, 20, 80, 40)  # 左上角位置
        button1.clicked.connect(self.open_window1)

        # 按钮 "退出" 放在右上角
        button2 = QPushButton("下一界面", self)
        button2.setGeometry(1024 - 100, 20, 80, 40)  # 右上角位置
        button2.clicked.connect(self.open_window3)

    def open_window1(self):
        self.window1 = Window1()
        self.window1.show()
        self.close()

    def open_window3(self):
        self.window3 = Window3()
        self.window3.show()
        self.close()

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(screen.center())
        self.move(frame.topLeft())


class Window3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗口 3")
        self.resize(1024, 720)
        self.center()

        # 按钮 "退出" 放在左上角
        button = QPushButton("退出", self)
        button.setGeometry(20, 20, 80, 40)  # 左上角位置
        button.clicked.connect(self.open_window2)

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(screen.center())
        self.move(frame.topLeft())

    def open_window2(self):
        self.window2 = Window2()
        self.window2.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Window1()
    main_window.show()
    sys.exit(app.exec_())
