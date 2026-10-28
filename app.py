import webview
import os
import sys
import json
import webbrowser
import shutil
from tkinter import Tk, filedialog
import winreg

# ----------------------------------------
# PATH HANDLING
# ----------------------------------------
if getattr(sys, 'frozen', False):
    EXE_DIR = os.path.dirname(sys.executable)
    BUNDLE_DIR = sys._MEIPASS
else:
    EXE_DIR = os.path.dirname(os.path.abspath(__file__))
    BUNDLE_DIR = EXE_DIR

DATA_LOC_FILE = os.path.join(EXE_DIR, "data_location.json")
DATA_DIR = None

win = None
HOME = None
LOGIN = None

# ----------------------------------------
# DATA FOLDER SETUP (TAILOR STYLE)
# ----------------------------------------
REG_PATH = r"Software\MahaSevaKendra"
REG_KEY = "DataPath"

def setup_data_folder():
    global DATA_DIR

    # ✅ STEP 1: TRY REGISTRY (SECOND RUN)
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        DATA_DIR, _ = winreg.QueryValueEx(key, REG_KEY)
        winreg.CloseKey(key)

        if DATA_DIR and os.path.exists(DATA_DIR):
            return   # 🔥 no popup
    except:
        pass

    # 🔥 STEP 2: FIRST RUN ONLY
    root = Tk()
    root.withdraw()

    selected = filedialog.askdirectory(
        title="Select folder to store Maha Seva Kendra data"
    )

    if not selected:
        sys.exit()

    DATA_DIR = os.path.join(selected, "MahaSevaKendraData")
    os.makedirs(DATA_DIR, exist_ok=True)

    # ✅ SAVE PATH INSIDE REGISTRY (NOT FILE)
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
    winreg.SetValueEx(key, REG_KEY, 0, winreg.REG_SZ, DATA_DIR)
    winreg.CloseKey(key)

    # create config.json INSIDE data folder
    config_path = os.path.join(DATA_DIR, "config.json")
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            json.dump({"initialized": True}, f)

    # extract JSON files only once
    for file in ["users.json", "links.json"]:
        src = os.path.join(BUNDLE_DIR, file)
        dst = os.path.join(DATA_DIR, file)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy(src, dst)


# ----------------------------------------
# API
# ----------------------------------------
class API:
    def login(self, username, password):
        try:
            with open(os.path.join(DATA_DIR, "users.json"), "r") as f:
                users = json.load(f)

            if users.get(username) == password:
                win.load_url(HOME)
                return True
            return False
        except:
            return False

    def open_site(self, url):
        webbrowser.open(url)

    def go_home(self):
        win.load_url(HOME)

    def go_login(self):
        win.load_url(LOGIN)

    def get_links(self):
        try:
            with open(os.path.join(DATA_DIR, "links.json"), "r") as f:
                return json.load(f)
        except:
            return {}

# ----------------------------------------
# START APP
# ----------------------------------------
def resource_path(file):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, file)
    return os.path.join(EXE_DIR, file)

def start():
    global win, HOME, LOGIN

    setup_data_folder()   # ⭐ FIXED LOGIC

    HOME = resource_path("index.html")
    LOGIN = resource_path("login.html")

    win = webview.create_window(
        "Maha Seva Kendra – Digital Services",
        LOGIN,
        width=1920,
        height=1080,
        js_api=API(),
        fullscreen=False
    )
    webview.start(gui="edgechromium", debug=False)

if __name__ == "__main__":
    start()
