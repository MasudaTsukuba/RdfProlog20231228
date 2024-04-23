"""
test_064_RdfProlog_list_number_math.py
tests for calculating list numbers
T. Masuda, 2023/12/15
"""

from src.RdfResolution import *

rdf_prolog = RdfProlog(rules_folder='../rules/rules_list_number_math')


def test_cons_5_list1_ans():
    # cons(5, list1, ?ans) ?ans = [5, 1]
    my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s1 <{OPERATION}> <{VAL}cons> .
            ?s1 <{VAL}variable_x> <{VAL}five> .
            ?s1 <{VAL}variable_y> <{VAL}list_one> .
            ?s1 <{VAL}variable_z> ?ans .
            ?s2 <{OPERATION}> <{VAL}cons> .
            ?s2 <{VAL}variable_x> ?car .
            ?s2 <{VAL}variable_y> ?cdr .
            ?s2 <{VAL}variable_z> ?ans .
            }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}five'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}list_one'

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
    # next([9], ?ans) = [0 1]
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

def test_list_next_9_ans0_next_ans0_ans():
    # next([9], ?ans0), next(?ans0, ?ans). ?ans = [1 1]
    my_question = f"""
        SELECT ?list_three ?car ?cdr WHERE {{
        ?s2 <{OPERATION}> <{VAL}next_list_number> . 
        ?s2 <{VAL}variable_x> <{VAL}list_nine> . 
        ?s2 <{VAL}variable_y> ?list_ten . 
        ?s3 <{OPERATION}> <{VAL}next_list_number> . 
        ?s3 <{VAL}variable_x> ?list_ten . 
        ?s3 <{VAL}variable_y> ?list_eleven . 
        ?s4 <{OPERATION}> <{VAL}cons> . 
        ?s4 <{VAL}variable_x> ?car_eleven . 
        ?s4 <{VAL}variable_y> ?cdr_eleven . 
        ?s4 <{VAL}variable_z> ?list_eleven . 
        ?s5 <{OPERATION}> <{VAL}cons> . 
        ?s5 <{VAL}variable_x> ?car . 
        ?s5 <{VAL}variable_y> ?cdr . 
        ?s5 <{VAL}variable_z> ?cdr_eleven . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car_eleven'] == f'{VAL}one'
    assert resolve_bindings[0]['?car'] == f'{VAL}one'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'

def test_list_next_ans_0():
    # next(?ans, [1])
    my_question = f"""
        SELECT ?list_one ?car ?cdr WHERE {{
        ?s3 <{OPERATION}> <{VAL}cons> . 
        ?s3 <{VAL}variable_x> <{VAL}zero> . 
        ?s3 <{VAL}variable_y> <{VAL}nil> . 
        ?s3 <{VAL}variable_z> ?list_zero . 
        ?s2 <{OPERATION}> <{VAL}next_list_number> . 
        ?s2 <{VAL}variable_x> ?list_minus1 . 
        ?s2 <{VAL}variable_y> ?list_zero . 
        ?s4 <{OPERATION}> <{VAL}cons> . 
        ?s4 <{VAL}variable_x> ?car . 
        ?s4 <{VAL}variable_y> ?cdr . 
        ?s4 <{VAL}variable_z> ?list_minus1 . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?list_zero'] == f'{VAL}list_zero'
    assert resolve_bindings[0]['?car'] == f'{VAL}minus_one'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


def test_list_next_ans_1():
    # next(?ans, [1])
    my_question = f"""
        SELECT ?list_one ?car ?cdr WHERE {{
        ?s3 <{OPERATION}> <{VAL}cons> . 
        ?s3 <{VAL}variable_x> <{VAL}one> . 
        ?s3 <{VAL}variable_y> <{VAL}nil> . 
        ?s3 <{VAL}variable_z> ?list_one . 
        ?s2 <{OPERATION}> <{VAL}next_list_number> . 
        ?s2 <{VAL}variable_x> ?list_zero . 
        ?s2 <{VAL}variable_y> ?list_one . 
        ?s4 <{OPERATION}> <{VAL}cons> . 
        ?s4 <{VAL}variable_x> ?car . 
        ?s4 <{VAL}variable_y> ?cdr . 
        ?s4 <{VAL}variable_z> ?list_zero . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    # assert resolve_bindings[0]['?list_zero'] == f'{VAL}list_zero'
    assert resolve_bindings[0]['?car'] == f'{VAL}zero'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


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


def test_add_1_1_ans():
    # add(1, 1, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <{OPERATION}> <{VAL}list_add> . 
        ?s <{VAL}variable_x> <{VAL}list_one> . 
        ?s <{VAL}variable_y> <{VAL}list_one> . 
        ?s <{VAL}variable_z> ?ans . 
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


def test_add_2_1_ans():
    # add(2, 1, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <{OPERATION}> <{VAL}list_add> . 
        ?s <{VAL}variable_x> <{VAL}list_two> . 
        ?s <{VAL}variable_y> <{VAL}list_one> . 
        ?s <{VAL}variable_z> ?ans . 
        ?s2 <{OPERATION}> <{VAL}cons> . 
        ?s2 <{VAL}variable_x> ?car . 
        ?s2 <{VAL}variable_y> ?cdr . 
        ?s2 <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}three'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


def test_add_1_2_ans():
    # add(1, 2, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <{OPERATION}> <{VAL}list_add> . 
        ?s <{VAL}variable_x> <{VAL}list_one> . 
        ?s <{VAL}variable_y> <{VAL}list_two> . 
        ?s <{VAL}variable_z> ?ans . 
        ?s2 <{OPERATION}> <{VAL}cons> . 
        ?s2 <{VAL}variable_x> ?car . 
        ?s2 <{VAL}variable_y> ?cdr . 
        ?s2 <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}three'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


def test_add_9_1_ans():
    # add(9, 1, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <{OPERATION}> <{VAL}list_add> . 
        ?s <{VAL}variable_x> <{VAL}list_nine> . 
        ?s <{VAL}variable_y> <{VAL}list_one> . 
        ?s <{VAL}variable_z> ?ans . 
        ?s2 <{OPERATION}> <{VAL}cons> . 
        ?s2 <{VAL}variable_x> ?car . 
        ?s2 <{VAL}variable_y> ?cdr . 
        ?s2 <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}zero'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}list_one'
    assert resolve_bindings[0]['?ans'] == f'{VAL}list_ten'


# def test_add_6_6_ans():
#     # add(6, 6, ?ans)
#     my_question = f"""
#         SELECT ?ans ?car ?cdr WHERE {{
#         ?s <{OPERATION}> <{VAL}list_add> .
#         ?s <{VAL}variable_x> <{VAL}list_six> .
#         ?s <{VAL}variable_y> <{VAL}list_six> .
#         ?s <{VAL}variable_z> ?ans .
#         ?s2 <{OPERATION}> <{VAL}cons> .
#         ?s2 <{VAL}variable_x> ?car .
#         ?s2 <{VAL}variable_y> ?cdr .
#         ?s2 <{VAL}variable_z> ?ans .
#         ?s3 <{OPERATION}> <{VAL}cons> .
#         ?s3 <{VAL}variable_x> ?cdar .
#         ?s3 <{VAL}variable_y> ?cddr .
#         ?s3 <{VAL}variable_z> ?cdr .
#         }}"""
#     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
#     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)
#     assert len(resolve_bindings) == 1
#     assert resolve_bindings[0]['?car'] == f'{VAL}two'
#     assert resolve_bindings[0]['?cdr'] == f'{VAL}list_one'


def test_add_2_ans_3():
    # add(2, ?ans, 3)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <{OPERATION}> <{VAL}list_add> . 
        ?s <{VAL}variable_x> <{VAL}list_two> . 
        ?s <{VAL}variable_y> ?ans . 
        ?s <{VAL}variable_z> <{VAL}list_three> . 
        ?s2 <{OPERATION}> <{VAL}cons> . 
        ?s2 <{VAL}variable_x> ?car . 
        ?s2 <{VAL}variable_y> ?cdr . 
        ?s2 <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}one'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


def test_add_ans_2_4():
    # add(?ans, 2, 4)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <{OPERATION}> <{VAL}list_add> . 
        ?s <{VAL}variable_x> ?ans . 
        ?s <{VAL}variable_y> <{VAL}list_two> . 
        ?s <{VAL}variable_z> <{VAL}list_four> . 
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


def test_subtract_4_2_ans():
    # subtract(4, 2, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <{OPERATION}> <{VAL}list_subtract> . 
        ?s <{VAL}variable_x> <{VAL}list_four> . 
        ?s <{VAL}variable_y> <{VAL}list_two> . 
        ?s <{VAL}variable_z> ?ans . 
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


def test_subtract_4_ans_1():
    # subtract(4, ?ans, 1)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <{OPERATION}> <{VAL}list_subtract> . 
        ?s <{VAL}variable_x> <{VAL}list_four> . 
        ?s <{VAL}variable_y> ?ans . 
        ?s <{VAL}variable_z> <{VAL}list_one> . 
        ?s2 <{OPERATION}> <{VAL}cons> . 
        ?s2 <{VAL}variable_x> ?car . 
        ?s2 <{VAL}variable_y> ?cdr . 
        ?s2 <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}three'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


