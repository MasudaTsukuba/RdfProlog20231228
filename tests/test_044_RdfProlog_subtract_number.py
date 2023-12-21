"""
test_044_RdfProlog_subtract_number.py
tests for subtracting symbolic numbers
T. Masuda, 2023/10/30
"""

from src.RdfPrologMain import RdfProlog, ClassSparqlQuery


rdf_prolog = RdfProlog(rules_folder='../rules/rules_number')


def test_answer_question1_3_minus_1():
    # subtract(3, 1, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/subtract_number> . 
        ?s <http://value.org/variable_x> <http://value.org/three> . 
        ?s <http://value.org/variable_y> <http://value.org/one> . 
        ?s <http://value.org/variable_z> ?ans . 
        }}
        """
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/two'


def test_answer_question2_4_minus_2():
    # subtract(4, 2, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{ ?s <http://value.org/operation> <http://value.org/subtract_number> .
        ?s <http://value.org/variable_x> <http://value.org/four> .
        ?s <http://value.org/variable_y> <http://value.org/two> .
        ?s <http://value.org/variable_z> ?ans .
        }} """
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/two'


def test_answer_question3_3_minus_2():
    # # subtract(3, 2, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/subtract_number> .
        ?s <http://value.org/variable_x> <http://value.org/three> .
        ?s <http://value.org/variable_y> <http://value.org/two> .
        ?s <http://value.org/variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=10)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/one'


def test_answer_question3b_next_of_5_minus_2():
    # subtract(5, 2, ?z), next(?z, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <http://value.org/operation> <http://value.org/subtract_number> .
        ?s1 <http://value.org/variable_x> <http://value.org/five> .
        ?s1 <http://value.org/variable_y> <http://value.org/two> .
        ?s1 <http://value.org/variable_z> ?z .
        ?s2 <http://value.org/operation> <http://value.org/next_number> .
        ?s2 <http://value.org/variable_x> ?z .
        ?s2 <http://value.org/variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/four'


def test_answer_question_5_minus_ans_equals_2():
    # subtract(5, ?ans, 2)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/subtract_number> .
        ?s <http://value.org/variable_x> <http://value.org/five> .
        ?s <http://value.org/variable_y> ?ans .
        ?s <http://value.org/variable_z> <http://value.org/two> .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/three'


def test_answer_complex_question_5_minus_2_next():
    # subtract(5, 2, ?z), next(?z, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <http://value.org/operation> <http://value.org/subtract_number> .
        ?s1 <http://value.org/variable_x> <http://value.org/five> .
        ?s1 <http://value.org/variable_y> <http://value.org/two> .
        ?s1 <http://value.org/variable_z> ?z .
        ?s2 <http://value.org/operation> <http://value.org/next_number> .
        ?s2 <http://value.org/variable_x> ?z .
        ?s2 <http://value.org/variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)  # ###################
    assert resolve_bindings[0]['?ans'] == f'http://value.org/four'


def test_answer_complex_question_3_minus_2_plus_2():
    # subtract(3, 2, ?z), add(?z, 2, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <http://value.org/operation> <http://value.org/subtract_number> .
        ?s1 <http://value.org/variable_x> <http://value.org/three> .
        ?s1 <http://value.org/variable_y> <http://value.org/two> .
        ?s1 <http://value.org/variable_z> ?z .
        ?s2 <http://value.org/operation> <http://value.org/add_number> .
        ?s2 <http://value.org/variable_x> ?z .
        ?s2 <http://value.org/variable_y> <http://value.org/two> .
        ?s2 <http://value.org/variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)  # ###################
    assert resolve_bindings[0]['?ans'] == f'http://value.org/three'
