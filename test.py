import webengine

class Api:
    def open_in_new_window(self, url):
        # This function will be called from JavaScript
        webview.create_window('New Window', url)

if __name__ == '__main__':
    api = Api()  # Create an instance of the Api class

    # URL to load in the main window
    main_url = 'http://localhost/extplorer.html'  # Change this to your desired URL

    # Create the main window with the specified URL and register the API
    main_window = webview.create_window('Main Window', main_url, js_api=api)

    # Start the webview application
    webview.start()
