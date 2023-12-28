"""Test function call.
test_059_RdfProlog_function_100.py
Test for function call.
T. Masuda, 2023/12/21
"""

from src.RdfResolution import *

rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')


def test_answer_question1_solve_simultaneous_linear_equation():
    # solve_simultaneous_linear_equation(2, 3, 12, 1, 1, 5, ?ans1, ?ans2)
    my_question = f"""
       SELECT ?ans1 ?ans2 WHERE {{
       ?s <{OPERATION}> <{VAL}solve_simultaneous_linear_equation> .
       ?s <{VAL}variable_a11> <{VAL}2> .
       ?s <{VAL}variable_a12> <{VAL}3> .
       ?s <{VAL}variable_b1> <{VAL}12> .
       ?s <{VAL}variable_a21> <{VAL}1> .
       ?s <{VAL}variable_a22> <{VAL}1> .
       ?s <{VAL}variable_b2> <{VAL}5> .
       ?s <{VAL}variable_x1> ?ans1 .
       ?s <{VAL}variable_x2> ?ans2 .
       }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans1'] == f'{VAL}3'
    assert resolve_bindings[0]['?ans2'] == f'{VAL}2'


def test_answer_question2_solve_simultaneous_linear_equation():
    # solve_simultaneous_linear_equation(2, 3, 12, 1, 1, 5, ?ans1, ?ans2)
    my_question = f"""
       SELECT ?ans1 ?ans2 WHERE {{
       ?s <{OPERATION}> <{VAL}solve_simultaneous_linear_equation> .
       ?s <{VAL}variable_a11> <{VAL}3> .
       ?s <{VAL}variable_a12> <{VAL}2> .
       ?s <{VAL}variable_b1> <{VAL}22> .
       ?s <{VAL}variable_a21> <{VAL}2> .
       ?s <{VAL}variable_a22> <{VAL}1> .
       ?s <{VAL}variable_b2> <{VAL}13> .
       ?s <{VAL}variable_x1> ?ans1 .
       ?s <{VAL}variable_x2> ?ans2 .
       }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans1'] == f'{VAL}4'
    assert resolve_bindings[0]['?ans2'] == f'{VAL}5'


def test_answer_question3_solve_simultaneous_linear_equation():
    # solve_simultaneous_linear_equation(2, 3, 12, 1, 1, 5, ?ans1, ?ans2), add(?ans1, ?ans2, ?ans) .
    my_question = f"""
       SELECT ?ans ?ans1 ?ans2 WHERE {{
       ?s <{OPERATION}> <{VAL}solve_simultaneous_linear_equation> .
       ?s <{VAL}variable_a11> <{VAL}3> .
       ?s <{VAL}variable_a12> <{VAL}2> .
       ?s <{VAL}variable_b1> <{VAL}22> .
       ?s <{VAL}variable_a21> <{VAL}2> .
       ?s <{VAL}variable_a22> <{VAL}1> .
       ?s <{VAL}variable_b2> <{VAL}13> .
       ?s <{VAL}variable_x1> ?ans1 .
       ?s <{VAL}variable_x2> ?ans2 .
       ?s2 <{OPERATION}> <{VAL}add_number> .
       ?s2 <{VAL}variable_x> ?ans1 .
       ?s2 <{VAL}variable_y> ?ans2 .
       ?s2 <{VAL}variable_z> ?ans .
       }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans1'] == f'{VAL}4'
    assert resolve_bindings[0]['?ans2'] == f'{VAL}5'
    assert resolve_bindings[0]['?ans'] == f'{VAL}9'


def test_answer_question4_factorial():
    # factorial(4, ?ans) -> ?ans = 24
    my_question = f"""
       SELECT ?ans WHERE {{
       ?s <{OPERATION}> <{VAL}factorial> .
       ?s <{VAL}variable_x> <{VAL}4> .
       ?s <{VAL}variable_fact> ?ans .
       }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}24'
