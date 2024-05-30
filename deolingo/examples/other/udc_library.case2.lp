
document("AIMA").
document("The Book of Why").
document("Think Fast. Think Slow.").
document("The Art of Loving").
document("The C Programming Language").
document("Causality").
document("Solving the Frame Problem").

member(udc, "Joe").
member(udc, "Ray").
member(udc_alumni, "Irene").

member(user_group(2), "Joe").
member(user_group(5), "Ray").
member(user_group(6), "Irene").

borrowed("AIMA", "Irene", 44).
borrowed("AIMA", "Irene").
borrowed("The Book of Why", "Irene").
borrowed("Think Fast. Think Slow.", "Irene").
borrowed("The Art of Loving", "Irene").
borrowed("The C Programming Language", "Irene").
borrowed("Causality", "Irene").
borrowed("Solving the Frame Problem", "Irene").

person(P) :- library_user(P).
&forbidden{go_out(Person)} :- curfew, person(Person).
&forbidden{go_to_library(Person)} :- &forbidden{go_out(Person)}.
&forbidden{return(Document, User) } :- &forbidden{go_to_library(User)}, document(Document).

go_to_library(User) :- return(Document, User), document(Document).
go_out(User) :- go_to_library(User).

curfew.

violated(User, return_policy) :- &violated_obligation{return(Document, User)}, document(Document).
violated(Person, curfew) :- &violated_prohibition{go_out(Person)}.
#show violated/2.
#show return/2.

