
from xclingo import XclingoControl

import re


def rewrite_program(program):
    lines = program.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith('%!'):
            lines[i] = re.sub(r"&(\w+){(.+)}", r"_deolingo_\1(\2)", line)
    return '\n'.join(lines)


class XDeolingoControl(XclingoControl):

    def __init__(self, n_solutions='1', n_explanations='1', auto_trace='none'):
        super().__init__(n_solutions=n_solutions, n_explanations=n_explanations, auto_trace=auto_trace)
        self.rewritten_program = ""

    def add(self, name, parameters, program):
        rewritten_program = rewrite_program(program)
        self.rewritten_program = rewritten_program
        #print("Rewritten program:" + rewritten_program)
        super().add(name, parameters, rewritten_program)
