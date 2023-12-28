RdfProlog
A software for executing Prolog inferences using RDF query functions.

Questions of Prolog is given in the form of SPARQL query.

FOr example, in the case of grandfather(jiro, Y):
SELECT ?ans WHERE {
    ?s VAL:operation　VAL:grandfather .
    ?s VAL:variable_x　VAL:jiro .
    ?s VAL:variable_y ?ans . }

Facts are also given in the form of RDF triples that have one common subject. Such kind of triples will be called a clause.

For example, the fact father(jiro, taro) is in the form of
VAL:rule_father_jiro_taro
    VAL:operation VAL:father ;
    VAL:variable_x VAL:jiro ;
    VAL:variable_y VAL:taro .

Inference rule are also in the form of RDF. A rule has the left_side and the right_side.
The left_side is a single clause having the same common subject VAL:left_side.
There are zero or more right_side representing the right_side clauses of Prolog rule.

The rule grandfather(X, Y) :- mother(X, U), father(U, Y) . becomes as follows:
VAL:grandfather_father_father
    VAL:left_side [
        VAL:operation VAL:grandfather ;
        VAL:variable_x VAR:x ;
        VAL:variable_y VAR:y ] ;
    VAL:right_side [
        VAL:child [
            VAL:operation VAL:mother ;
            VAL:variable_x VAR:x ;
            VAL:variable_y VAR:u ] ] ;
    VAL:right_side [
        VAL:child [
             VAL:operation VAL:father ;
             VAL:variable_x VAR:u ;
             VAL:variable_y VAR:y ] ] .

The rule in Prolog implicitly assumes the execution priority in the rule. In the above example, mother(X, U) is evaluated first, and father(U, Y) next.
This kind of priority is explicitly declared in RdfProlog. For example, the mother-father relation is declared as
VAL:control_grandfather_mother_father
    VAL:type VAL:control ;
    VAL:left_side [
        VAL:operation VAL:grandfather ;
        VAL:variable_x VAR:_x ;
        VAL:variable_y VAR:_y ] ;
    VAL:right_side [
        VAL:priority "1" ;
        VAL:child [
            VAL:operation VAL:mother ;
            VAL:variable_x VAR:_x ;
            VAL:variable_y VAR:_u ] ] ;
    VAL:right_side [
        VAL:priority "2" ;
        VAL:child [
            VAL:operation VAL:father ;
            VAL:variable_x VAR:_u ;
            VAL:variable_y VAR:_y ] ] .
The rule with execution priorities is called a control and explicitly declared as "VAL:type VAL:control".

Furthermore in Prolog the priority of applying the rules is also implicitly declared by the order of rules. That is, if the rules are declares as
    grandfather(X, Y) :- father(X, U), father(U, Y) .
    grandfather(X, Y) :- mother(X, U), father(U, Y) .
the first rule will be applied first, and the second rule second.

This kind of priorities between rules are also explicitly declared in RdfProlog. The collection is called an application and looks like
VAL:application_grandfather_x_y
    VAL:type VAL:application ;
    VAL:program VAL:false ;
    VAL:pattern [
        VAL:operation VAL:grandfather ;
        VAL:variable_x VAR:_x ;
        VAL:variable_y VAR:_y ] ;
    VAL:use [
        VAL:control VAL:control_grandfather_father_father ;
        VAL:priority "1" ] ;
    VAL:use [
        VAL:control VAL:control_grandfather_mother_father ;
        VAL:priority "2" ] ;
    VAL:priority "1" .

An application also has priority against other applications.

-----------------------------------------------------------------
Execution procedures
[answer_question method in RdfProlog class]
The question is given to this method of an instance of RdfProlog class.
    resolve_bindings = rdf_prolog.answer_question(my_question)
The results of the query is returned in the form of list[dict[str, str]], where list contains multiple results of the query and dict contains the variables in the question as keys and the associated values in dictionary values.

[reasoner method in Reasoner class]
reasoner method is the core of the inference. It calls recursively itself util all the clauses in the question are solved.
reasoner method returns a flag for success and resolve_bindings.
When reasoner finds some valid results, it returns True. If no valid answers are found, it returns False.
If the inference is succeeded, resolve_bindings contains the valid answers.

