
% Constitutive Norms (II).

#program always.

% (A) If you test positive, you ought to remain in quarantine until  you test negative.
&maintain_obligation(negative){quarantine} :- positive.

% (B) If you test positive and are in quarantine, you ought to report  your quarantine before you test negative.
&achieve_obligation(negative){report} :- positive, quarantine.

% (C) While you are violating an obligation to quarantine, it is forbidden to report you are in quarantine.
&forbidden{report} :- &violated_obligation{quarantine}.

% A quarantine counts as a confinement (with defaults applicable under non-violation).
confinement :- quarantine.
&obligatory{confinement} :- &non_violated_obligation{quarantine}.
-confinement :- -quarantine.
&obligatory{-confinement} :- &non_violated_obligation{-quarantine}.

#program initial.

&tel {
    &true
    ;> quarantine & positive
    ;> &true
    ;> negative
    ;> &true
}.
