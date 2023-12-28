"""
test_044_RdfProlog_subtract_number.py
tests for subtracting symbolic numbers
T. Masuda, 2023/10/30
"""

from src.RdfResolution import *


rdf_prolog = RdfProlog(rules_folder='../rules/rules_number')


def test_answer_question1_3_minus_1():
    # subtract(3, 1, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}subtract_number> . 
        ?s <{VAL}variable_x> <{VAL}three> . 
        ?s <{VAL}variable_y> <{VAL}one> . 
        ?s <{VAL}variable_z> ?ans . 
        }}
        """
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}two'


def test_answer_question2_4_minus_2():
    # subtract(4, 2, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{ ?s <{OPERATION}> <{VAL}subtract_number> .
        ?s <{VAL}variable_x> <{VAL}four> .
        ?s <{VAL}variable_y> <{VAL}two> .
        ?s <{VAL}variable_z> ?ans .
        }} """
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}two'


def test_answer_question3_3_minus_2():
    # # subtract(3, 2, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}subtract_number> .
        ?s <{VAL}variable_x> <{VAL}three> .
        ?s <{VAL}variable_y> <{VAL}two> .
        ?s <{VAL}variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=10)
    assert resolve_bindings[0]['?ans'] == f'{VAL}one'


def test_answer_question3b_next_of_5_minus_2():
    # subtract(5, 2, ?z), next(?z, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}subtract_number> .
        ?s1 <{VAL}variable_x> <{VAL}five> .
        ?s1 <{VAL}variable_y> <{VAL}two> .
        ?s1 <{VAL}variable_z> ?z .
        ?s2 <{OPERATION}> <{VAL}next_number> .
        ?s2 <{VAL}variable_x> ?z .
        ?s2 <{VAL}variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}four'


def test_answer_question_5_minus_ans_equals_2():
    # subtract(5, ?ans, 2)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}subtract_number> .
        ?s <{VAL}variable_x> <{VAL}five> .
        ?s <{VAL}variable_y> ?ans .
        ?s <{VAL}variable_z> <{VAL}two> .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}three'


def test_answer_complex_question_5_minus_2_next():
    # subtract(5, 2, ?z), next(?z, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}subtract_number> .
        ?s1 <{VAL}variable_x> <{VAL}five> .
        ?s1 <{VAL}variable_y> <{VAL}two> .
        ?s1 <{VAL}variable_z> ?z .
        ?s2 <{OPERATION}> <{VAL}next_number> .
        ?s2 <{VAL}variable_x> ?z .
        ?s2 <{VAL}variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)  # ###################
    assert resolve_bindings[0]['?ans'] == f'{VAL}four'


def test_answer_complex_question_3_minus_2_plus_2():
    # subtract(3, 2, ?z), add(?z, 2, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}subtract_number> .
        ?s1 <{VAL}variable_x> <{VAL}three> .
        ?s1 <{VAL}variable_y> <{VAL}two> .
        ?s1 <{VAL}variable_z> ?z .
        ?s2 <{OPERATION}> <{VAL}add_number> .
        ?s2 <{VAL}variable_x> ?z .
        ?s2 <{VAL}variable_y> <{VAL}two> .
        ?s2 <{VAL}variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)  # ###################
    assert resolve_bindings[0]['?ans'] == f'{VAL}three'