Within reasoner, the facts are first checked for the first clause of the question using search_facts() method.
If the fact search is successful, search_fact() method returns a list of bindings.
If the fact search fails, the list becomes empty.
For example, grandfather(taro, Y). will be failed, because there are no such fact registered.
The search for father(taro, U). will be succeeded, because a fact father(taro, jiro). is registered.
The bindings becomes [{'?u': '<{VAL}jiro>'}]
If the list is not empty, reasoner repeatedly applies the bindings to the rest of clauses and recursively call itself.

Reasoner next checks the existence of applicable rules by comparing the name of the operation and the matching between the arguments.
If there exist applicable rules, the matched clause is replaced by the right_side clauses of the rule and the bindings found while matching the left_side of the rule is applied to the remaining clauses.
Then the modified clauses are processed by reasoner.

-------------------------------------------------------
Execution sample of grandfather search

First the question is grandfather(taro, Y), which is represented as
        SELECT ?ans WHERE {
        ?s <http://value.org/operation> <http://value.org/grandfather> .
        ?s <http://value.org/variable_x> <http://value.org/taro> .
        ?s <http://value.org/variable_y> ?ans .
        }

reasoner first searches the fact matching grandfather(taro, Y), but fails.

reasoner then searches applications that have an operation name of "VAL:operation VAL:grandfather" and finds "VAL:application_grandfather_x_y".
This application has two controls "VAL:control_grandfather_father_father" and "VAL:control_grandfather_mother_father" and tries these controls (rules) in this order.

When the first control "VAL:control_grandfather_father_father" is applied, the question clause is replaced with the right_side of the rule and after applying the bindings becomes
    father(taro, U), father(U, Y).
Then reasoner tries to find facts and gets the fact father(taro, jiro) and the question clause become
    father(jiro, Y).
Unfortunately there exist no facts or applications that give the answer for the variable Y.

The reasoner goes back to the second control the application and the clauses become
    mother(taro, U), father(U, Y).

There is a fact mother(taro, hana). After applying this fact, the question becomes
    father(hana, Y).

Repeatedly there is a fact father(hana, ichiro) and the answer Y=ichiro is obtained.

-------------------------------------------------------
Example of symbolic arithmetics

Symbolic numbers are such that: one, two, three, ...

The fundamental facts are declared for the next relation as
    next(one, two).
    next(two, three).
    ...

Then the rule for addition X + Y = Z can be defined in Prolog as
    add(X, one, Z) :- next(X, Z) .
    add(X, Y, Z) :- next(U, Y), add(X, U, V), next(V, Z) .

Using these rules, a question add(two, one, Z) gives an answer Z=three, according to the first rule.

If the question is add(one, two, Z), the question is converted to next(U, two), add(one, U, V), next(V, Z) .
next(U, two) gives U=one and the remainder becomes add(one, one, V), next(V, Z) and further becomes next(one, V), next(V, Z).
Then V=two and next(two, Z). gives Z=three.

Thus the addition can be defined on the basis of next relation.

However, the superiority of Prolog is its flexibility that Prolog also can answer the question add(X, one, three).
By applying the first rule, the question add(X, one, three) becomes next(X, three) and according to the fact next(two, three), the answer X=two can be obtained.

THe problem of this flexibility becomes evident when answering the question add(one, Y, three).
The first rule cannot be applied to this question.
By applying the second rule, the question is converted to
    next(U, Y), add(X, U, V), next(V, Z) .
Since both U and X are not bound to fixed constant, the fact search returns all the pair of next numbers: U=one, X=two; U=two, X=three, ...
The reasoner tries the calculation of the remaining clauses for all the possible values of U.

To solve this problem, the order of applying rules must be changed depending on the arguments of a question.
FOr the question add(one, Y, three), the rules must be ordered
    add(X, Y, Z) :- next(V, Z), add(X, U, V), next(U, Y) .
Using this order, the question will be converted to next(V, three), add(one, U, V), next(U, Y) -> add(one, U, two), next(U, Y).
add(one, U, two) matches the first rule with binding U=one, and next(one, Y) gives the correct answer Y=two without executing unnecessary trials.

To implement this kind of argument dependent rule selection, we introduce a prefix SOME for a variable in the left_side of rules and also in the pattern declaration of applications.
While a normal variable with a prefix VAR matches against both a constant and a variable, a variable with SOME prefix only matches with a constant and not with avariable.
Thus the control and application for addition becomes

