import requests
import tkinter as tk
from tkinter import font
import webbrowser
from tkinter import *
from PIL import Image, ImageTk 
from tkinter import ttk
import os
from io import BytesIO
import customtkinter as ctk
import threading
import ctypes

## FUNCTIONS ##




def show_frame(frame):
    for f in (home_frame, game_frame, achievement_frame):
        f.pack_forget()
    frame.pack(fill="both", expand = True)


def update_avatar(): 
    img_pil = Image.open("images/avatar.jpg")

    img = ctk.CTkImage(
        light_image=img_pil,
        dark_image=img_pil,
        size=(184,184)
    )

    user_pfp.configure(image=img)
    user_pfp.image = img


def can_call_steam():
    return bool(api_key.strip()) and bool(steam_id.strip())

## CTk ##
ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")


## VARIABLES ##
api_key_text = open("text files/api_key.txt", "r+")
api_key = api_key_text.read()
api_key_text.close()
steam_id_text = open("text files/steam_id.txt", "r+")
steam_id = steam_id_text.read()
steam_id_text.close()
display_name_text = open("text files/display_name.txt", "r+")
display_name = display_name_text.read()
display_name_text.close()

## ROOT ##
root = ctk.CTk()
root.title("Steam Achievement Tracker")
root.resizable(True, True)

## FONTS ##
title_font = ctk.CTkFont(family="Arial", size=24, weight="bold")
italic_font = ctk.CTkFont(family="Arial", size=14, weight="bold")
link_font = ctk.CTkFont(family="Arial", size=14, weight="bold", underline=True)


## ROOT WIDGETS##
home_frame = ctk.CTkFrame(root)
game_frame = ctk.CTkScrollableFrame(root, width=800,height=800)
home_frame.pack(fill="both", expand=True)
achievement_frame = ctk.CTkFrame(root)
back_button_ach = ctk.CTkButton(achievement_frame, text="Back", width = 80, height = 40, command = lambda: show_frame(game_frame))

ach_frame_desc = ctk.CTkLabel(achievement_frame, font=ctk.CTkFont(family="Arial", size = 18, slant="italic"),text_color="grey")
ach_frame_title = ctk.CTkLabel(achievement_frame, font=ctk.CTkFont(family="Arial", size = 24, weight="bold"))
ach_frame_achieved = ctk.CTkLabel(achievement_frame, font=ctk.CTkFont(family="Arial", size = 24, weight="bold"))

achievement_loading_bar = ctk.CTkProgressBar(game_frame, mode = "indeterminate", indeterminate_speed = 2)  
def settings(choice):
    if choice == "Change API Key": 
        api_popup()
    elif choice == "Change Steam ID":
        steam_id_window()
    elif choice == "Update Achievements":
        get_game_stats(None)
    elif choice == settings:
        pass
    settings_menu.set("Settings")
settings_menu = ctk.CTkOptionMenu(
    home_frame,
    values=["Settings", "Change API Key", "Change Steam ID", "Update Achievements"],
    command = settings
)
settings_menu_game = ctk.CTkOptionMenu(
    game_frame,
    values=["Settings", "Change API Key", "Change Steam ID", "Update Achievements"],
    command = settings
)
settings_menu_ach = ctk.CTkOptionMenu(
    achievement_frame,
    values=["Settings", "Change API Key", "Change Steam ID", "Update Achievements"],
    command = settings
)



settings_menu.place(relx=1.0, rely=0, anchor="ne")



hello_user = ctk.CTkLabel(
home_frame,
text=(f""),
font= title_font,)

user_pfp = ctk.CTkLabel(
home_frame,
width=184,
height=184,
text="")

what_game = ctk.CTkLabel(
home_frame,
text="Which game would you like to track today?",
font=title_font,)

hello_user.pack(padx=20, pady=20)
user_pfp.pack(padx=20,pady=20)
what_game.pack(padx=10,pady=10)


## FUNCTIONS ##
def open_api_link(event):
    webbrowser.open("https://steamcommunity.com/dev/apikey")
