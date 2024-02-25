from clingo.ast import parse_string

from _deontic_ast_transformer import DeonticTransformer

from _deontic_atom import *


deolingo_theory = f"""
#theory _deolingo_ {{
    deontic_term {{
        & : 2, binary, left;
        - : 3, unary;
        ~ : 3, unary;
        | : 1, binary, left
    }};
    &{DeonticAtoms.OBLIGATORY.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.FORBIDDEN.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.OMISSIBLE.value.name}/0 : deontic_term, any;
    &{DeonticAtoms.PERMITTED.value.name}/0 : deontic_term, any
}}.
"""


class DeolingoTransformer:

    def __init__(self, add_to_program_callback, transformer=DeonticTransformer(), translate=False):
        self.deontic_transformer = transformer
        self._add_to_program_callback = add_to_program_callback
        self.translate = translate
        self.translated_program = ""
        transformer.translate = translate

    def transform(self, inputs):
        self._add_string_to_program(deolingo_theory)
        self._transform_and_add_source_inputs(inputs)
        self._add_common_deontic_rules()
        self._add_rules_for_each_deontic_atom()

    def _add_to_translation(self, statement):
        if self.translate:
            self.translated_program += str(statement)

    def _add_string_to_program(self, statement):
        parse_string(statement, self._add_to_program_callback)
        self._add_to_translation(statement)

    def _transform_and_add_to_program(self, statement):
        transformed_statement = self.deontic_transformer(statement)
        self._add_to_program_callback(transformed_statement)

    def _transform_and_add_source_inputs(self, inputs):
        for source_input in inputs:
            parse_string(source_input, self._transform_and_add_to_program)
        self._add_to_translation(self.deontic_transformer.translated_program)

    def _add_rules_for_each_deontic_atom(self):
        for deontic_atom in self.deontic_transformer.deontic_atoms:
            holds_positive = holds(deontic_atom)
            holds_negative = holds(f"-{deontic_atom}")
            is_deontic = deontic(deontic_atom)
            rules = [
                f"\n% Deontic atom rules for '{deontic_atom}'",
                f"{holds_positive} :- {deontic_atom}.",
                f"{holds_negative} :- -{deontic_atom}.",
                f"{is_deontic}."
            ]
            rules_as_string = "\n".join(rules) + '\n'
            self._add_string_to_program(rules_as_string)

    def _add_common_deontic_rules(self):
        violation_x = violated("X")
        fulfilled_x = fulfilled("X")
        ob_x = obligatory("X")
        ob_neg_x = obligatory("-X")
        fb_x = forbidden("X")
        fb_neg_x = forbidden("-X")
        holds_x = holds("X")
        holds_neg_x = holds("-X")
        deontic_x = deontic("X")
        implicit_permission_x = implicit_permission("X")
        omissible_x = omissible("X")
        permitted_x = permitted("X")
        deontic_rules = [
            f"\n% Deontic axiom D for DELX",
            f":- {ob_x}, {fb_x}, not {holds_x}, not {holds_neg_x}.",
            f"\n% Deontic operator rules",
            f"{violation_x} :- {ob_x}, {holds_neg_x}.",
            f"{violation_x} :- {fb_x}, {holds_x}.",
            f"{fulfilled_x} :- {ob_x}, {holds_x}.",
            f"{fulfilled_x} :- {fb_x}, {holds_neg_x}.",
            f"{ob_x} :- {fb_neg_x}.",
            f"{fb_x}  :- {ob_neg_x}.",
            f"{implicit_permission_x} :- not {fb_x}, {deontic_x}.",
            f"{omissible_x} :- -{ob_x}, {deontic_x}.",
            f"{permitted_x} :- -{fb_x}, {deontic_x}.",
            f"-{ob_x} :- {omissible_x}, {deontic_x}.",
            f"-{fb_x} :- {permitted_x}, {deontic_x}."
        ]
        deontic_rules_as_string = "\n".join(deontic_rules) + '\n'
        self._add_string_to_program(deontic_rules_as_string)
