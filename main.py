import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDesktopWidget


class Window1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗口 1")
        self.resize(1024, 720)
        self.center()  # 居中显示

        # 按钮 "进入"
        button = QPushButton("进入", self)
        button.setGeometry(1024 - 100, 20, 80, 40)  # 右上角位置
        button.clicked.connect(self.open_window2)

    def center(self):
        screen = QDesktopWidget().availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(screen.center())
        self.move(frame.topLeft())

    def open_window2(self):
        self.window2 = Window2()
        self.window2.show()
        self.close()


class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗口 2")
        self.resize(1024, 720)
        self.center()  # 居中显示

        # 按钮 "进入" 放在左上角
        button1 = QPushButton("上一个界面", self)
        button1.setGeometry(20, 20, 80, 40)  # 左上角位置
        button1.clicked.connect(self.open_window1)

        # 按钮 "退出" 放在右上角
        button2 = QPushButton("下一个界面", self)
        button2.setGeometry(1024 - 100, 20, 80, 40)  # 右上角位置
        button2.clicked.connect(self.open_window12)

    def center(self):
        screen = QDesktopWidget().availableGeometry()
        frame = self.frameGeometry()
        frame.moveCenter(screen.center())
        self.move(frame.topLeft())

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
        self.resize(1024, 720)
        self.center()  # 居中显示

        # 按钮 "退出" 放在左上角
        button = QPushButton("退出", self)
        button.setGeometry(20, 20, 80, 40)  # 左上角位置
        button.clicked.connect(self.open_window2)

    def center(self):
        screen = QDesktopWidget().availableGeometry()
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
