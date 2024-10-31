import sys
import webview
from PyQt5.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget, QPushButton

class WebViewWidget(QWidget):
    def __init__(self, url):
        super().__init__()
        self.open_webview(url)

    def open_webview(self, url):
        # Open the webview in a separate thread
        webview.create_window("Web page", url, width=800, height=600)
        webview.start()

class MainWindow(QTabWidget):
    def __init__(self):
        super().__init__()

        # Create and add tabs
        self.add_tab("Freelancer", "https://www.freelancer.com")
        self.add_tab("Upwork", "https://www.upwork.com")

    def add_tab(self, name, url):
        webview_widget = WebViewWidget(url)
        self.addTab(webview_widget, name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.setWindowTitle("PyQt Webview in Tab")
    main_window.resize(800, 600)
    main_window.show()
    
    sys.exit(app.exec())
