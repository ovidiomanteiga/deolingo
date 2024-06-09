
% C6 (Defeasible Deontic Detachment) (2nd example: Π ∪ (22) ∪ {f ∨¬f})

% (i) There must be no fence (f).
&forbidden{f}.

% (ii) If there is a fence, it must be a white (w) fence.
&obligatory{w} :- f, &forbidden{f}.

% (iii) If the cottage is by the sea (s), there must be a fence.
&obligatory{f} :- s.

% A white fence is a fence.
f :- w.

% If it is obligatory a white fence, then it is obligatory a fence.
&obligatory{f} :- &obligatory{w}.

% (vii) If we put a fence, we must put a street mailbox (m).
&obligatory{m} :- f.
&obligatory{m} :- &obligatory{f}, not -f.

% (viii) If we do not put a fence, we must not put a street mailbox.
&forbidden{m} :- -f.
&forbidden{m} :- &forbidden{f}, not f.

% Fence or not fence.
f; -f.