def open_steam_id_link(event):
    webbrowser.open("https://store.steampowered.com/account/")

def test_api_key(api_key):
    url = "https://api.steampowered.com/ISteamWebAPIUtil/GetSupportedAPIList/v0001//"
    params = {"key": api_key}
    r = requests.get(url, params=params, timeout=5)

    if r.status_code == 200:
        return True
    else: return False
def test_steam_id(steam_id):
    url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {"key": api_key, "steamids": steam_id}
    try: 
        r=requests.get(url, params=params,timeout=5)
        r.raise_for_status()
        data = r.json()
        player = data["response"]["players"][0]
        avatar_url = player["avatarfull"]
        display_name = player["personaname"]
        
        file_path_2 = "text files/display_name.txt"
        with open(file_path_2, "w", encoding = 'utf-8') as f:
            f.write(display_name)
            
            def update_username():
                hello_user.configure(text=(f"Hello,  {display_name}!"))
        update_username()
        avatar_response = requests.get(avatar_url)
        avatar_response.raise_for_status()
        file_path = "images/avatar.jpg"
        with open(file_path, "wb") as f:
            f.write(avatar_response.content)
        update_avatar()

        if "response" in data and "players" in data["response"] and len(data["response"]["players"]) > 0:
            return True
        else: return False
    except requests.RequestException:
        return False
         
        
def api_popup():
    api_key_popup = ctk.CTkToplevel(root)
    api_key_popup.title("Enter API Key")
    api_key_popup.geometry("500x400+710+340")
    api_key_popup.transient(root)
    api_key_label = ctk.CTkLabel(
        api_key_popup,
        text="Enter your Steam API key:",
        font=ctk.CTkFont(family="Arial", size=12, weight="bold"))
    api_key_label.pack(padx=10, pady=10)
 
    api_key_label2 = ctk.CTkLabel(
        api_key_popup,
        text="Don't know how to get your API key? Click here",
        font=ctk.CTkFont(family="Arial", size=12, weight="bold", underline=True),
        text_color="blue",
        cursor="hand2")
    api_key_label2.bind("<Button-1>", open_api_link)
    api_key_label2.pack(padx=10, pady=10)

    api_key_label4 = ctk.CTkLabel(
        api_key_popup,
        text="You can enter anything for the url.",
        font=italic_font)
    api_key_label4.pack(padx=10, pady=10)

    def get_api_key():
        global api_key 
        api_key = api_key_input.get()
        
        if test_api_key(api_key):
            api_success = ctk.CTkToplevel(root)
            api_success.geometry("500x150+710+465")
            api_success.title("Success!")
            api_success.transient(root)
            api_success.focus_force()
            
            def on_yay_click():
                api_success.destroy()
                steam_id_window()
               
            label = ctk.CTkLabel(
            api_success,
            text="API Key has been verified!",
            font = title_font)
            label.pack(padx=20, pady=20)

            btn1 = ctk.CTkButton(
            api_success,
            text="Yay!",
            height= 80,
            width= 80,
            command=on_yay_click)
            btn1.pack(padx=20, pady=10) 

            file_path = "text files/api_key.txt"
            with open(file_path, "w", encoding = 'utf-8') as f:
                f.write(api_key)
            api_key_popup.destroy()
        else:
            api_fail = ctk.CTkToplevel(root)
            api_fail.geometry("500x150+710+465")
            api_fail.title = "Fail!"
            api_fail.transient(root)
            api_fail.focus_force()
            
            label = ctk.CTkLabel(
            api_fail,
            text="Invalid API Key!",
            font = title_font)
            label.pack(padx=20, pady=20)

            btn1 = ctk.CTkButton(
            api_fail,
            text="Ok.",
            height= 1, width= 3,
            command=api_fail.destroy)
            btn1.pack(padx=20, pady=10)
            
            api_key_input.delete(0, tk.END)

    api_key_input = ctk.CTkEntry(
    api_key_popup,
    font=("Arial", 14))
    
    api_key_input.pack(padx=10, pady=10)

    api_key_button = ctk.CTkButton(
    api_key_popup,
    text="Enter",
    command=get_api_key,)
    
    api_key_button.pack(padx=10, pady=10)

    api_key_label3 = ctk.CTkLabel(
        api_key_popup,
        text="your api key only communicates with the steam servers," \
        " and is sent nowhere else.",
        font=ctk.CTkFont(family="Arial", size=12, slant="italic"),
        text_color="grey") 
    api_key_label3.pack(padx=10,pady=40)
    
