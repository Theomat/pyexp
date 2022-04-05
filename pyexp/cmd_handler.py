import sys
import os
import subprocess
from types import SimpleNamespace
from typing import Optional
from colorama import Fore
from pyexp.experiment import Experiment, Command, Artifcat
import pyexp.manager as mgr


def check_experiment_selected() -> Experiment:
    exp = mgr.get_selected()
    if exp is None:
        print(
            Fore.LIGHTRED_EX
            + "No experiment was selected, please select one."
            + Fore.RESET,
            file=sys.stderr,
        )
        sys.exit(1)
    return exp


def check_experiment_by_name(name: str, presence: bool) -> Optional[Experiment]:
    result = mgr.get_experiment(name)
    found = result is not None
    if found != presence:
        if presence:
            print(
                Fore.LIGHTRED_EX
                + f'No experiment with the specified name"{name}" was found.'
                + Fore.RESET,
                file=sys.stderr,
            )
        else:
            print(
                Fore.LIGHTRED_EX
                + "An experiment with the specified name already exists."
                + Fore.RESET,
                file=sys.stderr,
            )
        sys.exit(2)
    return result


# ==========================================================
# SHOW EXPERIMENTS =========================================
# ==========================================================


def list_experiments(args: SimpleNamespace) -> None:
    selected = mgr.get_selected()
    for exp in mgr.list_experiments():
        if exp == selected:
            print("*" + Fore.LIGHTGREEN_EX, end=" ")
        print(exp.name + Fore.RESET)


def show_experiment(args: SimpleNamespace) -> None:
    name: str = args.name
    if name is not None:
        exp = check_experiment_by_name(name, True)
    else:
        exp = check_experiment_selected()
    print("experiment:", exp.short_representation())


# ==========================================================
# MANAGE EXPERIMENTS =======================================
# ==========================================================


def new_experiment(args: SimpleNamespace) -> None:
    name: str = args.name
    check_experiment_by_name(name, False)

    exp = Experiment(name)
    mgr.save_experiment(exp)
    mgr.select(exp)


def sel_experiment(args: SimpleNamespace) -> None:
    name: str = args.name
    exp = check_experiment_by_name(name, True)
    mgr.select(exp)


def del_experiment(args: SimpleNamespace) -> None:
    name: str = args.name
    if name is not None:
        exp = check_experiment_by_name(name, True)
    else:
        exp = check_experiment_selected()
    mgr.delete_experiment(exp)


# ==========================================================
# MANAGE ARTIFACTS =========================================
# ==========================================================


def add_artifacts(args: SimpleNamespace) -> None:
    exp = check_experiment_selected()
    for p in args.paths:
        if not os.path.exists(p):
            print(
                Fore.LIGHTRED_EX + f'No such file exists:"{p}".' + Fore.RESET,
                file=sys.stderr,
            )
            continue
        absp = os.path.abspath(p)
        found = False
        for a in exp.artifacts:
            if a.path == absp:
                found = True
                break
        if found:
            continue
        a = Artifcat(p, absp)
        exp.artifacts.append(a)
    mgr.save_experiment(exp)


def del_artifacts(args: SimpleNamespace) -> None:
    exp = check_experiment_selected()
    to_remove = []
    for p in args.paths:
        absp = os.path.abspath(p)
        for a in exp.artifacts:
            if a not in to_remove and (a.path == absp or a.name == p):
                to_remove.append(a)
    for a in to_remove:
        exp.artifacts.remove(a)
    mgr.save_experiment(exp)


def show_artifacts(args: SimpleNamespace) -> None:
    name: str = args.name
    if name is not None:
        exp = check_experiment_by_name(name, True)
    else:
        exp = check_experiment_selected()
    for art in exp.artifacts:
        print(art.description())


def show_diff(args: SimpleNamespace) -> None:
    name: str = args.name
    if name is not None:
        exp = check_experiment_by_name(name, True)
    else:
        exp = check_experiment_selected()
    for art in exp.artifacts:
        if art.get_level() > 0:
            print(art.description())


# ==========================================================
# SAVE & LOAD ==============================================
# ==========================================================


def save_experiment(args: SimpleNamespace) -> None:
    name: str = args.name
    if name is not None:
        exp = check_experiment_by_name(name, True)
    else:
        exp = check_experiment_selected()
    exp.save_compressed(args.dst)
    mgr.save_experiment(exp)


# ==========================================================
# MANAGE COMMANDS ==========================================
# ==========================================================


def add_command(args: SimpleNamespace) -> None:
    exp = check_experiment_selected()
    cmd = " ".join(args.cmd)
    output = subprocess.run(
        ["git log -n 1 | grep commit"], stdout=subprocess.PIPE, shell=True
    ).stdout.decode("utf-8")
    if "commit" in output:
        commit = output[len("commit") + 2 :]
        print(commit)
        exp.commands.append(Command(cmd, commit))
    else:
        exp.commands.append(Command(cmd))

    # mgr.save_experiment(exp)
