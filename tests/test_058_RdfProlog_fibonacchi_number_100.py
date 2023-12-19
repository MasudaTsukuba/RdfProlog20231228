"""
test_058_RdfProlog_fibonacchi_number_100.py
tests for fibonacchi numbers
T. Masuda, 2023/12/14
"""

from src.RdfPrologMain import RdfProlog, ClassSparqlQuery


rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')


def test_answer_question1_fibonacchi_1_ans():
    # divide(1, 1, ?ans) = 1
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/fibonacchi_number> . 
        ?s <http://value.org/variable_x> <http://value.org/1> . 
        ?s <http://value.org/variable_y> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/1'


def test_answer_question2_fibonacchi_2_ans():
    # divide(2, 1, ?ans) = 2
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://value.org/operation> <http://value.org/fibonacchi_number> .
        ?s <http://value.org/variable_x> <http://value.org/2> .
        ?s <http://value.org/variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/1'


def test_answer_question3_fibonacchi_3_ans():
    # divide(1, 2, ?ans) = None
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/fibonacchi_number> .
        ?s <http://value.org/variable_x> <http://value.org/3> .
        ?s <http://value.org/variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/2'

def test_answer_question4_fibonacchi_4_ans():
    # divide(2, 2, ?ans) = 1
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/fibonacchi_number> .
        ?s <http://value.org/variable_x> <http://value.org/4> .
        ?s <http://value.org/variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/3'


def test_answer_question4_fibonacchi_5_ans():
    # divide(6, 2, ?ans) = 3
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/fibonacchi_number> .
        ?s <http://value.org/variable_x> <http://value.org/5> .
        ?s <http://value.org/variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/5'


def test_answer_question5_divide_6_ans():
    # divide(?ans, 2, 3)->ans:6
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/fibonacchi_number> .
        ?s <http://value.org/variable_x> <http://value.org/6> .
        ?s <http://value.org/variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=200)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/8'


def test_answer_complex_question1():
    # fibonacchi(3, ?y), next(?y, ?ans)->y:2, ans:3
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <http://value.org/operation> <http://value.org/fibonacchi_number> .
        ?s1 <http://value.org/variable_x> <http://value.org/3> .
        ?s1 <http://value.org/variable_y> ?y .
        ?s2 <http://value.org/operation> <http://value.org/next_number> .
        ?s2 <http://value.org/variable_x> ?y .
        ?s2 <http://value.org/variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=20)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/3'
