
% It ought to be that Jones goes to assist his neighbors.
&obligatory{jones_goes}.

% It ought to be that if Jones goes, then he tells them he is coming.
&obligatory{jones_tells} :- jones_goes.

% If Jones doesn’t go, then he ought not tell them he is coming.
&obligatory{-jones_tells} :- &obligatory{-jones_goes}.

% Jones doesn’t go.
-jones_goes.

% Check for violations of obligations.
violated_jones_goes :- &violated_obligation{jones_goes}.
violated_jones_not_tells :- &violated_obligation{-jones_tells}.
