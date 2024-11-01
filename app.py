import sys
import time

from PyQt5.QtGui import QKeySequence, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QShortcut, QSplashScreen
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from main_window import Ui_MainWindow
from print_handler import PrintHandler

import resources_rc


class StartupWindow(QSplashScreen):  # Use QSplashScreen for better look
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.SplashScreen)  # make the splash screen on top
        QTimer.singleShot(2500, lambda: self.close())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        pixmap = QPixmap(":/assets/logo.png")  # Replace with your splash screen image path
        splash = StartupWindow(pixmap)
        splash.show()

        self.extplorer_web_view = QWebEngineView()
        self.google_search_web_view = QWebEngineView()

        self.extplorer_web_view.setUrl(QUrl("https://online.statiebi.com/sencha_test"))
        self.google_search_web_view.setUrl(QUrl("http://localhost"))

        if self.ui.extplorer_tab.layout() is not None:
            self.ui.extplorer_tab.layout().addWidget(self.extplorer_web_view)
        else:
            print("Extplorer tab does not have a layout. Please set a layout in Qt Designer.")

        if self.ui.google_search_tab.layout() is not None:
            self.ui.google_search_tab.layout().addWidget(self.google_search_web_view)
        else:
            print("Google Search tab does not have a layout. Please set a layout in Qt Designer.")

        # Connect menu actions
        self.ui.action_Exit.triggered.connect(self.close)
        self.ui.action_About.triggered.connect(self.show_about_dialog)
        self.ui.action_Print.triggered.connect(self.print_document)
        self.ui.action_On_Top.triggered.connect(self.toggle_on_top)
        self.ui.action_Back.triggered.connect(self.go_back)
        self.ui.action_Forward.triggered.connect(self.go_forward)
        self.ui.action_Refresh.triggered.connect(self.refresh_page)

        # Set window to always be on top
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(":/assets/favicon.ico"))
        QTimer.singleShot(2000, self.showMaximized)

    def show_about_dialog(self):
        QMessageBox.about(self, "About", "Best Shop Extplorer 1.0!")

    def toggle_on_top(self, checked):
        if checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()

    def go_back(self):
        active_index = self.ui.tabWidget.currentIndex()
        if active_index == 0:
            current_view = self.extplorer_web_view
        elif active_index == 1:
            current_view = self.google_search_web_view
        else:
            return
        if current_view.history().canGoBack():
            current_view.back()

    def go_forward(self):
        active_index = self.ui.tabWidget.currentIndex()
        if active_index == 0:
            current_view = self.extplorer_web_view
        elif active_index == 1:
            current_view = self.google_search_web_view
        else:
            return
        if current_view.history().canGoForward():
            current_view.forward()

    def refresh_page(self):
        active_index = self.ui.tabWidget.currentIndex()
        if active_index == 0:
            current_view = self.extplorer_web_view
        elif active_index == 1:
            current_view = self.google_search_web_view
        else:
            return
        current_view.reload()

    def print_document(self):
        active_index = self.ui.tabWidget.currentIndex()
        if active_index == 0:
            view_to_print = self.extplorer_web_view
        elif active_index == 1:
            view_to_print = self.google_search_web_view
        else:
            return
        handler = PrintHandler()
        handler.setPage(view_to_print.page())
        handler.printPreview()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())
