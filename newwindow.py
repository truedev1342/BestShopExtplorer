from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from webengine import MyWebEngineView, MyWebEnginePage
from loadingsvg import LoadingSvgView
import resources_rc


class NewWindow(QMainWindow):
    def __init__(self, parent=None, url=""):
        super(NewWindow, self).__init__(parent)
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url

        self.is_loading = False
        self.new_page = MyWebEngineView(self)
        self.new_page.setPage(MyWebEnginePage(self))
        self.loading_svg = LoadingSvgView()
        self.new_page.setUrl(QUrl(url))
        self.main_page = QWidget(self)
        self.main_page.setStyleSheet("background-color: white;")

        self.setWindowTitle(url)
        self.resize(800, 600)
        self.setCentralWidget(self.main_page)
        self.layout = QVBoxLayout(self.main_page)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.new_page)
        self.layout.addWidget(self.loading_svg, alignment=Qt.AlignCenter)
        self.loading_svg.hide()
        self.main_page.setLayout(self.layout)

        self.new_page.loadStarted.connect(self.on_load_started)
        self.new_page.loadFinished.connect(self.on_load_finished)

    def on_load_started(self):
        self.is_loading = True
        self.loading_svg.show()
        self.new_page.hide()

    def on_load_finished(self):
        self.is_loading = False
        self.loading_svg.hide()
        self.new_page.show()
