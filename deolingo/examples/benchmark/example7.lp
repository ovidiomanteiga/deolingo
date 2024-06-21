
library_user(User) :- member(udc, User).
library_user(User) :- member(udc_alumni, User).
library_user(User) :- member(udc_external, User), authorized(User).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

&permitted{borrow(Document, freely)} :- document(Document), not &forbidden{borrow(Document)}.
&permitted{borrow(Document, restricted)} :- document(Document), not &forbidden{borrow(Document)}, restricted_borrowing(Document).

&forbidden{borrow(Document)} :- document_type(Document, magazine).
&forbidden{borrow(Document)} :- document_type(Document, rare).
&forbidden{borrow(Document)} :- document_type(Document, unique).
&forbidden{borrow(Document)} :- document_type(Document, unpublished).

document(Document) :- document_type(Document, Type).

&permitted{consult_in_room(Document)} :- &permitted{borrow(Document)}, document(Document).
&permitted{consult_in_room(Document)} :- restricted_borrowing(Document).

&permitted{excluded_from_loan(Document)} :- document_type(Document, reference).
&permitted{excluded_from_loan(Document)} :- document_type(Document, extensively_used).
&permitted{excluded_from_loan(Document)} :- document_type(Document, audiovisual_or_graphic).
&permitted{excluded_from_loan(Document)} :- excluded_at_discretion(Document).

&forbidden{borrow(Document)} :- excluded_from_loan(Document).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

id_document(university_id_card; official_id_card).
&obligatory{borrower_identification(User, ID)} :- library_user(User), id_document(ID), borrow(Document), borrowed(Document, User).

&permitted{renew(Document, User)} :- borrowed(Document, User), library_user(User).
&permitted{reservation(Document, User)} :- library_user(User), document(Document).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%!trace_rule {"The book % borrowed by % is overdue % days", Document, User, DaysBorrowed}
overdue(Document, User) :- borrowed(Document, User, DaysBorrowed), DaysBorrowed > Max, max_loan_days_user(User, Max).
%!trace_rule {"% must return % because it is overdue", User, Document}
&obligatory{return(Document, User)} :- overdue(Document, User).
&obligatory{return(Document, User)} :- borrowed_for_year(Document, User, Year), reservation(Document, AnotherUser), User!=AnotherUser.
borrowed(Document, User) :- borrowed_for_year(Document, User, Year), year(Year).
borrowed(Document, User) :- borrowed(Document, User, DaysBorrowed).

demand_return(User) :- &violated_obligation{return(Document, User)}, library_user(User).
&forbidden{overdue(Document, User)} :- borrowed(Document, User).

&forbidden{borrow(User)} :- overdue(Document, User), document(Document).
borrow(User) :- borrowed(Document, User), document(User).

&obligatory{restitution(Document, User)} :- missed(Document, User), not sold_out(Document).
&obligatory{restitution(SimilarDoc, User)} :- missed(Document, User), sold_out(Document), similar(Document, SimilarDoc).
&forbidden{borrow(User)} :- missed(Document, User), not restitution(Document, User).

&forbidden{get_degree(User)} :- overdue(Document, User).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

user_group(1..6).

% The maximum number of documents that can be borrowed depends on the group to which the user belongs.
max_docs_on_loan(1, 10). max_docs_on_loan(2, 15). max_docs_on_loan(3, 35).
max_docs_on_loan(4, 35). max_docs_on_loan(5, 100). max_docs_on_loan(6, 6).

number_docs_borrowed(User, Count) :- library_user(User), Count = #count{1, Document: borrowed(Document, User)}.

exceed_max_docs_loan(User) :- library_user(User), member(user_group(Group), User), max_docs_on_loan(Group, Max), number_docs_borrowed(User, Count), Count > Max.
&forbidden{exceed_max_docs_loan(User)} :- library_user(User).

% The maximum number of days that a document can be borrowed depends on the group to which the user belongs.
max_loan_days(1, 10). max_loan_days(2, 21). max_loan_days(3, 30).
max_loan_days(4, 365). max_loan_days(5, 365). max_loan_days(6, 10).
max_loan_days_user(User, Max) :- library_user(User), member(user_group(Group), User), max_loan_days(Group, Max).
exceed_max_loan_days(User) :- max_loan_days_user(User, Max),
                              #max{DaysBorrowed,Document,User: borrowed(Document, User, DaysBorrowed)} > Max.
&forbidden{exceed_max_loan_days(User)} :- library_user(User).

% The maximum number of renewals that can be made depends on the group to which the user belongs.
max_renewals(Group, indefinite) :- user_group(Group).

% The maximum number of reservations that can be made depends on the group to which the user belongs.
max_reservations(1, 10). max_reservations(2, 15). max_reservations(3, 35).
max_reservations(4, 35). max_reservations(5, 100). max_reservations(1, 6).

number_docs_reserved(User, Count) :- library_user(User), Count = #count{1, Document: reservation(Document, User)}.

exceed_max_docs_reserved(User) :- library_user(User), member(user_group(Group), User), max_reservations(Group, Max), number_docs_reserved(User, Count), Count > Max.
&forbidden{exceed_max_docs_reserved(User)} :- library_user(User).

% SPECIAL LOANS AND ELECTRONIC DEVICES LOANS
loan_type(weekend_and_holidays; non_school_periods; short_loan; bic_loan; laptop; ereader).
special_loan(weekend_and_holidays, Group, friday_to_monday, no_renewals, no_requests) :- user_group(Group).
special_loan(non_school_periods, 1, summer_21, indefinite, requests_allowed).
special_loan(short_loan, Group, 5, 2, requests_allowed) :- user_group(Group).
special_loan(short_loan, Group, 30, indefinite, requests_allowed) :- user_group(Group).
electronic_device_loan(laptop, Group, six_hours, 1, requests_allowed) :- user_group(Group).
electronic_device_loan(ereader, Group, 15, indefinite, requests_allowed) :- user_group(Group).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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
0 { borrowed(B, P, 20) } 1 :- document(B), person(P).

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
