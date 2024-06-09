
from clingo.ast import parse_string, parse_files

from deolingo._ast_transformer import DeonticASTTransformer, MultipleRuleException

from deolingo._deontic_atom import *
from deolingo._deolingo_theory import _DEOLINGO_THEORY
from deolingo._deontic_rules import DeonticRules


class DeolingoTranslator:

    # <editor-fold desc="Initialization">

    def __init__(self, add_to_program_callback, transformer=None, translate=False, add_theory=True,
                 add_deontic_rules=True, temporal=False, weak=False):
        self.deontic_transformer = transformer if transformer is not None else DeonticASTTransformer(translate)
        self._add_to_program_callback = add_to_program_callback
        self.translate = translate
        self.translated_program = ""
        self._translated_part = ""
        self._deolingo_theory_added = False
        self._deontic_rules_added = False
        self._add_theory = add_theory
        self._add_deontic_rules = add_deontic_rules
        self.temporal = temporal
        self.weak = weak

    # </editor-fold>

    # <editor-fold desc="Public methods">

    def transform_source(self, source):
        """Transforms the source input and adds it to the program."""
        return self.transform_sources([source])

    def transform_sources(self, inputs, files=None):
        """Transforms the source inputs and adds them to the program."""
        self._translated_part = ""
        self._add_deolingo_theory()
        self._transform_and_add_source_inputs(inputs, files)
        self._add_program_statement()
        self._add_common_deontic_rules()
        self._add_rules_for_each_deontic_atom()
        part = self._translated_part
        self._translated_part = ""
        return part

    # </editor-fold>

    # <editor-fold desc="Private methods">

    def _add_to_translation(self, statement):
        """Add the statement to the translated program if necessary."""
        if self.translate:
            statement_str = str(statement)
            self.translated_program += statement_str
            self._translated_part += statement_str

    def _add_string_to_program(self, statement, add_to_translation=True):
        """Add the statement to the program and to the translated program if necessary."""
        parse_string(statement, self._add_to_program_callback)
        if add_to_translation:
            self._add_to_translation(statement)

    def _add_deolingo_theory(self):
        """Add the Deolingo theory to the program if it has not been added yet."""
        if self._add_theory and not self._deolingo_theory_added:
            self._add_string_to_program(_DEOLINGO_THEORY, add_to_translation=self.translate)
            self._deolingo_theory_added = True

    def _transform_and_add_to_program(self, statement):
        """Transform the source statement and add it to the program."""
        try:
            self.deontic_transformer.translated_program = ""
            transformed_statement = self.deontic_transformer(statement)
            if str(transformed_statement) == "#program base.":
                return
            if self.deontic_transformer.translated_program == "":
                self._add_to_translation("\n" + str(transformed_statement))
            else:
                self._add_to_translation(self.deontic_transformer.translated_program)
            self._add_to_program_callback(transformed_statement)
        except MultipleRuleException as multiple_rule:
            self._add_multiple_rules_to_program(multiple_rule)

    def _add_multiple_rules_to_program(self, multiple_rule):
        if multiple_rule.line is not None:
            self.translated_program += f"\n% Source line: {multiple_rule.line.begin.line}\n"
        for rule in multiple_rule.rules:
            self._add_to_translation(str(rule) + "\n")
            self._add_to_program_callback(rule)

    def _transform_and_add_source_inputs(self, inputs, files=None):
        """Parses the source inputs, transforms them and adds them to the program."""
        if files is not None:
            parse_files(files, self._transform_and_add_to_program)
            return
        for source_input in inputs:
            parse_string(source_input, self._transform_and_add_to_program)

    def _add_rules_for_each_deontic_atom(self):
        """Add the reified truth rules for each deontic atom."""
        if not self._add_deontic_rules:
            return
        for deontic_atom in self.deontic_transformer.deontic_atoms:
            holds_positive = holds(deontic_atom)
            holds_negative = holds(f"-{deontic_atom}")
            rules = [
                f"\n% Deontic atom rules for '{deontic_atom}'",
                f"{holds_positive} :- {deontic_atom}.",
                f"{holds_negative} :- -{deontic_atom}.",
                f"{deontic_atom} :- {holds_positive}.",
                f"-{deontic_atom} :- {holds_negative}."
            ]
            rules_as_string = "\n".join(rules) + '\n'
            self._add_string_to_program(rules_as_string)

    def _add_program_statement(self):
        if self._add_deontic_rules and self.translate:
            self._transform_and_add_source_inputs(["#program base."])
        if self._add_deontic_rules and self.temporal:
            self._transform_and_add_source_inputs(["#program always."])

    def _add_common_deontic_rules(self):
        """Add the common deontic rules to the program if not added already."""
        if not self._add_deontic_rules or self._deontic_rules_added:
            return
        deontic_rules_as_string = DeonticRules.all_rules_as_string(self.weak)
        self._add_string_to_program(deontic_rules_as_string)
        self._deontic_rules_added = True

    # </editor-fold>
