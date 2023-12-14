"""
test_056_RdfProlog_multiply_number_100.py
tests for add uri numbers
T. Masuda, 2023/12/11
"""

from src.RdfPrologMain import RdfProlog, ClassSparqlQuery


rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')


def test_answer_question1_multiply_1_1_ans():
    # multiply(1, 1, ?ans) = 1
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/multiply_number> . 
        ?s <http://value.org/variable_x> <http://value.org/1> . 
        ?s <http://value.org/variable_y> <http://value.org/1> . 
        ?s <http://value.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/1'


def test_answer_question2_multiply_2_1_ans():
    # multiply(2, 1, ?ans) = 2
    my_question = f"""
        SELECT ?ans WHERE {{ ?s <http://value.org/operation> <http://value.org/multiply_number> .
        ?s <http://value.org/variable_x> <http://value.org/2> .
        ?s <http://value.org/variable_y> <http://value.org/1> .
        ?s <http://value.org/variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/2'


def test_answer_question3_multiply_1_2_ans():
    # multiply(1, 2, ?ans) = 2
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/multiply_number> .
        ?s <http://value.org/variable_x> <http://value.org/1> .
        ?s <http://value.org/variable_y> <http://value.org/2> .
        ?s <http://value.org/variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/2'


def test_answer_question4_multiply_2_2_ans():
    # multiply(2, 2, ?ans) = 4
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/multiply_number> .
        ?s <http://value.org/variable_x> <http://value.org/2> .
        ?s <http://value.org/variable_y> <http://value.org/2> .
        ?s <http://value.org/variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/4'


def test_answer_question4_multiply_3_2_ans():
    # multiply(3, 2, ?ans) = 6
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/multiply_number> .
        ?s <http://value.org/variable_x> <http://value.org/3> .
        ?s <http://value.org/variable_y> <http://value.org/2> .
        ?s <http://value.org/variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/6'


def test_answer_question5_multiply_ans_2_6():
    # multiply(?ans, 2, 6)->ans:3
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/multiply_number> .
        ?s <http://value.org/variable_x> ?ans .
        ?s <http://value.org/variable_y> <http://value.org/2> .
        ?s <http://value.org/variable_z> <http://value.org/6> .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, max_depth=10)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/3'


def test_answer_question6_multiply_3_ans_12():
    # multiply(?ans, 2, 6)->ans:3
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://value.org/operation> <http://value.org/multiply_number> .
        ?s <http://value.org/variable_x> <http://value.org/3> .
        ?s <http://value.org/variable_y> ?ans .
        ?s <http://value.org/variable_z> <http://value.org/12> .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, max_depth=30)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/4'

# def test_answer_complex_question1():
    # multiply(3, 2, ?z), next(?z, ?ans)->z:6, ans:7
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <http://value.org/operation> <http://value.org/multiply_number> .
        ?s1 <http://value.org/variable_x> <http://value.org/3> .
        ?s1 <http://value.org/variable_y> <http://value.org/2> .
        ?s1 <http://value.org/variable_z> ?z .
        ?s2 <http://value.org/operation> <http://value.org/next_number> .
        ?s2 <http://value.org/variable_x> ?z .
        ?s2 <http://value.org/variable_y> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/7'


def test_answer_complex_question2():
    # multiply(3, 2, ?z), multiply(?z, 5, ?ans)->z:6, ans:30
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <http://value.org/operation> <http://value.org/multiply_number> .
        ?s1 <http://value.org/variable_x> <http://value.org/3> .
        ?s1 <http://value.org/variable_y> <http://value.org/2> .
        ?s1 <http://value.org/variable_z> ?z .
        ?s2 <http://value.org/operation> <http://value.org/multiply_number> .
        ?s2 <http://value.org/variable_x> ?z .
        ?s2 <http://value.org/variable_y> <http://value.org/5> .
        ?s2 <http://value.org/variable_z> ?ans .
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, max_depth=100)
    assert resolve_bindings[0]['?ans'] == f'http://value.org/30'


# # def test_add_1_y_z():
# #     # add(1, ?y, ?z)->(1,2),(2,3),...,(9,10)
# #     my_question = f"""
# #         SELECT ?ans WHERE {{
# #         ?s <http://value.org/operation> <http://value.org/add_number> .
# #         ?s <http://value.org/variable_x> <http://value.org/1> .
# #         ?s <http://value.org/variable_y> ?y .
# #         ?s <http://value.org/variable_z> ?z .
# #         }}"""
# #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
# #     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=True, max_depth=200)
# #     assert len(resolve_bindings) == 98
#
#
# # def test_add_98_y_z():
# #     # add(98, ?y, ?z)->(1,99)
# #     my_question = f"""
# #         SELECT ?y ?z WHERE {{
# #         ?s <http://value.org/operation> <http://value.org/add_number> .
# #         ?s <http://value.org/variable_x> <http://value.org/98> .
# #         ?s <http://value.org/variable_y> ?y .
# #         ?s <http://value.org/variable_z> ?z .
# #         }}"""
# #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
# #     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=True, max_depth=200)
# #     assert resolve_bindings[0]['?y'] == f'http://value.org/1'
# #     assert resolve_bindings[0]['?z'] == f'http://value.org/99'
#
#
# # def test_add_x_1_z():
# #     # add(?x, 1, ?z)->(1,2),(2,3),...,(9,10)
# #     my_question = f"""
# #         SELECT ?x ?z WHERE {{
# #         ?s <http://value.org/operation> <http://value.org/add_number> .
# #         ?s <http://value.org/variable_x> ?x .
# #         ?s <http://value.org/variable_y> <http://value.org/1> .
# #         ?s <http://value.org/variable_z> ?z .
# #         }}"""
# #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
# #     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=True)
# #     assert len(resolve_bindings) == 98
#
#
# # def test_add_x_98_z():
# #     # add(?x, 98, ?z)->(1,99)
# #     my_question = f"""
# #         SELECT ?x ?z WHERE {{
# #         ?s <http://value.org/operation> <http://value.org/add_number> .
# #         ?s <http://value.org/variable_x> ?x .
# #         ?s <http://value.org/variable_y> <http://value.org/98> .
# #         ?s <http://value.org/variable_z> ?z .
# #         }}"""
# #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
# #     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=True, max_depth=200)
# #     assert resolve_bindings[0]['?x'] == 'http://value.org/1'
# #     assert resolve_bindings[0]['?z'] == 'http://value.org/99'
#
#
# # def test_add_x_y_2():
# #     # add(?x, ?y, 2)->(1,1)
# #     my_question = f"""
# #         SELECT ?x ?y WHERE {{
# #         ?s <http://value.org/operation> <http://value.org/add_number> .
# #         ?s <http://value.org/variable_x> ?x .
# #         ?s <http://value.org/variable_y> ?y .
# #         ?s <http://value.org/variable_z> <http://value.org/2> .
# #         }}"""
# #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
# #     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=True)
# #     assert resolve_bindings[0]['?x'] == 'http://value.org/1'
# #     assert resolve_bindings[0]['?y'] == 'http://value.org/1'
#
#
# # def test_add_x_y_3():
# #     # add(?x, ?y, 3)->(1,2),(2,1)
# #     my_question = f"""
# #         SELECT ?x ?y WHERE {{
# #         ?s <http://value.org/operation> <http://value.org/add_number> .
# #         ?s <http://value.org/variable_x> ?x .
# #         ?s <http://value.org/variable_y> ?y .
# #         ?s <http://value.org/variable_z> <http://value.org/3> .
# #         }}"""
# #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
# #     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=True, max_depth=10)
# #     assert len(resolve_bindings) == 2
#
#
# def test_max_depth_add_3_1_ans():
#     # add(3, 1, ?ans) max_depth=0
#     my_question = f"""
#         SELECT ?ans WHERE {{
#         ?s <http://value.org/operation> <http://value.org/add_number> .
#         ?s <http://value.org/variable_x> <http://value.org/3> .
#         ?s <http://value.org/variable_y> <http://value.org/1> .
#         ?s <http://value.org/variable_z> ?ans .
#         }}"""
#     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
#     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False, max_depth=1)
#     assert len(resolve_bindings) == 0
#
#
# def test_max_depth_add_3_1_ans_2():
#     # add(3, 1, ?ans) max_depth=1
#     my_question = f"""
#         SELECT ?ans WHERE {{
#         ?s <http://value.org/operation> <http://value.org/add_number> .
#         ?s <http://value.org/variable_x> <http://value.org/3> .
#         ?s <http://value.org/variable_y> <http://value.org/1> .
#         ?s <http://value.org/variable_z> ?ans .
#         }}"""
#     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
#     resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False, max_depth=2)
#     assert len(resolve_bindings) == 1
#     assert resolve_bindings[0]['?ans'] == 'http://value.org/4'
