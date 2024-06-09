
% UDC Library Loan Rules
% https://www.udc.es/export/sites/udc/biblioteca/_galeria_down/Normas_Prestamo_GL.pdf_2063069294.pdf


%%%%%%%%%%%%%%%%%
% 1 Purpose (N/A)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 2. Users of the library service

% 2.1. All members of the university community at UDC: individuals who study in official and UDC-specific training cycles, teaching and research staff (PDI), and administrative and service staff (PAS).
library_user(User) :- member(udc, User).

% 2.2 Former members of the university community at UDC, or individuals affiliated with entities that have agreements or arrangements for using the loan service.
library_user(User) :- member(udc_alumni, User).

% 2.3 Individuals external to the university community authorized by the University Library.
library_user(User) :- member(udc_external, User), authorized(User).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 3. Documents subject to the loan service

% 3.1. All the bibliographic materials of the UDC can be borrowed, but some materials may be excluded from the loan or subject to a regime of restricted loan. The exclusions or restrictions may obey reasons of use, antiquity, rarity or preservation.
&permitted{borrow(Document, freely)} :- document(Document), not &forbidden{borrow(Document)}.
&permitted{borrow(Document, restricted)} :- document(Document), not &forbidden{borrow(Document)}, restricted_borrowing(Document).

% 3.2. In general, they will be excluded from the loan, although they can be consulted at the library in which they are deposited:
% a) Magazines and other journals.
% b) Old, rare and precious documents.
% c) Modern documents already exhausted and difficult to replace.
% d) Theses and other unpublished academic works.
&forbidden{borrow(Document)} :- document_type(Document, magazine).
&forbidden{borrow(Document)} :- document_type(Document, rare).
&forbidden{borrow(Document)} :- document_type(Document, unique).
&forbidden{borrow(Document)} :- document_type(Document, unpublished).

document(Document) :- document_type(Document, Type).

&permitted{consult_in_room(Document)} :- &permitted{borrow(Document)}, document(Document).
&permitted{consult_in_room(Document)} :- restricted_borrowing(Document).

% 3.3. Based on the characteristics of the collection and the needs of each library, they may be excluded from loan or subject to a special loan:
% a) Reference works: encyclopedias, dictionaries, bibliographies, etc.
% b) The most used documents
% c) Audiovisual, graphic and cartographic documents
% d) Other documents according to the criteria of the center's library committee
&permitted{excluded_from_loan(Document)} :- document_type(Document, reference).
&permitted{excluded_from_loan(Document)} :- document_type(Document, extensively_used).
&permitted{excluded_from_loan(Document)} :- document_type(Document, audiovisual_or_graphic).
&permitted{excluded_from_loan(Document)} :- excluded_at_discretion(Document).

&forbidden{borrow(Document)} :- excluded_from_loan(Document).

% 3.4. The funds acquired from the research projects or from the resources external to the University, research contracts, etc. will be deposited in the library for its control and processing and will be served on a preferential basis loan to the director of said project until its completion.
&obligatory{preferent_loan(Document, Director)} :- adquired_by_research_project(Document, Project), director(Director, Project).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 4. Loan formalization and conditions

% 4.1. The loan will be formalized by presenting the identification card university or an official document that identifies the user.
id_document(university_id_card; official_id_card).
&obligatory{borrower_identification(User, ID)} :- library_user(User), id_document(ID), borrow(Document), borrowed(Document, User).

% 4.2. The conditions of the loan service depend on the group to which the person belongs that requests the loan and the type of document (see below Annex I. Conditions of loan).

% 4.3. Users will be able to renew the documents they have on loan, as well how to make reservations, in any library or by any means that is enabled for this purpose.
&permitted{renew(Document, User)} :- borrowed(Document, User), library_user(User).
&permitted{reservation(Document, User)} :- library_user(User), document(Document).

% 4.4. In order that any user can access the funds of all the libraries of the UDC, without the need to travel from its centre, there is the intercentre loan.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 5. Non-compliance with loan rules

% 5.1. Users have the obligation to return the loaned documents within the deadline. Similarly, if a document is borrowed by academic year, there is an obligation to return it when requested by another user.
%!trace_rule {"The book % borrowed by % is overdue % days", Document, User, DaysBorrowed}
overdue(Document, User) :- borrowed(Document, User, DaysBorrowed), DaysBorrowed > Max, max_loan_days_user(User, Max).
%!trace_rule {"% must return % because it is overdue", User, Document}
&obligatory{return(Document, User)} :- overdue(Document, User).
&obligatory{return(Document, User)} :- borrowed_for_year(Document, User, Year), reservation(Document, AnotherUser), User!=AnotherUser.
borrowed(Document, User) :- borrowed_for_year(Document, User, Year), year(Year).
borrowed(Document, User) :- borrowed(Document, User, DaysBorrowed).

% 5.2. In the event of non-compliance with point 5.1, the library will demand the return of documents. Under no circumstances will documents be given to users who have overdue or claimed loans.
demand_return(User) :- &violated_obligation{return(Document, User)}, library_user(User).
&forbidden{overdue(Document, User)} :- borrowed(Document, User).

% 5.3. The delay in the return of the documents on loan will be a reason for the penalty that will be incurred the temporary exclusion of the user of the loan service.
&forbidden{borrow(User)} :- overdue(Document, User), document(Document).
borrow(User) :- borrowed(Document, User), document(User).

% 5.4. In case of loss or deterioration, the user must return the work provided by another copy of the same edition. If the work is sold out you will have to purchase and deliver another with similar characteristics proposed by the library. As long as it is not restored to work, the user will be excluded from the loan service.
&obligatory{restitution(Document, User)} :- missed(Document, User), not sold_out(Document).
&obligatory{restitution(SimilarDoc, User)} :- missed(Document, User), sold_out(Document), similar(Document, SimilarDoc).
&forbidden{borrow(User)} :- missed(Document, User), not restitution(Document, User).

% 5.5. In order to ensure the return or replacement of the bibliographic funds belonging to the patrimony of the UDC, the secretariat of each center will be able to ask the Library for a report about the situation of the loan when the students request the issuance of the official title. If you have loans pending repayment, the Administration of the center may require its regularization.
&forbidden{get_degree(User)} :- overdue(Document, User).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 6. Modification of loan rules (N/A)


%%%%%%%%%%%%%%%%%%%%
% 7. Guarantee (N/A)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Annex I. Loan conditions.
% https://www.udc.es/export/sites/udc/biblioteca/_galeria_down/AnexoI_Condiciones_Prestamo_EN.pdf_2063069299.pdf

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

%From the moment of return, the user will be penalized without being able borrow books for as many business days as there are documents with an overdue loan and 
%accumulated days of delay, up to a maximum of 40 days. Penalties are cumulative. 
 
%Example: if the user has 4 books and is 5 days late in returning them, they will be penalized with 20 business days (4 weeks, if there are no holidays in between) without being 
%able to borrow documents.
