"""
test_050_RdfProlog_list_numer.py
test for numbers represented as a list
T. Masuda, 2023/11/28
"""

from src.RdfResolution import *

rdf_prolog = RdfProlog(rules_folder='../rules/rules_list_number')


def test_list_next_1_ans():
    # next([1], ?ans) = [2]
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{ 
        ?s1 <{OPERATION}> <{VAL}next_list_number> . 
        ?s1 <{VAL}variable_x> <{VAL}list_one> . 
        ?s1 <{VAL}variable_y> ?ans . 
        ?s2 <{OPERATION}> <{VAL}cons> . 
        ?s2 <{VAL}variable_x> ?car . 
        ?s2 <{VAL}variable_y> ?cdr . 
        ?s2 <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}two'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


def test_list_next_2_ans():
    # next([2], ?ans) = [3]
    my_question = f"""
        SELECT ?list_three ?car ?cdr WHERE {{
        ?s1 <{OPERATION}> <{VAL}cons> .
        ?s1 <{VAL}variable_x> <{VAL}two> .
        ?s1 <{VAL}variable_y> <{VAL}nil> .
        ?s1 <{VAL}variable_z> ?list_two .
        ?s2 <{OPERATION}> <{VAL}next_list_number> .
        ?s2 <{VAL}variable_x> ?list_two .
        ?s2 <{VAL}variable_y> ?list_three .
        ?s3 <{OPERATION}> <{VAL}cons> .
        ?s3 <{VAL}variable_x> ?car .
        ?s3 <{VAL}variable_y> ?cdr .
        ?s3 <{VAL}variable_z> ?list_three .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}three'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


def test_list_next_9_ans():
    # next([9], ?ans) = [0 1] means 10
    my_question = f"""
        SELECT ?list_three ?car ?cdr WHERE {{
        ?s1 <{OPERATION}> <{VAL}cons> .
        ?s1 <{VAL}variable_x> <{VAL}nine> .
        ?s1 <{VAL}variable_y> <{VAL}nil> .
        ?s1 <{VAL}variable_z> ?list_nine .
        ?s2 <{OPERATION}> <{VAL}next_list_number> .
        ?s2 <{VAL}variable_x> ?list_nine .
        ?s2 <{VAL}variable_y> ?list_ten .
        ?s3 <{OPERATION}> <{VAL}cons> .
        ?s3 <{VAL}variable_x> ?car_ten .
        ?s3 <{VAL}variable_y> ?cdr_ten .
        ?s3 <{VAL}variable_z> ?list_ten .
        ?s4 <{OPERATION}> <{VAL}cons> .
        ?s4 <{VAL}variable_x> ?car .
        ?s4 <{VAL}variable_y> ?cdr .
        ?s4 <{VAL}variable_z> ?cdr_ten .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car_ten'] == f'{VAL}zero'
    assert resolve_bindings[0]['?car'] == f'{VAL}one'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


def test_list_next_99_ans():
    # next([9, 9], ?ans) = [0, 0, 1] means 100
    my_question = f"""
        SELECT ?car_one_hundred ?car ?cdr WHERE {{
        ?s1 <{OPERATION}> <{VAL}cons> .
        ?s1 <{VAL}variable_x> <{VAL}nine> .
        ?s1 <{VAL}variable_y> <{VAL}nil> .
        ?s1 <{VAL}variable_z> ?list_nine .
        ?s1b <{OPERATION}> <{VAL}cons> .
        ?s1b <{VAL}variable_x> <{VAL}nine> .
        ?s1b <{VAL}variable_y> ?list_nine .
        ?s1b <{VAL}variable_z> ?list_ninety_nine .
        ?s2 <{OPERATION}> <{VAL}next_list_number> .
        ?s2 <{VAL}variable_x> ?list_ninety_nine .
        ?s2 <{VAL}variable_y> ?list_one_hundred .
        ?s3 <{OPERATION}> <{VAL}cons> .
        ?s3 <{VAL}variable_x> ?car_one_hundred .
        ?s3 <{VAL}variable_y> ?cdr_one_hundred .
        ?s3 <{VAL}variable_z> ?list_one_hundred .
        ?s4 <{OPERATION}> <{VAL}cons> .
        ?s4 <{VAL}variable_x> ?car .
        ?s4 <{VAL}variable_y> ?cdr .
        ?s4 <{VAL}variable_z> ?cdr_one_hundred .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car_one_hundred'] == f'{VAL}zero'
    assert resolve_bindings[0]['?car'] == f'{VAL}zero'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}list_one'


def test_list_next_ans_2():
    # next(?ans, [2])
    my_question = f"""
        SELECT ?list_one ?car ?cdr WHERE {{
        ?s3 <{OPERATION}> <{VAL}cons> .
        ?s3 <{VAL}variable_x> <{VAL}two> .
        ?s3 <{VAL}variable_y> <{VAL}nil> .
        ?s3 <{VAL}variable_z> ?list_two .
        ?s2 <{OPERATION}> <{VAL}next_list_number> .
        ?s2 <{VAL}variable_x> ?list_one .
        ?s2 <{VAL}variable_y> ?list_two .
        ?s4 <{OPERATION}> <{VAL}cons> . 
        ?s4 <{VAL}variable_x> ?car . 
        ?s4 <{VAL}variable_y> ?cdr . 
        ?s4 <{VAL}variable_z> ?list_one . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?list_one'] == f'{VAL}list_one'
    assert resolve_bindings[0]['?car'] == f'{VAL}one'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


def test_list_next_ans_3():
    # next(?ans, [3])
    my_question = f"""
        SELECT ?list_two ?car ?cdr WHERE {{
        ?s1 <{OPERATION}> <{VAL}cons> . 
        ?s1 <{VAL}variable_x> <{VAL}two> . 
        ?s1 <{VAL}variable_y> <{VAL}nil> . 
        ?s1 <{VAL}variable_z> ?list_two_dummy . 
        ?s3 <{OPERATION}> <{VAL}cons> . 
        ?s3 <{VAL}variable_x> <{VAL}three> . 
        ?s3 <{VAL}variable_y> <{VAL}nil> . 
        ?s3 <{VAL}variable_z> ?list_three . 
        ?s2 <{OPERATION}> <{VAL}next_list_number> . 
        ?s2 <{VAL}variable_x> ?list_two . 
        ?s2 <{VAL}variable_y> ?list_three . 
        ?s4 <{OPERATION}> <{VAL}cons> . 
        ?s4 <{VAL}variable_x> ?car . 
        ?s4 <{VAL}variable_y> ?cdr . 
        ?s4 <{VAL}variable_z> ?list_two . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}two'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


if __name__ == '__main__':
    test_list_next_ans_3()
