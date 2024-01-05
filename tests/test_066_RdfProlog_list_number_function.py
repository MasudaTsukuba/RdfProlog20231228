"""
test_066_RdfProlog_list_number_function.py
tests for function call of list numbers
T. Masuda, 2024/1/5
"""

from src.RdfResolution import *

rdf_prolog = RdfProlog(rules_folder='../rules/rules_list_number_math')


def test_function_cons_3_list2_ans():
    # function_cons()
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}function_cons> . 
        ?s1 <{VAL}variable_x> <{VAL}three> . 
        ?s1 <{VAL}variable_y> <{VAL}list_two> . 
        ?s1 <{VAL}variable_z> ?ans . 
        ?s2 <{OPERATION}> <{VAL}cons> . 
        ?s2 <{VAL}variable_x> ?car . 
        ?s2 <{VAL}variable_y> ?cdr . 
        ?s2 <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}three'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}list_two'


def test_function_add_list3_list2_ans():
    # function_add()
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}function_add> . 
        ?s1 <{VAL}variable_x> <{VAL}list_three> . 
        ?s1 <{VAL}variable_y> <{VAL}list_two> . 
        ?s1 <{VAL}variable_z> ?ans . 
        ?s2 <{OPERATION}> <{VAL}cons> . 
        ?s2 <{VAL}variable_x> ?car . 
        ?s2 <{VAL}variable_y> ?cdr . 
        ?s2 <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=300)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}five'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


def test_function_add_list7_list9_ans():
    # function_add()
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}function_add> . 
        ?s1 <{VAL}variable_x> <{VAL}list_seven> . 
        ?s1 <{VAL}variable_y> <{VAL}list_nine> . 
        ?s1 <{VAL}variable_z> ?ans . 
        ?s2 <{OPERATION}> <{VAL}cons> . 
        ?s2 <{VAL}variable_x> ?car . 
        ?s2 <{VAL}variable_y> ?cdr . 
        ?s2 <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=300)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}six'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}list_one'


def test_function_add_list17_list19_ans():
    # function_add()
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s3 <{OPERATION}> <{VAL}cons> . 
        ?s3 <{VAL}variable_x> <{VAL}seven> . 
        ?s3 <{VAL}variable_y> <{VAL}list_one> . 
        ?s3 <{VAL}variable_z> ?list_seventeen . 
        ?s4 <{OPERATION}> <{VAL}cons> . 
        ?s4 <{VAL}variable_x> <{VAL}nine> . 
        ?s4 <{VAL}variable_y> <{VAL}list_one> . 
        ?s4 <{VAL}variable_z> ?list_nineteen . 
        ?s1 <{OPERATION}> <{VAL}function_add> . 
        ?s1 <{VAL}variable_x> ?list_seventeen . 
        ?s1 <{VAL}variable_y> ?list_nineteen . 
        ?s1 <{VAL}variable_z> ?ans . 
        ?s2 <{OPERATION}> <{VAL}cons> . 
        ?s2 <{VAL}variable_x> ?car . 
        ?s2 <{VAL}variable_y> ?cdr . 
        ?s2 <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=300)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}six'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}list_three'


def test_function_add_list27_list39_ans():
    # function_add()
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s3 <{OPERATION}> <{VAL}cons> . 
        ?s3 <{VAL}variable_x> <{VAL}seven> . 
        ?s3 <{VAL}variable_y> <{VAL}list_two> . 
        ?s3 <{VAL}variable_z> ?list_27 . 
        ?s4 <{OPERATION}> <{VAL}cons> . 
        ?s4 <{VAL}variable_x> <{VAL}nine> . 
        ?s4 <{VAL}variable_y> <{VAL}list_three> . 
        ?s4 <{VAL}variable_z> ?list_39 . 
        ?s1 <{OPERATION}> <{VAL}function_add> . 
        ?s1 <{VAL}variable_x> ?list_27 . 
        ?s1 <{VAL}variable_y> ?list_39 . 
        ?s1 <{VAL}variable_z> ?ans . 
        ?s2 <{OPERATION}> <{VAL}cons> . 
        ?s2 <{VAL}variable_x> ?car . 
        ?s2 <{VAL}variable_y> ?cdr . 
        ?s2 <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=300)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}six'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}list_six'


def test_function_multiply_list3_list2_ans():
    # function_add()
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}function_multiply> . 
        ?s1 <{VAL}variable_x> <{VAL}list_three> . 
        ?s1 <{VAL}variable_y> <{VAL}list_two> . 
        ?s1 <{VAL}variable_z> ?ans . 
        ?s2 <{OPERATION}> <{VAL}cons> . 
        ?s2 <{VAL}variable_x> ?car . 
        ?s2 <{VAL}variable_y> ?cdr . 
        ?s2 <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=300)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}six'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


def test_function_multiply_list3_list6_ans():
    # function_add()
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}function_multiply> . 
        ?s1 <{VAL}variable_x> <{VAL}list_three> . 
        ?s1 <{VAL}variable_y> <{VAL}list_six> . 
        ?s1 <{VAL}variable_z> ?ans . 
        ?s2 <{OPERATION}> <{VAL}cons> . 
        ?s2 <{VAL}variable_x> ?car . 
        ?s2 <{VAL}variable_y> ?cdr . 
        ?s2 <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=300)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}eight'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}list_one'
