from src.voice_recognition import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSlider
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, Qt
from PyQt5.QtGui import QIcon
import time

class Worker(QObject):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            mic_thread = threading.Thread(target=listen_microphone)
            mic_thread.start()

            transcribe_streaming()

        except Exception as e:
            messages.append(f"An error occurred: {e}")
        except KeyboardInterrupt:
            messages.append('stop')
        finally:
            end_of_stream_event.set()
            mic_thread.join()
            self.finished.emit()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.worker = Worker()
        self.worker.finished.connect(self.on_worker_finished)

        layout = QVBoxLayout()

        self.btn = QPushButton('실행')
        self.btn.clicked.connect(self.on_click)
        layout.addWidget(self.btn)

        self.label = QLabel(self)
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Haru AI')
        self.setWindowIcon(QIcon('icon.png'))
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_messages)
        self.timer.start(1000)  # 1초마다 업데이트

    def show_messages(self):
        messages = get_messages()
        formatted_messages = '\n'.join(messages)
        self.label.setText(formatted_messages)

    def on_click(self):
        if self.btn.text() == '실행':
            self.btn.setText('종료')
            self.worker_thread = threading.Thread(target=self.worker.run)
            self.worker_thread.start()
        else:
            self.btn.setText('실행')
            end_of_stream_event.set()

    def on_worker_finished(self):
        self.worker_thread.join()
        messages.append("Exiting...")
        app.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())