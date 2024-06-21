
import sys
from typing import Callable

import clingo

import deolingo._version as deolingo_version
from deolingo._answer_set_rewriter import DeonticAnswerSetRewriter


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
        self._optimize_flag = clingo.Flag(False)
        self._weak_flag = clingo.Flag(False)
        self._generator = None
        self._llm = None
        self._n_explanations = 0
        self._temporal_flag = clingo.Flag(False)
        self._answer_set_rewriter = DeonticAnswerSetRewriter()
        self._xcontrol = None
        self._set_output_format_if_translating()

    # </editor-fold>

    # <editor-fold desc="clingo.Application override">

    def main(self, program, files):
        """This function implements the Application.main() function as required by clingo.clingo_main()."""
        if self._temporal_flag.flag:
            return self._solve_temporal_deontic_program(program, files)
        if self._benchmark_flag.flag:
            return self._run_benchmark()
        if self._generate_flag.flag:
            inputs = self._read_source_inputs_from_files(files)
            return self._generate_deontic_program(inputs)
        if self._explain_flag.flag:
            inputs = self._read_source_inputs_from_files(files)
            return self._explain_deontic_program(program, inputs)
        return self._solve_deontic_program(program, files)

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
        options.add_flag("deontic",
                         "optimize",
                         "Optimize the translation of the deontic logic program",
                         self._optimize_flag)
        options.add_flag("deontic",
                         "weak",
                         "Makes the deontic weak axiom a weak constraint to find inconsistencies",
                         self._weak_flag)

        def parser(value: str):
            from deolingo._generator import Generator
            try:
                self._generator = Generator(value)
                return True
            except ValueError:
                return False

        def llm_parser(value: str):
            self._llm = value
            return True

        def xparser(value: str):
            self._n_explanations = int(value)
            return True
        options.add("deontic", "generator", "Generative AI API to use in --generate mode",
                    parser, False, "gemini|gpt4all|openai|huggingfacehub")
        options.add("deontic", "llm", "Generative AI LLM model to be used in --generate mode",
                    llm_parser, False, "gemini-1.5-flash-latest")
        options.add("deontic", "explanations", "Number of explanations to generate",
                    xparser, False, "0..N")
        options.add_flag("deontic",
                         "temporal",
                         "Runs a temporal deontic logic program in Telingo",
                         self._temporal_flag)

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
        if "--translate" not in sys.argv and "--temporal" not in sys.argv:
            return
        for arg in sys.argv:
            if arg.startswith("--outf="):
                sys.argv.remove(arg)
        sys.argv.append("--outf=3")

    @staticmethod
    def _read_source_inputs_from_files(files):
        files = [open(file) for file in files]
        if len(files) == 0:
            files.append(sys.stdin)
        inputs = [file.read() for file in files]
        return inputs

    @staticmethod
    def _run_benchmark():
        from deolingo.domain.run_benchmark_command import RunBenchmarkCommand
        command = RunBenchmarkCommand()
        command.execute()

    def _generate_deontic_program(self, inputs):
        from deolingo.domain.generate_deontic_program_command import GenerateDeonticProgramCommand
        command = GenerateDeonticProgramCommand(inputs[0], generator_type=self._generator, llm=self._llm)
        command.execute()

    def _solve_deontic_program(self, program, files):
        from deolingo.domain.solve_deontic_program_command import SolveDeonticProgramCommand
        command = SolveDeonticProgramCommand(program, files, self._translate_flag.flag, self._optimize_flag.flag,
                                             self._weak_flag.flag)
        command.execute()

    def _explain_deontic_program(self, program, inputs, n_solutions='1'):
        from deolingo.domain.explain_deontic_program_command import ExplainDeonticProgramCommand
        n_solutions = int(program.configuration.solve.models)
        n_solutions_str = '1' if n_solutions < 0 else str(n_solutions)
        command = ExplainDeonticProgramCommand(inputs, n_solutions_str, self._n_explanations, self._translate_flag.flag,
                                               self._weak_flag.flag)
        command.execute()

    def _solve_temporal_deontic_program(self, program, files):
        from deolingo.domain.solve_temporal_deontic_program_command import SolveTemporalDeonticProgramCommand
        command = SolveTemporalDeonticProgramCommand(program, files, self._weak_flag.flag)
        command.execute()

    # </editor-fold>
