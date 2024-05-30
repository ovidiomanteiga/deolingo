
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

%!trace_rule {"% must not go out during curfew",Person}
&forbidden{go_out(Person)} :- curfew, person(Person).

%!trace_rule {"% must go out to go to the library",Person}
&forbidden{go_to_library(Person)} :- &forbidden{go_out(Person)}.

%!trace_rule {"% must go to the library to return %",User,Document}
&forbidden{return(Document, User)} :- &forbidden{go_to_library(User)}, document(Document).

%!trace_rule {"% goes to the library to return %",User,Document}
go_to_library(User) :- return(Document, User), document(Document).

%!trace_rule {"% goes out to the library",User}
go_out(User) :- go_to_library(User).

curfew.

%!trace_rule {"% violated the library return policy %",User}
violated(User, return_policy) :- &violated_obligation{return(Document, User)}, document(Document).

%!trace_rule {"% violated the curfew",Person}
violated(Person, curfew) :- &violated_prohibition{go_out(Person)}.

%#show violated/2.
%#show return/2.

return("AIMA", "Irene").

%!trace {"% must NOT return %",User,Document} &forbidden{return(Document, User)}.
%!trace {"% must return %",User,Document} &obligatory{return(Document, User)}.
%!trace {"% must NOT go out % ",User} &forbidden{go_out(User)}.

%!show_trace return(Document, User).
%!show_trace violated(Person, Rule).
%!show_trace &obligatory{return(Document, User)}.
%!show_trace &forbidden{return(Document, User)}.
