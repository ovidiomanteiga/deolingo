
% UDC Library Loan Rules
% https://www.udc.es/export/sites/udc/biblioteca/_galeria_down/Normas_Prestamo_GL.pdf_2063069294.pdf


% 1 Purpose (N/A)


% 2. Users of the library service

library_user(User) :- member(User, udc).
library_user(User) :- member(User, udc_alumni).
library_user(User) :- member(User, udc_external), authorized(User).


% 3. Documents subject to the loan service

&permitted{borrow(Document, freely)} :- contains(udc_collection, Document), not &forbidden{borrow(Document)}.
&permitted{borrow(Document, restricted)} :- contains(udc_collection, Document), not &forbidden{borrow(Document)}, restricted_borrowing(Document).

&forbidden{borrow(Document)} :- magazine(Document).
&forbidden{borrow(Document)} :- rare(Document).
&forbidden{borrow(Document)} :- unique(Document).
&forbidden{borrow(Document)} :- unpublished(Document).

&permitted{consult_in_room(Document)} :- &permitted{borrow(Document, _)}.
&permitted{consult_in_room(Document)} :- restricted_borrowing(Document).

&permitted{exclude_from_loan(Document)} :- reference(Document).
&permitted{exclude_from_loan(Document)} :- extensively_used(Document).
&permitted{exclude_from_loan(Document)} :- audiovisual_or_graphic(Document).
&permitted{exclude_from_loan(Document)} :- exclude_at_discretion(Document).

&forbidden{borrow(Document)} :- exclude_from_loan(Document).

&obligatory{preferent_loan(Document, Director)} :- adquired_by_research_project(Document, Project), director(Director, Project).


% 4. Loan formalization and conditions

id_document(university_id_card; official_id_card).
&obligatory{borrower_identification(User, ID)} :- library_user(User), id_document(ID).

% See Anex I below.

&permitted{renew(Document, User)} :- borrowed(Document, User), library_user(User).
&permitted{book(Document, User)} :- library_user(User).


% 5. Non-compliance with loan rules

&obligatory{return(Document, User, Deadline)} :- borrowed(Document, User, Deadline).
&obligatory{return(Document, User)} :- borrowed_for_year(Document, User, _), book(Document, AnotherUser), User!=AnotherUser.
borrowed(Document, User) :- borrowed_for_year(Document, User, _).

overdue(Document, User) :- return(Document, User, Deadline), today(Date), Deadline > Date.
&forbidden{overdue(Document, User)}.

&forbidden{borrow(User)} :- overdue(_, User).
borrow(User) :- borrowed(_, User).

&obligatory{restitution(Document, User)} :- missed(Document, User), not sold_out(Document).
&obligatory{restitution(SimilarDoc, User)} :- missed(Document, User), sold_out(Document), similar(Document, SimilarDoc).
&forbidden{borrow(User)} :-  missed(Document, User), not restitution(Document, User).

&forbidden{get_degree(User)} :- overdue(_, User).


% 6. Modification of loan rules (N/A)


% 7. Guarantee (N/A)


% Annex I. Loan conditions.
% https://www.udc.es/export/sites/udc/biblioteca/_galeria_down/AnexoI_Condiciones_Prestamo_EN.pdf_2063069299.pdf

user_group(1..6).

max_docs_on_loan(1, 10). max_docs_on_loan(2, 15). max_docs_on_loan(3, 35).
max_docs_on_loan(4, 35). max_docs_on_loan(5, 100). max_docs_on_loan(6, 6).
exceed_max_docs_loan(User) :- library_user(User), member(user_group(Group), User), max_docs_on_loan(Group, Max), #count{1,Document: borrowed(Document, User)} > Max.
&forbidden{exceed_max_docs_loan(User)} :- library_user(User).

max_loan_days(1, 10). max_loan_days(2, 21). max_loan_days(3, 30). 
max_loan_days(4, 365). max_loan_days(5, 365). max_loan_days(6, 10). 

max_renewals(Group, indefinite) :- user_group(Group).

max_bookings(1, 10). max_bookings(2, 10). max_bookings(1, 10). 
max_bookings(1, 10). max_bookings(1, 10). max_bookings(1, 10). 


loan_type(weekend_and_holidays; non_school_periods; short_loan; bic_loan; laptop; ereader).
special_loan(weekend_and_holidays, Group, friday_to_monday, no_renewals, no_requests) :- user_group(Group).
special_loan(non_school_periods, 1, summer_21, indefinite, requests_allowed).
special_loan(short_loan, Group, 5, 2, requests_allowed) :- user_group(Group).
special_loan(short_loan, Group, 30, indefinite, requests_allowed) :- user_group(Group).
electronic_device_loan(laptop, Group, six_hours, 1, requests_allowed) :- user_group(Group).
electronic_device_loan(ereader, Group, 15, indefinite, requests_allowed) :- user_group(Group).

%From the moment of return, the user will be penalized without being able borrow books for as many business days as there are documents with an overdue loan and 
%accumulated days of delay, up to a maximum of 40 days. Penalties are cumulative. 
 
%Example: if the user has 4 books and is 5 days late in returning them, they will be penalized with 20 business days (4 weeks, if there are no holidays in between) without being 
%able to borrow documents.
