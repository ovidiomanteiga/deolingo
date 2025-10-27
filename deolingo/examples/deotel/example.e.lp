
#program always.

% (A) If you test positive, you ought to remain in quarantine until  you test negative.
&maintain_obligation(negative){quarantine} :- positive.

% (B) If you test positive and are in quarantine, you ought to report  your quarantine before you test negative.
&achieve_obligation(negative){report} :- positive, quarantine.

% (C) While you are violating an obligation to quarantine, it is forbidden to report you are in quarantine.
&forbidden{report} :- &violated_obligation{quarantine}.

% (E) If the lockdown ends (le), the obligations to remain in quarantine and report your quarantine are canceled.
&not_maintain_obligation(negative){quarantine} :- lockdown_ends.
&not_achieve_obligation(negative){report} :- lockdown_ends.
