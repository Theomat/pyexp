import pickle
import os
import shutil
import tempfile
from colorama import Fore
from dataclasses import dataclass, field
from datetime import datetime
from time import time
from typing import List



def date_since_str(ltime: float) -> str:
    if ltime < 0:
        return "never"
    diff = time() - ltime
    if diff < 60:
        return "a few seconds ago"
    if diff < 3600:
        min = round(diff / 60)
        return f"{min} minute{'s' if min > 1 else ''} ago"
    if diff < 3600 * 24:
        min = round(diff / 3600)
        return f"{min} hour{'s' if min > 1 else ''} ago"
    if diff < 3600 * 24 * 100:
        min = round(diff / 3600)
        return f"{min} day{'s' if min > 1 else ''} ago"
    return datetime.fromtimestamp(ltime).date()

@dataclass
class Artifcat:
    name: str
    path: str
    last_saved: float = field(default=-1)


    def description(self) -> str:
        last = date_since_str(self.last_saved)
        color = ""
        logo = " "
        msg = "last saved: "
        if not os.path.exists(self.path):
            logo = "-"
            color = Fore.RED
            msg = "file is missing, last saved:"
        else:
            if self.last_saved < 0:
                logo = "+"
                color = Fore.LIGHTGREEN_EX
            else:
                lastm = os.stat(self.path).st_mtime
                if lastm > self.last_saved:
                    logo = "~"
                    color = Fore.LIGHTYELLOW_EX
                    msg = "file has changed since "

        s = color + logo + f" {self.name} ({msg}{last}){Fore.RESET}\n\t{self.path}"
        return s

    def get_level(self) -> int:
        if not os.path.exists(self.path):
            return 1
        else:
            if self.last_saved < 0:
                return 2
            else:
                lastm = os.stat(self.path).st_mtime
                if lastm > self.last_saved:
                    return 3
        return 0

@dataclass
class Command:
    cmdline: str
    githead: str = field(default="none")


@dataclass
class Experiment:
    name: str
    artifacts: List[Artifcat] = field(default_factory=lambda: [])
    commands: List[Command] = field(default_factory=lambda: [])
    last_saved: float = field(default=-1)


    def write_description_file(self, path: str) -> None:
        with open(os.path.join(path, self.name), "wb") as fd:
            pickle.dump({"name": self.name,
                        "artifacts": self.artifacts,
                        "commands": self.commands,
                        "last_saved": self.last_saved}, fd)

    def write_cmd_log(self, path: str) -> None:
        with open(path, "w")  as fd:
            fd.writelines(f"[{cmd.githead}]" + cmd.cmdline for cmd in self.commands)

    @staticmethod
    def from_description_file(path: str) -> 'Experiment':
        with open(path, "rb") as fd:
            d = pickle.load(fd)
        return Experiment(**d)


    def short_representation(self) -> str:
        nart = len(self.artifacts)
        ncmd = len(self.commands)
        levels = set(a.get_level() for a in self.artifacts)
        color = Fore.RESET
        if len(levels) >= 1:
            levels = [l for l in levels if l > 0]
            level = 3 if len(levels) > 1 else (levels[0] if len(levels) == 1 else 0)
            color = [Fore.RESET, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX][level]
        s = f"{self.name} (last saved: {date_since_str(self.last_saved)}, {color}{nart} artifact{'s' if nart > 1 else ''}{Fore.RESET}, {ncmd} command{'s' if ncmd > 1 else ''})"
        return s

    def save_compressed(self, dst: str) -> None:
        extension = dst[dst.rindex(".") + 1:]
        with tempfile.TemporaryDirectory() as tmpdir:
            for artifact in self.artifacts:
                shutil.copyfile(artifact.path, tmpdir + "/" + artifact.name)
            self.write_description_file(tmpdir)
            self.write_cmd_log(tmpdir + "/experiment_commangs.log")
            file_name = shutil.make_archive(self.name, extension, tmpdir)
        shutil.move(file_name, dst)
        self.last_saved = time()
        for a in self.artifacts:
            a.last_saved = time()