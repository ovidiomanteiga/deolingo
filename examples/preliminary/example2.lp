% I must normally work,
% On weekends, I have an explicit permission not to work
% It is not a weekend, I decided not to work
&ob{work} :- not &nob{work}.
&nob{work} :- weekend.
-weekend.
-work.