"""
test_058_RdfProlog_fibonacci_number_100.py
tests for fibonacci numbers
T. Masuda, 2023/12/14
"""

from src.RdfResolution import *


rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')


def test_answer_question1_fibonacci_1_ans():
    # fibonacci(1, ?ans) ?ans = 1
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}fibonacci_number> . 
        ?s <{VAL}variable_x> <{VAL}1> . 
        ?s <{VAL}variable_y> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}1'


def test_answer_question2_fibonacci_2_ans():
    # divide(2, 1, ?ans) = 2
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <{OPERATION}> <{VAL}fibonacci_number> .
        ?s <{VAL}variable_x> <{VAL}2> .
        ?s <{VAL}variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}1'


def test_answer_question3_fibonacci_3_ans():
    # divide(1, 2, ?ans) = None
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}fibonacci_number> .
        ?s <{VAL}variable_x> <{VAL}3> .
        ?s <{VAL}variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}2'

def test_answer_question4_fibonacci_4_ans():
    # divide(2, 2, ?ans) = 1
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}fibonacci_number> .
        ?s <{VAL}variable_x> <{VAL}4> .
        ?s <{VAL}variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}3'


def test_answer_question4_fibonacci_5_ans():
    # divide(6, 2, ?ans) = 3
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}fibonacci_number> .
        ?s <{VAL}variable_x> <{VAL}5> .
        ?s <{VAL}variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}5'


def test_answer_question5_divide_6_ans():
    # divide(?ans, 2, 3)->ans:6
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}fibonacci_number> .
        ?s <{VAL}variable_x> <{VAL}6> .
        ?s <{VAL}variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=200)
    assert resolve_bindings[0]['?ans'] == f'{VAL}8'


def test_answer_complex_question1():
    # fibonacci(3, ?y), next(?y, ?ans)->y:2, ans:3
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}fibonacci_number> .
        ?s1 <{VAL}variable_x> <{VAL}3> .
        ?s1 <{VAL}variable_y> ?y .
        ?s2 <{OPERATION}> <{VAL}next_number> .
        ?s2 <{VAL}variable_x> ?y .
        ?s2 <{VAL}variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=20)
    assert resolve_bindings[0]['?ans'] == f'{VAL}3'
