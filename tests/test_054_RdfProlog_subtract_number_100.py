"""
test_054_RdfProlog_subtract_number_100.py
tests for subtracting uri numbers
T. Masuda, 2023/12/11
"""

from src.RdfResolution import *


rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')


def test_answer_question1_3_minus_1():
    # subtract(3, 1, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}subtract_number> . 
        ?s <{VAL}variable_x> <{VAL}3> . 
        ?s <{VAL}variable_y> <{VAL}1> . 
        ?s <{VAL}variable_z> ?ans . 
        }}
        """
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}2'


def test_answer_question2_4_minus_2():
    # subtract(4, 2, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{ ?s <{OPERATION}> <{VAL}subtract_number> .
        ?s <{VAL}variable_x> <{VAL}4> .
        ?s <{VAL}variable_y> <{VAL}2> .
        ?s <{VAL}variable_z> ?ans .
        }} """
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}2'


def test_answer_question3_3_minus_2():
    # # subtract(3, 2, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}subtract_number> .
        ?s <{VAL}variable_x> <{VAL}3> .
        ?s <{VAL}variable_y> <{VAL}2> .
        ?s <{VAL}variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=10)
    assert resolve_bindings[0]['?ans'] == f'{VAL}1'


def test_answer_question3b_next_of_5_minus_2():
    # subtract(5, 2, ?z), next(?z, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}subtract_number> .
        ?s1 <{VAL}variable_x> <{VAL}5> .
        ?s1 <{VAL}variable_y> <{VAL}2> .
        ?s1 <{VAL}variable_z> ?z .
        ?s2 <{OPERATION}> <{VAL}next_number> .
        ?s2 <{VAL}variable_x> ?z .
        ?s2 <{VAL}variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}4'


def test_answer_question_5_minus_ans_equals_2():
    # subtract(5, ?ans, 2)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}subtract_number> .
        ?s <{VAL}variable_x> <{VAL}5> .
        ?s <{VAL}variable_y> ?ans .
        ?s <{VAL}variable_z> <{VAL}2> .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}3'


def test_answer_complex_question_5_minus_2_next():
    # subtract(5, 2, ?z), next(?z, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}subtract_number> .
        ?s1 <{VAL}variable_x> <{VAL}5> .
        ?s1 <{VAL}variable_y> <{VAL}2> .
        ?s1 <{VAL}variable_z> ?z .
        ?s2 <{OPERATION}> <{VAL}next_number> .
        ?s2 <{VAL}variable_x> ?z .
        ?s2 <{VAL}variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)  # ###################
    assert resolve_bindings[0]['?ans'] == f'{VAL}4'


def test_answer_complex_question_3_minus_2_plus_2():
    # subtract(3, 2, ?z), add(?z, 2, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}subtract_number> .
        ?s1 <{VAL}variable_x> <{VAL}3> .
        ?s1 <{VAL}variable_y> <{VAL}2> .
        ?s1 <{VAL}variable_z> ?z .
        ?s2 <{OPERATION}> <{VAL}add_number> .
        ?s2 <{VAL}variable_x> ?z .
        ?s2 <{VAL}variable_y> <{VAL}2> .
        ?s2 <{VAL}variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)  # ###################
    assert resolve_bindings[0]['?ans'] == f'{VAL}3'
