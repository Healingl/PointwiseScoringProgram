import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QGraphicsView,
    QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class Window1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗口 1")
        self.resize(1024, 720)
        self.center()

        # 按钮 "进入"
        button = QPushButton("进入", self)
        button.setGeometry(1024 - 100, 20, 80, 40)  # 右上角位置
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


class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("窗口 2")
        self.resize(1024, 720)
        self.center()

        # 图片显示相关
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(20, 80, 984, 600)
        self.view.setRenderHints(self.view.renderHints() | Qt.SmoothTransformation)

        # 按钮 "进入" 放在左上角
        button1 = QPushButton("进入", self)
        button1.setGeometry(20, 20, 80, 40)  # 左上角位置
        button1.clicked.connect(self.open_window3)

        # 按钮 "退出" 放在右上角
        button2 = QPushButton("退出", self)
        button2.setGeometry(1024 - 100, 20, 80, 40)  # 右上角位置
        button2.clicked.connect(self.open_window1)

        # 按钮 "选择图片"
        self.load_button = QPushButton("选择图片", self)
        self.load_button.setGeometry(450, 20, 100, 40)
        self.load_button.clicked.connect(self.load_image)

        # 支持拖拽功能
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.display_image(file_path)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "图像文件 (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_path:
            self.display_image(file_path)

    def display_image(self, file_path):
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            self.scene.clear()
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(pixmap_item)
            self.view.fitInView(pixmap_item, Qt.KeepAspectRatio)

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
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
