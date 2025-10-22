from typing import List
import os

unlocked_items = {}
item_id_to_name_map = {0: "Asher"}
loc_name_to_id_map = {"Asher - Win a game":0, "Asher - Get X Goals+Assists":1, "Asher - Get X Saves":2, "Asher - Get X KOs":3, "Asher - Get X Redirects":4, "Asher - Get X Orbs":5}
game_communication_path = os.path.expandvars(r"%localappdata%/OSAP") if "localappdata" in os.environ else os.path.expandvars(r"$Home/OSAP")
required_lp_count = 0
goals_plus_assists_x = 4
saves_x = 80
kos_x = 2
redirects_x = 100
orbs_x = 30

def check_character_unlocked(character: str) -> bool:
    return character in unlocked_items.keys()

def send_checks(data):
    completed_checks = []
    if data["Won"]:
        completed_checks.append(f"{data['Character']} - Win a game")
    if data["Goals"] + data["Assists"] > goals_plus_assists_x:
        completed_checks.append(f"{data['Character']} - Get X Goals+Assists")
    if data["Saves"] > saves_x:
        completed_checks.append(f"{data['Character']} - Get X Saves")
    if data["KOs"] > kos_x:
        completed_checks.append(f"{data['Character']} - Get X KOs")
    if data["Redirects"] > redirects_x:
        completed_checks.append(f"{data['Character']} - Get X Redirects")
    if data["Orbs"] > orbs_x:
        completed_checks.append(f"{data['Character']} - Get X Orbs")
    for i in range(len(completed_checks)):
        fname = "send"+str(loc_name_to_id_map[completed_checks[i]])
        with open(os.path.join(game_communication_path, fname), 'w') as f:
            f.close()

def check_victory():
    if "LP" in unlocked_items.keys():
        if unlocked_items["LP"] > required_lp_count:
            with open(os.path.join(game_communication_path, "victory"), "w") as f:
                f.close()

def get_unlocked_characters() -> List[str]:
    chars = []
    for key in unlocked_items.keys():
        if key != "LP":
            chars.append(key)

def update_items():
    if required_lp_count == 0:
        check_config()
    global unlocked_items
    unlocked_items = {}
    for root, dirs, files in os.walk(game_communication_path):
        for file in files:
            if file.startswith("AP"):
                with open(os.path.join(game_communication_path, file), 'r') as f:
                    item_id = int(f.readline())
                    print(item_id)
                    item_name = item_id_to_name_map[item_id]
                    if item_name in unlocked_items.keys():
                        unlocked_items[item_name]+=1
                    else:
                        unlocked_items[item_name] = 1
                    f.close()
    check_victory()

def check_config():
    global required_lp_count, kos_x, orbs_x, saves_x, redirects_x, goals_plus_assists_x
    with open(os.path.join(game_communication_path, "Required_LP.cfg"), "r") as f:
        required_lp_count = int(f.readline())
    with open(os.path.join(game_communication_path, "Required_KOs.cfg"), "r") as f:
        kos_x = int(f.readline())
    with open(os.path.join(game_communication_path, "Required_Orbs.cfg"), "r") as f:
        orbs_x = int(f.readline())
    with open(os.path.join(game_communication_path, "Required_Saves.cfg"), "r") as f:
        saves_x = int(f.readline())
    with open(os.path.join(game_communication_path, "Required_Redirects.cfg"), "r") as f:
        redirects_x = int(f.readline())
    with open(os.path.join(game_communication_path, "Required_GoalsAssists.cfg"), "r") as f:
        goals_plus_assists_x = int(f.readline())