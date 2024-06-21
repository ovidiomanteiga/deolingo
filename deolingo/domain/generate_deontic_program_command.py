
from deolingo._generator import DeonticProgramGenerator
from deolingo.domain.use_case_command import UseCaseCommand


class GenerateDeonticProgramCommand(UseCaseCommand):

    def __init__(self, input_text, generator_type=None, llm=None):
        super().__init__()
        self.input_text = input_text
        self.generator = DeonticProgramGenerator(generator=generator_type, llm=llm)

    def execute(self, params=None):
        program = self.generator.generate_program(self.input_text)
        print(program)

