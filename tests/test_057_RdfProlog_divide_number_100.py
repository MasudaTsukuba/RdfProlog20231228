"""
test_057_RdfProlog_divide_number_100.py
tests for divide uri numbers
T. Masuda, 2023/12/14
"""

from src.RdfResolution import *


rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')


def test_answer_question1_divide_1_1_ans():
    # divide(1, 1, ?ans) = 1
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}divide_number> . 
        ?s <{VAL}variable_x> <{VAL}1> . 
        ?s <{VAL}variable_y> <{VAL}1> . 
        ?s <{VAL}variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}1'


def test_answer_question2_divide_2_1_ans():
    # divide(2, 1, ?ans) = 2
    my_question = f"""
        SELECT ?ans WHERE {{ ?s <{OPERATION}> <{VAL}divide_number> .
        ?s <{VAL}variable_x> <{VAL}2> .
        ?s <{VAL}variable_y> <{VAL}1> .
        ?s <{VAL}variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}2'


def test_answer_question3_divide_1_2_ans():
    # divide(1, 2, ?ans) = None
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}divide_number> .
        ?s <{VAL}variable_x> <{VAL}1> .
        ?s <{VAL}variable_y> <{VAL}2> .
        ?s <{VAL}variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 0


def test_answer_question4_divide_2_2_ans():
    # divide(2, 2, ?ans) = 1
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}divide_number> .
        ?s <{VAL}variable_x> <{VAL}2> .
        ?s <{VAL}variable_y> <{VAL}2> .
        ?s <{VAL}variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}1'


def test_answer_question4_divide_6_2_ans():
    # divide(6, 2, ?ans) = 3
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}divide_number> .
        ?s <{VAL}variable_x> <{VAL}6> .
        ?s <{VAL}variable_y> <{VAL}2> .
        ?s <{VAL}variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}3'


def test_answer_question5_divide_ans_2_3():
    # divide(?ans, 2, 3)->ans:6
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}divide_number> .
        ?s <{VAL}variable_x> ?ans .
        ?s <{VAL}variable_y> <{VAL}2> .
        ?s <{VAL}variable_z> <{VAL}3> .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)
    assert resolve_bindings[0]['?ans'] == f'{VAL}6'


def test_answer_question6_divide_12_ans_3():
    # divide(12, ?ans, 3)->ans:4
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <{OPERATION}> <{VAL}divide_number> .
        ?s <{VAL}variable_x> <{VAL}12> .
        ?s <{VAL}variable_y> ?ans .
        ?s <{VAL}variable_z> <{VAL}3> .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)
    assert resolve_bindings[0]['?ans'] == f'{VAL}4'


def test_answer_complex_question1():
    # divide(6, 3, ?z), next(?z, ?ans)->z:2, ans:3
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}divide_number> .
        ?s1 <{VAL}variable_x> <{VAL}6> .
        ?s1 <{VAL}variable_y> <{VAL}3> .
        ?s1 <{VAL}variable_z> ?z .
        ?s2 <{OPERATION}> <{VAL}next_number> .
        ?s2 <{VAL}variable_x> ?z .
        ?s2 <{VAL}variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}3'


def test_answer_complex_question2():
    # divide(12, 2, ?z), divide(?z, 3, ?ans)->z:6, ans:2
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <{OPERATION}> <{VAL}divide_number> .
        ?s1 <{VAL}variable_x> <{VAL}12> .
        ?s1 <{VAL}variable_y> <{VAL}2> .
        ?s1 <{VAL}variable_z> ?z .
        ?s2 <{OPERATION}> <{VAL}divide_number> .
        ?s2 <{VAL}variable_x> ?z .
        ?s2 <{VAL}variable_y> <{VAL}3> .
        ?s2 <{VAL}variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)
    assert resolve_bindings[0]['?ans'] == f'{VAL}2'


# # def test_add_1_y_z():
# #     # add(1, ?y, ?z)->(1,2),(2,3),...,(9,10)
# #     my_question = f"""
# #         SELECT ?ans WHERE {{
# #         ?s <{OPERATION}> <{VAL}add_number> .
# #         ?s <{VAL}variable_x> <{VAL}1> .
# #         ?s <{VAL}variable_y> ?y .
# #         ?s <{VAL}variable_z> ?z .
# #         }}"""
# #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
# #     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10, depth_limit=200)
# #     assert len(resolve_bindings) == 98
#
#
# # def test_add_98_y_z():
# #     # add(98, ?y, ?z)->(1,99)
# #     my_question = f"""
# #         SELECT ?y ?z WHERE {{
# #         ?s <{OPERATION}> <{VAL}add_number> .
# #         ?s <{VAL}variable_x> <{VAL}98> .
# #         ?s <{VAL}variable_y> ?y .
# #         ?s <{VAL}variable_z> ?z .
# #         }}"""
# #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
# #     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10, depth_limit=200)
# #     assert resolve_bindings[0]['?y'] == f'{VAL}1'
# #     assert resolve_bindings[0]['?z'] == f'{VAL}99'
#
#
# # def test_add_x_1_z():
# #     # add(?x, 1, ?z)->(1,2),(2,3),...,(9,10)
# #     my_question = f"""
# #         SELECT ?x ?z WHERE {{
# #         ?s <{OPERATION}> <{VAL}add_number> .
# #         ?s <{VAL}variable_x> ?x .
# #         ?s <{VAL}variable_y> <{VAL}1> .
# #         ?s <{VAL}variable_z> ?z .
# #         }}"""
# #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
# #     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10)
# #     assert len(resolve_bindings) == 98
#
#
# # def test_add_x_98_z():
# #     # add(?x, 98, ?z)->(1,99)
# #     my_question = f"""
# #         SELECT ?x ?z WHERE {{
# #         ?s <{OPERATION}> <{VAL}add_number> .
# #         ?s <{VAL}variable_x> ?x .
# #         ?s <{VAL}variable_y> <{VAL}98> .
# #         ?s <{VAL}variable_z> ?z .
# #         }}"""
# #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
# #     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10, depth_limit=200)
# #     assert resolve_bindings[0]['?x'] == f'{VAL}1'
# #     assert resolve_bindings[0]['?z'] == f'{VAL}99'
#
#
# # def test_add_x_y_2():
# #     # add(?x, ?y, 2)->(1,1)
# #     my_question = f"""
# #         SELECT ?x ?y WHERE {{
# #         ?s <{OPERATION}> <{VAL}add_number> .
# #         ?s <{VAL}variable_x> ?x .
# #         ?s <{VAL}variable_y> ?y .
# #         ?s <{VAL}variable_z> <{VAL}2> .
# #         }}"""
# #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
# #     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10)
# #     assert resolve_bindings[0]['?x'] == f'{VAL}1'
# #     assert resolve_bindings[0]['?y'] == f'{VAL}1'
#
#
# # def test_add_x_y_3():
# #     # add(?x, ?y, 3)->(1,2),(2,1)
# #     my_question = f"""
# #         SELECT ?x ?y WHERE {{
# #         ?s <{OPERATION}> <{VAL}add_number> .
# #         ?s <{VAL}variable_x> ?x .
# #         ?s <{VAL}variable_y> ?y .
# #         ?s <{VAL}variable_z> <{VAL}3> .
# #         }}"""
# #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
# #     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10, depth_limit=10)
# #     assert len(resolve_bindings) == 2
#
#
# def test_depth_limit_add_3_1_ans():
#     # add(3, 1, ?ans) depth_limit=0
#     my_question = f"""
#         SELECT ?ans WHERE {{
#         ?s <{OPERATION}> <{VAL}add_number> .
#         ?s <{VAL}variable_x> <{VAL}3> .
#         ?s <{VAL}variable_y> <{VAL}1> .
#         ?s <{VAL}variable_z> ?ans .
#         }}"""
#     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
#     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=1)
#     assert len(resolve_bindings) == 0
#
#
# def test_depth_limit_add_3_1_ans_2():
#     # add(3, 1, ?ans) depth_limit=1
#     my_question = f"""
#         SELECT ?ans WHERE {{
#         ?s <{OPERATION}> <{VAL}add_number> .
#         ?s <{VAL}variable_x> <{VAL}3> .
#         ?s <{VAL}variable_y> <{VAL}1> .
#         ?s <{VAL}variable_z> ?ans .
#         }}"""
#     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
#     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=2)
#     assert len(resolve_bindings) == 1
#     assert resolve_bindings[0]['?ans'] == f'{VAL}4'
