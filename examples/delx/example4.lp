% C4 (CTD and Defeasible Obligations) 
% (i) There must be no fence, unless a permission is granted
&fb{f} :- not &nfb{f}.
% (ii) If there is a fence, it must be a white (w) fence.
&ob{w} :- f, &fb{f}.
% (vi) If the cottage is by the sea (s), there may be a fence.
&nfb{f} :- s.
% If it is obligatory a white fence, then it is obligatory a fence.
&ob{f} :- &ob{w}.
% The cottage is by the sea.
%s.
% There is a fence.
%f.