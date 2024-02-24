
from os import listdir
from os.path import isfile, join, isdir
from pathlib import Path

import clingo
import clingo.ast as ast

from _transformer import DeolingoTransformer
from _deontic_atom import DeonticAtoms, unprefix


def rewrite_atoms(atoms):
    """
    Rewrites the atom by removing the prefix '_deolingo_' if present.
    """
    rewritten_atoms = []
    for atom in atoms:
        is_negated = atom.name.startswith("-")
        atom_name = atom.name[1:] if is_negated else atom.name
        deontic_atom = DeonticAtoms.with_prefixed_name(atom_name)
        str_atom = str(atom)
        str_atom = str_atom[1:] if is_negated else str_atom
        if deontic_atom is None:
            rewritten_atoms.append(str_atom)
            continue
        if deontic_atom in [DeonticAtoms.DEONTIC, DeonticAtoms.HOLDS]:
            continue
        unprefixed = unprefix(str_atom)
        rewritten = unprefixed if not is_negated else "-" + unprefixed
        rewritten_atoms.append(rewritten)
    return rewritten_atoms


def rewrite_model(model: clingo.Model):
    """
    Rewrites the atoms of the given model by removing the prefix '_deolingo_' if present.
    """
    atoms = model.symbols(shown=True)
    rewritten_atoms = rewrite_atoms(atoms)
    return rewritten_atoms


def run_deolingo(prog, all_models=False):
    ctl = clingo.Control()
    if all_models:
        ctl.configuration.solve.models = 0
    with ast.ProgramBuilder(ctl) as b:
        transformer = DeolingoTransformer(b.add)
        transformer.transform([prog])
    ctl.ground([("base", [])])
    models = []
    def on_model(m):
        nonlocal models
        models += [rewrite_model(m)]
    solved = ctl.solve(on_model=on_model)
    for m in models:
        print("Answer: " + str(m))
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