def test_subtract_ans_5_2():
    # subtract(?ans, 5, 2)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <{OPERATION}> <{VAL}list_subtract> . 
        ?s <{VAL}variable_x> ?ans . 
        ?s <{VAL}variable_y> <{VAL}list_five> . 
        ?s <{VAL}variable_z> <{VAL}list_two> . 
        ?s2 <{OPERATION}> <{VAL}cons> . 
        ?s2 <{VAL}variable_x> ?car . 
        ?s2 <{VAL}variable_y> ?cdr . 
        ?s2 <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}seven'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


def test_multiply_2_1_ans():
    # multiply(2, 1, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <{OPERATION}> <{VAL}list_multiply> . 
        ?s <{VAL}variable_x> <{VAL}list_two> . 
        ?s <{VAL}variable_y> <{VAL}list_one> . 
        ?s <{VAL}variable_z> ?ans . 
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


# def test_multiply_3_2_ans():
#     # multiply(3, 2, ?ans) -> ?ans = 6
#     my_question = f"""
#         SELECT ?ans ?car ?cdr WHERE {{
#         ?s <{OPERATION}> <{VAL}list_multiply> .
#         ?s <{VAL}variable_x> <{VAL}list_three> .
#         ?s <{VAL}variable_y> <{VAL}list_two> .
#         ?s <{VAL}variable_z> ?ans .
#         ?s2 <{OPERATION}> <{VAL}cons> .
#         ?s2 <{VAL}variable_x> ?car .
#         ?s2 <{VAL}variable_y> ?cdr .
#         ?s2 <{VAL}variable_z> ?ans .
#         }}"""
#     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
#     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=60)
#     assert len(resolve_bindings) == 1
#     assert resolve_bindings[0]['?car'] == f'{VAL}six'
#     assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


