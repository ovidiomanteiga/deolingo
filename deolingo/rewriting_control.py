
from typing import Sequence, Optional

from clingo import Logger

from deolingo._rewriting_translator import DeolingoRewritingTranslator
from deolingo.control import DeolingoControl


class DeolingoRewritingControl(DeolingoControl):
    """Extends the DeolingoControl class to use an optimized translator that rewrites the deontic atoms
     to their equivalents before solving the deontic logic program."""

    # <editor-fold desc="Initialization">

    def __init__(self, arguments: Sequence[str] = None, logger: Optional[Logger] = None,
                 message_limit: int = 20, grouped=False):
        super().__init__(arguments, logger, message_limit, grouped, optimize=True)

    # </editor-fold>
