"""
test_RdfProlog_subtract_number.py
T. Masuda, 2023/10/30
"""

from src.RdfPrologMain import RdfProlog, ClassSparqlQuery


rdf_prolog = RdfProlog(rules_folder='rules_number')


def test_answer_question1_3_minus_1():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # subtract(3, 1, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://example.org/operation> <http://example.org/subtract_number> . 
        ?s <http://example.org/variable_x> <http://example.org/three> . 
        ?s <http://example.org/variable_y> <http://example.org/one> . 
        ?s <http://example.org/variable_z> ?ans . 
        }}
        """
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://example.org/two'


def test_answer_question2_4_minus_2():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # subtract(4, 2, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{ ?s <http://example.org/operation> <http://example.org/subtract_number> .
        ?s <http://example.org/variable_x> <http://example.org/four> .
        ?s <http://example.org/variable_y> <http://example.org/two> .
        ?s <http://example.org/variable_z> ?ans .
        }} """
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://example.org/two'


def test_answer_question3_3_minus_2():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # # subtract(3, 2, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://example.org/operation> <http://example.org/subtract_number> .
        ?s <http://example.org/variable_x> <http://example.org/three> .
        ?s <http://example.org/variable_y> <http://example.org/two> .
        ?s <http://example.org/variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False, max_depth=10)
    assert resolve_bindings[0]['?ans'] == f'http://example.org/one'


def test_answer_question3b_next_of_5_minus_2():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # subtract(5, 2, ?z), next(?z, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <http://example.org/operation> <http://example.org/subtract_number> .
        ?s1 <http://example.org/variable_x> <http://example.org/five> .
        ?s1 <http://example.org/variable_y> <http://example.org/two> .
        ?s1 <http://example.org/variable_z> ?z .
        ?s2 <http://example.org/operation> <http://example.org/next_number> .
        ?s2 <http://example.org/variable_x> ?z .
        ?s2 <http://example.org/variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://example.org/four'


def test_answer_question_5_minus_ans_equals_2():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # subtract(5, ?ans, 2)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://example.org/operation> <http://example.org/subtract_number> .
        ?s <http://example.org/variable_x> <http://example.org/five> .
        ?s <http://example.org/variable_y> ?ans .
        ?s <http://example.org/variable_z> <http://example.org/two> .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://example.org/three'


def test_answer_complex_question_5_minus_2_next():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # subtract(5, 2, ?z), next(?z, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <http://example.org/operation> <http://example.org/subtract_number> .
        ?s1 <http://example.org/variable_x> <http://example.org/five> .
        ?s1 <http://example.org/variable_y> <http://example.org/two> .
        ?s1 <http://example.org/variable_z> ?z .
        ?s2 <http://example.org/operation> <http://example.org/next_number> .
        ?s2 <http://example.org/variable_x> ?z .
        ?s2 <http://example.org/variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)  # ###################
    assert resolve_bindings[0]['?ans'] == f'http://example.org/four'


def test_answer_complex_question_3_minus_2_plus_2():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # subtract(3, 2, ?z), add(?z, 2, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <http://example.org/operation> <http://example.org/subtract_number> .
        ?s1 <http://example.org/variable_x> <http://example.org/three> .
        ?s1 <http://example.org/variable_y> <http://example.org/two> .
        ?s1 <http://example.org/variable_z> ?z .
        ?s2 <http://example.org/operation> <http://example.org/add_number> .
        ?s2 <http://example.org/variable_x> ?z .
        ?s2 <http://example.org/variable_y> <http://example.org/two> .
        ?s2 <http://example.org/variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)  # ###################
    assert resolve_bindings[0]['?ans'] == f'http://example.org/three'
