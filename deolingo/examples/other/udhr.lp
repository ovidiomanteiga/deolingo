
% Universal Declaration of Human Rights
% Adopted and proclaimed by General Assembly resolution 217 A (III) of 10 December 1948
% http://www.un.org/en/universal-declaration-human-rights/


%%%%%%%%%%%%%%
% ARTICLE 1  %
%%%%%%%%%%%%%%

% All human beings are born free and equal in dignity and rights.
&obligatory{free(Human)} :- human(Human).
&obligatory{equal_in_dignity(Human)} :- human(Human).
&obligatory{equal_in_rights(Human)} :- human(Human).

% They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.
&obligatory{endowed_with_reason(Human)} :- human(Human).
&obligatory{endowed_with_conscience(Human)} :- human(Human).
&obligatory{act_in_brotherhood(Human1, Human2)} :- human(Human1), human(Human2).


%%%%%%%%%%%%%%
% ARTICLE 2  %
%%%%%%%%%%%%%%

% Everyone is entitled to all the rights and freedoms set forth in this Declaration, without distinction of any kind.
&obligatory{entitled_to_rights(Human)} :- human(Human).

% Such as race, colour, sex, language, religion, political or other opinion, national or social origin, property, birth or other status.
&forbidden{distinction(race, Human)} :- human(Human).
&forbidden{distinction(colour, Human)} :- human(Human).
&forbidden{distinction(sex, Human)} :- human(Human).
&forbidden{distinction(language, Human)} :- human(Human).
&forbidden{distinction(religion, Human)} :- human(Human).
&forbidden{distinction(opinion, Human)} :- human(Human).
&forbidden{distinction(national_origin, Human)} :- human(Human).
&forbidden{distinction(social_origin, Human)} :- human(Human).
&forbidden{distinction(property, Human)} :- human(Human).
&forbidden{distinction(birth, Human)} :- human(Human).
&forbidden{distinction(other_status, Human)} :- human(Human).

% Furthermore, no distinction shall be made on the basis of the political, jurisdictional or international status of the country or territory to which a person belongs, whether it be independent, trust, non-self-governing or under any other limitation of sovereignty.
&forbidden{distinction(Status, Human)} :- human(Human), political_status(Status, Country), country_of(Human, Country).
&forbidden{distinction(Status, Human)} :- human(Human), jurisdictional_status(Status, Country), country_of(Human, Country).
&forbidden{distinction(Status, Human)} :- human(Human), international_status(Status, Country), country_of(Human, Country).


%%%%%%%%%%%%%%
% ARTICLE 3  %
%%%%%%%%%%%%%%

