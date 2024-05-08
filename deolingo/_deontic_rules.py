
from deolingo._deontic_atom import *


class DeonticRules:

    @staticmethod
    def all_rules():
        return [
            *DeonticRules.deontic_weak_axiom(),
            *DeonticRules.violation_fullfillment(),
            *DeonticRules.obligation_prohibition_equivalence(),
            *DeonticRules.implicit_permission_omission(),
            *DeonticRules.permissible_omissible_rules(),
            *DeonticRules.optional_definition(),
            *DeonticRules.permitted_omissible_defaults(),
            *DeonticRules.obligation_violation_fulfillment(),
            *DeonticRules.default_obligation(),
            *DeonticRules.prohibition_violation_fulfillment(),
            *DeonticRules.default_prohibition(),
            *DeonticRules.deontic_rules(),
        ]

    @staticmethod
    def all_rules_as_string():
        return "\n".join(DeonticRules.all_rules()) + '\n'

    @staticmethod
    def deontic_weak_axiom():
        return [
            f"\n% Deontic axiom D for DELX",
            f":- {obligatory('X')}, {forbidden('X')}, not {holds('X')}, not {holds('-X')}.",
        ]

    @staticmethod
    def violation_fullfillment():
        return [
            f"\n% Violation",
            f"{violated('X')} :- {violated_obligation('X')}.",
            f"{violated('X')} :- {violated_prohibition('X')}.",
            f"\n% Fulfillment",
            f"{fulfilled('X')} :- {fulfilled_obligation('X')}.",
            f"{fulfilled('X')} :- {fulfilled_prohibition('X')}.",
        ]

    @staticmethod
    def obligation_prohibition_equivalence():
        return [
            f"\n% Obligation/prohibition equivalence",
            f"{obligatory('X')} :- {forbidden('-X')}.",
            f"{forbidden('-X')} :- {obligatory('X')}.",
            f"{forbidden('X')}  :- {obligatory('-X')}.",
            f"{obligatory('-X')} :- {forbidden('X')}.",
            f"-{obligatory('X')} :- -{forbidden('-X')}.",
            f"-{forbidden('-X')} :- -{obligatory('X')}.",
            f"-{forbidden('X')}  :- -{obligatory('-X')}.",
            f"-{obligatory('-X')} :- -{forbidden('X')}.",
        ]

    @staticmethod
    def implicit_permission_omission():
        return [
            f"\n% Implicit permission",
            f"{permitted_implicitly('X')} :- not {forbidden('X')}, {deontic('X')}.",
            f"not {forbidden('X')} :- {permitted_implicitly('X')}.",
            f"\n% Implicit omission",
            f"{omissible_implicitly('X')} :- not {obligatory('X')}, {deontic('X')}.",
            f"not {obligatory('X')} :- {omissible_implicitly('X')}.",
        ]

    @staticmethod
    def permissible_omissible_rules():
        return [
            f"\n% Permissible and omissible",
            f"{omissible('X')} :- -{obligatory('X')}.",
            f"-{obligatory('X')} :- {omissible('X')}.",
            f"{permitted('X')} :- -{forbidden('X')}.",
            f"-{forbidden('X')} :- {permitted('X')}.",
            f"-{omissible('X')} :- {obligatory('X')}.",
            f"{obligatory('X')} :- -{omissible('X')}.",
            f"-{permitted('X')} :- {forbidden('X')}.",
            f"{forbidden('X')} :- -{permitted('X')}.",
        ]

    @staticmethod
    def optional_definition():
        return [
            f"\n% Optional",
            f"{optional('X')} :- {omissible('X')}, {permitted('X')}.",
            f"{omissible('X')} :- {optional('X')}.",
            f"{permitted('X')} :- {optional('X')}.",
        ]

    @staticmethod
    def permitted_omissible_defaults():
        return [
            f"\n% Permitted by default",
            f"{permitted_by_default('X')} :- not not {forbidden('X')}; {deontic('X')}.",
            f"{permitted_by_default('X')} :- {permitted('X')}; {deontic('X')}.",
            f"{permitted('X')} :- not {forbidden('X')}, {permitted_by_default('X')}.",
            f"\n% Omissible by default",
            f"{omissible_by_default('X')} :- not not {obligatory('X')}; {deontic('X')}.",
            f"{omissible_by_default('X')} :- {omissible('X')}; {deontic('X')}.",
            f"{omissible('X')} :- not {obligatory('X')}, {omissible_by_default('X')}.",
        ]

    @staticmethod
    def obligation_violation_fulfillment():
        return [
            f"\n% Obligation violation",
            f"{violated_obligation('X')} :- {obligatory('X')}, {holds('-X')}.",
            f"{obligatory('X')} :- {violated_obligation('X')}.",
            f"{holds('-X')} :- {violated_obligation('X')}.",
            f"\n% Fulfilled obligation",
            f"{fulfilled_obligation('X')} :- {obligatory('X')}, {holds('X')}.",
            f"{obligatory('X')} :- {fulfilled_obligation('X')}.",
            f"{holds('X')} :- {fulfilled_obligation('X')}.",
            f"\n% Non-fulfilled obligation",
            f"{non_fulfilled_obligation('X')} :- {obligatory('X')}, not {holds('X')}.",
            f"{obligatory('X')} :- {non_fulfilled_obligation('X')}.",
            f"not {holds('X')} :- {non_fulfilled_obligation('X')}.",
            f"\n% Non-violated obligation",
            f"{non_violated_obligation('X')} :- {obligatory('X')}, not {holds('-X')}.",
            f"{obligatory('X')} :- {non_violated_obligation('X')}.",
            f"not {holds('-X')} :- {non_violated_obligation('X')}.",
            f"\n% Undetermined obligation",
            f"{undetermined_obligation('X')} :- {obligatory('X')}, not {holds('X')}, not {holds('-X')}.",
            f"{obligatory('X')} :- {undetermined_obligation('X')}.",
            f"not {holds('X')} :- {undetermined_obligation('X')}.",
            f"not {holds('-X')} :- {undetermined_obligation('X')}.",
        ]

    @staticmethod
    def default_obligation():
        return [
            f"\n% Default obligation",
            f"{default_obligation('X')} :- not not {permitted('-X')}; {deontic('X')}.",
            f"{default_obligation('X')} :- {obligatory('X')}; {deontic('X')}.",
            f"{obligatory('X')} :- not {permitted('-X')}, {default_obligation('X')}.",
        ]

    @staticmethod
    def prohibition_violation_fulfillment():
        return [
            f"\n% Violated prohibition",
            f"{violated_prohibition('X')} :- {forbidden('X')}, {holds('X')}.",
            f"{forbidden('X')} :- {violated_prohibition('X')}.",
            f"{holds('X')} :- {violated_prohibition('X')}.",
            f"\n% Fulfilled prohibition",
            f"{fulfilled_prohibition('X')} :- {forbidden('X')}, {holds('-X')}.",
            f"{forbidden('X')} :- {fulfilled_prohibition('X')}.",
            f"{holds('-X')} :- {fulfilled_prohibition('X')}.",
            f"\n% Non-fulfilled prohibition",
            f"{non_fulfilled_prohibition('X')} :- {forbidden('X')}, not {holds('-X')}.",
            f"{forbidden('X')} :- {non_fulfilled_prohibition('X')}.",
            f"not {holds('-X')} :- {non_fulfilled_prohibition('X')}.",
            f"\n% Non-violated prohibition",
            f"{non_violated_prohibition('X')} :- {forbidden('X')}, not {holds('X')}.",
            f"{forbidden('X')} :- {non_violated_prohibition('X')}.",
            f"not {holds('X')} :- {non_violated_prohibition('X')}.",
            f"\n% Undetermined prohibition",
            f"{undetermined_prohibition('X')} :- {forbidden('X')}, not {holds('X')}, not {holds('-X')}.",
            f"{forbidden('X')} :- {undetermined_prohibition('X')}.",
            f"not {holds('X')} :- {undetermined_prohibition('X')}.",
            f"not {holds('-X')} :- {undetermined_prohibition('X')}.",
        ]

    @staticmethod
    def default_prohibition():
        return [
            f"\n% Default prohibition",
            f"{default_prohibition('X')} :- not not {permitted('X')}; {deontic('X')}.",
            f"{default_prohibition('X')} :- {forbidden('X')}; {deontic('X')}.",
            f"{forbidden('X')} :- not {permitted('X')}, {default_prohibition('X')}.",
        ]

    @staticmethod
    def deontic_rules():
        return [
            f"\n% Deontic",
            f"{deontic('X')} :- {obligatory('X')}.",
            f"{deontic('X')} :- {obligatory('-X')}.",
            f"{deontic('X')} :- {forbidden('X')}.",
            f"{deontic('X')} :- {forbidden('-X')}.",
        ]