##################################################################
# controls

VAL:control_add_number_x_1_z
    VAL:type VAL:control ;
    VAL:left_side [
        VAL:operation VAL:add_number ;
        VAL:variable_x VAR:_x ;
        VAL:variable_y VAL:1 ;
        VAL:variable_z VAR:_z ] ;
    VAL:right_side [
        VAL:priority "1" ;
        VAL:child [
            VAL:operation VAL:next_number ;
            VAL:variable_x VAR:_x ;
            VAL:variable_y VAR:_z ] ] ;
    VAL:priority "1" .

VAL:control_add_number_1_y_z
    VAL:type VAL:control ;
    VAL:left_side [
        VAL:operation VAL:add_number ;
        VAL:variable_x VAL:1 ;
        VAL:variable_y VAR:_y ;
        VAL:variable_z VAR:_z ] ;
    VAL:right_side [
        VAL:priority "1" ;
        VAL:child [
            VAL:operation VAL:next_number ;
            VAL:variable_x VAR:_y ;
            VAL:variable_y VAR:_z ] ] ;
    VAL:priority "1" .

VAL:control_add_number_sx_sy_z
    VAL:type VAL:control ;
    VAL:left_side [
        VAL:operation VAL:add_number ;
        VAL:variable_x VAR:_sx ;
        VAL:variable_y VAR:_sy ;
        VAL:variable_z VAR:_z ] ;
    VAL:right_side [
        VAL:priority "1" ;
        VAL:child [
            VAL:operation VAL:next_number ;
            VAL:variable_x VAR:_u ;
            VAL:variable_y VAR:_sy ] ] ;
    VAL:right_side [
        VAL:priority "2" ;
        VAL:child [
            VAL:operation VAL:add_number ;
            VAL:variable_x VAR:_sx ;
            VAL:variable_y VAR:_u ;
            VAL:variable_z VAR:_v ] ] ;
    VAL:right_side [
        VAL:priority "3" ;
        VAL:child [
            VAL:operation VAL:next_number ;
            VAL:variable_x VAR:_v ;
            VAL:variable_y VAR:_z ] ] ;
    VAL:priority "2" .

VAL:control_add_number_sx_y_sz
    VAL:type VAL:control ;
    VAL:left_side [
        VAL:operation VAL:add_number ;
        VAL:variable_x VAR:_sx ;
        VAL:variable_y VAR:_y ;
        VAL:variable_z VAR:_sz ] ;
    VAL:right_side [
        VAL:priority "1" ;
        VAL:child [
            VAL:operation VAL:next_number ;
            VAL:variable_x VAR:_u ;
            VAL:variable_y VAR:_sx ] ] ;
    VAL:right_side [
        VAL:priority "2" ;
        VAL:child [
            VAL:operation VAL:next_number ;
            VAL:variable_x VAR:_v ;
            VAL:variable_y VAR:_sz ] ] ;
    VAL:right_side [
        VAL:priority "3" ;
        VAL:child [
            VAL:operation VAL:add_number ;
            VAL:variable_x VAR:_y ;
            VAL:variable_y VAR:_u ;
            VAL:variable_z VAR:_v ] ] ;
    VAL:priority "2" .

VAL:control_add_number_x_sy_sz
    VAL:type VAL:control ;
    VAL:left_side [
        VAL:operation VAL:add_number ;
        VAL:variable_x VAR:_x ;
        VAL:variable_y VAR:_sy ;
        VAL:variable_z VAR:_sz ] ;
    VAL:right_side [
        VAL:priority "1" ;
        VAL:child [
            VAL:operation VAL:next_number ;
            VAL:variable_x VAR:_u ;
            VAL:variable_y VAR:_sy ] ] ;
    VAL:right_side [
        VAL:priority "2" ;
        VAL:child [
            VAL:operation VAL:next_number ;
            VAL:variable_x VAR:_v ;
            VAL:variable_y VAR:_sz ] ] ;
    VAL:right_side [
        VAL:priority "3" ;
        VAL:child [
            VAL:operation VAL:add_number ;
            VAL:variable_x VAR:_x ;
            VAL:variable_y VAR:_u ;
            VAL:variable_z VAR:_v ] ] ;
    VAL:priority "2" .