# def test_multiply_3_ans_9():
#     # multiply(3, ?ans, 9) -> ?ans = 3
#     my_question = f"""
#         SELECT ?ans ?car ?cdr WHERE {{
#         ?s <{OPERATION}> <{VAL}list_multiply> .
#         ?s <{VAL}variable_x> <{VAL}list_three> .
#         ?s <{VAL}variable_y> ?ans .
#         ?s <{VAL}variable_z> <{VAL}list_nine> .
#         ?s2 <{OPERATION}> <{VAL}cons> .
#         ?s2 <{VAL}variable_x> ?car .
#         ?s2 <{VAL}variable_y> ?cdr .
#         ?s2 <{VAL}variable_z> ?ans .
#         }}"""
#     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
#     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=150)
#     assert len(resolve_bindings) == 1
#     assert resolve_bindings[0]['?car'] == f'{VAL}three'
#     assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


# def test_divide_4_2_ans():
#     # divide(4, 2, ?ans)
#     my_question = f"""
#         SELECT ?ans ?car ?cdr WHERE {{
#         ?s <{OPERATION}> <{VAL}list_divide> .
#         ?s <{VAL}variable_x> <{VAL}list_four> .
#         ?s <{VAL}variable_y> <{VAL}list_two> .
#         ?s <{VAL}variable_z> ?ans .
#         ?s2 <{OPERATION}> <{VAL}cons> .
#         ?s2 <{VAL}variable_x> ?car .
#         ?s2 <{VAL}variable_y> ?cdr .
#         ?s2 <{VAL}variable_z> ?ans .
#         }}"""
#     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
#     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=200)
#     assert len(resolve_bindings) == 1
#     assert resolve_bindings[0]['?car'] == f'{VAL}two'
#     assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


