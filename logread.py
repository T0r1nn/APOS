from typing import Dict
import os

class LogWatcher:
    def __init__(self):
        self.file = os.path.expandvars("%localappdata%/OmegaStrikers/Saved/Logs/OmegaStrikers.log")
        self.most_recent_timestamp = self.getMostRecentTimestamp()
    def checkHasPlayedGame(self) -> bool:
        with open(self.file, "r") as file:
            lines = file.readlines()
            lines.reverse()
            for line in lines:
                if "TeamThatWonMatch" in line and self.getTimestampFromLine(line) > self.most_recent_timestamp:
                    return True
            return False
    def getLastCharPlayed(self) -> str:
        with open(self.file, "r") as file:
            lines = file.readlines()
            lines.reverse()
            for line in lines:
                if "VOD_" in line and "_CharacterIntro" in line:
                    return line.split("VOD_")[1].split("_CharacterIntro")[0]
            return ""
    def getLastGameInfo(self) -> Dict[str, str|int]:
        character = self.getLastCharPlayed()
        with open(self.file, "r") as file:
            last_char = ""
            last_score = ""
            victor = ""
            stats_dict = {"Character": character, "Team": "", "Score": 0}
            lines = file.readlines()
            lines.reverse()
            for line in lines:
                if "NewTeam = EAssignedTeam::" in line:
                    stats_dict["Team"] = line.split("NewTeam = EAssignedTeam::")[1].strip()
                    break
                if "TeamTwo's NumPointsThisSet changed from" in line and " to 0" not in line:
                    last_score = "TeamTwo"
                    if last_char != "":
                        if last_char == character and last_score == stats_dict["Team"]:
                            stats_dict["Score"] += 1
                        last_score = ""
                        last_char = ""
                if "TeamOne's NumPointsThisSet changed from" in line and " to 0" not in line:
                    last_score = "TeamOne"
                    if last_char != "":
                        if last_char == character and last_score == stats_dict["Team"]:
                            stats_dict["Score"] += 1
                        last_score = ""
                        last_char = ""
                if "TeamThatWonMatch" in line:
                    if "TeamOne" in line:
                        victor = "TeamOne"
                    if "TeamTwo" in line:
                        victor = "TeamTwo"
                if "VOD_" in line and "_GoalScore" in line:
                    name = line.split("VOD_")[1].split("_GoalScore")[0]
                    if last_score != "":
                        if last_char == character and last_score == stats_dict["Team"]:
                            stats_dict["Score"] += 1
                        last_score = ""
                        last_char = ""
                    else:
                        last_char = name
            stats_dict["Won"] = stats_dict["Team"] == victor
            return stats_dict
    def getTimestampFromLine(self, line: str) -> int:
        timestamp = line.split("]")[0][1:]
        [date, time] = timestamp.split("-")
        [year, month, day] = date.split(".")
        [hour, minute, seconds] = time.split(".")
        [seconds, ms] = seconds.split(":")
        return int(ms) + int(seconds)*100 + int(minute)*6000 + int(hour) * 3600000 + int(day) * 86400000 + int(month) * 31 + int(year) * 366
    def getMostRecentTimestamp(self) -> int:
        with open(self.file, "r") as file:
            recent_line = file.readlines()[-1]
            return self.getTimestampFromLine(recent_line)