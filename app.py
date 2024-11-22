import sys
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QVBoxLayout, QPushButton, QTabBar, QTabWidget
from PyQt5.QtCore import Qt, QTimer
from browser_widget import BrowserWidget
from main_window import Ui_MainWindow
from print_handler import PrintHandler
from startup import StartupWindow
from newwindow import NewWindow
import resources_rc

URL_EXTPLORER = "https://online.statiebi.com/sencha_test"
URL_GOOGLE_SEARCH = "https://www.google.com"

# URL_EXTPLORER = "http://localhost/extplorer.html"
# URL_GOOGLE_SEARCH = "http://localhost"


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Splash screen
        self.splash = StartupWindow()
        self.tabWidget = QTabWidget(self.ui.centralwidget)
        font = QFont()
        font.setPointSize(14)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet("QTabWidget::pane { padding: 0px; margin: 0px; }")
        self.tabWidget.clear()
        self.addTab("Extplorer", URL_EXTPLORER)
        self.addTab("Google Search", URL_GOOGLE_SEARCH)
        self.tabWidget.setCurrentIndex(0)
        self.ui.verticalLayout.addWidget(self.tabWidget)

        # Connect menu actions
        self.ui.action_Exit.triggered.connect(self.close)
        self.ui.action_About.triggered.connect(self.show_about_dialog)
        self.ui.action_Print.triggered.connect(self.print_document)
        self.ui.action_On_Top.triggered.connect(self.toggle_on_top)

        # Set window to always be on top
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(":/assets/favicon.ico"))
        QTimer.singleShot(2000, self.showMaximized)

    def addTab(self, title: str, url: str):
        new_web_view = BrowserWidget(parent=self, url=url)

        if self.tabWidget.layout() is None:
            layout = QVBoxLayout(self.tabWidget)
            self.tabWidget.setLayout(layout)

        self.tabWidget.addTab(new_web_view, title)
        self.tabWidget.setCurrentWidget(new_web_view)

    def show_about_dialog(self):
        QMessageBox.about(self, "About", "Best Shop Extplorer 1.0!")

    def toggle_on_top(self, checked):
        if checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()

    def open_new_tab(self, url):
        new_web_view = BrowserWidget(parent=self, url=url)

        if self.tabWidget.layout() is None:
            layout = QVBoxLayout(self.tabWidget)
            self.tabWidget.setLayout(layout)

        index = self.tabWidget.addTab(new_web_view, url)
        self.tabWidget.setCurrentWidget(new_web_view)

        close_button = QPushButton()
        close_button.setIcon(QIcon(":/assets/cancel.png"))
        close_button.setFlat(True)
        close_button.setFixedSize(20, 20)
        close_button.clicked.connect(lambda: self.close_tab(index))
        tab_bar = self.tabWidget.tabBar()
        tab_bar.setTabButton(index, QTabBar.ButtonPosition.RightSide, close_button)

    def close_tab(self, index):
        if index >= 0:
            self.tabWidget.removeTab(index)

    def open_new_window(self, url):
        new_window = NewWindow(self, url=url)
        new_window.showMaximized()

    def print_document(self):
        active_view = self.tabWidget.currentWidget()
        view_to_print = active_view.web_view
        handler = PrintHandler()
        handler.setPage(view_to_print.page())
        handler.printPreview()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())
