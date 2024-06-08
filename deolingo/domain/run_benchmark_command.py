
from deolingo._benchmark import BenchmarkRunner
from deolingo.domain.use_case_command import UseCaseCommand


class RunBenchmarkCommand(UseCaseCommand):

    def __init__(self):
        super().__init__()
        self.runner = BenchmarkRunner()

    def execute(self):
        self.runner.run_benchmark()
        self.runner.print_results()
