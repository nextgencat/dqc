import customtkinter as ctk
import requests
from dummy_manager import run_new_process

# -- discord game list
IDS_URL = "https://discord.com/api/v10/applications/detectable"
# -- ctk settings
TITLE = "Discord Quest Completer"

# -- fetching data
response = requests.get(IDS_URL, timeout=10)
response.raise_for_status()

data = response.json()
  
# handle process start button

def clean_name(raw: str) -> str:
    raw = raw.lstrip(">").replace("\\", "/")
    raw = raw.split("/")[-1]
    return "".join(c for c in raw if c not in '<>:"|?*')

def start_process(app):
    print("----------------------------")
    print(app["name"])
    print(app["executables"][0]["name"])
    print(app["id"])

    name = None

    for a in app["executables"]:
        if not a["name"].lower().endswith(".exe"):
            continue
        name = clean_name(a["name"])
        break

    if name is None:
        print("error")
    else: 
        run_new_process(name)

# seartch hand;e

def search_handle(event=None):
    target = search_bar.get().strip().lower()

    for widget in search_frame.winfo_children():
        widget.destroy()
    
    if not target:
        return

    found = []
    for app in data:
        if target in app["name"].lower():
            found.append(app)
            if len(found) >= 20:
                break
    
    for app in found:
        ctk.CTkButton(search_frame, text=app["name"], command=lambda a=app: start_process(a)).pack(padx=(2.5), pady=(2.5), anchor="w")

app = ctk.CTk()
app.geometry("600x500")
app.title(TITLE)

search_bar = ctk.CTkEntry(app, placeholder_text="Search game", width=300, height=35)
search_bar.pack(padx=10, pady=(10, 0), anchor="w")
search_bar.bind("<Return>", search_handle)

search_frame = ctk.CTkScrollableFrame(app, width=580, height=480)
search_frame.pack(padx=10, pady=(2.5,5), anchor="w")

app.mainloop()