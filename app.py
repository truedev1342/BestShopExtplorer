import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QVBoxLayout, QPushButton, QTabBar
from PyQt5.QtCore import Qt, QUrl, QTimer
from main_window import Ui_MainWindow
from print_handler import PrintHandler
from startup import StartupWindow
from loadingsvg import LoadingSvgView
from webengine import MyWebEngineView, MyWebEnginePage
from newwindow import NewWindow
import resources_rc

URL_EXTPLORER = "https://online.statiebi.com/sencha_test"
URL_GOOGLE_SEARCH = "https://www.google.com"


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.is_loading = False

        # Splash screen
        self.splash = StartupWindow()

        # Original icon path
        self.refresh_button = QIcon(":/assets/refresh.png")
        self.cancel_icon = QIcon(":/assets/cancel.png")

        # Set webview and url
        self.extplorer_web_view = MyWebEngineView(self)
        self.extplorer_web_view.setPage(MyWebEnginePage(self))
        self.google_search_web_view = MyWebEngineView()
        self.google_search_web_view.setPage(MyWebEnginePage(self.google_search_web_view))
        self.extplorer_web_view.setUrl(QUrl(URL_EXTPLORER))
        self.google_search_web_view.setUrl(QUrl(URL_GOOGLE_SEARCH))
        self.setup_tab(self.ui.extplorer_tab, self.extplorer_web_view)
        self.setup_tab(self.ui.google_search_tab, self.google_search_web_view)

        self.loading_svg_widget = LoadingSvgView()

        self.extplorer_web_view.loadStarted.connect(self.on_load_started)
        self.extplorer_web_view.loadFinished.connect(self.on_load_finished)

        self.google_search_web_view.loadStarted.connect(self.on_load_started)
        self.google_search_web_view.loadFinished.connect(self.on_load_finished)

        self.extplorer_web_view.urlChanged.connect(self.setBackForwardBtnStatus)
        self.google_search_web_view.urlChanged.connect(self.setBackForwardBtnStatus)

        # Connect menu actions
        self.ui.action_Exit.triggered.connect(self.close)
        self.ui.action_About.triggered.connect(self.show_about_dialog)
        self.ui.action_Print.triggered.connect(self.print_document)
        self.ui.action_On_Top.triggered.connect(self.toggle_on_top)
        self.ui.action_Back.triggered.connect(self.go_back)
        self.ui.action_Forward.triggered.connect(self.go_forward)
        self.ui.action_Refresh.triggered.connect(self.refresh_page)
        self.ui.tabWidget.currentChanged.connect(self.setBackForwardBtnStatus)

        self.setBackForwardBtnStatus()

        # Set window to always be on top
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(":/assets/favicon.ico"))
        QTimer.singleShot(2000, self.showMaximized)

    @staticmethod
    def setup_tab(tab, web_view):
        if tab.layout() is not None:
            tab.layout().addWidget(web_view)
        else:
            print("Tab does not have a layout. Please set a layout in Qt Designer.")

    def show_about_dialog(self):
        QMessageBox.about(self, "About", "Best Shop Extplorer 1.0!")

    def toggle_on_top(self, checked):
        if checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()

    def navigate_view(self, direction):
        active_index = self.ui.tabWidget.currentIndex()
        if active_index == 0:
            current_view = self.extplorer_web_view
        elif active_index == 1:
            current_view = self.google_search_web_view
        else:
            return
        if direction == "back" and current_view.history().canGoBack():
            current_view.back()
        elif direction == "forward" and current_view.history().canGoForward():
            current_view.forward()

    def go_back(self):
        self.navigate_view("back")

    def go_forward(self):
        self.navigate_view("forward")

    def setBackForwardBtnStatus(self):
        active_index = self.ui.tabWidget.currentIndex()
        if active_index == 0:
            current_view = self.extplorer_web_view
        elif active_index == 1:
            current_view = self.google_search_web_view
        else:
            return
        self.ui.action_Back.setEnabled(current_view.history().canGoBack())
        self.ui.action_Forward.setEnabled(current_view.history().canGoForward())

    def show_loading_svg(self):
        current_tab = self.ui.tabWidget.currentWidget()
        if current_tab.layout() is None:
            layout = QVBoxLayout(current_tab)
            current_tab.setLayout(layout)
        layout = current_tab.layout()
        layout.addWidget(self.loading_svg_widget, alignment=Qt.AlignCenter)
        self.loading_svg_widget.show()
        self.extplorer_web_view.hide()
        self.google_search_web_view.hide()

    def hide_loading_svg(self):
        self.loading_svg_widget.hide()
        current_tab = self.ui.tabWidget.currentWidget()
        if current_tab.layout() is not None:
            current_tab.layout().removeWidget(self.loading_svg_widget)
            self.extplorer_web_view.show()
            self.google_search_web_view.show()

    def on_load_started(self):
        self.ui.action_Refresh.setIcon(self.cancel_icon)
        self.is_loading = True
        self.show_loading_svg()

    def on_load_finished(self):
        self.ui.action_Refresh.setIcon(self.refresh_button)
        self.is_loading = False
        self.hide_loading_svg()

    def refresh_page(self):
        active_index = self.ui.tabWidget.currentIndex()
        if active_index == 0:
            current_view = self.extplorer_web_view
        elif active_index == 1:
            current_view = self.google_search_web_view
        else:
            return
        if self.is_loading:
            current_view.stop()
        else:
            current_view.reload()

    def open_new_tab(self, url):
        new_web_view = MyWebEngineView(self)
        new_web_view.setPage(MyWebEnginePage(new_web_view))
        new_web_view.setUrl(QUrl(url))

        if self.ui.tabWidget.layout() is None:
            layout = QVBoxLayout(self.ui.tabWidget)
            self.ui.tabWidget.setLayout(layout)

        index = self.ui.tabWidget.addTab(new_web_view, url)
        self.ui.tabWidget.setCurrentWidget(new_web_view)

        close_button = QPushButton()
        close_button.setIcon(QIcon(":/assets/cancel.png"))
        close_button.setFlat(True)
        close_button.setFixedSize(20, 20)
        close_button.clicked.connect(lambda: self.close_tab(index))
        tab_bar = self.ui.tabWidget.tabBar()
        tab_bar.setTabButton(index, QTabBar.ButtonPosition.RightSide, close_button)

    def close_tab(self, index):
        if index >= 0:
            self.ui.tabWidget.removeTab(index)

    def open_new_window(self, url):
        new_window = NewWindow(self, url=url)
        new_window.showMaximized()

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
