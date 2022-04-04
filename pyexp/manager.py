import os
from typing import List, Optional
from pyexp.experiment import Experiment

PATH = os.environ['HOME'] + "/.pyexp/"


def list_experiments() -> List[Experiment]:
    EXPERIMENTS = []
    if not os.path.exists(PATH):
        os.makedirs(PATH, exist_ok=True)

    for entry in os.scandir(PATH):
        if entry.is_file(follow_symlinks=False) and entry.name != "_selected":
            EXPERIMENTS.append(Experiment.from_description_file(entry.path))
    return EXPERIMENTS

def save_experiment(exp: Experiment) -> None:
    if not os.path.exists(PATH):
        os.makedirs(PATH, exist_ok=True)
    exp.write_description_file(PATH)


def get_experiment(name: str) -> Optional[Experiment]:
    desc_file = os.path.join(PATH, name)
    if os.path.exists(desc_file):
        return Experiment.from_description_file(desc_file)
    return None

def delete_experiment(exp: Experiment) -> None:
    desc_file = os.path.join(PATH, exp.name)
    if get_selected() == exp:
        select(None)
    if os.path.exists(desc_file):
        os.remove(desc_file)

def select(exp: Optional[Experiment]) -> None:
    global selected
    selected = exp
    with open(os.path.join(PATH, "_selected"), "w") as fd:
        fd.write("" if selected is None else selected.name)

def get_selected() -> Optional[Experiment]:
    file = os.path.join(PATH, "_selected")
    if not os.path.exists(file):
        return None
    with open(file, "r") as fd:
        name = fd.readline()
    if len(name) == 0:
        return None
    return get_experiment(name)
