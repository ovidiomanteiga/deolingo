
import time

import prettytable.prettytable

from deolingo.examples import ExampleReader

from deolingo.control import DeolingoControl
from deolingo.rewriting_control import DeolingoRewritingControl


class BenchmarkRunner:
    """
    Class that runs benchmarks for the Deolingo system using all the examples in the examples folder.
    It measures the time it takes to translate the deontic logic programs into ASP programs and to solve them.
    It also measures the Clingo grounding size in terms of the number of ground atoms and the number of ground rules.
    """

    def __init__(self):
        self.solvers = [DeolingoControl, DeolingoRewritingControl]
        self._example_reader = ExampleReader()
        table = prettytable.PrettyTable()
        table.field_names = ["Example", "Solver", "Time (s)", "CPU Time (s)", "Rules", "Atoms"]
        table.align["Example"] = "l"
        table.align["Solver"] = "l"
        table.align["Time (s)"] = "r"
        table.align["CPU Time (s)"] = "r"
        table.align["Rules"] = "r"
        table.align["Atoms"] = "r"
        self._table = table

    def run_benchmark(self):
        """Run the benchmark with all examples and print the results."""
        examples = self._example_reader.read_examples()
        for example in examples:
            if example.name.startswith("telingo/"):
                continue
            is_first_solver = True
            for solver in self.solvers:
                print(f"Running benchmark for {example.name} with {solver.__name__}...")
                self.run_benchmark_for_example(example, solver, is_first_solver)
                is_first_solver = False
            if len(self.solvers) > 1:
                self._table.add_row(["" for _ in range(len(self._table.field_names))])

    def print_results(self):
        """Print the results of the benchmark."""
        print(self._table)

    def run_benchmark_for_example(self, example, solver, is_first_solver):
        """Run the benchmark for the given example and print the results."""
        program = solver()
        if hasattr(program, "configuration"):
            program.configuration.solve.statistics = 2
            program.configuration.solve.models = 0
        program.add("base", [], example.contents)
        program.ground([("base", [])])
        start = time.time()
        program.solve()
        end = time.time()
        print(f"Time: {end - start:.2f} seconds")
        stats = program.statistics
        self._table.add_row([
            example.name if is_first_solver else "",
            solver.__name__,
            f"{end - start:.2f}",
            f"{stats['summary']['times']['cpu']:.2f}",
            int(stats['problem']['lp']['rules']),
            int(stats['problem']['lp']['atoms'])
        ])
