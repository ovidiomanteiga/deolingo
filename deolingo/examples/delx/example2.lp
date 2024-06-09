
% C2 (Contrary-to-Duty (CTD) and Compliance)

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

% (v) If you put a fence when forbidden, you should pay a fine.
&obligatory{pay} :- &forbidden{f}, f.
