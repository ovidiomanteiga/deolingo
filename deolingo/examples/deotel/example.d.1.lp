
% Compensatory Obligations (I).

#program always.

% (A) If you test positive, you ought to remain in quarantine until  you test negative.
&maintain_obligation(negative){quarantine} :- positive.

% (B) If you test positive and are in quarantine, you ought to report  your quarantine before you test negative.
&achieve_obligation(negative){report} :- positive, quarantine.

% (C) While you are violating an obligation to quarantine, it is forbidden to report you are in quarantine.
&forbidden{report} :- &violated_obligation{quarantine}.

% (D) An obligation to pay a fine by the end of the month arises from violating the obligation to quarantine.
&achieve_obligation(end_of_month){fine} :- &violated_obligation{quarantine}.

#program initial.

&tel {
    &true
    ;> quarantine & positive
    ;> -quarantine & -report
    ;> negative
    ;> &true
    ;> end_of_month
    ;> &true
}.
