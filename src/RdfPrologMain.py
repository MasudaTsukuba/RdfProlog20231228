"""Main module to run RdfProlog
RdfPrologMain.py
Executing Prolog on RDF query system
Main function
2022/12/20, 2023/3/16, 2023/10/30, 2023/11/6, 2023/11/28
T. Masuda
"""
import os.path
import logging

from src.RdfClass import ClassSparqlQuery
from src.RdfResolution import RdfProlog, start_log


def main():
    """Main function for RdfProlog.

    Args:

    Returns:

    """
    start_log()

    # next
    if True:  # next
        # rdf_prolog = RdfProlog(rules_folder='rules/rules_number')
        # # next(1, ?ans)
        # my_question = f"""
        #    SELECT ?ans WHERE {{
        #    ?s <http://value.org/operation> <http://value.org/next_number> .
        #    ?s <http://value.org/variable_x> <http://value.org/one> .
        #    ?s <http://value.org/variable_y> ?ans .
        #    }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        # # xxx = resolve_bindings[0]['?ans']
        # pass

    #     # next(?ans, 3)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/next_number> .
    #        ?s <http://value.org/variable_x> ?ans .
    #        ?s <http://value.org/variable_y> <http://value.org/three> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     pass
    #
    #     # next(1, 2)
    #     my_question = f"""
    #        SELECT ?s WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/next_number> .
    #        ?s <http://value.org/variable_x> <http://value.org/one> .
    #        ?s <http://value.org/variable_y> <http://value.org/two> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     pass
    #
    #     # next(1, 3)
    #     my_question = f"""
    #        SELECT ?s WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/next_number> . 
    #        ?s <http://value.org/variable_x> <http://value.org/one> . 
    #        ?s <http://value.org/variable_y> <http://value.org/three> . 
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     pass
    #
    #     # next(1, ?z),next(?z, ?ans)
    #     # my_question = f"""
    #     #    SELECT ?ans WHERE {{
    #     #    ?s1 <http://value.org/operation> <http://value.org/next_number> . 
    #     #    ?s1 <http://value.org/variable_x> <http://value.org/one> . 
    #     #    ?s1 <http://value.org/variable_y> ?z . 
    #     #    ?s2 <http://value.org/operation> <http://value.org/next_number> . 
    #     #    ?s2 <http://value.org/variable_x> ?z . 
    #     #    ?s2 <http://value.org/variable_y> ?ans . 
    #     #    }}"""
    #     # next(1, ?z),next(?z, ?x)
    #     my_question = f"""
    #        SELECT ?x WHERE {{
    #        ?s1 <http://value.org/operation> <http://value.org/next_number> . 
    #        ?s1 <http://value.org/variable_x> <http://value.org/one> . 
    #        ?s1 <http://value.org/variable_y> ?z . 
    #        ?s2 <http://value.org/operation> <http://value.org/next_number> . 
    #        ?s2 <http://value.org/variable_x> ?z . 
    #        ?s2 <http://value.org/variable_y> ?x . 
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     pass
    #
    #     # next(?x, ?y)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/next_number> . 
    #        ?s <http://value.org/variable_x> ?x . 
    #        ?s <http://value.org/variable_y> ?y . 
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        pass

    # add
    if True:
        rdf_prolog = RdfProlog(rules_folder='../rules/rules_number')

        # add(3, 1, ?ans)
        my_question = f"""
           SELECT ?ans WHERE {{
           ?s <http://value.org/operation> <http://value.org/add_number> .
           ?s <http://value.org/variable_x> <http://value.org/three> .
           ?s <http://value.org/variable_y> <http://value.org/one> .
           ?s <http://value.org/variable_z> ?ans .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # add(3, 1, ?z)
        my_question = f"""
           SELECT ?z WHERE {{
           ?s <http://value.org/operation> <http://value.org/add_number> .
           ?s <http://value.org/variable_x> <http://value.org/three> .
           ?s <http://value.org/variable_y> <http://value.org/one> .
           ?s <http://value.org/variable_z> ?z .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        pass

        # add(2, 2, ?ans)
        my_question = f"""
           SELECT ?ans WHERE {{ ?s <http://value.org/operation> <http://value.org/add_number> .
           ?s <http://value.org/variable_x> <http://value.org/two> .
           ?s <http://value.org/variable_y> <http://value.org/two> .
           ?s <http://value.org/variable_z> ?z .
           }} """
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        pass

    #     # add(3, 2, ?ans)
    #     # my_question = f"""
    #     #    SELECT ?ans WHERE {{
    #     #    ?s <http://value.org/operation> <http://value.org/add_number> .
    #     #    ?s <http://value.org/variable_x> <http://value.org/three> .
    #     #    ?s <http://value.org/variable_y> <http://value.org/two> .
    #     #    ?s <http://value.org/variable_z> ?ans .
    #     #    }}"""
    #
    #     # add(3, 2, ?z)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/add_number> .
    #        ?s <http://value.org/variable_x> <http://value.org/three> .
    #        ?s <http://value.org/variable_y> <http://value.org/two> .
    #        ?s <http://value.org/variable_z> ?z .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     pass
    #
    #     # add(3, 2, ?z), next(?z, ?ans)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s1 <http://value.org/operation> <http://value.org/add_number> .
    #        ?s1 <http://value.org/variable_x> <http://value.org/three> .
    #        ?s1 <http://value.org/variable_y> <http://value.org/two> .
    #        ?s1 <http://value.org/variable_z> ?z .
    #        ?s2 <http://value.org/operation> <http://value.org/next_number> .
    #        ?s2 <http://value.org/variable_x> ?z .
    #        ?s2 <http://value.org/variable_y> ?ans .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     pass
    #
    #     # add(3, 2, ?z), add(?z, 2, ?ans) -> 3+2+2 = 7
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s1 <http://value.org/operation> <http://value.org/add_number> .
    #        ?s1 <http://value.org/variable_x> <http://value.org/three> .
    #        ?s1 <http://value.org/variable_y> <http://value.org/two> .
    #        ?s1 <http://value.org/variable_z> ?z .
    #        ?s2 <http://value.org/operation> <http://value.org/add_number> .
    #        ?s2 <http://value.org/variable_x> ?z .
    #        ?s2 <http://value.org/variable_y> <http://value.org/two> .
    #        ?s2 <http://value.org/variable_z> ?ans .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     pass
    #
    #     # add(2, ?ans, 3)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/add_number> .
    #        ?s <http://value.org/variable_x> <http://value.org/two> .
    #        ?s <http://value.org/variable_y> ?ans .
    #        ?s <http://value.org/variable_z> <http://value.org/three> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # rdf_prolog.answer_question(my_sparql_query)

        # add(3, ?ans, 5)
        my_question = f"""
           SELECT ?ans WHERE {{
           ?s <http://value.org/operation> <http://value.org/add_number> .
           ?s <http://value.org/variable_x> <http://value.org/three> .
           ?s <http://value.org/variable_y> ?ans .
           ?s <http://value.org/variable_z> <http://value.org/five> .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        rdf_prolog.answer_question(my_sparql_query)

        # add(1, ?y, ?z)
        my_question = f"""
           SELECT ?y ?z WHERE {{
           ?s <http://value.org/operation> <http://value.org/add_number> .
           ?s <http://value.org/variable_x> <http://value.org/one> .
           ?s <http://value.org/variable_y> ?y .
           ?s <http://value.org/variable_z> ?z .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10, depth_limit=100)
        pass

    #     # add(9, ?y, ?z)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/add_number> .
    #        ?s <http://value.org/variable_x> <http://value.org/nine> .
    #        ?s <http://value.org/variable_y> ?y .
    #        ?s <http://value.org/variable_z> ?z .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10)
    #     pass
    #
    #     # add(?x, 1, ?z)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/add_number> .
    #        ?s <http://value.org/variable_x> ?x .
    #        ?s <http://value.org/variable_y> <http://value.org/one> .
    #        ?s <http://value.org/variable_z> ?z .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10)
    #     pass
    #
    #     # add(?x, 9, ?z)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/add_number> .
    #        ?s <http://value.org/variable_x> ?x .
    #        ?s <http://value.org/variable_y> <http://value.org/nine> .
    #        ?s <http://value.org/variable_z> ?z .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10)
    #     pass
    #
    #     # add(?x, ?y, 2)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/add_number> .
    #        ?s <http://value.org/variable_x> ?x .
    #        ?s <http://value.org/variable_y> ?y .
    #        ?s <http://value.org/variable_z> <http://value.org/two> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10)
    #     pass
    #
    #     # add(?x, ?y, 3)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/add_number> .
    #        ?s <http://value.org/variable_x> ?x .
    #        ?s <http://value.org/variable_y> ?y .
    #        ?s <http://value.org/variable_z> <http://value.org/three> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10)
    #     pass
    #
    #     # add(3, 1, ?ans) depth_limit=0
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/add_number> .
    #        ?s <http://value.org/variable_x> <http://value.org/three> .
    #        ?s <http://value.org/variable_y> <http://value.org/one> .
    #        ?s <http://value.org/variable_z> ?ans .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=1)
    #
    #     # add(3, 1, ?ans) depth_limit=1
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/add_number> .
    #        ?s <http://value.org/variable_x> <http://value.org/three> .
    #        ?s <http://value.org/variable_y> <http://value.org/one> .
    #        ?s <http://value.org/variable_z> ?ans .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=2)
        pass

    # subtract
    if True:
    #     rdf_prolog = RdfProlog(rules_folder='../rules/rules_number')
    #     # subtract(5, 3, ?ans)
    #     my_question = f"""
    #         SELECT ?ans WHERE {{
    #         ?s <http://value.org/operation> <http://value.org/subtract_number> .
    #         ?s <http://value.org/variable_x> <http://value.org/five> .
    #         ?s <http://value.org/variable_y> <http://value.org/three> .
    #         ?s <http://value.org/variable_z> ?ans .
    #         }}
    #         """
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # rdf_prolog.answer_question(my_sparql_query)
    #
    #     # subtract(3, 2, ?ans)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/subtract_number> .
    #        ?s <http://value.org/variable_x> <http://value.org/three> .
    #        ?s <http://value.org/variable_y> <http://value.org/two> .
    #        ?s <http://value.org/variable_z> ?ans .
    #        }}
    #         """
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # rdf_prolog.answer_question(my_sparql_query)
    #
    #     # subtract(3, 2, ?z), add(?z, 2, ?ans)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s1 <http://value.org/operation> <http://value.org/subtract_number> .
    #        ?s1 <http://value.org/variable_x> <http://value.org/three> .
    #        ?s1 <http://value.org/variable_y> <http://value.org/two> .
    #        ?s1 <http://value.org/variable_z> ?z .
    #        ?s2 <http://value.org/operation> <http://value.org/add_number> .
    #        ?s2 <http://value.org/variable_x> ?z .
    #        ?s2 <http://value.org/variable_y> <http://value.org/two> .
    #        ?s2 <http://value.org/variable_z> ?ans .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        pass

    # next_100
    if True:  # next_100
    #     rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')
    #     # next(1, ?ans)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/next_number> .
    #        ?s <http://value.org/variable_x> <http://value.org/1> .
    #        ?s <http://value.org/variable_y> ?ans .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     # xxx = resolve_bindings[0]['?ans']
        pass

    # add_100
    if True:
        # rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')
        # add(3, ?ans, 5)->ans:2
        my_question = f"""
            SELECT ?ans WHERE {{
            ?s <http://value.org/operation> <http://value.org/add_number> . 
            ?s <http://value.org/variable_x> <http://value.org/3> . 
            ?s <http://value.org/variable_y> ?ans . 
            ?s <http://value.org/variable_z> <http://value.org/5> . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=10)

    # multiply_100
    if True:  # multiply_100
        # rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')

        # multiply(2, 1, ?ans)
        my_question = f"""
           SELECT ?ans WHERE {{
           ?s <http://value.org/operation> <http://value.org/multiply_number> .
           ?s <http://value.org/variable_x> <http://value.org/2> .
           ?s <http://value.org/variable_y> <http://value.org/1> .
           ?s <http://value.org/variable_z> ?ans .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        # xxx = resolve_bindings[0]['?ans']
        pass

        # multiply(1, 2, ?ans)
        my_question = f"""
                   SELECT ?ans WHERE {{
                   ?s <http://value.org/operation> <http://value.org/multiply_number> .
                   ?s <http://value.org/variable_x> <http://value.org/1> .
                   ?s <http://value.org/variable_y> <http://value.org/2> .
                   ?s <http://value.org/variable_z> ?ans .
                   }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        # xxx = resolve_bindings[0]['?ans']
        pass

        # multiply(2, 2, ?ans)
        my_question = f"""
           SELECT ?ans WHERE {{
           ?s <http://value.org/operation> <http://value.org/multiply_number> .
           ?s <http://value.org/variable_x> <http://value.org/2> .
           ?s <http://value.org/variable_y> <http://value.org/2> .
           ?s <http://value.org/variable_z> ?ans .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        # xxx = resolve_bindings[0]['?ans']
        pass

        # multiply(3, 2, ?ans) = 6
        my_question = f"""
            SELECT ?ans WHERE {{
            ?s <http://value.org/operation> <http://value.org/multiply_number> .
            ?s <http://value.org/variable_x> <http://value.org/3> .
            ?s <http://value.org/variable_y> <http://value.org/2> .
            ?s <http://value.org/variable_z> ?ans .
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # multiply(?ans, 2, 6)
        my_question = f"""
           SELECT ?ans WHERE {{
           ?s <http://value.org/operation> <http://value.org/multiply_number> .
           ?s <http://value.org/variable_x> ?ans .
           ?s <http://value.org/variable_y> <http://value.org/2> .
           ?s <http://value.org/variable_z> <http://value.org/6> .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)
        # xxx = resolve_bindings[0]['?ans']
        pass

        # divide(?ans, 2, 3)
        my_question = f"""
            SELECT ?ans WHERE {{
            ?s <http://value.org/operation> <http://value.org/divide_number> .
            ?s <http://value.org/variable_x> ?ans .
            ?s <http://value.org/variable_y> <http://value.org/2> .
            ?s <http://value.org/variable_z> <http://value.org/3> .
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        # xxx = resolve_bindings[0]['?ans']
        pass

    # fibonacci_100
    if True:  # fibonacci_100
        # rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')

        # fibonacci(1, ?ans) ?ans = 1
        my_question = f"""
            SELECT ?ans WHERE {{
            ?s <http://value.org/operation> <http://value.org/fibonacci_number> . 
            ?s <http://value.org/variable_x> <http://value.org/1> . 
            ?s <http://value.org/variable_y> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

    # function_100
    if True:  # function_100
        # rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')

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
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        # xxx = resolve_bindings[0]['?ans']

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
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # factorial(4, ?ans) -> ?ans = 24
        my_question = f"""
           SELECT ?ans WHERE {{
           ?s <http://value.org/operation> <http://value.org/factorial> .
           ?s <http://value.org/variable_x> <http://value.org/4> .
           ?s <http://value.org/variable_fact> ?ans .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        pass

    # family
    if True:
    #     rdf_prolog = RdfProlog(rules_folder='../rules/rules_human')
    #     # grandfather(taro, ?ans)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/grandfather> .
    #        ?s <http://value.org/variable_x> <http://value.org/taro> .
    #        ?s <http://value.org/variable_y> ?ans .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        pass

    # mortal
    if True:
    #     rdf_prolog = RdfProlog(rules_folder='../rules/rules_human')
    #     # mortal(?ans)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/mortal> .
    #        ?s <http://value.org/variable_x> ?ans .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # rdf_prolog.answer_question(my_sparql_query)
        pass

    # knows
    if True:
        # rdf_prolog = RdfProlog(rules_folder='../rules/rules_human')

    #     # knows(andy, bob)
    #     my_question = f"""
    #        SELECT ?s WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/knows_direct> .
    #        ?s <http://value.org/variable_x> <http://value.org/andy> .
    #        ?s <http://value.org/variable_y> <http://value.org/bob> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # rdf_prolog.answer_question(my_sparql_query)
    #
    #     # knows_direct(andy, chris)
    #     my_question = f"""
    #        SELECT ?s WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/knows_direct> .
    #        ?s <http://value.org/variable_x> <http://value.org/andy> .
    #        ?s <http://value.org/variable_y> <http://value.org/chris> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # rdf_prolog.answer_question(my_sparql_query)
    #
        # knows_direct(andy, ?ans)
        my_question = f"""
           SELECT ?s ?ans WHERE {{
           ?s <http://value.org/operation> <http://value.org/knows_direct> .
           ?s <http://value.org/variable_x> <http://value.org/andy> .
           ?s <http://value.org/variable_y> ?ans .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # rdf_prolog.answer_question(my_sparql_query, results_limit=2)
    #
    #     # knows_indirect(andy, chris)
    #     my_question = f"""
    #        SELECT ?s WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/knows_indirect> .
    #        ?s <http://value.org/variable_x> <http://value.org/andy> .
    #        ?s <http://value.org/variable_y> <http://value.org/chris> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # rdf_prolog.answer_question(my_sparql_query)
    #
    #     # knows_indirect(andy, edgar)
    #     my_question = f"""
    #        SELECT ?s WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/knows_indirect> .
    #        ?s <http://value.org/variable_x> <http://value.org/andy> .
    #        ?s <http://value.org/variable_y> <http://value.org/edgar> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # rdf_prolog.answer_question(my_sparql_query)
    #
        # knows_indirect(andy, ?ans)
        my_question = f"""
           SELECT ?s WHERE {{
           ?s <http://value.org/operation> <http://value.org/knows_indirect> .
           ?s <http://value.org/variable_x> <http://value.org/andy> .
           ?s <http://value.org/variable_y> ?ans .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # rdf_prolog.answer_question(my_sparql_query)

        # knows(andy, ?ans)
        my_question = f"""
           SELECT ?ans WHERE {{
           ?s <http://value.org/operation> <http://value.org/knows> .
           ?s <http://value.org/variable_x> <http://value.org/andy> .
           ?s <http://value.org/variable_y> ?ans .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # rdf_prolog.answer_question(my_sparql_query, results_limit=4)
        pass

    # list_number next
    # if True:
    #     rdf_prolog = RdfProlog(rules_folder='../rules/rules_list_number')
    #     # next(1, ?ans)
    #     my_question = f"""
    #        SELECT ?ans ?car ?cdr WHERE {{
    #        ?s <http://value.org/operation> <http://value.org/next_list_number> .
    #        ?s <http://value.org/variable_x> <http://value.org/list_one> .
    #        ?s <http://value.org/variable_y> ?ans .
    #        ?s2 <http://value.org/operation> <http://value.org/cons> .
    #        ?s2 <http://value.org/variable_x> ?car .
    #        ?s2 <http://value.org/variable_y> ?cdr .
    #        ?s2 <http://value.org/variable_z> ?ans .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

    #     # next(2, ?ans)
    #     my_question = f"""
    #        SELECT ?list_three ?car ?cdr WHERE {{
    #        ?s1 <http://value.org/operation> <http://value.org/cons> . 
    #        ?s1 <http://value.org/variable_x> <http://value.org/two> . 
    #        ?s1 <http://value.org/variable_y> <http://value.org/nil> . 
    #        ?s1 <http://value.org/variable_z> ?list_two . 
    #        ?s2 <http://value.org/operation> <http://value.org/next_list_number> . 
    #        ?s2 <http://value.org/variable_x> ?list_two . 
    #        ?s2 <http://value.org/variable_y> ?list_three . 
    #        ?s3 <http://value.org/operation> <http://value.org/cons> . 
    #        ?s3 <http://value.org/variable_x> ?car . 
    #        ?s3 <http://value.org/variable_y> ?cdr . 
    #        ?s3 <http://value.org/variable_z> ?list_three . 
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #
    #     # next(9, ?ans)
    #     my_question = f"""
    #        SELECT ?list_three ?car ?cdr WHERE {{
    #        ?s1 <http://value.org/operation> <http://value.org/cons> . 
    #        ?s1 <http://value.org/variable_x> <http://value.org/nine> . 
    #        ?s1 <http://value.org/variable_y> <http://value.org/nil> . 
    #        ?s1 <http://value.org/variable_z> ?list_nine . 
    #        ?s2 <http://value.org/operation> <http://value.org/next_list_number> . 
    #        ?s2 <http://value.org/variable_x> ?list_nine . 
    #        ?s2 <http://value.org/variable_y> ?list_ten . 
    #        ?s3 <http://value.org/operation> <http://value.org/cons> . 
    #        ?s3 <http://value.org/variable_x> ?car_ten . 
    #        ?s3 <http://value.org/variable_y> ?cdr_ten . 
    #        ?s3 <http://value.org/variable_z> ?list_ten . 
    #        ?s4 <http://value.org/operation> <http://value.org/cons> . 
    #        ?s4 <http://value.org/variable_x> ?car . 
    #        ?s4 <http://value.org/variable_y> ?cdr . 
    #        ?s4 <http://value.org/variable_z> ?cdr_ten . 
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #
    #     # next(?ans, [2])
    #     my_question = f"""
    #        SELECT ?list_one ?car ?cdr WHERE {{
    #        ?s3 <http://value.org/operation> <http://value.org/cons> . 
    #        ?s3 <http://value.org/variable_x> <http://value.org/two> . 
    #        ?s3 <http://value.org/variable_y> <http://value.org/nil> . 
    #        ?s3 <http://value.org/variable_z> ?list_two . 
    #        ?s2 <http://value.org/operation> <http://value.org/next_list_number> . 
    #        ?s2 <http://value.org/variable_x> ?list_one . 
    #        ?s2 <http://value.org/variable_y> ?list_two . 
    #        ?s4 <http://value.org/operation> <http://value.org/cons> . 
    #        ?s4 <http://value.org/variable_x> ?car . 
    #        ?s4 <http://value.org/variable_y> ?cdr . 
    #        ?s4 <http://value.org/variable_z> ?list_one . 
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #
    #     # next(?ans, [3])
    #     my_question = f"""
    #        SELECT ?list_two ?car ?cdr WHERE {{
    #        ?s3 <http://value.org/operation> <http://value.org/cons> . 
    #        ?s3 <http://value.org/variable_x> <http://value.org/three> . 
    #        ?s3 <http://value.org/variable_y> <http://value.org/nil> . 
    #        ?s3 <http://value.org/variable_z> ?list_three . 
    #        ?s2 <http://value.org/operation> <http://value.org/next_list_number> . 
    #        ?s2 <http://value.org/variable_x> ?list_two . 
    #        ?s2 <http://value.org/variable_y> ?list_three . 
    #        ?s4 <http://value.org/operation> <http://value.org/cons> . 
    #        ?s4 <http://value.org/variable_x> ?car . 
    #        ?s4 <http://value.org/variable_y> ?cdr . 
    #        ?s4 <http://value.org/variable_z> ?list_two . 
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #
    #     # next(?ans, [3])
    #     my_question = f"""
    #        SELECT ?list_two ?car ?cdr WHERE {{
    #        ?s1 <http://value.org/operation> <http://value.org/cons> . 
    #        ?s1 <http://value.org/variable_x> <http://value.org/two> . 
    #        ?s1 <http://value.org/variable_y> <http://value.org/nil> . 
    #        ?s1 <http://value.org/variable_z> ?list_dummy . 
    #        ?s3 <http://value.org/operation> <http://value.org/cons> . 
    #        ?s3 <http://value.org/variable_x> <http://value.org/three> . 
    #        ?s3 <http://value.org/variable_y> <http://value.org/nil> . 
    #        ?s3 <http://value.org/variable_z> ?list_three . 
    #        ?s2 <http://value.org/operation> <http://value.org/next_list_number> . 
    #        ?s2 <http://value.org/variable_x> ?list_two . 
    #        ?s2 <http://value.org/variable_y> ?list_three . 
    #        ?s4 <http://value.org/operation> <http://value.org/cons> . 
    #        ?s4 <http://value.org/variable_x> ?car . 
    #        ?s4 <http://value.org/variable_y> ?cdr . 
    #        ?s4 <http://value.org/variable_z> ?list_two . 
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        pass

    # list number next
    if True:
        # rdf_prolog = RdfProlog(rules_folder='../rules/rules_list_number')

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
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # next([9, 9], ?ans) = [0, 0, 1] means 100
        my_question = f"""
            SELECT ?car_one_hundred ?car ?cdr WHERE {{
            ?s1 <http://value.org/operation> <http://value.org/cons> .
            ?s1 <http://value.org/variable_x> <http://value.org/nine> .
            ?s1 <http://value.org/variable_y> <http://value.org/nil> .
            ?s1 <http://value.org/variable_z> ?list_nine .
            ?s1b <http://value.org/operation> <http://value.org/cons> .
            ?s1b <http://value.org/variable_x> <http://value.org/nine> .
            ?s1b <http://value.org/variable_y> ?list_nine .
            ?s1b <http://value.org/variable_z> ?list_ninety_nine .
            ?s2 <http://value.org/operation> <http://value.org/next_list_number> .
            ?s2 <http://value.org/variable_x> ?list_ninety_nine .
            ?s2 <http://value.org/variable_y> ?list_one_hundred .
            ?s3 <http://value.org/operation> <http://value.org/cons> .
            ?s3 <http://value.org/variable_x> ?car_one_hundred .
            ?s3 <http://value.org/variable_y> ?cdr_one_hundred .
            ?s3 <http://value.org/variable_z> ?list_one_hundred .
            ?s4 <http://value.org/operation> <http://value.org/cons> .
            ?s4 <http://value.org/variable_x> ?car .
            ?s4 <http://value.org/variable_y> ?cdr .
            ?s4 <http://value.org/variable_z> ?cdr_one_hundred .
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

    # list number add
    if True:
        # rdf_prolog = RdfProlog(rules_folder='../rules/rules_list_number_add')
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
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

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
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

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
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

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
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # add(1, ?ans, 2)
        my_question = f"""
           SELECT ?ans ?car ?cdr WHERE {{
           ?s <http://value.org/operation> <http://value.org/list_add> . 
           ?s <http://value.org/variable_x> <http://value.org/list_one> . 
           ?s <http://value.org/variable_y> ?ans . 
           ?s <http://value.org/variable_z> <http://value.org/list_two> . 
           ?s2 <http://value.org/operation> <http://value.org/cons> . 
           ?s2 <http://value.org/variable_x> ?car . 
           ?s2 <http://value.org/variable_y> ?cdr . 
           ?s2 <http://value.org/variable_z> ?ans . 
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)


        # add(1, ?ans, 3)
        my_question = f"""
           SELECT ?ans ?car ?cdr WHERE {{
           ?s <http://value.org/operation> <http://value.org/list_add> . 
           ?s <http://value.org/variable_x> <http://value.org/list_one> . 
           ?s <http://value.org/variable_y> ?ans . 
           ?s <http://value.org/variable_z> <http://value.org/list_three> . 
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)
        pass

     # list number math
    if True:
        # rdf_prolog = RdfProlog(rules_folder='../rules/rules_list_number_math')

        # next([9, 9], ?ans) = [0, 0, 1] means 100
        my_question = f"""
            SELECT ?car_one_hundred ?car ?cdr WHERE {{
            ?s1 <http://value.org/operation> <http://value.org/cons> .
            ?s1 <http://value.org/variable_x> <http://value.org/nine> .
            ?s1 <http://value.org/variable_y> <http://value.org/nil> .
            ?s1 <http://value.org/variable_z> ?list_nine .
            ?s1b <http://value.org/operation> <http://value.org/cons> .
            ?s1b <http://value.org/variable_x> <http://value.org/nine> .
            ?s1b <http://value.org/variable_y> ?list_nine .
            ?s1b <http://value.org/variable_z> ?list_ninety_nine .
            ?s2 <http://value.org/operation> <http://value.org/next_list_number> .
            ?s2 <http://value.org/variable_x> ?list_ninety_nine .
            ?s2 <http://value.org/variable_y> ?list_one_hundred .
            ?s3 <http://value.org/operation> <http://value.org/cons> .
            ?s3 <http://value.org/variable_x> ?car_one_hundred .
            ?s3 <http://value.org/variable_y> ?cdr_one_hundred .
            ?s3 <http://value.org/variable_z> ?list_one_hundred .
            ?s4 <http://value.org/operation> <http://value.org/cons> .
            ?s4 <http://value.org/variable_x> ?car .
            ?s4 <http://value.org/variable_y> ?cdr .
            ?s4 <http://value.org/variable_z> ?cdr_one_hundred .
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

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
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

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
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

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
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # multiply(2, 1, ?ans) -> ?ans = 2
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s <http://value.org/operation> <http://value.org/list_multiply> . 
            ?s <http://value.org/variable_x> <http://value.org/list_three> . 
            ?s <http://value.org/variable_y> <http://value.org/list_one> . 
            ?s <http://value.org/variable_z> ?ans . 
            ?s2 <http://value.org/operation> <http://value.org/cons> . 
            ?s2 <http://value.org/variable_x> ?car . 
            ?s2 <http://value.org/variable_y> ?cdr . 
            ?s2 <http://value.org/variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)

        # multiply(3, 1, ?ans) -> ?ans = 3
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s <http://value.org/operation> <http://value.org/list_multiply> . 
            ?s <http://value.org/variable_x> <http://value.org/list_three> . 
            ?s <http://value.org/variable_y> <http://value.org/list_one> . 
            ?s <http://value.org/variable_z> ?ans . 
            ?s2 <http://value.org/operation> <http://value.org/cons> . 
            ?s2 <http://value.org/variable_x> ?car . 
            ?s2 <http://value.org/variable_y> ?cdr . 
            ?s2 <http://value.org/variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)

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
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)

        # multiply(3, ?ans, 3) -> ?ans = 1
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s <http://value.org/operation> <http://value.org/list_multiply> . 
            ?s <http://value.org/variable_x> <http://value.org/list_three> . 
            ?s <http://value.org/variable_y> ?ans . 
            ?s <http://value.org/variable_z> <http://value.org/list_three> . 
            ?s2 <http://value.org/operation> <http://value.org/cons> . 
            ?s2 <http://value.org/variable_x> ?car . 
            ?s2 <http://value.org/variable_y> ?cdr . 
            ?s2 <http://value.org/variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)

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
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=150)

        # divide(6, 2, ?ans) -> ?ans = [3]
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s1 <http://value.org/operation> <http://value.org/cons> . 
            ?s1 <http://value.org/variable_x> <http://value.org/six> . 
            ?s1 <http://value.org/variable_y> <http://value.org/nil> . 
            ?s1 <http://value.org/variable_z> ?list_15 . 
            ?s2 <http://value.org/operation> <http://value.org/list_divide> . 
            ?s2 <http://value.org/variable_x> ?list_15 . 
            ?s2 <http://value.org/variable_y> <http://value.org/list_two> . 
            ?s2 <http://value.org/variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=50)

        # divide(5, 2, ?ans)
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s <http://value.org/operation> <http://value.org/list_divide> .
            ?s <http://value.org/variable_x> <http://value.org/list_five> .
            ?s <http://value.org/variable_y> <http://value.org/list_two> .
            ?s <http://value.org/variable_z> ?ans .
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=200)

        # fibinacci(1, ?ans) -> ?ans = 1
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s <http://value.org/operation> <http://value.org/fibonacci_number> . 
            ?s <http://value.org/variable_x> <http://value.org/list_one> . 
            ?s <http://value.org/variable_y> ?ans . 
            ?s2 <http://value.org/operation> <http://value.org/cons> . 
            ?s2 <http://value.org/variable_x> ?car . 
            ?s2 <http://value.org/variable_y> ?cdr . 
            ?s2 <http://value.org/variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)

        # fibinacci(3, ?ans) -> ?ans = 2
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s <http://value.org/operation> <http://value.org/fibonacci_number> . 
            ?s <http://value.org/variable_x> <http://value.org/list_three> . 
            ?s <http://value.org/variable_y> ?ans . 
            ?s2 <http://value.org/operation> <http://value.org/cons> . 
            ?s2 <http://value.org/variable_x> ?car . 
            ?s2 <http://value.org/variable_y> ?cdr . 
            ?s2 <http://value.org/variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=300)

        pass


if __name__ == '__main__':
    main()  # execute the main function
