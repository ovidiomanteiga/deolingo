
% Collection of library documents.
document("AIMA").
document("The Book of Why").
document("Think Fast. Think Slow.").
document("The Art of Loving").
document("The Bible").
document("Causality").
document("Solving the Frame Problem").

% Library users and their groups.
member(udc, "Joe"). member(user_group(2), "Joe").
member(udc, "Ray"). member(user_group(5), "Ray").
member(udc_alumni, "Irene"). member(user_group(6), "Irene").

% Book loan status.
borrowed("AIMA", "Irene", 44).
borrowed("The Book of Why", "Irene", 1).
borrowed("Think Fast. Think Slow.", "Irene", 2).
borrowed("The Art of Loving", "Irene", 3).
borrowed("The Bible", "Irene", 4).
borrowed("Causality", "Irene", 5).
borrowed("Solving the Frame Problem", "Irene", 6).

% A library user is a person.
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

%!trace_rule {"% cannot go to the library without going out",User}
-go_to_library(User) :- -go_out(User).

%!trace_rule {"% cannot return a book without going to the library",User}
-return(Document, User) :- -go_to_library(User), document(Document).

%!trace_rule {"% violated the library return policy",User}
violated(User, return_policy) :- &violated_obligation{return(Document, User)}, document(Document).

%!trace_rule {"% violated the curfew",Person}
violated(Person, curfew) :- &violated_prohibition{go_out(Person)}, curfew.

%!trace_rule {"It is obligatory to call the police if someone violated the curfew"}
&obligatory{call_the_police} :- &violated_prohibition{go_out(Person)}, curfew.

%!trace_rule {"% violated the curfew",User}
violated(User, max_loan_policy) :- &violated_prohibition{exceed_max_docs_loan(User)}.

%!trace_rule {"% must notify the library since she violated the return policy during the curfew",User}
&obligatory{notify_library(User)} :- &violated_obligation{return(Document, User)}, document(Document), curfew.

must_notify_library(User) :- &obligatory{notify_library(User)}.

#show violated/2.
#show return/2.
#show must_notify_library/1.
&show{obligatory}.

%!trace {"% must NOT return %",User,Document} &forbidden{return(Document, User)}.
%!trace {"% must return %",User,Document} &obligatory{return(Document, User)}.
%!trace {"% must NOT go out",User} &forbidden{go_out(User)}.

%!show_trace return(Document, User).
%!show_trace violated(Person, Rule).
%!show_trace must_notify_library(User).
%!show_trace &obligatory{return(Document, User)}.
%!show_trace &forbidden{return(Document, User)}.
