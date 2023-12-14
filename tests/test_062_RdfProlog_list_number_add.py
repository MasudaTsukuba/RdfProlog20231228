"""
test_062_RdfProlog_list_number_add.py
tests for adding list numbers
T. Masuda, 2023/11/28
"""

from src.RdfPrologMain import RdfProlog, ClassSparqlQuery

rdf_prolog = RdfProlog(rules_folder='../rules/rules_list_number_add')


def test_list_next_1_ans():
    # next([1], ?ans) = [2]
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s1 <http://value.org/operation> <http://value.org/next_list_number> .
        ?s1 <http://value.org/variable_x> <http://value.org/list_one> .
        ?s1 <http://value.org/variable_y> ?ans .
        ?s2 <http://value.org/operation> <http://value.org/cons> .
        ?s2 <http://value.org/variable_x> ?car .
        ?s2 <http://value.org/variable_y> ?cdr .
        ?s2 <http://value.org/variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == 'http://value.org/two'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_list_next_2_ans():
    # next([2], ?ans) = [3]
    my_question = f"""
        SELECT ?list_three ?car ?cdr WHERE {{
        ?s1 <http://value.org/operation> <http://value.org/cons> .
        ?s1 <http://value.org/variable_x> <http://value.org/two> .
        ?s1 <http://value.org/variable_y> <http://value.org/nil> .
        ?s1 <http://value.org/variable_z> ?list_two .
        ?s2 <http://value.org/operation> <http://value.org/next_list_number> .
        ?s2 <http://value.org/variable_x> ?list_two .
        ?s2 <http://value.org/variable_y> ?list_three .
        ?s3 <http://value.org/operation> <http://value.org/cons> .
        ?s3 <http://value.org/variable_x> ?car . 
        ?s3 <http://value.org/variable_y> ?cdr . 
        ?s3 <http://value.org/variable_z> ?list_three . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == 'http://value.org/three'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_list_next_9_ans():
    # next([9], ?ans) = [0 1]
    my_question = f"""
        SELECT ?list_three ?car ?cdr WHERE {{
        ?s1 <http://value.org/operation> <http://value.org/cons> . 
        ?s1 <http://value.org/variable_x> <http://value.org/nine> . 
        ?s1 <http://value.org/variable_y> <http://value.org/nil> . 
        ?s1 <http://value.org/variable_z> ?list_nine . 
        ?s2 <http://value.org/operation> <http://value.org/next_list_number> . 
        ?s2 <http://value.org/variable_x> ?list_nine . 
        ?s2 <http://value.org/variable_y> ?list_ten . 
        ?s3 <http://value.org/operation> <http://value.org/cons> . 
        ?s3 <http://value.org/variable_x> ?car_ten . 
        ?s3 <http://value.org/variable_y> ?cdr_ten . 
        ?s3 <http://value.org/variable_z> ?list_ten . 
        ?s4 <http://value.org/operation> <http://value.org/cons> . 
        ?s4 <http://value.org/variable_x> ?car . 
        ?s4 <http://value.org/variable_y> ?cdr . 
        ?s4 <http://value.org/variable_z> ?cdr_ten . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car_ten'] == 'http://value.org/zero'
    assert resolve_bindings[0]['?car'] == 'http://value.org/one'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_list_next_ans_2():
    # next(?ans, [2])
    my_question = f"""
        SELECT ?list_one ?car ?cdr WHERE {{
        ?s3 <http://value.org/operation> <http://value.org/cons> . 
        ?s3 <http://value.org/variable_x> <http://value.org/two> . 
        ?s3 <http://value.org/variable_y> <http://value.org/nil> . 
        ?s3 <http://value.org/variable_z> ?list_two . 
        ?s2 <http://value.org/operation> <http://value.org/next_list_number> . 
        ?s2 <http://value.org/variable_x> ?list_one . 
        ?s2 <http://value.org/variable_y> ?list_two . 
        ?s4 <http://value.org/operation> <http://value.org/cons> . 
        ?s4 <http://value.org/variable_x> ?car . 
        ?s4 <http://value.org/variable_y> ?cdr . 
        ?s4 <http://value.org/variable_z> ?list_one . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?list_one'] == 'http://value.org/list_one'
    assert resolve_bindings[0]['?car'] == 'http://value.org/one'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_list_next_ans_3():
    # next(?ans, [3])
    my_question = f"""
        SELECT ?list_two ?car ?cdr WHERE {{
        ?s1 <http://value.org/operation> <http://value.org/cons> . 
        ?s1 <http://value.org/variable_x> <http://value.org/two> . 
        ?s1 <http://value.org/variable_y> <http://value.org/nil> . 
        ?s1 <http://value.org/variable_z> ?list_two_dummy . 
        ?s3 <http://value.org/operation> <http://value.org/cons> . 
        ?s3 <http://value.org/variable_x> <http://value.org/three> . 
        ?s3 <http://value.org/variable_y> <http://value.org/nil> . 
        ?s3 <http://value.org/variable_z> ?list_three . 
        ?s2 <http://value.org/operation> <http://value.org/next_list_number> . 
        ?s2 <http://value.org/variable_x> ?list_two . 
        ?s2 <http://value.org/variable_y> ?list_three . 
        ?s4 <http://value.org/operation> <http://value.org/cons> . 
        ?s4 <http://value.org/variable_x> ?car . 
        ?s4 <http://value.org/variable_y> ?cdr . 
        ?s4 <http://value.org/variable_z> ?list_two . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == 'http://value.org/two'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_add_1_1_ans():
    # add(1, 1, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_add> . 
        ?s <http://value.org/variable_x> <http://value.org/list_one> . 
        ?s <http://value.org/variable_y> <http://value.org/list_one> . 
        ?s <http://value.org/variable_z> ?ans . 
        ?s2 <http://value.org/operation> <http://value.org/cons> . 
        ?s2 <http://value.org/variable_x> ?car . 
        ?s2 <http://value.org/variable_y> ?cdr . 
        ?s2 <http://value.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == 'http://value.org/two'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_add_2_1_ans():
    # add(2, 1, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_add> . 
        ?s <http://value.org/variable_x> <http://value.org/list_two> . 
        ?s <http://value.org/variable_y> <http://value.org/list_one> . 
        ?s <http://value.org/variable_z> ?ans . 
        ?s2 <http://value.org/operation> <http://value.org/cons> . 
        ?s2 <http://value.org/variable_x> ?car . 
        ?s2 <http://value.org/variable_y> ?cdr . 
        ?s2 <http://value.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == 'http://value.org/three'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_add_1_2_ans():
    # add(1, 2, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_add> . 
        ?s <http://value.org/variable_x> <http://value.org/list_one> . 
        ?s <http://value.org/variable_y> <http://value.org/list_two> . 
        ?s <http://value.org/variable_z> ?ans . 
        ?s2 <http://value.org/operation> <http://value.org/cons> . 
        ?s2 <http://value.org/variable_x> ?car . 
        ?s2 <http://value.org/variable_y> ?cdr . 
        ?s2 <http://value.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == 'http://value.org/three'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_add_9_1_ans():
    # add(9, 1, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_add> . 
        ?s <http://value.org/variable_x> <http://value.org/list_nine> . 
        ?s <http://value.org/variable_y> <http://value.org/list_one> . 
        ?s <http://value.org/variable_z> ?ans . 
        ?s2 <http://value.org/operation> <http://value.org/cons> . 
        ?s2 <http://value.org/variable_x> ?car . 
        ?s2 <http://value.org/variable_y> ?cdr . 
        ?s2 <http://value.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == 'http://value.org/zero'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/list_one'
    assert resolve_bindings[0]['?ans'] == 'http://value.org/list_ten'
