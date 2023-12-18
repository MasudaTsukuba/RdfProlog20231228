"""
test_064_RdfProlog_list_number_math.py
tests for calculating list numbers
T. Masuda, 2023/12/15
"""

from src.RdfPrologMain import RdfProlog, ClassSparqlQuery

rdf_prolog = RdfProlog(rules_folder='../rules/rules_list_number_math')


def test_cons_5_list1_ans():
    # cons(5, list1, ?ans) ?ans = [5, 1]
    my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s1 <http://value.org/operation> <http://value.org/cons> .
            ?s1 <http://value.org/variable_x> <http://value.org/five> .
            ?s1 <http://value.org/variable_y> <http://value.org/list_one> .
            ?s1 <http://value.org/variable_z> ?ans .
            ?s2 <http://value.org/operation> <http://value.org/cons> .
            ?s2 <http://value.org/variable_x> ?car .
            ?s2 <http://value.org/variable_y> ?cdr .
            ?s2 <http://value.org/variable_z> ?ans .
            }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == 'http://value.org/five'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/list_one'

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

def test_list_next_9_ans0_next_ans0_ans():
    # next([9], ?ans0), next(?ans0, ?ans). ?ans = [1 1]
    my_question = f"""
        SELECT ?list_three ?car ?cdr WHERE {{
        ?s2 <http://value.org/operation> <http://value.org/next_list_number> . 
        ?s2 <http://value.org/variable_x> <http://value.org/list_nine> . 
        ?s2 <http://value.org/variable_y> ?list_ten . 
        ?s3 <http://value.org/operation> <http://value.org/next_list_number> . 
        ?s3 <http://value.org/variable_x> ?list_ten . 
        ?s3 <http://value.org/variable_y> ?list_eleven . 
        ?s4 <http://value.org/operation> <http://value.org/cons> . 
        ?s4 <http://value.org/variable_x> ?car_eleven . 
        ?s4 <http://value.org/variable_y> ?cdr_eleven . 
        ?s4 <http://value.org/variable_z> ?list_eleven . 
        ?s5 <http://value.org/operation> <http://value.org/cons> . 
        ?s5 <http://value.org/variable_x> ?car . 
        ?s5 <http://value.org/variable_y> ?cdr . 
        ?s5 <http://value.org/variable_z> ?cdr_eleven . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car_eleven'] == 'http://value.org/one'
    assert resolve_bindings[0]['?car'] == 'http://value.org/one'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'

def test_list_next_ans_0():
    # next(?ans, [1])
    my_question = f"""
        SELECT ?list_one ?car ?cdr WHERE {{
        ?s3 <http://value.org/operation> <http://value.org/cons> . 
        ?s3 <http://value.org/variable_x> <http://value.org/zero> . 
        ?s3 <http://value.org/variable_y> <http://value.org/nil> . 
        ?s3 <http://value.org/variable_z> ?list_ozero . 
        ?s2 <http://value.org/operation> <http://value.org/next_list_number> . 
        ?s2 <http://value.org/variable_x> ?list_minus1 . 
        ?s2 <http://value.org/variable_y> ?list_zero . 
        ?s4 <http://value.org/operation> <http://value.org/cons> . 
        ?s4 <http://value.org/variable_x> ?car . 
        ?s4 <http://value.org/variable_y> ?cdr . 
        ?s4 <http://value.org/variable_z> ?list_minus1 . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 0
    # assert resolve_bindings[0]['?list_zero'] == 'http://value.org/list_zero'
    # assert resolve_bindings[0]['?car'] == 'http://value.org/minus_one'
    # assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_list_next_ans_1():
    # next(?ans, [1])
    my_question = f"""
        SELECT ?list_one ?car ?cdr WHERE {{
        ?s3 <http://value.org/operation> <http://value.org/cons> . 
        ?s3 <http://value.org/variable_x> <http://value.org/one> . 
        ?s3 <http://value.org/variable_y> <http://value.org/nil> . 
        ?s3 <http://value.org/variable_z> ?list_one . 
        ?s2 <http://value.org/operation> <http://value.org/next_list_number> . 
        ?s2 <http://value.org/variable_x> ?list_zero . 
        ?s2 <http://value.org/variable_y> ?list_one . 
        ?s4 <http://value.org/operation> <http://value.org/cons> . 
        ?s4 <http://value.org/variable_x> ?car . 
        ?s4 <http://value.org/variable_y> ?cdr . 
        ?s4 <http://value.org/variable_z> ?list_zero . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    # assert resolve_bindings[0]['?list_zero'] == 'http://value.org/list_zero'
    assert resolve_bindings[0]['?car'] == 'http://value.org/zero'
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


def test_add_6_6_ans():
    # add(6, 6, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_add> . 
        ?s <http://value.org/variable_x> <http://value.org/list_six> . 
        ?s <http://value.org/variable_y> <http://value.org/list_six> . 
        ?s <http://value.org/variable_z> ?ans . 
        ?s2 <http://value.org/operation> <http://value.org/cons> . 
        ?s2 <http://value.org/variable_x> ?car . 
        ?s2 <http://value.org/variable_y> ?cdr . 
        ?s2 <http://value.org/variable_z> ?ans . 
        ?s3 <http://value.org/operation> <http://value.org/cons> . 
        ?s3 <http://value.org/variable_x> ?cdar . 
        ?s3 <http://value.org/variable_y> ?cddr . 
        ?s3 <http://value.org/variable_z> ?cdr . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False, max_depth=100)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == 'http://value.org/two'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/list_one'


def test_add_2_ans_3():
    # add(2, ?ans, 3)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_add> . 
        ?s <http://value.org/variable_x> <http://value.org/list_two> . 
        ?s <http://value.org/variable_y> ?ans . 
        ?s <http://value.org/variable_z> <http://value.org/list_three> . 
        ?s2 <http://value.org/operation> <http://value.org/cons> . 
        ?s2 <http://value.org/variable_x> ?car . 
        ?s2 <http://value.org/variable_y> ?cdr . 
        ?s2 <http://value.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == 'http://value.org/one'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_add_ans_2_4():
    # add(?ans, 2, 4)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_add> . 
        ?s <http://value.org/variable_x> ?ans . 
        ?s <http://value.org/variable_y> <http://value.org/list_two> . 
        ?s <http://value.org/variable_z> <http://value.org/list_four> . 
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


def test_subtract_4_2_ans():
    # subtract(4, 2, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_subtract> . 
        ?s <http://value.org/variable_x> <http://value.org/list_four> . 
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
    assert resolve_bindings[0]['?car'] == 'http://value.org/two'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_subtract_4_ans_1():
    # subtract(4, ?ans, 1)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_subtract> . 
        ?s <http://value.org/variable_x> <http://value.org/list_four> . 
        ?s <http://value.org/variable_y> ?ans . 
        ?s <http://value.org/variable_z> <http://value.org/list_one> . 
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


def test_subtract_ans_5_2():
    # subtract(?ans, 5, 2)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_subtract> . 
        ?s <http://value.org/variable_x> ?ans . 
        ?s <http://value.org/variable_y> <http://value.org/list_five> . 
        ?s <http://value.org/variable_z> <http://value.org/list_two> . 
        ?s2 <http://value.org/operation> <http://value.org/cons> . 
        ?s2 <http://value.org/variable_x> ?car . 
        ?s2 <http://value.org/variable_y> ?cdr . 
        ?s2 <http://value.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == 'http://value.org/seven'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_multiply_2_1_ans():
    # multiply(2, 1, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_multiply> . 
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
    assert resolve_bindings[0]['?car'] == 'http://value.org/two'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_multiply_3_2_ans():
    # multiply(3, 2, ?ans) -> ?ans = 6
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_multiply> . 
        ?s <http://value.org/variable_x> <http://value.org/list_three> . 
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
    assert resolve_bindings[0]['?car'] == 'http://value.org/six'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_multiply_3_ans_9():
    # multiply(3, ?ans, 9) -> ?ans = 3
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_multiply> . 
        ?s <http://value.org/variable_x> <http://value.org/list_three> . 
        ?s <http://value.org/variable_y> ?ans . 
        ?s <http://value.org/variable_z> <http://value.org/list_nine> . 
        ?s2 <http://value.org/operation> <http://value.org/cons> . 
        ?s2 <http://value.org/variable_x> ?car . 
        ?s2 <http://value.org/variable_y> ?cdr . 
        ?s2 <http://value.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False, max_depth=100)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == 'http://value.org/three'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_divide_4_2_ans():
    # divide(4, 2, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_divide> . 
        ?s <http://value.org/variable_x> <http://value.org/list_four> . 
        ?s <http://value.org/variable_y> <http://value.org/list_two> . 
        ?s <http://value.org/variable_z> ?ans . 
        ?s2 <http://value.org/operation> <http://value.org/cons> . 
        ?s2 <http://value.org/variable_x> ?car . 
        ?s2 <http://value.org/variable_y> ?cdr . 
        ?s2 <http://value.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False, max_depth=100)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == 'http://value.org/two'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_divide_5_1_ans():
    # divide(5, 1, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_divide> . 
        ?s <http://value.org/variable_x> <http://value.org/list_five> . 
        ?s <http://value.org/variable_y> <http://value.org/list_one> . 
        ?s <http://value.org/variable_z> ?ans . 
        ?s2 <http://value.org/operation> <http://value.org/cons> . 
        ?s2 <http://value.org/variable_x> ?car . 
        ?s2 <http://value.org/variable_y> ?cdr . 
        ?s2 <http://value.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False, max_depth=100)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == 'http://value.org/five'
    assert resolve_bindings[0]['?cdr'] == 'http://value.org/nil'


def test_divide_5_2_ans():
    # divide(5, 1, ?ans)
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s <http://value.org/operation> <http://value.org/list_divide> . 
        ?s <http://value.org/variable_x> <http://value.org/list_five> . 
        ?s <http://value.org/variable_y> <http://value.org/list_two> . 
        ?s <http://value.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False, max_depth=100)
    assert len(resolve_bindings) == 0


def test_divide_6_2_ans():
    # divide(6, 2, ?ans) -> ?ans = [3]
    my_question = f"""
        SELECT ?ans ?car ?cdr WHERE {{
        ?s1 <http://value.org/operation> <http://value.org/cons> . 
        ?s1 <http://value.org/variable_x> <http://value.org/six> . 
        ?s1 <http://value.org/variable_y> <http://value.org/nil> . 
        ?s1 <http://value.org/variable_z> ?list_6 . 
        ?s2 <http://value.org/operation> <http://value.org/list_divide> . 
        ?s2 <http://value.org/variable_x> ?list_6 . 
        ?s2 <http://value.org/variable_y> <http://value.org/list_two> . 
        ?s2 <http://value.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False, max_depth=50)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?ans'] == 'http://value.org/list_three'
