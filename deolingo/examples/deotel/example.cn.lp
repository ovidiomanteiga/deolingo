
% Constitutive Norms.

#program always.

% (A') Unless  you are explicitly permitted to do otherwise, upon testing positive you must quarantine until you test negative.
&maintain_default_obligation(negative){quarantine} :- positive.

% (B) If you test positive and are in quarantine, you ought to report  your quarantine before you test negative.
&achieve_obligation(negative){report} :- positive, quarantine.

% (C) While you are violating an obligation to quarantine, it is forbidden to report you are in quarantine.
&forbidden{report} :- &violated_obligation{quarantine}.

% A quarantine counts as a confinement.
confinement :- quarantine.
&obligatory{confinement} :- &obligatory{quarantine}.
-confinement :- -quarantine.
&obligatory{-confinement} :- &obligatory{-quarantine}.
