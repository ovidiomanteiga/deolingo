
import sys
from typing import Callable

import clingo
import clingo.ast as ast

import deolingo._version as deolingo_version
from deolingo._answer_set_rewriter import DeonticAnswerSetRewriter
from deolingo._translator import DeolingoTranslator
from deolingo.xcontrol import XDeolingoControl


class DeolingoApplication(clingo.Application):
    """
    Application object as accepted by clingo.clingo_main().
    Rewrites the incoming deontic logic programs into deontic ASP programs and solves them.
    """

    # <editor-fold desc="Initialization">

    def __init__(self):
        """
        Initializes the application setting the program name. See clingo.clingo_main().
        """
        self.program_name = "deolingo"
        self.version = deolingo_version.__version__
        self._translate_flag = clingo.Flag(False)
        self._ungrouped_flag = clingo.Flag(False)
        self._explain_flag = clingo.Flag(False)
        self._benchmark_flag = clingo.Flag(False)
        self._generate_flag = clingo.Flag(False)
        self._answer_set_rewriter = DeonticAnswerSetRewriter()
        self._xcontrol = None
        self._set_output_format_if_translating()

    # </editor-fold>

    # <editor-fold desc="clingo.Application override">

    def main(self, program, files):
        """This function implements the Application.main() function as required by clingo.clingo_main()."""
        if self._benchmark_flag.flag:
            return self._run_benchmark()
        if self._generate_flag.flag:
            inputs = self._read_source_inputs_from_files(files)
            return self._generate_deontic_program(inputs)
        if self._explain_flag.flag:
            inputs = self._read_source_inputs_from_files(files)
            return self._run_with_xcontrol(inputs)
        else:
            self._run_with_clingo_control(program, files)

    def register_options(self, options: clingo.ApplicationOptions):
        """Registers the options for the application."""
        options.add_flag("deontic",
                         "translate",
                         "Translate a deontic logic program into an ASP program",
                         self._translate_flag)
        options.add_flag("deontic",
                         "ungrouped",
                         "Do not group the answer sets deontic worlds",
                         self._ungrouped_flag)
        options.add_flag("deontic",
                         "explain",
                         "Use Xclingo to generate explanations",
                         self._explain_flag)
        options.add_flag("deontic",
                         "benchmark",
                         "Run benchmark with all examples and print the results",
                         self._benchmark_flag)
        options.add_flag("deontic",
                         "generate",
                         "Generates a deontic logic program from a given natural language input",
                         self._generate_flag)

    def print_model(self, model: clingo.Model, printer: Callable[[], None] = None):
        """Prints the atoms of the given model.
        This function is called for each model of the problem."""
        atoms = model.symbols(shown=True)
        grouped = not self._ungrouped_flag.flag
        self._answer_set_rewriter._grouped = grouped
        rewritten_facts, obligations, prohibitions = self._answer_set_rewriter.rewrite_atoms(atoms)
        if grouped:
            print(f'FACTS: {", ".join(rewritten_facts)}')
            print(f'OBLIGATIONS: {", ".join(obligations)}')
            print(f'PROHIBITIONS: {", ".join(prohibitions)}')
            print()
        else:
            print(", ".join(rewritten_facts))

    # </editor-fold>

    # <editor-fold desc="Private methods">

    @staticmethod
    def _set_output_format_if_translating():
        if "--translate" not in sys.argv:
            return
        for arg in sys.argv:
            if arg.startswith("--outf="):
                sys.argv.remove(arg)
        sys.argv.append("--outf=3")

    @staticmethod
    def _run_benchmark():
        from deolingo._benchmark import BenchmarkRunner
        runner = BenchmarkRunner()
        runner.run_benchmark()
        runner.print_results()

    def _generate_deontic_program(self, inputs):
        from deolingo._generator import DeonticProgramGenerator, Generator
        generator = DeonticProgramGenerator(generator=Generator.GEMINI)
        program = generator.generate_program(inputs[0])
        print(program)

    @staticmethod
    def _read_source_inputs_from_files(files):
        files = [open(file) for file in files]
        if len(files) == 0:
            files.append(sys.stdin)
        inputs = [file.read() for file in files]
        return inputs

    def _run_with_clingo_control(self, program, files):
        with ast.ProgramBuilder(program) as builder:
            transformer = DeolingoTranslator(builder.add, translate=self._translate_flag.flag)
            transformer.transform_sources(None, files)
        if self._translate_flag.flag:
            print(transformer.translated_program)
            return
        program.configuration.solve.quiet = True
        program.ground([("base", [])])
        program.solve(on_model=None, async_=False)

    def _run_with_xcontrol(self, inputs):
        self._xcontrol = XDeolingoControl(n_solutions='0', n_explanations='0', auto_trace='none')
        self._xcontrol.add_inputs(inputs)
        if self._translate_flag.flag:
            print(self._xcontrol.rewritten_program)
            return
        self._xcontrol.ground([("base", [])])
        self._print_text_explanations()

    def _print_text_explanations(self):
        n = 0
        for answer in self._xcontrol.explain():
            n += 1
            print(f'Answer {n}')
            for expl in answer:
                print(expl.ascii_tree())

    # </editor-fold>
