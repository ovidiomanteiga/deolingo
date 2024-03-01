
import sys
from typing import Callable

import clingo
import clingo.ast as ast

from deolingo import _version
from deolingo.facade import rewrite_atoms
from deolingo._transformer import DeolingoTransformer


class DeolingoApplication(clingo.Application):
    """
    Application object as accepted by clingo.clingo_main().
    Rewrites the incoming deontic logic programs into deontic ASP programs and solves them.
    """
    def __init__(self):
        """
        Initializes the application setting the program name.
        See clingo.clingo_main().
        """
        self.program_name = "deolingo"
        self.version = _version.__version__
        self.translate_flag = clingo.Flag(False)

    def register_options(self, options: clingo.ApplicationOptions):
        """
        Registers the options for the application.
        """
        # add an option to translate the deontic logic program into an ASP program
        options.add_flag("deontic", "translate",
                         "Translate a deontic logic program into an ASP program", self.translate_flag)

    def print_model(self, model: clingo.Model, printer: Callable[[], None] = None):
        """
        Prints the atoms of the given model.
        This function is called for each model of the problem.
        """
        atoms = model.symbols(shown=True)
        rewritten_atoms = rewrite_atoms(atoms)
        print("Answer: " + str(rewritten_atoms))

    def main(self, prg, files):
        """
        Implements the incremental solving loop.
        This function implements the Application.main() function as required by
        clingo.clingo_main().
        """
        with ast.ProgramBuilder(prg) as b:
            files = [open(f) for f in files]
            if len(files) == 0:
                files.append(sys.stdin)
            inputs = [f.read() for f in files]
            transformer = DeolingoTransformer(b.add, translate=self.translate_flag.flag)
            transformer.transform(inputs)
        if self.translate_flag.flag:
            print(transformer.translated_program)
            return
        prg.configuration.solve.quiet = True
        prg.ground([("base", [])])
        prg.solve(on_model=None, async_=False)
