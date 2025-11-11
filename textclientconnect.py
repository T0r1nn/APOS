from typing import List
import os

unlocked_items = {}
item_id_to_name_map = {1869590: 'Juliette', 1869591: 'Estelle', 1869592: 'Dubu', 1869593: 'Luna', 1869594: 'Juno', 1869595: 'Asher', 1869596: 'Kai', 1869597: 'Era', 1869598: 'X', 1869599: 'Ai.Mi', 1869600: 'Finii', 1869601: 'Zentaro', 1869602: 'Octavia', 1869603: 'Vyce', 1869604: 'Mako', 1869605: 'Rune', 1869606: "Drek_ar", 1869607: 'Atlas', 1869608: 'Nao', 1869609: 'Rasmus', 1869610: 'Kazan', 1869611: 'LP', 1869674: 'LP'}
loc_name_to_id_map = {'Juliette - Get X Goals+Assists': 1869590, 'Juliette - Get X KOs': 1869591, 'Juliette - Get X Saves': 1869592, 'Juliette - Get X Redirects': 1869593, 'Juliette - Get X Orbs': 1869594, 'Juliette - Get X Wins': 1869595, 'Estelle - Get X Goals+Assists': 1869596, 'Estelle - Get X KOs': 1869597, 'Estelle - Get X Saves': 1869598, 'Estelle - Get X Redirects': 1869599, 'Estelle - Get X Orbs': 1869600, 'Estelle - Get X Wins': 1869601, 'Dubu - Get X Goals+Assists': 1869602, 'Dubu - Get X KOs': 1869603, 'Dubu - Get X Saves': 1869604, 'Dubu - Get X Redirects': 1869605, 'Dubu - Get X Orbs': 1869606, 'Dubu - Get X Wins': 1869607, 'Luna - Get X Goals+Assists': 1869608, 'Luna - Get X KOs': 1869609, 'Luna - Get X Saves': 1869610, 'Luna - Get X Redirects': 1869611, 'Luna - Get X Orbs': 1869612, 'Luna - Get X Wins': 1869613, 'Juno - Get X Goals+Assists': 1869614, 'Juno - Get X KOs': 1869615, 'Juno - Get X Saves': 1869616, 'Juno - Get X Redirects': 1869617, 'Juno - Get X Orbs': 1869618, 'Juno - Get X Wins': 1869619, 'Asher - Get X Goals+Assists': 1869620, 'Asher - Get X KOs': 1869621, 'Asher - Get X Saves': 1869622, 'Asher - Get X Redirects': 1869623, 'Asher - Get X Orbs': 1869624, 'Asher - Get X Wins': 1869625, 'Kai - Get X Goals+Assists': 1869626, 'Kai - Get X KOs': 1869627, 'Kai - Get X Saves': 1869628, 'Kai - Get X Redirects': 1869629, 'Kai - Get X Orbs': 1869630, 'Kai - Get X Wins': 1869631, 'Era - Get X Goals+Assists': 1869632, 'Era - Get X KOs': 1869633, 'Era - Get X Saves': 1869634, 'Era - Get X Redirects': 1869635, 'Era - Get X Orbs': 1869636, 'Era - Get X Wins': 1869637, 'X - Get X Goals+Assists': 1869638, 'X - Get X KOs': 1869639, 'X - Get X Saves': 1869640, 'X - Get X Redirects': 1869641, 'X - Get X Orbs': 1869642, 'X - Get X Wins': 1869643, 'Ai.Mi - Get X Goals+Assists': 1869644, 'Ai.Mi - Get X KOs': 1869645, 'Ai.Mi - Get X Saves': 1869646, 'Ai.Mi - Get X Redirects': 1869647, 'Ai.Mi - Get X Orbs': 1869648, 'Ai.Mi - Get X Wins': 1869649, 'Finii - Get X Goals+Assists': 1869650, 'Finii - Get X KOs': 1869651, 'Finii - Get X Saves': 1869652, 'Finii - Get X Redirects': 1869653, 'Finii - Get X Orbs': 1869654, 'Finii - Get X Wins': 1869655, 'Zentaro - Get X Goals+Assists': 1869656, 'Zentaro - Get X KOs': 1869657, 'Zentaro - Get X Saves': 1869658, 'Zentaro - Get X Redirects': 1869659, 'Zentaro - Get X Orbs': 1869660, 'Zentaro - Get X Wins': 1869661, 'Octavia - Get X Goals+Assists': 1869662, 'Octavia - Get X KOs': 1869663, 'Octavia - Get X Saves': 1869664, 'Octavia - Get X Redirects': 1869665, 'Octavia - Get X Orbs': 1869666, 'Octavia - Get X Wins': 1869667, 'Vyce - Get X Goals+Assists': 1869668, 'Vyce - Get X KOs': 1869669, 'Vyce - Get X Saves': 1869670, 'Vyce - Get X Redirects': 1869671, 'Vyce - Get X Orbs': 1869672, 'Vyce - Get X Wins': 1869673, 'Mako - Get X Goals+Assists': 1869674, 'Mako - Get X KOs': 1869675, 'Mako - Get X Saves': 1869676, 'Mako - Get X Redirects': 1869677, 'Mako - Get X Orbs': 1869678, 'Mako - Get X Wins': 1869679, 'Rune - Get X Goals+Assists': 1869680, 'Rune - Get X KOs': 1869681, 'Rune - Get X Saves': 1869682, 'Rune - Get X Redirects': 1869683, 'Rune - Get X Orbs': 1869684, 'Rune - Get X Wins': 1869685, "Drek_ar - Get X Goals+Assists": 1869686, "Drek_ar - Get X KOs": 1869687, "Drek_ar - Get X Saves": 1869688, "Drek_ar - Get X Redirects": 1869689, "Drek_ar - Get X Orbs": 1869690, "Drek_ar - Get X Wins": 1869691, 'Atlas - Get X Goals+Assists': 1869692, 'Atlas - Get X KOs': 1869693, 'Atlas - Get X Saves': 1869694, 'Atlas - Get X Redirects': 1869695, 'Atlas - Get X Orbs': 1869696, 'Atlas - Get X Wins': 1869697, 'Nao - Get X Goals+Assists': 1869698, 'Nao - Get X KOs': 1869699, 'Nao - Get X Saves': 1869700, 'Nao - Get X Redirects': 1869701, 'Nao - Get X Orbs': 1869702, 'Nao - Get X Wins': 1869703, 'Rasmus - Get X Goals+Assists': 1869704, 'Rasmus - Get X KOs': 1869705, 'Rasmus - Get X Saves': 1869706, 'Rasmus - Get X Redirects': 1869707, 'Rasmus - Get X Orbs': 1869708, 'Rasmus - Get X Wins': 1869709, 'Kazan - Get X Goals+Assists': 1869710, 'Kazan - Get X KOs': 1869711, 'Kazan - Get X Saves': 1869712, 'Kazan - Get X Redirects': 1869713, 'Kazan - Get X Orbs': 1869714, 'Kazan - Get X Wins': 1869715}
game_communication_path = os.path.expandvars(r"%localappdata%/OSAP") if "localappdata" in os.environ else os.path.expandvars(r"$Home/OSAP")
required_lp_count = 0
goals_plus_assists_x = 4
saves_x = 80
kos_x = 2
redirects_x = 100
orbs_x = 30
prev_lp = 0

def check_character_unlocked(character: str) -> bool:
    return character in unlocked_items.keys()

def send_checks(data):
    completed_checks = []
    if data["Won"]:
        completed_checks.append(f"{data['Character']} - Get X Wins")
    if data["Goals"] + data["Assists"] >= goals_plus_assists_x:
        completed_checks.append(f"{data['Character']} - Get X Goals+Assists")
    if data["Saves"] >= saves_x:
        completed_checks.append(f"{data['Character']} - Get X Saves")
    if data["KOs"] >= kos_x:
        completed_checks.append(f"{data['Character']} - Get X KOs")
    if data["Redirects"] >= redirects_x:
        completed_checks.append(f"{data['Character']} - Get X Redirects")
    if data["Orbs"] >= orbs_x:
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
    return chars

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
                    item_name = item_id_to_name_map[item_id]
                    if item_name in unlocked_items.keys():
                        unlocked_items[item_name]+=1
                    else:
                        unlocked_items[item_name] = 1
                    f.close()
    check_victory()
    if(unlocked_items['LP'] > prev_lp):
        prev_lp = unlocked_items['LP']
        print(f"Gotten {prev_lp} lp out of {required_lp_count} needed for victory")

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