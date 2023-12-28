"""
test_042_RdfProlog_add_number.py
tests for add symbolic numbers
T. Masuda, 2023/11/28
"""

from src.RdfResolution import *


rdf_prolog = RdfProlog(rules_folder='../rules/rules_number')


def test_answer_question1_add_3_1():
    # add(3, 1, ?ans) = 4
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}add_number> . 
        ?s <{VAL}variable_x> <{VAL}three> . 
        ?s <{VAL}variable_y> <{VAL}one> . 
        ?s <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}four'


def test_answer_question2_add_2_2_ans():
    # add(2, 2, ?ans) = 4
    my_question = f"""
        SELECT ?ans WHERE {{ ?s <{OPERATION}> <{VAL}add_number> . 
        ?s <{VAL}variable_x> <{VAL}two> . 
        ?s <{VAL}variable_y> <{VAL}two> . 
        ?s <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}four'


def test_answer_question3_add_3_2_ans():
    # add(3, 2, ?ans) = 5
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}add_number> . 
        ?s <{VAL}variable_x> <{VAL}three> . 
        ?s <{VAL}variable_y> <{VAL}two> . 
        ?s <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}five'


def test_answer_question4_add_3_ans_5():
    # add(3, ?ans, 5)->ans:2
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}add_number> . 
        ?s <{VAL}variable_x> <{VAL}three> . 
        ?s <{VAL}variable_y> ?ans . 
        ?s <{VAL}variable_z> <{VAL}five> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}two'


def test_answer_question4b_add_2_ans_3():
    # add(2, ?ans, 3)->ans:1
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}add_number> . 
        ?s <{VAL}variable_x> <{VAL}two> . 
        ?s <{VAL}variable_y> ?ans . 
        ?s <{VAL}variable_z> <{VAL}three> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=10)
    assert resolve_bindings[0]['?ans'] == f'{VAL}one'


def test_answer_complex_question1():
    # add(3, 2, ?z), next(?z, ?ans)->z:5, ans:6
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}add_number> . 
        ?s1 <{VAL}variable_x> <{VAL}three> . 
        ?s1 <{VAL}variable_y> <{VAL}two> . 
        ?s1 <{VAL}variable_z> ?z . 
        ?s2 <{OPERATION}> <{VAL}next_number> . 
        ?s2 <{VAL}variable_x> ?z . 
        ?s2 <{VAL}variable_y> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)  # ###################
    assert resolve_bindings[0]['?ans'] == f'{VAL}six'


def test_answer_complex_question2():
    # add(3, 2, ?z), add(?z, 2, ?ans)->z:5, ans:7
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}add_number> . 
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
    assert resolve_bindings[0]['?ans'] == f'{VAL}seven'


def test_add_1_y_z():
    # add(1, ?y, ?z)->(1,2),(2,3),...,(9,10)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}add_number> . 
        ?s <{VAL}variable_x> <{VAL}one> . 
        ?s <{VAL}variable_y> ?y . 
        ?s <{VAL}variable_z> ?z . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10, depth_limit=30)
    assert len(resolve_bindings) == 9


def test_add_9_y_z():
    # add(9, ?y, ?z)->(1,10)
    my_question = f"""
        SELECT ?y ?z WHERE {{
        ?s <{OPERATION}> <{VAL}add_number> . 
        ?s <{VAL}variable_x> <{VAL}nine> . 
        ?s <{VAL}variable_y> ?y . 
        ?s <{VAL}variable_z> ?z . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10, depth_limit=20)
    assert resolve_bindings[0]['?y'] == f'{VAL}one'
    assert resolve_bindings[0]['?z'] == f'{VAL}ten'


def test_add_x_1_z():
    # add(?x, 1, ?z)->(1,2),(2,3),...,(9,10)
    my_question = f"""
        SELECT ?x ?z WHERE {{
        ?s <{OPERATION}> <{VAL}add_number> . 
        ?s <{VAL}variable_x> ?x . 
        ?s <{VAL}variable_y> <{VAL}one> . 
        ?s <{VAL}variable_z> ?z . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10)
    assert len(resolve_bindings) == 9


def test_add_x_9_z():
    # add(?x, 9, ?z)->(1,10)
    my_question = f"""
        SELECT ?x ?z WHERE {{
        ?s <{OPERATION}> <{VAL}add_number> . 
        ?s <{VAL}variable_x> ?x . 
        ?s <{VAL}variable_y> <{VAL}nine> . 
        ?s <{VAL}variable_z> ?z . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10)
    assert resolve_bindings[0]['?x'] == f'{VAL}one'
    assert resolve_bindings[0]['?z'] == f'{VAL}ten'


def test_add_x_y_2():
    # add(?x, ?y, 2)->(1,1)
    my_question = f"""
        SELECT ?x ?y WHERE {{
        ?s <{OPERATION}> <{VAL}add_number> . 
        ?s <{VAL}variable_x> ?x . 
        ?s <{VAL}variable_y> ?y . 
        ?s <{VAL}variable_z> <{VAL}two> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10)
    assert resolve_bindings[0]['?x'] == f'{VAL}one'
    assert resolve_bindings[0]['?y'] == f'{VAL}one'


def test_add_x_y_3():
    # add(?x, ?y, 3)->(1,2),(2,1)
    my_question = f"""
        SELECT ?x ?y WHERE {{
        ?s <{OPERATION}> <{VAL}add_number> . 
        ?s <{VAL}variable_x> ?x . 
        ?s <{VAL}variable_y> ?y . 
        ?s <{VAL}variable_z> <{VAL}three> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10, depth_limit=10)
    assert len(resolve_bindings) == 2


def test_depth_limit_add_3_1_ans():
    # add(3, 1, ?ans) depth_limit=0
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}add_number> . 
        ?s <{VAL}variable_x> <{VAL}three> . 
        ?s <{VAL}variable_y> <{VAL}one> . 
        ?s <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=1)
    assert len(resolve_bindings) == 0


def test_depth_limit_add_3_1_ans_2():
    # add(3, 1, ?ans) depth_limit=1
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}add_number> . 
        ?s <{VAL}variable_x> <{VAL}three> . 
        ?s <{VAL}variable_y> <{VAL}one> . 
        ?s <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=2)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?ans'] == f'{VAL}four'
