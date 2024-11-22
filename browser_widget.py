from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction, QHBoxLayout, QSpacerItem, QSizePolicy
from webengine import MyWebEngineView, MyWebEnginePage
from loadingsvg import LoadingSvgView


class BrowserWidget(QWidget):
    def __init__(self, parent=None, url="https://www.google.com"):
        super(BrowserWidget, self).__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.toolbar = QToolBar()
        self.is_loading = False

        self.web_view = MyWebEngineView(parent)
        self.web_view.setPage(MyWebEnginePage(parent))
        self.web_view.setUrl(QUrl(url))
        self.web_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        self.web_view.urlChanged.connect(self.update_action_states)
        self.loading_svg_view = LoadingSvgView()
        self.loading_svg_view.hide()

        self.back_action = QAction(QIcon(":/assets/arrow_left.png"), "Back", self)
        self.back_action.triggered.connect(self.web_view.back)

        self.forward_action = QAction(QIcon(":/assets/arrow_right.png"), "Forward", self)
        self.forward_action.triggered.connect(self.web_view.forward)

        self.refresh_action = QAction(QIcon(":/assets/refresh.png"), "Refresh", self)
        self.refresh_action.triggered.connect(self.refresh_or_cancel)

        self.init_toolbar()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.web_view)
        self.layout.addWidget(self.loading_svg_view)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.web_view.loadStarted.connect(self.on_load_started)
        self.web_view.loadFinished.connect(self.on_load_finished)
        self.web_view.loadFinished.connect(self.update_action_states)
        self.update_action_states()

    def init_toolbar(self):
        self.toolbar.setStyleSheet("QToolBar { spacing: 10px; padding: 2px;}")

        left_padding_widget = QWidget()
        left_padding_widget.setFixedWidth(5)
        self.toolbar.addWidget(left_padding_widget)

        self.toolbar.addAction(self.back_action)
        self.toolbar.addAction(self.forward_action)
        self.toolbar.addAction(self.refresh_action)

        self.update_action_states()

    def update_action_states(self):
        self.back_action.setEnabled(self.web_view.history().canGoBack())
        self.forward_action.setEnabled(self.web_view.history().canGoForward())

    def refresh_or_cancel(self):
        if self.is_loading:
            self.web_view.stop()
        else:
            self.web_view.reload()

    def on_load_started(self):
        self.is_loading = True
        self.refresh_action.setIcon(QIcon(":/assets/cancel.png"))
        self.loading_svg_view.show()
        self.web_view.hide()

    def on_load_finished(self, success):
        self.is_loading = False
        self.refresh_action.setIcon(QIcon(":/assets/refresh.png"))
        self.loading_svg_view.hide()
        self.web_view.show()
        self.update_action_states()
