
% C4 (CTD and Defeasible Obligations) ((18) ∪ (3) ∪ {s,f})

% (i) There must be no fence, unless a permission is granted
&forbidden{f} :- not &permitted{f}.

% (ii) If there is a fence, it must be a white (w) fence.
&obligatory{w} :- f, &forbidden{f}.

% (vi) If the cottage is by the sea (s), there may be a fence.
&permitted{f} :- s.

% A white fence is a fence.
f :- w.

% If it is obligatory a white fence, then it is obligatory a fence.
&obligatory{f} :- &obligatory{w}.

% The cottage is by the sea.
s.

% There is a fence.
f.
