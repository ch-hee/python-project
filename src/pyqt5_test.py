import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

class TestGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Python GUI Program")

        btn = QPushButton('버튼1', self)
        btn.move(80, 13)
        btn.clicked.connect(self.btn_clicked)

        self.move(500, 500)
        self.resize(1000, 500)
        self.show()

    def btn_clicked(self):
        print('버튼이 클릭되었습니다.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TestGUI()
    sys.exit(app.exec_())