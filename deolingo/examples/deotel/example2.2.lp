
#program always.

&maintain_obligation(negative){quarantine} :- positive.
&achieve_obligation(negative){report} :- positive, quarantine.
&forbidden{report} :- &violated_obligation{quarantine}.

#program initial.
positive.

&tel{ &true ;> &true ;> negative ;> &true }.
