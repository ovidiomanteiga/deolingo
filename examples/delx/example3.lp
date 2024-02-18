% C3 (CTD and Dilemmas)
% (i) There must be no fence (f).
&ob{-f}.
% (ii) If there is a fence, it must be a white (w) fence.
&ob{w} :- f.
% (iii) If the cottage is by the sea (s), there must be a fence.
&ob{f} :- s.
% If it is obligatory a white fence, then it is obligatory a fence.
&ob{f} :- &ob{w}.
% (v) If you put a fence when forbidden, you should pay a fine.
&ob{pay} :- &fb{f}, f.
% There is a fence.
f.