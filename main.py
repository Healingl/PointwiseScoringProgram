# -*- coding: utf-8 -*-
# @Time : 2024/11/15 21:24
# @Author : Yuzhou Zhuang
# @Email : 605540375@qq.com

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget


class Window1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗口 1")
        self.setGeometry(100, 100, 1024, 720)

        # 按钮
        button = QPushButton("跳转到窗口 2", self)
        button.clicked.connect(self.open_window2)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_window2(self):
        self.window2 = Window2()
        self.window2.show()
        self.close()


class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗口 2")
        self.setGeometry(100, 100, 1024, 720)

        # 按钮
        button1 = QPushButton("跳转到窗口 1", self)
        button1.clicked.connect(self.open_window1)
        button2 = QPushButton("跳转到窗口 3", self)
        button2.clicked.connect(self.open_window3)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_window1(self):
        self.window1 = Window1()
        self.window1.show()
        self.close()

    def open_window3(self):
        self.window3 = Window3()
        self.window3.show()
        self.close()


class Window3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗口 3")
        self.setGeometry(100, 100, 1024, 720)

        # 按钮
        button = QPushButton("跳转到窗口 2", self)
        button.clicked.connect(self.open_window2)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_window2(self):
        self.window2 = Window2()
        self.window2.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Window1()
    main_window.show()
    sys.exit(app.exec_())

