"""
test_040_RdfProlog_next_number.py
test for numbers declared as English names
T. Masuda, 2023/11/28
"""

from src.RdfPrologMain import RdfProlog, ClassSparqlQuery

rdf_prolog = RdfProlog(rules_folder='../rules/rules_number')


def test_answer_question1_next_1_ans():
    # next(1, ?ans) = 2
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/next_number> .
        ?s <http://value.org/variable_x> <http://value.org/one> .
        ?s <http://value.org/variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == 'http://value.org/two'


def test_answer_question2_next_ans_3():
    # next(?ans, 3) = 2
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/next_number> .
        ?s <http://value.org/variable_x> ?ans .
        ?s <http://value.org/variable_y> <http://value.org/three> .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == 'http://value.org/two'


def test_answer_question3_next_1_2():
    # next(1, 2) = True
    my_question = f"""
        SELECT ?s WHERE {{
        ?s <http://value.org/operation> <http://value.org/next_number> .
        ?s <http://value.org/variable_x> <http://value.org/one> .
        ?s <http://value.org/variable_y> <http://value.org/two> .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1


def test_answer_question4_next_1_3():
    # next(1, 3) = False
    my_question = f"""
        SELECT ?s WHERE {{
        ?s <http://value.org/operation> <http://value.org/next_number> .
        ?s <http://value.org/variable_x> <http://value.org/one> .
        ?s <http://value.org/variable_y> <http://value.org/three> .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 0


def test_answer_question5_next_1_z_next_z_x():
    # next(1, ?z),next(?z, ?x)->z:2, x:3
    my_question = f"""
        SELECT ?x WHERE {{
        ?s1 <http://value.org/operation> <http://value.org/next_number> .
        ?s1 <http://value.org/variable_x> <http://value.org/one> .
        ?s1 <http://value.org/variable_y> ?z .
        ?s2 <http://value.org/operation> <http://value.org/next_number> .
        ?s2 <http://value.org/variable_x> ?z .
        ?s2 <http://value.org/variable_y> ?x .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?x'] == 'http://value.org/three'


def test_answer_next_x_y():
    # next(?x, ?y)->(1,2), (2,3), ..., (9,10)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/next_number> .
        ?s <http://value.org/variable_x> ?x .
        ?s <http://value.org/variable_y> ?y .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=True)
    assert len(resolve_bindings) == 9
