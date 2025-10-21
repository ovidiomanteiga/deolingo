
#program always.

% ◻(p → Mn(q)) (A)
% (A) If you test positive, you ought to remain in quarantine until  you test negative.  
&maintain_obligation(negative){quarantine} :- positive.
% Example trace:
% 0: positive, &obligatory{quarantine}
% 1: &obligatory{quarantine}
% 2: negative

%◻((p ∧ q) → An(r)) (B)
% (B) If you test positive and are in quarantine, you ought to report  your quarantine before you test negative.  
&achieve_obligation(negative){report} :- positive, quarantine.
% Example trace:
% 0: positive, quarantine, &obligatory{report}
% 1: &obligatory{report}
% 2: negative
% Or another trace:
% 0: positive, quarantine, &obligatory{report}
% 1: &obligatory{report}
% 2: report

%◻(Ovq → F r ) (C)
% (C) While you are violating an obligation to quarantine, it is  forbidden to report you are in quarantine.
&forbidden{report} :- &violated_obligation{quarantine}.
% Example trace:
% 0: positive, &obligatory{quarantine}
% 1: &obligatory{quarantine}, -quarantine, &forbidden{report}, &violated_obligation{quarantine}
% 2: &obligatory{quarantine}, quarantine
% 3: negative, quarantine