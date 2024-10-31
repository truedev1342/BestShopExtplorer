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

        pixmap = QPixmap(":/splash.png")  # Replace with your splash screen image path
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
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionAbout.triggered.connect(self.show_about_dialog)
        self.ui.action_Print.triggered.connect(self.print_document)
        self.ui.actionOn_Top.triggered.connect(self.toggle_on_top)

        self.shortcut_f1 = QShortcut(QKeySequence(Qt.Key_F1), self)
        self.shortcut_f1.activated.connect(self.show_about_dialog)
        self.shortcut_ctrl_p = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_P), self)
        self.shortcut_ctrl_p.activated.connect(self.print_document)

        # Set window to always be on top
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(":/favicon.ico"))
        QTimer.singleShot(2000, self.showMaximized)

    def show_about_dialog(self):
        QMessageBox.about(self, "About", "Best Shop Extplorer 1.0!")

    def toggle_on_top(self, checked):
        if checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()

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
