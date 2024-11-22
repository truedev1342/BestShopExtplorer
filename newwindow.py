from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from browser_widget import BrowserWidget
from main_window import Ui_MainWindow
from print_handler import PrintHandler
import resources_rc

# URL_EXTPLORER = "https://online.statiebi.com/sencha_test"
# URL_GOOGLE_SEARCH = "https://www.google.com"

URL_EXTPLORER = "http://localhost/extplorer.html"
URL_GOOGLE_SEARCH = "http://localhost"


class NewWindow(QMainWindow):
    def __init__(self, parent=None, url=""):
        super(NewWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.action_Exit.triggered.connect(self.close)
        self.ui.action_About.triggered.connect(self.show_about_dialog)
        self.ui.action_Print.triggered.connect(self.print_document)
        self.ui.action_On_Top.triggered.connect(self.toggle_on_top)

        # Set window to always be on top
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(":/assets/favicon.ico"))

        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url

        self.new_page = BrowserWidget(parent=self, url=url)
        self.ui.verticalLayout.addWidget(self.new_page)
    def show_about_dialog(self):
        QMessageBox.about(self, "About", "Best Shop Extplorer 1.0!")

    def toggle_on_top(self, checked):
        if checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()

    def print_document(self):
        view_to_print = self.new_page.web_view
        handler = PrintHandler()
        handler.setPage(view_to_print.page())
        handler.printPreview()
