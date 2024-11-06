import sys

from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer, QSvgWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QSplashScreen, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QUrl, QTimer, QFile
from PyQt5.QtWebEngineWidgets import QWebEngineView
from main_window import Ui_MainWindow
from print_handler import PrintHandler
import resources_rc

URL_EXTPLORER = "http://localhost/extplorer.html"
URL_GOOGLE_SEARCH = "http://localhost"


class StartupWindow(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.SplashScreen)
        QTimer.singleShot(2500, lambda: self.close())


class AnimatedSvgWidget(QSvgWidget):
    def __init__(self, svg_file):
        super().__init__()
        r = self.renderer()
        r.setFramesPerSecond(60)
        r.load(svg_file)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.is_loading = False

        # Splash screen
        pixmap = QPixmap(":/assets/logo.png")
        splash = StartupWindow(pixmap)
        splash.show()

        # Original icon path
        self.refresh_button = QIcon(":/assets/refresh.png")
        self.cancel_icon = QIcon(":/assets/cancel.png")

        # Set webview and url
        self.extplorer_web_view = QWebEngineView()
        self.google_search_web_view = QWebEngineView()
        self.extplorer_web_view.setUrl(QUrl(URL_EXTPLORER))
        self.google_search_web_view.setUrl(QUrl(URL_GOOGLE_SEARCH))
        self.setup_tab(self.ui.extplorer_tab, self.extplorer_web_view)
        self.setup_tab(self.ui.google_search_tab, self.google_search_web_view)

        # self.loading_svg_widget = AnimatedSvgWidget(":/assets/loading.svg")
        self.loading_svg_widget = QWebEngineView()
        # self.loading_svg_widget.setUrl(QUrl(":/assets/loading.svg"))
        self.loading_svg_widget.setFixedSize(100, 100)
        self.loading_svg_widget.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.loading_svg_widget.hide()
        self.load_svg_as_data_url(":/assets/loading.svg")

        self.extplorer_web_view.loadStarted.connect(self.on_load_started)
        self.extplorer_web_view.loadFinished.connect(self.on_load_finished)

        self.google_search_web_view.loadStarted.connect(self.on_load_started)
        self.google_search_web_view.loadFinished.connect(self.on_load_finished)

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

    def load_svg_as_data_url(self, resource_path):
        file = QFile(resource_path)
        if not file.open(QFile.ReadOnly):
            print(f"Cannot open {resource_path}")
            return
        svg_content = file.readAll().data().decode("utf-8")
        file.close()
        html = f"""
                <html>
                <head>
                    <style>
                        body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; }}
                        svg {{
                            width: 100%;
                            height: 100%;
                            preserveAspectRatio: xMidYMid meet; /* Adjust as necessary */
                        }}
                    </style>
                </head>
                <body>
                    {svg_content}
                </body>
                </html>
                """
        self.loading_svg_widget.setHtml(html)

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

    def on_load_finished(self, success):
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
