% C6 (Defeasible Deontic Detachment) (2nd example)
% (i) There must be no fence (f).
&ob{-f}.
% (ii) If there is a fence, it must be a white (w) fence.
&ob{w} :- f.
% (iii) If the cottage is by the sea (s), there must be a fence.
&ob{f} :- s.
% If it is obligatory a white fence, then it is obligatory a fence.
&ob{f} :- &ob{w}.
% (vii) If we put a fence, we must put a street mailbox (m).
&ob{m} :- f.
&ob{m} :- &ob{f}, not -f.
% (viii) If we do not put a fence, we must not put a street mailbox.
&fb{m} :- -f.
&fb{m} :- &fb{f}, not f.
% Fence or not fence.
f;-f.