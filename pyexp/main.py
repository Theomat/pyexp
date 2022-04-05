import argparse

import pyexp.cmd_handler as cmd_handler

def main() -> None:

    parser = argparse.ArgumentParser(description="Python experiment manager.")


    # Experiment creation/deletion/suprression
    subparsers = parser.add_subparsers(help="sub-command help")



    parser_new = subparsers.add_parser("list", help="list all experiments")
    parser_new.set_defaults(func=cmd_handler.list_experiments)

    parser_new = subparsers.add_parser("show", help="show selected experiment")
    parser_new.add_argument("-n", "--name", type=str, help="name of the new experiment")
    parser_new.set_defaults(func=cmd_handler.show_experiment)



    parser_new = subparsers.add_parser("new", help="create a new experiment")
    parser_new.add_argument("name", type=str, help="name of the new experiment")
    parser_new.set_defaults(func=cmd_handler.new_experiment)

    parser_sel = subparsers.add_parser("sel", help="select specified experiment")
    parser_sel.add_argument("name", type=str, help="name of the experiment")
    parser_sel.set_defaults(func=cmd_handler.sel_experiment)

    parser_sel = subparsers.add_parser("del", help="delete specified experiment")
    parser_sel.add_argument("-n", "--name", type=str, help="name of the experiment")
    parser_sel.set_defaults(func=cmd_handler.del_experiment)



    parser_sel = subparsers.add_parser("add", help="add artifacts to the experiment")
    parser_sel.add_argument("paths", type=str, nargs="+", help="name of the experiment")
    parser_sel.set_defaults(func=cmd_handler.add_artifacts)

    parser_sel = subparsers.add_parser("rm", help="remove artifacts from the experiment")
    parser_sel.add_argument("paths", type=str, nargs="+", help="name of the experiment")
    parser_sel.set_defaults(func=cmd_handler.del_artifacts)

    parser_new = subparsers.add_parser("artifacts", help="show artifacts of the selected experiment")
    parser_new.add_argument("-n", "--name", type=str, help="name of the new experiment")
    parser_new.set_defaults(func=cmd_handler.show_artifacts)

    parser_new = subparsers.add_parser(
        "diff", help="show diff for artifacts of the selected experiment"
    )
    parser_new.add_argument("-n", "--name", type=str, help="name of the new experiment")
    parser_new.set_defaults(func=cmd_handler.show_diff)


    parser_sel = subparsers.add_parser("save", help="save a compressed version of the experiment")
    parser_sel.add_argument("-n", "--name", type=str, help="name of the experiment")
    parser_sel.add_argument("dst", type=str, help="destination file (extensions: zip, tar, tar.bz2, tar.gz, tar.xz)")
    parser_sel.set_defaults(func=cmd_handler.save_experiment)

    # parser_sel = subparsers.add_parser("load", help="load a compressed version of the experiment")
    # parser_sel.add_argument("-n", "--name", type=str, help="name of the experiment")
    # parser_sel.add_argument("src", type=str, help="source file")
    # parser_sel.set_defaults(func=cmd_handler.load_experiment)

    parser_sel = subparsers.add_parser("cmd", help="add a command to the experiment")
    parser_sel.add_argument("cmd", type=str, default="-", nargs="+", help="the command to add. - represents the last command. default: -")
    parser_sel.set_defaults(func=cmd_handler.add_command)


    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)


if __name__ == "__main__":
    main()