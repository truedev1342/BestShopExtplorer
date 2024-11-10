from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage


class MyWebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super(MyWebEngineView, self).__init__(parent)


class MyWebEnginePage(QWebEnginePage):

    def createWindow(self, type: QWebEnginePage.WebWindowType) -> QWebEnginePage:
        print(f"opening new tab or window")

    def acceptNavigationRequest(self, url: QUrl, nav_type: QWebEnginePage.NavigationType, is_main_frame: bool) -> bool:
        if nav_type == QWebEnginePage.NavigationTypeLinkClicked:
            print(f"Opening URL in new tab: {url.toString()}")
        return super().acceptNavigationRequest(url, nav_type, is_main_frame)