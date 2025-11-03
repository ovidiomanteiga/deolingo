
from deolingo._deontic_atom import *


class DeonticRules:

    @staticmethod
    def all_rules(weak=False, temporal=False):
        weakAxiom = DeonticRules.deontic_weak_axiom_weak_constraint() if weak else DeonticRules.deontic_weak_axiom()
        rules = [
            *weakAxiom,
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
        if temporal:
            rules.extend(DeonticRules.maintain_rules())
            rules.extend(DeonticRules.achieve_rules())
        return rules

    @staticmethod
    def all_rules_as_string(weak=False, temporal=False):
        return "\n".join(DeonticRules.all_rules(weak=weak, temporal=temporal)) + '\n'

    @staticmethod
    def deontic_weak_axiom():
        return [
            f"\n% Deontic weak axiom D for DELX",
            f":- {obligatory('X')}, {forbidden('X')}, not {holds('X')}, not {holds('-X')}.",
        ]

    @staticmethod
    def deontic_weak_axiom_weak_constraint():
        return [
            "\n% Deontic weak axiom D for DELX (weak constraint)",
            f"deolingo_inconsistency(X) :- not deolingo_inconsistency(-X),"
                f" {obligatory('X')}, {forbidden('X')}, not {holds('X')}, not {holds('-X')}.",
            ":~ deolingo_inconsistency(X). [1@1, X]",
            "#show deolingo_inconsistency/1.",
            '%!trace {"INCONSISTENCY: % is obligatory and forbidden without factual information!", X} '
                'deolingo_inconsistency(X).\n',
            "%!show_trace deolingo_inconsistency(X).",
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
            f"{forbidden('X')}  :- {obligatory('-X')}.",
            f"-{obligatory('X')} :- -{forbidden('-X')}.",
            f"-{forbidden('X')}  :- -{obligatory('-X')}.",
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
            f"{permitted_by_default('X')} :- {permitted('X')}.",
            f"{permitted('X')} :- not {forbidden('X')}, {permitted_by_default('X')}.",
            f"\n% Omissible by default",
            f"{omissible_by_default('X')} :- not not {obligatory('X')}; {deontic('X')}.",
            f"{omissible_by_default('X')} :- {omissible('X')}.",
            f"{omissible('X')} :- not {obligatory('X')}, {omissible_by_default('X')}.",
        ]

    @staticmethod
    def obligation_violation_fulfillment():
        return [
            f"\n% Obligation violation",
            DeonticRules.derive_violated_obligation(),
            f"{obligatory('X')} :- {violated_obligation('X')}.",
            f"{holds('-X')} :- {violated_obligation('X')}.",
            f"\n% Fulfilled obligation",
            DeonticRules.derive_fulfilled_obligation(),
            f"{obligatory('X')} :- {fulfilled_obligation('X')}.",
            f"{holds('X')} :- {fulfilled_obligation('X')}.",
            f"\n% Non-fulfilled obligation",
            DeonticRules.derive_non_fulfilled_obligation(),
            f"{obligatory('X')} :- {non_fulfilled_obligation('X')}.",
            f"not {holds('X')} :- {non_fulfilled_obligation('X')}.",
            f"\n% Non-violated obligation",
            DeonticRules.derive_non_violated_obligation(),
            f"{obligatory('X')} :- {non_violated_obligation('X')}.",
            f"not {holds('-X')} :- {non_violated_obligation('X')}.",
            f"\n% Undetermined obligation",
            DeonticRules.derive_undetermined_obligation(),
            f"{obligatory('X')} :- {undetermined_obligation('X')}.",
            f"not {holds('X')} :- {undetermined_obligation('X')}.",
            f"not {holds('-X')} :- {undetermined_obligation('X')}.",
        ]

    @staticmethod
    def derive_violated_obligation():
        return f"{violated_obligation('X')} :- {obligatory('X')}, {holds('-X')}."

    @staticmethod
    def derive_fulfilled_obligation():
        return f"{fulfilled_obligation('X')} :- {obligatory('X')}, {holds('X')}."

    @staticmethod
    def derive_non_fulfilled_obligation():
        return f"{non_fulfilled_obligation('X')} :- {obligatory('X')}, not {holds('X')}."

    @staticmethod
    def derive_non_violated_obligation():
        return f"{non_violated_obligation('X')} :- {obligatory('X')}, not {holds('-X')}."

    @staticmethod
    def derive_undetermined_obligation():
        return f"{undetermined_obligation('X')} :- {obligatory('X')}, not {holds('X')}, not {holds('-X')}."

    @staticmethod
    def default_obligation():
        return [
            f"\n% Default obligation",
            f"{default_obligation('X')} :- not not {permitted('-X')}; {deontic('X')}.",
            f"{default_obligation('X')} :- {obligatory('X')}.",
            f"{obligatory('X')} :- not {permitted('-X')}, {default_obligation('X')}.",
        ]

    @staticmethod
    def prohibition_violation_fulfillment():
        return [
            f"\n% Violated prohibition",
            DeonticRules.derive_violated_prohibition(),
            f"{forbidden('X')} :- {violated_prohibition('X')}.",
            f"{holds('X')} :- {violated_prohibition('X')}.",
            f"\n% Fulfilled prohibition",
            DeonticRules.derive_fulfilled_prohibition(),
            f"{forbidden('X')} :- {fulfilled_prohibition('X')}.",
            f"{holds('-X')} :- {fulfilled_prohibition('X')}.",
            f"\n% Non-fulfilled prohibition",
            DeonticRules.derive_non_fulfilled_prohibition(),
            f"{forbidden('X')} :- {non_fulfilled_prohibition('X')}.",
            f"not {holds('-X')} :- {non_fulfilled_prohibition('X')}.",
            f"\n% Non-violated prohibition",
            DeonticRules.derive_non_violated_prohibition(),
            f"{forbidden('X')} :- {non_violated_prohibition('X')}.",
            f"not {holds('X')} :- {non_violated_prohibition('X')}.",
            f"\n% Undetermined prohibition",
            DeonticRules.derive_undetermined_prohibition(),
            f"{forbidden('X')} :- {undetermined_prohibition('X')}.",
            f"not {holds('X')} :- {undetermined_prohibition('X')}.",
            f"not {holds('-X')} :- {undetermined_prohibition('X')}.",
        ]

    # same as above but with prohibition

    @staticmethod
    def derive_violated_prohibition():
        return f"{violated_prohibition('X')} :- {forbidden('X')}, {holds('X')}."

    @staticmethod
    def derive_fulfilled_prohibition():
        return f"{fulfilled_prohibition('X')} :- {forbidden('X')}, {holds('-X')}."

    @staticmethod
    def derive_non_fulfilled_prohibition():
        return f"{non_fulfilled_prohibition('X')} :- {forbidden('X')}, not {holds('-X')}."

    @staticmethod
    def derive_non_violated_prohibition():
        return f"{non_violated_prohibition('X')} :- {forbidden('X')}, not {holds('X')}."

    @staticmethod
    def derive_undetermined_prohibition():
        return f"{undetermined_prohibition('X')} :- {forbidden('X')}, not {holds('X')}, not {holds('-X')}."

    @staticmethod
    def default_prohibition():
        return [
            f"\n% Default prohibition",
            f"{default_prohibition('X')} :- not not {permitted('X')}; {deontic('X')}.",
            f"{default_prohibition('X')} :- {forbidden('X')}.",
            f"{forbidden('X')} :- not {permitted('X')}, {default_prohibition('X')}.",
        ]

    @staticmethod
    def deontic_rules():
        return [
            f"\n% Deontic",
            f"{deontic('X')} :- {obligatory('X')}.",
            f"{deontic('X')} :- {deontic('-X')}.",
        ]

    @staticmethod
    def maintain_rules():
        return [
            f"\n% Maintain Obligation",
            f"#program dynamic.",
            f"{maintain_obligation('Obligation', 'Until')} :- {maintain_obligation('Obligation', 'Until', prev=True)}, not {holds('Until')}, not {cancel_maintain_obligation('Obligation', 'Until')}.",
            f"{maintain_default_obligation('Obligation', 'Until')} :- {maintain_default_obligation('Obligation', 'Until', prev=True)}, not {holds('Until')}, not {cancel_maintain_obligation('Obligation', 'Until')}.",
            f"{maintain_permission('Permission', 'Until')} :- {maintain_permission('Permission', 'Until', prev=True)}, not {holds('Until')}, not {cancel_maintain_permission('Permission', 'Until')}.",
            f"{maintain_default_permission('Permission', 'Until')} :- {maintain_default_permission('Permission', 'Until', prev=True)}, not {holds('Until')}, not {cancel_maintain_default_permission('Permission', 'Until')}.",
            f"{maintain_prohibition('Prohibition', 'Until')} :- {maintain_prohibition('Prohibition', 'Until', prev=True)}, not {holds('Until')}, not {cancel_maintain_prohibition('Prohibition', 'Until')}.",
            f"{maintain_default_prohibition('Prohibition', 'Until')} :- {maintain_default_prohibition('Prohibition', 'Until', prev=True)}, not {holds('Until')}, not {cancel_maintain_default_prohibition('Prohibition', 'Until')}.",
            f"{maintain_omission('Omission', 'Until')} :- {maintain_omission('Omission', 'Until', prev=True)}, not {holds('Until')}, not {cancel_maintain_omission('Omission', 'Until')}.",
            f"{maintain_default_omission('Omission', 'Until')} :- {maintain_default_omission('Omission', 'Until', prev=True)}, not {holds('Until')}, not {cancel_maintain_default_omission('Omission', 'Until')}.",
            f"#program always.",
            f"{obligatory('Obligation')} :- {maintain_obligation('Obligation', 'Until')}, not {holds('Until', prev=True)}.",
            f"-{maintain_obligation('Obligation', 'Until')} :- {cancel_maintain_obligation('Obligation', 'Until')}.",
            f"{cancel_maintain_obligation('Obligation', 'Until')} :- -{maintain_obligation('Obligation', 'Until')}.",
            f"{default_obligation('Obligation')} :- {maintain_default_obligation('Obligation', 'Until')}, not {holds('Until', prev=True)}.",
            f"-{maintain_default_obligation('Obligation', 'Until')} :- {cancel_maintain_obligation('Obligation', 'Until')}.",
            f"{cancel_maintain_obligation('Obligation', 'Until')} :- -{maintain_default_obligation('Obligation', 'Until')}.",
            f"{permitted('Permission')} :- {maintain_permission('Permission', 'Until')}, not {holds('Until', prev=True)}.",
            f"-{maintain_permission('Permission', 'Until')} :- {cancel_maintain_permission('Permission', 'Until')}.",
            f"{cancel_maintain_permission('Permission', 'Until')} :- -{maintain_permission('Permission', 'Until')}.",
            f"{permitted_by_default('Permission')} :- {maintain_default_permission('Permission', 'Until')}, not {holds('Until', prev=True)}.",
            f"-{maintain_default_permission('Permission', 'Until')} :- {cancel_maintain_default_permission('Permission', 'Until')}.",
            f"{cancel_maintain_default_permission('Permission', 'Until')} :- -{maintain_default_permission('Permission', 'Until')}.",
            f"{forbidden('Prohibition')} :- {maintain_prohibition('Prohibition', 'Until')}, not {holds('Until', prev=True)}.",
            f"-{maintain_prohibition('Prohibition', 'Until')} :- {cancel_maintain_prohibition('Prohibition', 'Until')}.",
            f"{cancel_maintain_prohibition('Prohibition', 'Until')} :- -{maintain_prohibition('Prohibition', 'Until')}.",
            f"{default_prohibition('Prohibition')} :- {maintain_default_prohibition('Prohibition', 'Until')}, not {holds('Until', prev=True)}.",
            f"-{maintain_default_prohibition('Prohibition', 'Until')} :- {cancel_maintain_default_prohibition('Prohibition', 'Until')}.",
            f"{cancel_maintain_default_prohibition('Prohibition', 'Until')} :- -{maintain_default_prohibition('Prohibition', 'Until')}.",
            f"{omissible('Omission')} :- {maintain_omission('Omission', 'Until')}, not {holds('Until', prev=True)}.",
            f"-{maintain_omission('Omission', 'Until')} :- {cancel_maintain_omission('Omission', 'Until')}.",
            f"{cancel_maintain_omission('Omission', 'Until')} :- -{maintain_omission('Omission', 'Until')}.",
            f"{omissible_by_default('Omission')} :- {maintain_default_omission('Omission', 'Until')}, not {holds('Until', prev=True)}.",
            f"-{maintain_default_omission('Omission', 'Until')} :- {cancel_maintain_default_omission('Omission', 'Until')}.",
            f"{cancel_maintain_default_omission('Omission', 'Until')} :- -{maintain_default_omission('Omission', 'Until')}.",
        ]

    @staticmethod
    def achieve_rules():
        return [
            f"\n% Achieve Obligation",
            f"#program dynamic.",
            f"{achieve_obligation('Obligation', 'Until')} :- {achieve_obligation('Obligation', 'Until', prev=True)}, not {holds('Until', prev=True)}, not {holds('Obligation', prev=True)}, not {cancel_achieve_obligation('Obligation', 'Until')}.",
            f"{achieve_permission('Permission', 'Until')} :- {achieve_permission('Permission', 'Until', prev=True)}, not {holds('Until', prev=True)}, not {holds('Permission', prev=True)}, not {cancel_achieve_permission('Permission', 'Until')}.",
            f"{achieve_prohibition('Prohibition', 'Until')} :- {achieve_prohibition('Prohibition', 'Until', prev=True)}, not {holds('Until', prev=True)}, not {holds('Prohibition', prev=True)}, not {cancel_achieve_prohibition('Prohibition', 'Until')}.",
            f"{achieve_omission('Omission', 'Until')} :- {achieve_omission('Omission', 'Until', prev=True)}, not {holds('Until', prev=True)}, not {holds('Omission', prev=True)}, not {cancel_achieve_omission('Omission', 'Until')}.",
            f"#program always.",
            f"{obligatory('Obligation')} :- {achieve_obligation('Obligation', 'Until')}, {holds('Until')}.",
            f"{obligatory('Obligation')} :- {achieve_obligation('Obligation', 'Until')}, {holds('Obligation')}.",
            f"-{achieve_obligation('Obligation', 'Until')} :- {cancel_achieve_obligation('Obligation', 'Until')}.",
            f"{cancel_achieve_obligation('Obligation', 'Until')} :- -{achieve_obligation('Obligation', 'Until')}.",
            f"{permitted('Permission')} :- {achieve_permission('Permission', 'Until')}, {holds('Until')}.",
            f"{permitted('Permission')} :- {achieve_permission('Permission', 'Until')}, {holds('Permission')}.",
            f"-{achieve_permission('Permission', 'Until')} :- {cancel_achieve_permission('Permission', 'Until')}.",
            f"{cancel_achieve_permission('Permission', 'Until')} :- -{achieve_permission('Permission', 'Until')}.",
            f"{forbidden('Prohibition')} :- {achieve_prohibition('Prohibition', 'Until')}, {holds('Until')}.",
            f"{forbidden('Prohibition')} :- {achieve_prohibition('Prohibition', 'Until')}, {holds('Prohibition')}.",
            f"-{achieve_prohibition('Prohibition', 'Until')} :- {cancel_achieve_prohibition('Prohibition', 'Until')}.",
            f"{cancel_achieve_prohibition('Prohibition', 'Until')} :- -{achieve_prohibition('Prohibition', 'Until')}.",
            f"{omissible('Omission')} :- {achieve_omission('Omission', 'Until')}, {holds('Until')}.",
            f"{omissible('Omission')} :- {achieve_omission('Omission', 'Until')}, {holds('Omission')}.",
            f"-{achieve_omission('Omission', 'Until')} :- {cancel_achieve_omission('Omission', 'Until')}.",
            f"{cancel_achieve_omission('Omission', 'Until')} :- -{achieve_omission('Omission', 'Until')}.",
        ]