% Everyone has the right to life, liberty and security of person.
&obligatory{has_right_to(Human, life)} :- human(Human).
&obligatory{has_right_to(Human, liberty)} :- human(Human).
&obligatory{has_right_to(Human, security)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 4  %
%%%%%%%%%%%%%%

% No one shall be held in slavery or servitude; slavery and the slave trade shall be prohibited in all their forms.
&forbidden{slavery(Human)} :- human(Human).
&forbidden{servitude(Human)} :- human(Human).
&forbidden{slave_trade(Human)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 5  %
%%%%%%%%%%%%%%

% No one shall be subjected to torture or to cruel, inhuman or degrading treatment or punishment.
&forbidden{torture(Human)} :- human(Human).
&forbidden{cruel_treatment(Human)} :- human(Human).
&forbidden{inhuman_treatment(Human)} :- human(Human).
&forbidden{degrading_treatment(Human)} :- human(Human).
&forbidden{cruel_punishment(Human)} :- human(Human).
&forbidden{inhuman_punishment(Human)} :- human(Human).
&forbidden{degrading_punishment(Human)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 6  %
%%%%%%%%%%%%%%

% Everyone has the right to recognition everywhere as a person before the law.
&obligatory{has_right_to(Human, recognition_as_person_before_law)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 7  %
%%%%%%%%%%%%%%

% All are equal before the law and are entitled without any discrimination to equal protection of the law.
&obligatory{equal_before_law(Human)} :- human(Human).
&obligatory{equal_protection_of_law(Human)} :- human(Human).

% All are entitled to equal protection against any discrimination in violation of this Declaration and against any incitement to such discrimination.
&obligatory{protection_against_discrimination(Human)} :- human(Human).
&obligatory{protection_against_incitement(Human)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 8  %
%%%%%%%%%%%%%%

% Everyone has the right to an effective remedy by the competent national tribunals for acts violating the fundamental rights granted by the constitution or by law.
&obligatory{has_right_to(Human, effective_remedy(Acts, Tribunal))} :- human(Human), violate_fundamental_rights(Acts), competent_national_tribunal(Tribunal).


%%%%%%%%%%%%%%
% ARTICLE 9  %
%%%%%%%%%%%%%%

% No one shall be subjected to arbitrary arrest, detention or exile.
&forbidden{arbitrary_arrest(Human)} :- human(Human).
&forbidden{arbitrary_detention(Human)} :- human(Human).
&forbidden{arbitrary_exile(Human)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 10 %
%%%%%%%%%%%%%%

% Everyone is entitled in full equality to a fair and public hearing by an independent and impartial tribunal, in the determination of his rights and obligations and of any criminal charge against him.
&obligatory{has_right_to(Human, fair_hearing)} :- human(Human).
&obligatory{has_right_to(Human, public_hearing)} :- human(Human).
&obligatory{independent_tribunal(Human)} :- human(Human).
&obligatory{impartial_tribunal(Human)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 11 %
%%%%%%%%%%%%%%

% (1) Everyone charged with a penal offence has the right to be presumed innocent until proved guilty according to law in a public trial at which he has had all the guarantees necessary for his defence.
&obligatory{presumed_innocent(Human)} :- charged_with_offence(Human), human(Human).
&obligatory{proven_guilty(Human)} :- public_trial(Human), charged_with_offence(Human), human(Human).
&obligatory{guarantees_for_defence(Human)} :- charged_with_offence(Human), human(Human).

% (2) No one shall be held guilty of any penal offence on account of any act or omission which did not constitute a penal offence, under national or international law, at the time when it was committed. Nor shall a heavier penalty be imposed than the one that was applicable at the time the penal offence was committed.
&forbidden{guilty_of_non_offence(Human)} :- act_or_omission(Human), human(Human).
&forbidden{heavier_penalty(Human)} :- penal_offence_committed(Human), human(Human).


%%%%%%%%%%%%%%
% ARTICLE 12 %
%%%%%%%%%%%%%%

% No one shall be subjected to arbitrary interference with his privacy, family, home or correspondence, nor to attacks upon his honour and reputation. Everyone has the right to the protection of the law against such interference or attacks.
&forbidden{arbitrary_interference(Human, privacy)} :- human(Human).
&forbidden{arbitrary_interference(Human, family)} :- human(Human).
&forbidden{arbitrary_interference(Human, home)} :- human(Human).
&forbidden{arbitrary_interference(Human, correspondence)} :- human(Human).
&forbidden{attacks_on_honour(Human)} :- human(Human).
&forbidden{attacks_on_reputation(Human)} :- human(Human).
&obligatory{protection_of_law(Human)} :- human(Human), interference_or_attack(Human).


%%%%%%%%%%%%%%
% ARTICLE 13 %
%%%%%%%%%%%%%%

% (1) Everyone has the right to freedom of movement and residence within the borders of each state.
&obligatory{freedom_of_movement(Human)} :- human(Human).
&obligatory{freedom_of_residence(Human)} :- human(Human).

% (2) Everyone has the right to leave any country, including his own, and to return to his country.
&obligatory{has_right_to(Human, leave_country)} :- human(Human).
&obligatory{has_right_to(Human, return_to_country)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 14 %
%%%%%%%%%%%%%%

% (1) Everyone has the right to seek and to enjoy in other countries asylum from persecution.
&obligatory{has_right_to(Human, asylum)} :- human(Human).

% (2) This right may not be invoked in the case of prosecutions genuinely arising from non-political crimes or from acts contrary to the purposes and principles of the United Nations.
&forbidden{has_right_to(Human, asylum_for_non_political_crimes)} :- human(Human).
&forbidden{has_right_to(Human, asylum_for_un_acts)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 15 %
%%%%%%%%%%%%%%

% (1) Everyone has the right to a nationality.
&obligatory{has_right_to(Human, nationality)} :- human(Human).

% (2) No one shall be arbitrarily deprived of his nationality nor denied the right to change his nationality.
&forbidden{arbitrary_deprivation_of_nationality(Human)} :- human(Human).
&obligatory{has_right_to(Human, change_nationality)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 16 %
%%%%%%%%%%%%%%

% Men and women of full age, without any limitation due to race, nationality or religion, have the right to marry and to found a family. They are entitled to equal rights as to marriage, during marriage and at its dissolution.
&obligatory{has_right_to(Human, marry)} :- human(Human), adult(Human).
&obligatory{has_right_to(Human, found_family)} :- human(Human), adult(Human).
&forbidden{limitation_due_to_race(Human)} :- human(Human), adult(Human).
&forbidden{limitation_due_to_nationality(Human)} :- human(Human), adult(Human).
&forbidden{limitation_due_to_religion(Human)} :- human(Human), adult(Human).
&obligatory{equal_rights_in_marriage(Human)} :- human(Human), married(Human).
&obligatory{equal_rights_in_divorce(Human)} :- human(Human), divorced(Human).

% Marriage shall be entered into only with the free and full consent of the intending spouses.
&forbidden{forced_marriage(Human1, Human2)} :- human(Human1), human(Human2).
&obligatory{full_consent_marriage(Human1, Human2)} :- human(Human1), human(Human2).

% The family is the natural and fundamental group unit of society and is entitled to protection by society and the State.
&obligatory{protection_of_family(Human)} :- family(Human).


%%%%%%%%%%%%%%
% ARTICLE 17 %
%%%%%%%%%%%%%%

% Everyone has the right to own property alone as well as in association with others.
&obligatory{has_right_to(Human, own_property)} :- human(Human).
&obligatory{has_right_to(Human, own_property_in_association)} :- human(Human).

% No one shall be arbitrarily deprived of his property.
&forbidden{arbitrary_deprivation_of_property(Human)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 18 %
%%%%%%%%%%%%%%

% Everyone has the right to freedom of thought, conscience and religion; this right includes freedom to change his religion or belief, and freedom, either alone or in community with others and in public or private, to manifest his religion or belief in teaching, practice, worship and observance.
&obligatory{has_right_to(Human, freedom_of_thought)} :- human(Human).
&obligatory{has_right_to(Human, freedom_of_conscience)} :- human(Human).
&obligatory{has_right_to(Human, freedom_of_religion)} :- human(Human).
&obligatory{has_right_to(Human, change_religion)} :- human(Human).
&obligatory{has_right_to(Human, manifest_religion)} :- human(Human).
&obligatory{has_right_to(Human, teach_religion)} :- human(Human).
&obligatory{has_right_to(Human, practice_religion)} :- human(Human).
&obligatory{has_right_to(Human, worship)} :- human(Human).
&obligatory{has_right_to(Human, observe_religion)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 19 %
%%%%%%%%%%%%%%

% Everyone has the right to freedom of opinion and expression; this right includes freedom to hold opinions without interference and to seek, receive and impart information and ideas through any media and regardless of frontiers.
&obligatory{has_right_to(Human, freedom_of_opinion)} :- human(Human).
&obligatory{has_right_to(Human, freedom_of_expression)} :- human(Human).
&obligatory{has_right_to(Human, hold_opinions)} :- human(Human).
&obligatory{has_right_to(Human, seek_information)} :- human(Human).
&obligatory{has_right_to(Human, receive_information)} :- human(Human).
&obligatory{has_right_to(Human, impart_information)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 20 %
%%%%%%%%%%%%%%

% Everyone has the right to freedom of peaceful assembly and association.
&obligatory{has_right_to(Human, peaceful_assembly)} :- human(Human).
&obligatory{has_right_to(Human, association)} :- human(Human).

% No one may be compelled to belong to an association.
&forbidden{compulsory_association(Human)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 21 %
%%%%%%%%%%%%%%

% (1) Everyone has the right to take part in the government of his country, directly or through freely chosen representatives.
&obligatory{has_right_to(Human, take_part_in_government)} :- human(Human).

% (2) Everyone has the right of equal access to public service in his country.
&obligatory{has_right_to(Human, equal_access_to_public_service)} :- human(Human).

% (3) The will of the people shall be the basis of the authority of government; this will shall be expressed in periodic and genuine elections which shall be by universal and equal suffrage and shall be held by secret vote or by equivalent free voting procedures.
&obligatory{basis_of_authority_government(will_of_the_people)}.
&obligatory{periodic_elections}.
&obligatory{genuine_elections}.
&obligatory{universal_suffrage}.
&obligatory{equal_suffrage}.
&obligatory{secret_vote}.
&obligatory{free_voting_procedures}.


%%%%%%%%%%%%%%
% ARTICLE 22 %
%%%%%%%%%%%%%%

% Everyone, as a member of society, has the right to social security and is entitled to realization, through national effort and international co-operation and in accordance with the organization and resources of each State, of the economic, social and cultural rights indispensable for his dignity and the free development of his personality.
&obligatory{has_right_to(Human, social_security)} :- human(Human).
&obligatory{has_right_to(Human, realization_of_economic_rights)} :- human(Human).
&obligatory{has_right_to(Human, realization_of_social_rights)} :- human(Human).
&obligatory{has_right_to(Human, realization_of_cultural_rights)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 23 %
%%%%%%%%%%%%%%

% (1) Everyone has the right to work, to free choice of employment, to just and favourable conditions of work and to protection against unemployment.
&obligatory{has_right_to(Human, work)} :- human(Human).
&obligatory{has_right_to(Human, free_choice_of_employment)} :- human(Human).
&obligatory{has_right_to(Human, favourable_work_conditions)} :- human(Human).
&obligatory{has_right_to(Human, protection_against_unemployment)} :- human(Human).

% (2) Everyone, without any discrimination, has the right to equal pay for equal work.
&obligatory{equal_pay(Human1, Human2)} :- human(Human1), human(Human2), equal_work(Human1, Human2).

% (3) Everyone who works has the right to just and favourable remuneration ensuring for himself and his family an existence worthy of human dignity, and supplemented, if necessary, by other means of social protection.
&obligatory{has_right_to(Human, favourable_remuneration)} :- human(Human), works(Human).
&obligatory{has_right_to(Human, social_protection)} :- human(Human).

% (4) Everyone has the right to form and to join trade unions for the protection of his interests.
&obligatory{has_right_to(Human, form_trade_unions)} :- human(Human).
&obligatory{has_right_to(Human, join_trade_unions)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 24 %
%%%%%%%%%%%%%%

% Everyone has the right to rest and leisure, including reasonable limitation of working hours and periodic holidays with pay.
&obligatory{has_right_to(Human, rest)} :- human(Human).
&obligatory{has_right_to(Human, leisure)} :- human(Human).
&obligatory{has_right_to(Human, limit_working_hours)} :- human(Human).
&obligatory{has_right_to(Human, holidays_with_pay)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 25 %
%%%%%%%%%%%%%%

% (1) Everyone has the right to a standard of living adequate for the health and well-being of himself and of his family, including food, clothing, housing and medical care and necessary social services, and the right to security in the event of unemployment, sickness, disability, widowhood, old age or other lack of livelihood in circumstances beyond his control.
&obligatory{has_right_to(Human, adequate_living_standard)} :- human(Human).
&obligatory{has_right_to(Human, food)} :- human(Human).
&obligatory{has_right_to(Human, clothing)} :- human(Human).
&obligatory{has_right_to(Human, housing)} :- human(Human).
&obligatory{has_right_to(Human, medical_care)} :- human(Human).
&obligatory{has_right_to(Human, social_services)} :- human(Human).
&obligatory{has_right_to(Human, security)} :- human(Human), unemployed(Human).
&obligatory{has_right_to(Human, security)} :- human(Human), sick(Human).
&obligatory{has_right_to(Human, security)} :- human(Human), disabled(Human).
&obligatory{has_right_to(Human, security)} :- human(Human), widow(Human).
&obligatory{has_right_to(Human, security)} :- human(Human), elderly(Human).
&obligatory{has_right_to(Human, security)} :- human(Human), lacks_livelihood(Human).

% (2) Motherhood and childhood are entitled to special care and assistance. All children, whether born in or out of wedlock, shall enjoy the same social protection.
&obligatory{special_care_for_motherhood(Human)} :- mother(Human).
&obligatory{special_care_for_childhood(Human)} :- child(Human).
&obligatory{equal_social_protection_for_children(Human)} :- child(Human).


%%%%%%%%%%%%%%
% ARTICLE 26 %
%%%%%%%%%%%%%%

% (1) Everyone has the right to education. Education shall be free, at least in the elementary and fundamental stages. Elementary education shall be compulsory. Technical and professional education shall be made generally available and higher education shall be equally accessible to all on the basis of merit.
&obligatory{has_right_to(Human, education)} :- human(Human).
&obligatory{free_elementary_education(Human)} :- human(Human).
&obligatory{compulsory_elementary_education(Human)} :- human(Human).
&obligatory{available_technical_education(Human)} :- human(Human).
&obligatory{available_professional_education(Human)} :- human(Human).
&obligatory{equal_access_to_higher_education(Human)} :- human(Human), merit_based(Human).

% (2) Education shall be directed to the full development of the human personality and to the strengthening of respect for human rights and fundamental freedoms. It shall promote understanding, tolerance and friendship among all nations, racial or religious groups, and shall further the activities of the United Nations for the maintenance of peace.
&obligatory{education_for_personality_development(Human)} :- human(Human).
&obligatory{education_for_human_rights_respect(Human)} :- human(Human).
&obligatory{education_for_fundamental_freedoms_respect(Human)} :- human(Human).
&obligatory{education_for_understanding(Human)} :- human(Human).
&obligatory{education_for_tolerance(Human)} :- human(Human).
&obligatory{education_for_friendship(Human)} :- human(Human).
&obligatory{education_for_un_peace_activities(Human)} :- human(Human).

% (3) Parents have a prior right to choose the kind of education that shall be given to their children.
&obligatory{has_right_to(Human1, children_education_choice)} :- parent(Human1, Human2), human(Human1), human(Human2).


%%%%%%%%%%%%%%
% ARTICLE 27 %
%%%%%%%%%%%%%%

% (1) Everyone has the right freely to participate in the cultural life of the community, to enjoy the arts and to share in scientific advancement and its benefits.
&obligatory{has_right_to(Human, cultural_participation)} :- human(Human).
&obligatory{has_right_to(Human, enjoy_arts)} :- human(Human).
&obligatory{has_right_to(Human, scientific_advancement)} :- human(Human).

% (2) Everyone has the right to the protection of the moral and material interests resulting from any scientific, literary or artistic production of which he is the author.
&obligatory{has_right_to(Human, protection_of_interests)} :- human(Human), author(Human).


%%%%%%%%%%%%%%
% ARTICLE 28 %
%%%%%%%%%%%%%%

% Everyone is entitled to a social and international order in which the rights and freedoms set forth in this Declaration can be fully realized.
&obligatory{has_right_to(Human, social_order)} :- human(Human).
&obligatory{has_right_to(Human, international_order)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 29 %
%%%%%%%%%%%%%%

% (1) Everyone has duties to the community in which alone the free and full development of his personality is possible.
&obligatory{duty_to_community(Human)} :- human(Human).

% (2) In the exercise of his rights and freedoms, everyone shall be subject only to such limitations as are determined by law solely for the purpose of securing due recognition and respect for the rights and freedoms of others and of meeting the just requirements of morality, public order and the general welfare in a democratic society.
&obligatory{limitations_on_rights_and_freedoms(Human)} :- human(Human), determined_by_law(Human).

% (3) These rights and freedoms may in no case be exercised contrary to the purposes and principles of the United Nations.
&forbidden{exercise_rights_against_un_purposes(Human)} :- human(Human).


%%%%%%%%%%%%%%
% ARTICLE 30 %
%%%%%%%%%%%%%%

% Nothing in this Declaration may be interpreted as implying for any State, group or person any right to engage in any activity or to perform any act aimed at the destruction of any of the rights and freedoms set forth herein.
&forbidden{activity_aimed_at_destruction_of_rights(Human)} :- human(Human).
&forbidden{act_aimed_at_destruction_of_rights(Human)} :- human(Human).
