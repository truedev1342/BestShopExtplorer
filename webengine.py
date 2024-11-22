from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage


class MyWebEngineView(QWebEngineView):
    def __init__(self, parent=None):
        super(MyWebEngineView, self).__init__(parent)


class MyWebEnginePage(QWebEnginePage):

    def __init__(self, parent=None, open_mode=0):
        super(MyWebEnginePage, self).__init__(parent)
        self.open_mode = open_mode
        self.parent = parent

    def createWindow(self, nav_type: QWebEnginePage.WebWindowType) -> QWebEnginePage:
        self.open_mode = 0
        if nav_type == QWebEnginePage.WebBrowserTab or nav_type == QWebEnginePage.WebBrowserBackgroundTab:
            self.open_mode = 1
        else:
            self.open_mode = 2
        return MyWebEnginePage(self.parent, open_mode=self.open_mode)

    def acceptNavigationRequest(self, url: QUrl, nav_type: QWebEnginePage.NavigationType, is_main_frame: bool) -> bool:
        if nav_type == QWebEnginePage.NavigationTypeLinkClicked:
            if self.open_mode == 1:
                self.parent.open_new_tab(url.toString())
                return True
            elif self.open_mode == 2:
                self.parent.open_new_window(url.toString())
                return True
        result = super().acceptNavigationRequest(url, nav_type, is_main_frame)
        return result
