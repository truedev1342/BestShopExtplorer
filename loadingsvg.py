from PyQt5.QtCore import Qt, QFile
from PyQt5.QtWebEngineWidgets import QWebEngineView
import resources_rc


class LoadingSvgView(QWebEngineView):
    def __init__(self):
        super(LoadingSvgView, self).__init__()
        self.setFixedSize(100, 100)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
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
        self.setHtml(html)
        self.hide()
