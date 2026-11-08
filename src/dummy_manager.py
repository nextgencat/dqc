import os
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

OUTPUT_DIR = Path("output").resolve()
DEFAULT_NAME = "dummy"  # без .exe
DUMMY_PATH = OUTPUT_DIR / (DEFAULT_NAME + ".exe")


def find_exe():
    if not OUTPUT_DIR.exists():
        return None
    for f in OUTPUT_DIR.glob("*"):
        if f.is_file() and f.suffix.lower() == ".exe":
            return f
    return None


def build_dummy():
    existing = find_exe()
    if existing:
        print(f"exe already exists: {existing.name}")
        return existing

    print("building a dummy file..")

    gui_code = '''
import os
import sys
import tkinter as tk

title = os.path.splitext(os.path.basename(sys.executable))[0]

root = tk.Tk()
root.title(title)
root.geometry("400x200")
tk.Label(root, text=title, font=("Arial", 14)).pack(pady=30)
root.mainloop()
'''

    with tempfile.TemporaryDirectory() as tmp:
        script_path = os.path.join(tmp, "app.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(gui_code)

        subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--onefile", "--noconsole",
            "--name", DEFAULT_NAME,
            "--distpath", str(OUTPUT_DIR),
            "--workpath", os.path.join(tmp, "build"),
            "--specpath", tmp,
            script_path,
        ], check=True)

    print(f"Ready: {DUMMY_PATH}")
    return DUMMY_PATH


def run_new_process(name):
    if not name.lower().endswith(".exe"):
        name += ".exe"

    src = build_dummy()
    dst = OUTPUT_DIR / name

    if dst != src and not dst.exists():
        shutil.copyfile(src, dst)

    return subprocess.Popen([str(dst)], cwd=str(OUTPUT_DIR))