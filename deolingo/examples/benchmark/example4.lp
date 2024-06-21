
% Speed limit in highways in Spain in km/h
speed_limit(120).

% Range of speed values in km/h
speed_value(1..300).

% Calculate maximum speed of a car
max_speed(Car, MaxS) :- #max{S,Car: speed(Car,S)} = MaxS, car(Car).

% If the max speed is MaxS, then the smaller speed values are not the max speed.
-max_speed(Car, NoMaxS) :- max_speed(Car, MaxS), speed_value(NoMaxS), NoMaxS<MaxS.

% If the speed limit is X, then it is obligatory that the maximum speed is X.
&obligatory{max_speed(Car, SL)} :- speed_limit(SL), car(Car).

% min speed, max speed, fine amount in euros, points to deduct, is criminal offense?
violation_severity(120, 150, 100, 0, "no").
violation_severity(150, 170, 300, 2, "no").
violation_severity(170, 180, 400, 4, "no").
violation_severity(180, 190, 500, 6, "no").
violation_severity(190, 1000, 600, 6, "yes").

% Consequences of speed violation for the owner of a car depending on the speed of the car.
speed_violation(Owner, FineAmount, Points, Criminal) :-
                        &violated_obligation{max_speed(Car, SpeedLimit)},
                        max_speed(Car, MaxS), MaxS>MinSInRange, MaxS<=MaxSInRange, owned_by(Owner, Car),
                        violation_severity(MinSInRange, MaxSInRange, FineAmount, Points, Criminal).

% If the owner of a car has violated the speed limit, then it is obligatory to pay the fine.
&obligatory{pay(Owner, FineAmount)} :- speed_violation(Owner, FineAmount, _, _).

% If the owner of a car has violated the speed limit, then some points are to be deducted from their license.
points_deducted_from_license(Owner, Points) :- speed_violation(Owner, _, Points, _).

% If the owner of a car has violated the speed limit to the extent it is a criminal offense, they might go to jail.
can_go_to_jail(Owner) :- speed_violation(Owner, _, _, "yes").

% Cars and their owners
#const n=45.
car(1..n).
owner(1..n).
owned_by(Owner,Car) :- owner(Owner), car(Car), Owner=Car.

% Speed of cars measured in km/h by the police
1 {speed(C, S): speed_value(S), S>120+C} 1 :- car(C).

pay_due(Owner,FineAmount) :- &obligatory{pay(Owner, FineAmount)}.

#minimize{Points@2, Owner: points_deducted_from_license(Owner, Points)}.
#minimize{FineAmount@1, Owner: pay_due(Owner,FineAmount)}.


#show max_speed/2.
#show points_deducted_from_license/2.
#show can_go_to_jail/1.