def steam_id_window():
    steam_id_window = ctk.CTkToplevel(root)   
    steam_id_window.title("Enter Steam ID")
    steam_id_window.geometry("500x400+710+340")
    steam_id_window.transient(root)

    steam_id_label = ctk.CTkLabel(
        steam_id_window,
        text="Enter your Steam ID:",
        font=title_font,
    )   
    steam_id_label2 = ctk.CTkLabel(
        steam_id_window,
        text="Don't know how to get your Steam ID? Click here",
        font=link_font,
        text_color="blue",
        cursor="hand2",
    )
    steam_id_label2.bind("<Button-1>", open_steam_id_link)
    canvas = ctk.CTkCanvas(
        steam_id_window,
        width =294,
        height=92,
        background = steam_id_window.cget("fg_color")[1],
        highlightthickness=0 
    )
    steam_id_label3 = ctk.CTkLabel(
        steam_id_window,
        text="The achievement tracker will not work for private profiles.",
        font=italic_font,
    )
    img = Image.open("images/Steam_Id_Image.png")
    img = ImageTk.PhotoImage(img)
    canvas.create_image(294//2,92//2, image=img, anchor="center")
    canvas.img = img

    def get_steam_id():
        global steam_id 
        steam_id = steam_id_input.get()
        if test_steam_id(steam_id):
            refresh_game_combo()
            id_success = ctk.CTkToplevel(root)
            id_success.geometry("500x150+710+465")
            id_success.title("Success!")
            id_success.transient(root)
            id_success.focus_force()
            label = ctk.CTkLabel(id_success, text="Steam ID has been verified!", font = title_font)
            btn1 = ctk.CTkButton(id_success, text="Yay!",height= 80, width= 80, command =id_success.destroy)
            file_path = "text files/steam_id.txt"
            with open(file_path, "w", encoding = 'utf-8') as f:
                f.write(steam_id)
            steam_id_window.destroy()
            label.pack(padx=20, pady=20)
            btn1.pack(padx=20, pady=10) 
        else:
            id_fail = ctk.CTkToplevel(root)
            id_fail.geometry("500x150+710+465")
            id_fail.title = "Fail!"
            id_fail.transient(root)
            id_fail.focus_force()
            label = ctk.CTkLabel(id_fail, text="Invalid Steam ID!", font = title_font)
            btn1 = ctk.CTkButton(id_fail, text="Ok.",height= 80, width= 80, command=id_fail.destroy)
            label.pack(padx=20, pady=20)
            btn1.pack(padx=20, pady=10)
            steam_id_input.delete(0, tk.END)

    steam_id_button = ctk.CTkButton(steam_id_window, text="Enter", command=get_steam_id)
    steam_id_input = ctk.CTkEntry(steam_id_window, font=("Arial", 20))
    steam_id_label.pack(padx=10, pady=10)
    steam_id_input.pack(padx=10, pady=10)
    steam_id_button.pack(padx=10, pady=10)
    steam_id_label2.pack(padx=10, pady=10)
    steam_id_label3.pack(padx=10, pady=10)
    canvas.pack(padx=10,pady=10)

## API ##
def get_owned_games():
    if not can_call_steam():
        return
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        "key": api_key,
        "steamid": steam_id,
        "include_appinfo": True,
        "include_played_free_games": True
    }

    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()

    games_list = data.get("response", {}).get("games", [])
    return games_list

games_list = get_owned_games()

