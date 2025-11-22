import webview
from backend import Api

def main():
    api = Api()
    window = webview.create_window("PyEDB Explorer", "index.html", width=1200, height=800, js_api=api)
    api.set_window(window)
    webview.start()


if __name__ == "__main__":
    main()
