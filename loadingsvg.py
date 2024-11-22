from PyQt5.QtCore import Qt, QFile
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QHBoxLayout
import resources_rc


class LoadingSvgView(QWidget):
    def __init__(self):
        super(LoadingSvgView, self).__init__()
        self.svg_view = QWebEngineView()
        self.svg_view.setFixedSize(100, 100)
        self.svg_view.setAttribute(Qt.WA_TransparentForMouseEvents)
        file = QFile(":/assets/loading.svg")
        if not file.open(QFile.ReadOnly):
            print(f"Cannot open loading.svg")
            return
        svg_content = file.readAll().data().decode("utf-8")
        file.close()
        html = f"""
                <html>
                <head>
                    <style>
                        body, html {{
                            margin: 0;
                            padding: 0;
                            width: 100%;
                            height: 100%;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                        }}
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
        self.svg_view.setHtml(html)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.svg_view)
        self.setLayout(self.layout)