def get_game_list():
    if not games_list:
        return[]
    
    game_list = []
    for game in games_list: 
        app_id = game.get("appid")
        
        try:
            url = "https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/"
            params = {
                "key": api_key,
                "appid": app_id,}
            
                
            r = requests.get(url, params = params)
            data = r.json()
            achievements = data.get("game", {}).get("availableGameStats", {}).get("achievements", [])
            
            if len(achievements) > 0:
                  game_list.append({
                    "name": game.get("name"),
                    "appid": game.get("appid"),
                    "icon_url": game.get("img_icon_url")
                })
        except: 
            pass
                    
    return game_list
        


## IF STATEMENTS ##
if not api_key:
    api_popup()

if os.path.exists("images/avatar.jpg") and display_name:
    update_avatar()
    def update_username():
        hello_user.configure(text=(f"Hello, {display_name}!"))
    update_username()

if api_key and not steam_id:
    steam_id_window()

## COMBO BOX ##
def refresh_game_combo():
    global games_list, game_list, game_names
    games_list = get_owned_games() or []
    game_list = get_game_list() or []
    game_names = [game["name"] for game in game_list]
    game_combo.configure(values=game_names)
    if game_names:
        game_combo.set(game_names[0])

game_list = get_game_list() or []
game_names = [game["name"] for game in game_list]

game_combo = ctk.CTkComboBox(
    home_frame,
    values=game_names,
    state="readonly",
    width = 300,
)
combo_loading_bar = ctk.CTkProgressBar(home_frame, mode = "indeterminate", indeterminate_speed = 2)  
imgicon_ref = None


def get_game_stats(event):
    combo_loading_bar.pack(padx=10,pady=10)
    combo_loading_bar.start()
    root.update_idletasks()
   
    thread = threading.Thread(target=fetch_game_data_thread)  
    thread.start()


def fetch_game_data_thread():   
    selected_name = game_combo.get()
    if not selected_name:
        root.after(0, lambda: combo_loading_bar.stop())
        root.after(0, lambda: combo_loading_bar.pack_forget())
        print("not selected name")
        return
    
    global imgicon_ref
    selected_name = game_combo.get()
    

    collected_progress = [] 
    root.after(0, achievement_loading_bar.grid(row = 3, column = 1, columnspan= 4, sticky ="n"))
    root.after(0, achievement_loading_bar.start())

    for game in game_list:
        if game["name"] == selected_name:
            appid = game["appid"]
            icon_url = game["icon_url"]
            icon = f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg"

            url_player = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/"
            params_player = {"key": api_key, "steamid": steam_id, "appid": appid}
            url_schema = "https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/"
            params_schema = {"key": api_key, "steamid": steam_id, "appid": appid}

            r_player = requests.get(url_player, params=params_player)
            r_player.raise_for_status()
            player_data = r_player.json()
            player_achievements = player_data.get("playerstats", {}).get("achievements", [])
            
            r_schema = requests.get(url_schema, params=params_schema)
            r_schema.raise_for_status()
            schema_data = r_schema.json()
            achievements_schema = schema_data.get("game", {}).get("availableGameStats", {}).get("achievements", [])

            global progress_list
            progress_list = []

            for ach_schema in achievements_schema:
                ach_name = ach_schema.get("name")
                display_name =  ach_schema.get("displayName")
                description = ach_schema.get("description")
                ach_icon_url = ach_schema.get("icon")

                player_ach = next((a for a in player_achievements if a["apiname"] == ach_name), None)
                achieved = player_ach["achieved"] if player_ach else None

                achievement_icon = None
                if ach_icon_url:
                    try:
                        icon_response = requests.get(ach_icon_url)
                        icon_response.raise_for_status()
                        achievement_icon = Image.open(BytesIO(icon_response.content))
                        achievement_icon = achievement_icon.resize((64, 64))
                        achievement_icon = ImageTk.PhotoImage(achievement_icon)
                    except:
                        achievement_icon = None
                
                progress_list.append({
                    "name": ach_name,
                    "display_name": display_name,
                    "description": description,
                    "achieved": achieved,
                    "icon": achievement_icon
                })

            
                
            response = requests.get(icon)
            response.raise_for_status()
            global imgicon
            imgicon = Image.open(BytesIO(response.content))
            imgicon = ImageTk.PhotoImage(imgicon)
            imgicon_ref = imgicon


            root.after(0, lambda: update_game_gui(selected_name))
            break


