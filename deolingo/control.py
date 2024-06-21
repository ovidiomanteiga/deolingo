
from typing import Sequence, Optional, overload, Union, Tuple, Callable

from clingo import Control, Logger, ast, Symbol, Model, StatisticsMap, SolveResult, SolveHandle

from deolingo._answer_set_rewriter import DeonticAnswerSetRewriter
from deolingo._rewriting_translator import DeolingoRewritingTranslator
from deolingo._translator import DeolingoTranslator


class DeolingoControl(Control):
    """Extends the clingo.Control class to translate and solve deontic logic programs."""

    # <editor-fold desc="Initialization">

    def __init__(self, arguments: Sequence[str] = None, logger: Optional[Logger] = None,
                 message_limit: int = 20, grouped=False, optimize=False):
        if arguments is None:
            arguments = []
        super().__init__(arguments, logger, message_limit)
        self._translate_control = Control(arguments, logger, message_limit)
        self._program_builder = ast.ProgramBuilder(self._translate_control)
        self._transformer = DeolingoRewritingTranslator(self._program_builder.add, translate=True, add_theory=False) if optimize \
            else DeolingoTranslator(self._program_builder.add, translate=True)
        self._rewriter = DeonticAnswerSetRewriter(grouped=grouped)
        self._add_deolingo_theory_and_deontic_rules()

    # </editor-fold>

    # <editor-fold desc="clingo.Control override">

    def _add2(self, name: str, parameters: Sequence[str], program: str) -> None:
        translated = self._transformer.transform_source(program)
        super()._add2(name, parameters, translated)

    def solve(
        self,
        assumptions: Sequence[Union[Tuple[Symbol, bool], int]] = [],
        on_model: Optional[Callable[[Model], Optional[bool]]] = None,
        on_unsat: Optional[Callable[[Sequence[int]], None]] = None,
        on_statistics: Optional[Callable[[StatisticsMap, StatisticsMap], None]] = None,
        on_finish: Optional[Callable[[SolveResult], None]] = None,
        on_core: Optional[Callable[[Sequence[int]], None]] = None,
        yield_: bool = False,
        async_: bool = False,
    ) -> Union[SolveHandle, SolveResult]:
        return super().solve(assumptions, self._on_model(on_model), on_unsat, on_statistics,
                             on_finish, on_core, yield_, async_)

    # </editor-fold>

    # <editor-fold desc="Private methods">

    def _add_deolingo_theory_and_deontic_rules(self):
        translated = self._transformer.transform_sources("")
        super()._add2("base", [], translated)

    def _on_model(self, on_model_callback):
        """On model callback wrapper that rewrites the atoms of the model."""
        if on_model_callback is None:
            return None
        return lambda model: on_model_callback(self._rewriter.rewrite_model(model))

    # </editor-fold>
