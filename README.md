# Pyexp

This is a command line tool to manage experiments and easily produce artifacts to save your experiments.
Example usage:

```bash
pyexp new my_exp
pyexp add myfile1.csv my_second_file.pt ../my_folder
pyexp save exp.bz2
pyexp rm myfile1.csv
```

What actually happens is we store the paths to the artifacts that you add to your experiment and only resolve them when saving a snapshot of the experiment.

We recommend you write a ``command.log`` with the shell history to reproduce the experiment.

<!-- toc -->

- [Usage](#usage)
- [Autocompletion](#autocompletion)

<!-- tocstop -->

## Usage

```
usage: pyexp [-h] [--version] {list,show,new,sel,del,add,rm,artifacts,diff,save,cmd} ...

Python experiment manager.

positional arguments:
  {list,show,new,sel,del,add,rm,artifacts,diff,save,cmd}
                        sub-command help
    list                list all experiments
    show                show selected experiment
    new                 create a new experiment
    sel                 select specified experiment
    del                 delete specified experiment
    add                 add artifacts to the experiment
    rm                  remove artifacts from the experiment
    artifacts           show artifacts of the selected experiment
    diff                show diff for artifacts of the selected experiment
    save                save a compressed version of the experiment
    cmd                 add a command to the experiment

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
```

## Autocompletion

The script ``autocomplete/_comp_pyexp.sh`` manages the autocompletion for you.
To install, you just need to make sure the script is sourced when you start your terminal.
