import webview
from backend import Api

def main():
    api = Api()
    webview.create_window("EDB Explorer", "index.html", width=1200, height=800, js_api=api)
    webview.start()


if __name__ == "__main__":
    main()
