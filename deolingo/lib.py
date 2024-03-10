
from os import listdir
from os.path import isfile, join, isdir
from pathlib import Path

from deolingo.control import DeolingoControl


def solve(prog, all_models=False):
    ctl = DeolingoControl()
    if all_models:
        ctl.configuration.solve.models = 0
    ctl.add(prog)
    ctl.ground()
    models = []

    def on_model(model):
        nonlocal models
        models.append(model)
        return model
    ctl.solve(on_model=on_model)
    return models


def read_examples():
    """
    Returns a list of all examples reading from folders in /examples
    """
    examples_folder = Path(__file__).parent / "examples"
    folders = [f for f in listdir(examples_folder) if isdir(join(examples_folder, f))]
    examples_files = []
    for folder in folders:
        folder = examples_folder / folder
        examples_files += [folder / f for f in listdir(folder) if isfile(join(folder, f)) and f.endswith(".lp")]

    def name(f):
        return f.parent.name + "/" + f.name
    files = [(name(f), open(f)) for f in examples_files]
    examples = [(f[0], f[1].read()) for f in files]
    return examples


def read_example(example):
    """
    Returns a list of all examples reading from folders in /examples
    """
    examples_folder = Path(__file__).parent / "examples"
    if isfile(join(examples_folder, example)) and example.endswith(".lp"):
        example_file = examples_folder / example
    else:
        return None

    def name(f):
        return f.parent.name + "/" + f.name
    file = (name(example_file), open(example_file))
    examples = (file[0], file[1].read())
    return examples
