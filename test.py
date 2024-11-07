import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage


class CustomWebEngineView(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setPage(CustomWebEnginePage(self))


class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent):
        super().__init__(parent)

    def acceptNavigationRequest(self, url, navigationType, isMainFrame):
        # Handle navigation requests
        if navigationType == QWebEnginePage.NavigationTypeOther:
            # If the request is from a window.open call
            self.view().goto(url.toString())  # Use the view's goto method
            return False  # Prevent default handling
        return super().acceptNavigationRequest(url, navigationType, isMainFrame)

    def javascriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"JS message: {message} (Line: {lineNumber}, Source: {sourceID})")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = CustomWebEngineView()

    # Set the HTML content directly with the button and script.
    html_content = '''
    <html>
    <body>
        <button onclick="myFunction()">Try it</button>
        <script>
        function myFunction() {
            window.open("https://www.w3schools.com");
        }
        </script>
    </body>
    </html>
    '''

    view.setHtml(html_content)  # Use setHtml to set custom HTML content
    view.show()
    sys.exit(app.exec_())
