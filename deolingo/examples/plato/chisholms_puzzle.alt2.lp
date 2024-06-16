
% It ought to be that Jones goes to assist his neighbors.
&obligatory{jones_goes}.

% It ought to be that if Jones goes, then he tells them he is coming.
&obligatory{jones_tells | jones_goes}.

% If Jones doesn’t go, then he ought not tell them he is coming.
&obligatory{-jones_tells | -jones_goes}.

% Jones doesn’t go.
-jones_goes.

% Either Jones tells or he doesn’t.
jones_tells; -jones_tells.

% Check for violations of obligations.
violated_obligation(X) :- &violated_obligation{X}.
