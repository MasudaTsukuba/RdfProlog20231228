"""
test_059_RdfProlog_function_100.py
test for function call
T. Masuda, 2023/12/21
"""

from src.RdfPrologMain import RdfProlog, ClassSparqlQuery

rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')


def test_answer_question1_solve_simultaneous_linear_equation():
    # solve_simultaneous_linear_equation(2, 3, 12, 1, 1, 5, ?ans1, ?ans2)
    my_question = f"""
       SELECT ?ans1 ?ans2 WHERE {{
       ?s <http://value.org/operation> <http://value.org/solve_simultaneous_linear_equation> .
       ?s <http://value.org/variable_a11> <http://value.org/2> .
       ?s <http://value.org/variable_a12> <http://value.org/3> .
       ?s <http://value.org/variable_b1> <http://value.org/12> .
       ?s <http://value.org/variable_a21> <http://value.org/1> .
       ?s <http://value.org/variable_a22> <http://value.org/1> .
       ?s <http://value.org/variable_b2> <http://value.org/5> .
       ?s <http://value.org/variable_x1> ?ans1 .
       ?s <http://value.org/variable_x2> ?ans2 .
       }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans1'] == 'http://value.org/3'
    assert resolve_bindings[0]['?ans2'] == 'http://value.org/2'


def test_answer_question2_solve_simultaneous_linear_equation():
    # solve_simultaneous_linear_equation(2, 3, 12, 1, 1, 5, ?ans1, ?ans2)
    my_question = f"""
       SELECT ?ans1 ?ans2 WHERE {{
       ?s <http://value.org/operation> <http://value.org/solve_simultaneous_linear_equation> .
       ?s <http://value.org/variable_a11> <http://value.org/3> .
       ?s <http://value.org/variable_a12> <http://value.org/2> .
       ?s <http://value.org/variable_b1> <http://value.org/22> .
       ?s <http://value.org/variable_a21> <http://value.org/2> .
       ?s <http://value.org/variable_a22> <http://value.org/1> .
       ?s <http://value.org/variable_b2> <http://value.org/13> .
       ?s <http://value.org/variable_x1> ?ans1 .
       ?s <http://value.org/variable_x2> ?ans2 .
       }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans1'] == 'http://value.org/4'
    assert resolve_bindings[0]['?ans2'] == 'http://value.org/5'


def test_answer_question3_solve_simultaneous_linear_equation():
    # solve_simultaneous_linear_equation(2, 3, 12, 1, 1, 5, ?ans1, ?ans2), add(?ans1, ?ans2, ?ans) .
    my_question = f"""
       SELECT ?ans ?ans1 ?ans2 WHERE {{
       ?s <http://value.org/operation> <http://value.org/solve_simultaneous_linear_equation> .
       ?s <http://value.org/variable_a11> <http://value.org/3> .
       ?s <http://value.org/variable_a12> <http://value.org/2> .
       ?s <http://value.org/variable_b1> <http://value.org/22> .
       ?s <http://value.org/variable_a21> <http://value.org/2> .
       ?s <http://value.org/variable_a22> <http://value.org/1> .
       ?s <http://value.org/variable_b2> <http://value.org/13> .
       ?s <http://value.org/variable_x1> ?ans1 .
       ?s <http://value.org/variable_x2> ?ans2 .
       ?s2 <http://value.org/operation> <http://value.org/add_number> .
       ?s2 <http://value.org/variable_x> ?ans1 .
       ?s2 <http://value.org/variable_y> ?ans2 .
       ?s2 <http://value.org/variable_z> ?ans .
       }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans1'] == 'http://value.org/4'
    assert resolve_bindings[0]['?ans2'] == 'http://value.org/5'
    assert resolve_bindings[0]['?ans'] == 'http://value.org/9'
