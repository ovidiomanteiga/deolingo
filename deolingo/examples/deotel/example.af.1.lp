
% Defeasible Obligations (I).

#program always.

% (A') Unless  you are explicitly permitted to do otherwise, upon testing positive you must quarantine until you test negative.
&maintain_default_obligation(negative){quarantine} :- positive.

% (B) If you test positive and are in quarantine, you ought to report  your quarantine before you test negative.
&achieve_obligation(negative){report} :- positive, quarantine.

% (C) While you are violating an obligation to quarantine, it is forbidden to report you are in quarantine.
&forbidden{report} :- &violated_obligation{quarantine}.

% (F) It is  permissible to leave quarantine in the case of an emergency, until the situation is solved (a maintenance permission).
&maintain_permission(solved){-quarantine} :- emergency.

#program initial.

&tel {
    &true
    ;> quarantine & positive
    ;> quarantine
    ;> emergency & -quarantine
    ;> -quarantine
    ;> solved
    ;> &true
}.