def update_game_gui(selected_name):
        icon_canvas.delete("all")
        icon_canvas.create_image(900//2,600//2, image=imgicon, anchor="center")
        game_label.configure(text=selected_name)

        combo_loading_bar.stop()
        combo_loading_bar.pack_forget()

        achievement_loading_bar.grid_forget()

        show_frame(game_frame)
        
        achievement_gui()
      


           


game_combo.configure(command=get_game_stats)
game_combo.pack(padx=10,pady=10)


game_label = ctk.CTkLabel(game_frame, font = title_font)
icon_canvas = ctk.CTkCanvas(game_frame, width=900, height=600, highlightthickness=0, background = game_frame.cget("fg_color")[1])
back_button = ctk.CTkButton(game_frame, text="Back", width = 80, height = 40, command = lambda: show_frame(home_frame))

def achievement_gui():
    for widget in game_frame.winfo_children():
        if widget not in [game_label, icon_canvas, back_button, achievement_loading_bar, settings_menu_game]:
            widget.destroy()
    
    for i, ach in enumerate(progress_list):

        row = i // 2 + 3
        col = (i % 2) * 2 + 1


        icon_canvas2 = ctk.CTkCanvas(game_frame, width=64, height=64, highlightthickness=0, background = game_frame.cget("fg_color")[1])
        icon_canvas2.configure(cursor="hand2")
        icon = progress_list[i]["icon"]
        icon_canvas2.delete("all")
        item = icon_canvas2.create_image(64//2,64//2, image=icon, anchor="center")
        icon_canvas2.grid(row=row, column=col, padx=10, pady=10)
        display_name_text2 = progress_list[i]["display_name"]
        icon_canvas2.tag_bind(item, "<Button-1>", lambda e, a = ach: ach_frame_func(a))
        if progress_list[i]["achieved"]:
            global achieved_text
            achieved_text = "Yes"
        else:
            achieved_text = "No"
        text = f"{display_name_text2}\nAchieved: {achieved_text}"
            
        label = ctk.CTkLabel(game_frame, text=text)
        label.grid(row=row, column=col + 1, sticky="nesw", padx=10, pady=10)
        
        
for i in (0, 2, 4, 5):
    game_frame.grid_columnconfigure(i, weight=2, uniform="a")
for i in (1,3):
    game_frame.grid_columnconfigure(i, weight=1, uniform="a")

for r in range(3):
    game_frame.grid_rowconfigure(r, weight=1)
icon_canvas_ach = ctk.CTkCanvas(achievement_frame, width=64, height=64, highlightthickness=0, background = game_frame.cget("fg_color")[1])
def ach_frame_func(ach):
    print(ach)
    if ach.get("description"):
        desctext=ach["description"] 
    else:
        desctext = "No description ):"

    titletext = ach["display_name"]
    if ach.get("achieved"):
        ach_text = "Yes"
    else:
        ach_text = "No"
    ach_frame_desc.configure(text=desctext)
    ach_frame_title.configure(text=titletext)
    ach_frame_achieved.configure(text=f"Achieved: {ach_text}")
    
    back_button_ach.place(relx=0,rely=0)
    show_frame(achievement_frame)
    icon = ach["icon"]
    icon_canvas_ach.delete("all")
    icon_canvas_ach.create_image(64//2,64//2, image=icon, anchor="center")
    icon_canvas_ach.pack(padx=10,pady=(400, 10))
    ach_frame_title.pack(padx=10,pady=10)
    ach_frame_desc.pack(padx=10,pady=10)
    settings_menu_ach.place(relx=1.0, rely=0, anchor="ne")

game_label.grid(row=0, columnspan ="6", sticky="n")
icon_canvas.grid(row=1, column=0, columnspan=6, padx=10, pady=(0, 10), sticky="n")
back_button.grid(row=0, column=0, sticky="nw")
settings_menu_game.place(relx=1.0, rely=0, anchor="ne")
root.mainloop()