
from xclingo import XclingoControl

import re

import clingo.ast as ast

from deolingo._translator import DeolingoTranslator
from deolingo._deontic_atom import _DEOLINGO_ATOM_PREFIX


def rewrite_program(program):
    lines = program.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith('%!'):
            repl = _DEOLINGO_ATOM_PREFIX + r"\1(\2)"
            lines[i] = re.sub(r"&(\w+){(.+)}", repl, line)
    return '\n'.join(lines)


class XDeolingoControl(XclingoControl):

    def __init__(self, n_solutions='1', n_explanations='1', auto_trace='none', weak=False):
        super().__init__(n_solutions=n_solutions, n_explanations=n_explanations, auto_trace=auto_trace)
        self.rewritten_program = ""
        self._transformer = DeolingoTranslator(self._add_to_xcontrol, translate=True, add_theory=False, weak=weak)

    def add(self, name, parameters, program):
        translated_part = self._transformer.transform_source(program)
        self._add_translated(translated_part)

    def add_inputs(self, inputs):
        self._transformer.transform_sources(inputs)
        xprogram = self._transformer.translated_program
        self._add_translated(xprogram)

    def _add_translated(self, xprogram):
        rewritten_program = rewrite_program(xprogram)
        self.rewritten_program = rewritten_program
        super().add("base", [], rewritten_program)

    def _add_to_xcontrol(self, statement: ast.AST) -> None:
        pass