##################################################################
# applications

VAL:application_add_number_sx_sy_z
   VAL:type VAL:application ;
    VAL:program VAL:true ;
    VAL:pattern [
        VAL:operation VAL:add_number ;
        VAL:variable_x SOME:_x ;
        VAL:variable_y SOME:_y ;
        VAL:variable_z VAR:_z ] ;
    VAL:use [
        VAL:control VAL:control_add_number_x_1_z ;
        VAL:priority "1" ] ;
   VAL:use [
        VAL:control VAL:control_add_number_sx_sy_z ;
        VAL:priority "2" ] ;
    VAL:priority "1".

VAL:application_add_number_sx_y_sz
   VAL:type VAL:application ;
    VAL:program VAL:true ;
    VAL:pattern [
        VAL:operation VAL:add_number ;
        VAL:variable_x SOME:_x ;
        VAL:variable_y VAR:_y ;
        VAL:variable_z SOME:_z ] ;
    VAL:use [
        VAL:control VAL:control_add_number_1_y_z ;
        VAL:priority "1" ] ;
   VAL:use [
        VAL:control VAL:control_add_number_sx_y_sz ;
        VAL:priority "2" ] ;
    VAL:priority "1".

VAL:application_add_number_x_sy_sz
    VAL:type VAL:application ;
    VAL:program VAL:false ;
    VAL:pattern [
        VAL:operation VAL:add_number ;
        VAL:variable_x VAR:_x ;
        VAL:variable_y SOME:_y ;
        VAL:variable_z SOME:_z ] ;
    VAL:use [
        VAL:control VAL:control_add_number_x_1_z ;
        VAL:priority "1" ] ;
    VAL:use [
        VAL:control VAL:control_add_number_x_sy_sz ;
        VAL:priority "2" ] ;
    VAL:priority "2" .

Based on these argument dependent rule application, subtraction controls and applications are defines as follows:

##################################################################
# applications

VAL:application_subtract_number_sx_sy_z
    VAL:type VAL:application ;
    VAL:program VAL:false ;
    VAL:pattern [
        VAL:operation VAL:subtract_number ;
        VAL:variable_x SOME:_x ;
        VAL:variable_y SOME:_y ;
        VAL:variable_z VAR:_z ] ;
    VAL:use [
        VAL:control VAL:control_subtract_number_x_y_z ] .

VAL:application_subtract_number_sx_y_sz
    VAL:type VAL:application ;
    VAL:program VAL:false ;
    VAL:pattern [
        VAL:operation VAL:subtract_number ;
        VAL:variable_x SOME:_x ;
        VAL:variable_y VAR:_y ;
        VAL:variable_z SOME:_z ] ;
    VAL:use [
        VAL:control VAL:control_subtract_number_x_y_z ] .

VAL:application_subtract_number_x_sy_sz
    VAL:type VAL:application ;
    VAL:program VAL:false ;
    VAL:pattern [
        VAL:operation VAL:subtract_number ;
        VAL:variable_x VAR:_x ;
        VAL:variable_y SOME:_y ;
        VAL:variable_z SOME:_z ] ;
    VAL:use [
        VAL:control VAL:control_subtract_number_x_y_z ] .

-------------------------------------------------------
Introduction of list numbers

Symbolic numbers such as VAL:one are finite and cannot handle any numbers unless they are defined in next() predicates.

Therefore, a list representation of natural numbers (positive integers) is introduced.

A number 1 is represented with a list [1], and 23 with [3, 2]. The least significant digit is the first and the most significant digit last.

Since there are no direct method for handling a list in RDF, a list is constructed with cons operator.

A list [1] is cons(1, nil), where 1 is a symbolic number and nil represents empty.

The first argument of cons is a car element and the second argument is a cdr element as in Lisp.

A list [3, 2] is cons(3, cons(2, nil)).

To handle any number, cons() is assumed to be always declared as a fact, but in reality, it is not possible.

Therefore, each time query for cons(const, const) appears, the cons element is registered in the RDF graph and is returned as a fact.

This way, numbers with any size will be handled with Prolog.

Next, add, subtract, multiply, divide operations have been implemented.