# def test_divide_5_1_ans():
#     # divide(5, 1, ?ans)
#     my_question = f"""
#         SELECT ?ans ?car ?cdr WHERE {{
#         ?s <{OPERATION}> <{VAL}list_divide> .
#         ?s <{VAL}variable_x> <{VAL}list_five> .
#         ?s <{VAL}variable_y> <{VAL}list_one> .
#         ?s <{VAL}variable_z> ?ans .
#         ?s2 <{OPERATION}> <{VAL}cons> .
#         ?s2 <{VAL}variable_x> ?car .
#         ?s2 <{VAL}variable_y> ?cdr .
#         ?s2 <{VAL}variable_z> ?ans .
#         }}"""
#     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
#     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=200)
#     assert len(resolve_bindings) == 1
#     assert resolve_bindings[0]['?car'] == f'{VAL}five'
#     assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


# def test_divide_5_2_ans():
#     # divide(5, 2, ?ans)
#     my_question = f"""
#         SELECT ?ans ?car ?cdr WHERE {{
#         ?s <{OPERATION}> <{VAL}list_divide> .
#         ?s <{VAL}variable_x> <{VAL}list_five> .
#         ?s <{VAL}variable_y> <{VAL}list_two> .
#         ?s <{VAL}variable_z> ?ans .
#         }}"""
#     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
#     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=200)
#     assert len(resolve_bindings) == 0


# def test_divide_6_2_ans():
#     # divide(6, 2, ?ans) -> ?ans = [3]
#     my_question = f"""
#         SELECT ?ans ?car ?cdr WHERE {{
#         ?s1 <{OPERATION}> <{VAL}cons> .
#         ?s1 <{VAL}variable_x> <{VAL}six> .
#         ?s1 <{VAL}variable_y> <{VAL}nil> .
#         ?s1 <{VAL}variable_z> ?list_6 .
#         ?s2 <{OPERATION}> <{VAL}list_divide> .
#         ?s2 <{VAL}variable_x> ?list_6 .
#         ?s2 <{VAL}variable_y> <{VAL}list_two> .
#         ?s2 <{VAL}variable_z> ?ans .
#         }}"""
#     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
#     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=200)
#     assert len(resolve_bindings) == 1
#     assert resolve_bindings[0]['?ans'] == f'{VAL}list_three'


def test_fibonacci_1_ans():
    # fibinacci(1, ?ans) -> ?ans = 1
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <{OPERATION}> <{VAL}fibonacci_number> .
        ?s <{VAL}variable_x> <{VAL}list_one> .
        ?s <{VAL}variable_y> ?ans .
        ?s2 <{OPERATION}> <{VAL}cons> .
        ?s2 <{VAL}variable_x> ?car .
        ?s2 <{VAL}variable_y> ?cdr .
        ?s2 <{VAL}variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}one'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


def test_fibonacci_2_ans():
    # fibinacci(2, ?ans) -> ?ans = 1
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <{OPERATION}> <{VAL}fibonacci_number> .
        ?s <{VAL}variable_x> <{VAL}list_two> .
        ?s <{VAL}variable_y> ?ans .
        ?s2 <{OPERATION}> <{VAL}cons> .
        ?s2 <{VAL}variable_x> ?car .
        ?s2 <{VAL}variable_y> ?cdr .
        ?s2 <{VAL}variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == f'{VAL}one'
    assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'


# def test_fibonacci_3_ans():
#     # fibinacci(3, ?ans) -> ?ans = 2
#     my_question = f"""
#         SELECT ?ans ?car ?cdr WHERE {{
#         ?s <{OPERATION}> <{VAL}fibonacci_number> .
#         ?s <{VAL}variable_x> <{VAL}list_three> .
#         ?s <{VAL}variable_y> ?ans .
#         ?s2 <{OPERATION}> <{VAL}cons> .
#         ?s2 <{VAL}variable_x> ?car .
#         ?s2 <{VAL}variable_y> ?cdr .
#         ?s2 <{VAL}variable_z> ?ans .
#         }}"""
#     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
#     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=200)
#     assert len(resolve_bindings) == 1
#     assert resolve_bindings[0]['?car'] == f'{VAL}two'
#     assert resolve_bindings[0]['?cdr'] == f'{VAL}nil'
