% C6 (Defeasible Deontic Detachment) (1st example)
% (i) There must be no fence (f).
&obligatory{-f}.
% (ii) If there is a fence, it must be a white (w) fence.
&obligatory{w} :- f.
% (iii) If the cottage is by the sea (s), there must be a fence.
&obligatory{f} :- s.
% If it is obligatory a white fence, then it is obligatory a fence.
&obligatory{f} :- &obligatory{w}.
% (vii) If we put a fence, we must put a street mailbox (m).
&obligatory{m} :- f.
% (viii) If we do not put a fence, we must not put a street mailbox.
&forbidden{m} :- -f.
% Fence or not fence.
f;-f.