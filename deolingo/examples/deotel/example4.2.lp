
#program always.

&maintain_obligation(negative){quarantine} :- positive.
&achieve_obligation(negative){report} :- positive, quarantine.
&forbidden{report} :- &violated_obligation{quarantine}.

#program initial.
positive.

% Just to make quarantine and report deontic atoms.
&obligatory{quarantine}. &obligatory{report}.

&tel{ 
    &true 
    ;> positive & quarantine 
    ;> quarantine
    ;> report
    ;> &true
    ;> negative 
    ;> &true
}.

