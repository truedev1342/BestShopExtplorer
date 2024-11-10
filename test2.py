import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl  # Import QUrl


class CustomWebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setUrl(QUrl("http://localhost/extplorer.html"))  # Set a default URL


class CustomWebEnginePage(QWebEnginePage):

    def javaScriptConsoleMessage(self, level, msg, lineNumber, sourceID):
        print(f"JavaScript Console: {msg} (Line {lineNumber})")

    def createWindow(self, type: 'QWebEnginePage.WebWindowType') -> 'QWebEnginePage':
        print(f"Opening URL in new window:")

    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        if nav_type == QWebEnginePage.NavigationTypeLinkClicked:
            print(f"Opening URL in new tab: {url.toString()}")
            return False  # Cancel the current navigation
        return super().acceptNavigationRequest(url, nav_type, is_main_frame)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QWebEngineView Example")
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.open_new_tab()  # Open the first tab

        # Setup a menu for opening new tabs
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        new_tab_action = QAction('New Tab', self)
        new_tab_action.triggered.connect(self.open_new_tab)
        file_menu.addAction(new_tab_action)

    def open_new_tab(self, url=None):
        if url is None:
            url = QUrl("http://localhost/extplorer.html")  # Create QUrl for the default URL
        web_view = CustomWebEngineView(self)
        web_view.setPage(CustomWebEnginePage(web_view))
        web_view.setUrl(url)  # Set URL using QUrl
        self.tab_widget.addTab(web_view, url.toString())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.resize(1024, 768)
    main_win.show()
    sys.exit(app.exec_())
