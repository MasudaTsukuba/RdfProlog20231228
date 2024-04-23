"""Main module to run RdfProlog
RdfPrologMain.py
Executing Prolog on RDF query system
Main function
2022/12/20, 2023/3/16, 2023/10/30, 2023/11/6, 2023/11/28
T. Masuda
"""
# import os.path
# import logging

from src.RdfClass import *
from src.RdfResolution import RdfProlog, start_log


def main():
    """Main function for RdfProlog.

    Args:

    Returns:

    """
    start_log()

    # next
    if True:  # next
    #     rdf_prolog = RdfProlog(rules_folder='rules/rules_number')
    #     # next(1, ?ans)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <{OPERATION}> <{VAL}next_number> .
    #        ?s <{VAL}variable_x> <{VAL}one> .
    #        ?s <{VAL}variable_y> ?ans .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     xxx = resolve_bindings[0]['?ans']
    #     pass

    #     # next(?ans, 3)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <{OPERATION}> <{VAL}next_number> .
    #        ?s <{VAL}variable_x> ?ans .
    #        ?s <{VAL}variable_y> <{VAL}three> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     pass
    #
    #     # next(1, 2)
    #     my_question = f"""
    #        SELECT ?s WHERE {{
    #        ?s <{OPERATION}> <{VAL}next_number> .
    #        ?s <{VAL}variable_x> <{VAL}one> .
    #        ?s <{VAL}variable_y> <{VAL}two> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     pass
    #
    #     # next(1, 3)
    #     my_question = f"""
    #        SELECT ?s WHERE {{
    #        ?s <{OPERATION}> <{VAL}next_number> .
    #        ?s <{VAL}variable_x> <{VAL}one> .
    #        ?s <{VAL}variable_y> <{VAL}three> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     pass
    #
    #     # next(1, ?z),next(?z, ?ans)
    #     # my_question = f"""
    #     #    SELECT ?ans WHERE {{
    #     #    ?s1 <{OPERATION}> <{VAL}next_number> .
    #     #    ?s1 <{VAL}variable_x> <{VAL}one> .
    #     #    ?s1 <{VAL}variable_y> ?z .
    #     #    ?s2 <{OPERATION}> <{VAL}next_number> .
    #     #    ?s2 <{VAL}variable_x> ?z .
    #     #    ?s2 <{VAL}variable_y> ?ans .
    #     #    }}"""
    #     # next(1, ?z),next(?z, ?x)
    #     my_question = f"""
    #        SELECT ?x WHERE {{
    #        ?s1 <{OPERATION}> <{VAL}next_number> .
    #        ?s1 <{VAL}variable_x> <{VAL}one> .
    #        ?s1 <{VAL}variable_y> ?z .
    #        ?s2 <{OPERATION}> <{VAL}next_number> .
    #        ?s2 <{VAL}variable_x> ?z .
    #        ?s2 <{VAL}variable_y> ?x .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     pass
    #
    #     # next(?x, ?y)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <{OPERATION}> <{VAL}next_number> .
    #        ?s <{VAL}variable_x> ?x .
    #        ?s <{VAL}variable_y> ?y .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        pass

    # add
    if True:
        # rdf_prolog = RdfProlog(rules_folder='../rules/rules_number')

        # add(3, 1, ?ans)
        my_question = f"""
           SELECT ?ans WHERE {{
           ?s <{OPERATION}> <{VAL}add_number> .
           ?s <{VAL}variable_x> <{VAL}three> .
           ?s <{VAL}variable_y> <{VAL}one> .
           ?s <{VAL}variable_z> ?ans .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # add(3, 1, ?z)
        my_question = f"""
           SELECT ?z WHERE {{
           ?s <{OPERATION}> <{VAL}add_number> .
           ?s <{VAL}variable_x> <{VAL}three> .
           ?s <{VAL}variable_y> <{VAL}one> .
           ?s <{VAL}variable_z> ?z .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        pass

        # add(2, 2, ?ans)
        my_question = f"""
           SELECT ?ans WHERE {{ ?s <{OPERATION}> <{VAL}add_number> .
           ?s <{VAL}variable_x> <{VAL}two> .
           ?s <{VAL}variable_y> <{VAL}two> .
           ?s <{VAL}variable_z> ?z .
           }} """
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        pass

    #     # add(3, 2, ?ans)
    #     # my_question = f"""
    #     #    SELECT ?ans WHERE {{
    #     #    ?s <{OPERATION}> <{VAL}add_number> .
    #     #    ?s <{VAL}variable_x> <{VAL}three> .
    #     #    ?s <{VAL}variable_y> <{VAL}two> .
    #     #    ?s <{VAL}variable_z> ?ans .
    #     #    }}"""
    #
    #     # add(3, 2, ?z)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <{OPERATION}> <{VAL}add_number> .
    #        ?s <{VAL}variable_x> <{VAL}three> .
    #        ?s <{VAL}variable_y> <{VAL}two> .
    #        ?s <{VAL}variable_z> ?z .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     pass
    #
    #     # add(3, 2, ?z), next(?z, ?ans)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s1 <{OPERATION}> <{VAL}add_number> .
    #        ?s1 <{VAL}variable_x> <{VAL}three> .
    #        ?s1 <{VAL}variable_y> <{VAL}two> .
    #        ?s1 <{VAL}variable_z> ?z .
    #        ?s2 <{OPERATION}> <{VAL}next_number> .
    #        ?s2 <{VAL}variable_x> ?z .
    #        ?s2 <{VAL}variable_y> ?ans .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     pass
    #
    #     # add(3, 2, ?z), add(?z, 2, ?ans) -> 3+2+2 = 7
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s1 <{OPERATION}> <{VAL}add_number> .
    #        ?s1 <{VAL}variable_x> <{VAL}three> .
    #        ?s1 <{VAL}variable_y> <{VAL}two> .
    #        ?s1 <{VAL}variable_z> ?z .
    #        ?s2 <{OPERATION}> <{VAL}add_number> .
    #        ?s2 <{VAL}variable_x> ?z .
    #        ?s2 <{VAL}variable_y> <{VAL}two> .
    #        ?s2 <{VAL}variable_z> ?ans .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #     pass
    #
    #     # add(2, ?ans, 3)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <{OPERATION}> <{VAL}add_number> .
    #        ?s <{VAL}variable_x> <{VAL}two> .
    #        ?s <{VAL}variable_y> ?ans .
    #        ?s <{VAL}variable_z> <{VAL}three> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # rdf_prolog.answer_question(my_sparql_query)

        # add(3, ?ans, 5)
        my_question = f"""
           SELECT ?ans WHERE {{
           ?s <{OPERATION}> <{VAL}add_number> .
           ?s <{VAL}variable_x> <{VAL}three> .
           ?s <{VAL}variable_y> ?ans .
           ?s <{VAL}variable_z> <{VAL}five> .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # rdf_prolog.answer_question(my_sparql_query)

        # add(1, ?y, ?z)
        my_question = f"""
           SELECT ?y ?z WHERE {{
           ?s <{OPERATION}> <{VAL}add_number> .
           ?s <{VAL}variable_x> <{VAL}one> .
           ?s <{VAL}variable_y> ?y .
           ?s <{VAL}variable_z> ?z .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10, depth_limit=100)
        pass

    #     # add(9, ?y, ?z)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <{OPERATION}> <{VAL}add_number> .
    #        ?s <{VAL}variable_x> <{VAL}nine> .
    #        ?s <{VAL}variable_y> ?y .
    #        ?s <{VAL}variable_z> ?z .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10)
    #     pass
    #
    #     # add(?x, 1, ?z)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <{OPERATION}> <{VAL}add_number> .
    #        ?s <{VAL}variable_x> ?x .
    #        ?s <{VAL}variable_y> <{VAL}one> .
    #        ?s <{VAL}variable_z> ?z .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10)
    #     pass
    #
    #     # add(?x, 9, ?z)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <{OPERATION}> <{VAL}add_number> .
    #        ?s <{VAL}variable_x> ?x .
    #        ?s <{VAL}variable_y> <{VAL}nine> .
    #        ?s <{VAL}variable_z> ?z .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10)
    #     pass
    #
    #     # add(?x, ?y, 2)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <{OPERATION}> <{VAL}add_number> .
    #        ?s <{VAL}variable_x> ?x .
    #        ?s <{VAL}variable_y> ?y .
    #        ?s <{VAL}variable_z> <{VAL}two> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10)
    #     pass
    #
    #     # add(?x, ?y, 3)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <{OPERATION}> <{VAL}add_number> .
    #        ?s <{VAL}variable_x> ?x .
    #        ?s <{VAL}variable_y> ?y .
    #        ?s <{VAL}variable_z> <{VAL}three> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=10)
    #     pass
    #
    #     # add(3, 1, ?ans) depth_limit=0
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <{OPERATION}> <{VAL}add_number> .
    #        ?s <{VAL}variable_x> <{VAL}three> .
    #        ?s <{VAL}variable_y> <{VAL}one> .
    #        ?s <{VAL}variable_z> ?ans .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=1)
    #
    #     # add(3, 1, ?ans) depth_limit=1
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <{OPERATION}> <{VAL}add_number> .
    #        ?s <{VAL}variable_x> <{VAL}three> .
    #        ?s <{VAL}variable_y> <{VAL}one> .
    #        ?s <{VAL}variable_z> ?ans .
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
    #         ?s <{OPERATION}> <{VAL}subtract_number> .
    #         ?s <{VAL}variable_x> <{VAL}five> .
    #         ?s <{VAL}variable_y> <{VAL}three> .
    #         ?s <{VAL}variable_z> ?ans .
    #         }}
    #         """
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # rdf_prolog.answer_question(my_sparql_query)
    #
    #     # subtract(3, 2, ?ans)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s <{OPERATION}> <{VAL}subtract_number> .
    #        ?s <{VAL}variable_x> <{VAL}three> .
    #        ?s <{VAL}variable_y> <{VAL}two> .
    #        ?s <{VAL}variable_z> ?ans .
    #        }}
    #         """
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # rdf_prolog.answer_question(my_sparql_query)
    #
    #     # subtract(3, 2, ?z), add(?z, 2, ?ans)
    #     my_question = f"""
    #        SELECT ?ans WHERE {{
    #        ?s1 <{OPERATION}> <{VAL}subtract_number> .
    #        ?s1 <{VAL}variable_x> <{VAL}three> .
    #        ?s1 <{VAL}variable_y> <{VAL}two> .
    #        ?s1 <{VAL}variable_z> ?z .
    #        ?s2 <{OPERATION}> <{VAL}add_number> .
    #        ?s2 <{VAL}variable_x> ?z .
    #        ?s2 <{VAL}variable_y> <{VAL}two> .
    #        ?s2 <{VAL}variable_z> ?ans .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        pass

    # next_100
    if True:  # next_100
        # rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')
        # # next(1, ?ans)
        # my_question = f"""
        #    SELECT ?ans WHERE {{
        #    ?s <{OPERATION}> <{VAL}next_number> .
        #    ?s <{VAL}variable_x> <{VAL}1> .
        #    ?s <{VAL}variable_y> ?ans .
        #    }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        # # xxx = resolve_bindings[0]['?ans']
        pass

    # add_100
    if True:
        # rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')

        # add(3, ?ans, 5)->ans:2
        my_question = f"""
            SELECT ?ans WHERE {{
            ?s <{OPERATION}> <{VAL}add_number> . 
            ?s <{VAL}variable_x> <{VAL}3> . 
            ?s <{VAL}variable_y> ?ans . 
            ?s <{VAL}variable_z> <{VAL}5> . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=10)

    # multiply_100
    if True:  # multiply_100
        # rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')

        # multiply(2, 1, ?ans)
        my_question = f"""
           SELECT ?ans WHERE {{
           ?s <{OPERATION}> <{VAL}multiply_number> .
           ?s <{VAL}variable_x> <{VAL}2> .
           ?s <{VAL}variable_y> <{VAL}1> .
           ?s <{VAL}variable_z> ?ans .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=10)
        # xxx = resolve_bindings[0]['?ans']
        pass

        # multiply(1, 2, ?ans)
        my_question = f"""
                   SELECT ?ans WHERE {{
                   ?s <{OPERATION}> <{VAL}multiply_number> .
                   ?s <{VAL}variable_x> <{VAL}1> .
                   ?s <{VAL}variable_y> <{VAL}2> .
                   ?s <{VAL}variable_z> ?ans .
                   }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        # xxx = resolve_bindings[0]['?ans']
        pass

        # multiply(2, 2, ?ans)
        my_question = f"""
           SELECT ?ans WHERE {{
           ?s <{OPERATION}> <{VAL}multiply_number> .
           ?s <{VAL}variable_x> <{VAL}2> .
           ?s <{VAL}variable_y> <{VAL}2> .
           ?s <{VAL}variable_z> ?ans .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        # xxx = resolve_bindings[0]['?ans']
        pass

        # multiply(3, 2, ?ans) = 6
        my_question = f"""
            SELECT ?ans WHERE {{
            ?s <{OPERATION}> <{VAL}multiply_number> .
            ?s <{VAL}variable_x> <{VAL}3> .
            ?s <{VAL}variable_y> <{VAL}2> .
            ?s <{VAL}variable_z> ?ans .
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # multiply(?ans, 2, 6)
        my_question = f"""
           SELECT ?ans WHERE {{
           ?s <{OPERATION}> <{VAL}multiply_number> .
           ?s <{VAL}variable_x> ?ans .
           ?s <{VAL}variable_y> <{VAL}2> .
           ?s <{VAL}variable_z> <{VAL}6> .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)
        # xxx = resolve_bindings[0]['?ans']
        pass

        # divide(?ans, 2, 3)
        my_question = f"""
            SELECT ?ans WHERE {{
            ?s <{OPERATION}> <{VAL}divide_number> .
            ?s <{VAL}variable_x> ?ans .
            ?s <{VAL}variable_y> <{VAL}2> .
            ?s <{VAL}variable_z> <{VAL}3> .
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
            ?s <{OPERATION}> <{VAL}fibonacci_number> . 
            ?s <{VAL}variable_x> <{VAL}1> . 
            ?s <{VAL}variable_y> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

    # function_100
    if True:  # function_100
        # rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_100')

        # solve_simultaneous_linear_equation(2, 3, 12, 1, 1, 5, ?ans1, ?ans2)
        my_question = f"""
           SELECT ?ans1 ?ans2 WHERE {{
           ?s <{OPERATION}> <{VAL}solve_simultaneous_linear_equation> .
           ?s <{VAL}variable_a11> <{VAL}2> .
           ?s <{VAL}variable_a12> <{VAL}3> .
           ?s <{VAL}variable_b1> <{VAL}12> .
           ?s <{VAL}variable_a21> <{VAL}1> .
           ?s <{VAL}variable_a22> <{VAL}1> .
           ?s <{VAL}variable_b2> <{VAL}5> .
           ?s <{VAL}variable_x1> ?ans1 .
           ?s <{VAL}variable_x2> ?ans2 .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        # xxx = resolve_bindings[0]['?ans']

        # solve_simultaneous_linear_equation(2, 3, 12, 1, 1, 5, ?ans1, ?ans2), add(?ans1, ?ans2, ?ans) .
        my_question = f"""
           SELECT ?ans ?ans1 ?ans2 WHERE {{
           ?s <{OPERATION}> <{VAL}solve_simultaneous_linear_equation> .
           ?s <{VAL}variable_a11> <{VAL}3> .
           ?s <{VAL}variable_a12> <{VAL}2> .
           ?s <{VAL}variable_b1> <{VAL}22> .
           ?s <{VAL}variable_a21> <{VAL}2> .
           ?s <{VAL}variable_a22> <{VAL}1> .
           ?s <{VAL}variable_b2> <{VAL}13> .
           ?s <{VAL}variable_x1> ?ans1 .
           ?s <{VAL}variable_x2> ?ans2 .
           ?s2 <{OPERATION}> <{VAL}add_number> .
           ?s2 <{VAL}variable_x> ?ans1 .
           ?s2 <{VAL}variable_y> ?ans2 .
           ?s2 <{VAL}variable_z> ?ans .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # factorial(4, ?ans) -> ?ans = 24
        my_question = f"""
           SELECT ?ans WHERE {{
           ?s <{OPERATION}> <{VAL}factorial> .
           ?s <{VAL}variable_x> <{VAL}4> .
           ?s <{VAL}variable_fact> ?ans .
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
    #        ?s <{OPERATION}> <{VAL}grandfather> .
    #        ?s <{VAL}variable_x> <{VAL}taro> .
    #        ?s <{VAL}variable_y> ?ans .
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
    #        ?s <{OPERATION}> <{VAL}mortal> .
    #        ?s <{VAL}variable_x> ?ans .
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
    #        ?s <{OPERATION}> <{VAL}knows_direct> .
    #        ?s <{VAL}variable_x> <{VAL}andy> .
    #        ?s <{VAL}variable_y> <{VAL}bob> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # rdf_prolog.answer_question(my_sparql_query)
    #
    #     # knows_direct(andy, chris)
    #     my_question = f"""
    #        SELECT ?s WHERE {{
    #        ?s <{OPERATION}> <{VAL}knows_direct> .
    #        ?s <{VAL}variable_x> <{VAL}andy> .
    #        ?s <{VAL}variable_y> <{VAL}chris> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # rdf_prolog.answer_question(my_sparql_query)
    #
        # knows_direct(andy, ?ans)
        my_question = f"""
           SELECT ?s ?ans WHERE {{
           ?s <{OPERATION}> <{VAL}knows_direct> .
           ?s <{VAL}variable_x> <{VAL}andy> .
           ?s <{VAL}variable_y> ?ans .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # rdf_prolog.answer_question(my_sparql_query, results_limit=2)
    #
    #     # knows_indirect(andy, chris)
    #     my_question = f"""
    #        SELECT ?s WHERE {{
    #        ?s <{OPERATION}> <{VAL}knows_indirect> .
    #        ?s <{VAL}variable_x> <{VAL}andy> .
    #        ?s <{VAL}variable_y> <{VAL}chris> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # rdf_prolog.answer_question(my_sparql_query)
    #
    #     # knows_indirect(andy, edgar)
    #     my_question = f"""
    #        SELECT ?s WHERE {{
    #        ?s <{OPERATION}> <{VAL}knows_indirect> .
    #        ?s <{VAL}variable_x> <{VAL}andy> .
    #        ?s <{VAL}variable_y> <{VAL}edgar> .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # rdf_prolog.answer_question(my_sparql_query)
    #
        # knows_indirect(andy, ?ans)
        my_question = f"""
           SELECT ?s WHERE {{
           ?s <{OPERATION}> <{VAL}knows_indirect> .
           ?s <{VAL}variable_x> <{VAL}andy> .
           ?s <{VAL}variable_y> ?ans .
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # rdf_prolog.answer_question(my_sparql_query)

        # knows(andy, ?ans)
        my_question = f"""
           SELECT ?ans WHERE {{
           ?s <{OPERATION}> <{VAL}knows> .
           ?s <{VAL}variable_x> <{VAL}andy> .
           ?s <{VAL}variable_y> ?ans .
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
    #        ?s <{OPERATION}> <{VAL}next_list_number> .
    #        ?s <{VAL}variable_x> <{VAL}list_one> .
    #        ?s <{VAL}variable_y> ?ans .
    #        ?s2 <{OPERATION}> <{VAL}cons> .
    #        ?s2 <{VAL}variable_x> ?car .
    #        ?s2 <{VAL}variable_y> ?cdr .
    #        ?s2 <{VAL}variable_z> ?ans .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

    #     # next(2, ?ans)
    #     my_question = f"""
    #        SELECT ?list_three ?car ?cdr WHERE {{
    #        ?s1 <{OPERATION}> <{VAL}cons> .
    #        ?s1 <{VAL}variable_x> <{VAL}two> .
    #        ?s1 <{VAL}variable_y> <{VAL}nil> .
    #        ?s1 <{VAL}variable_z> ?list_two .
    #        ?s2 <{OPERATION}> <{VAL}next_list_number> .
    #        ?s2 <{VAL}variable_x> ?list_two .
    #        ?s2 <{VAL}variable_y> ?list_three .
    #        ?s3 <{OPERATION}> <{VAL}cons> .
    #        ?s3 <{VAL}variable_x> ?car .
    #        ?s3 <{VAL}variable_y> ?cdr .
    #        ?s3 <{VAL}variable_z> ?list_three .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #
    #     # next(9, ?ans)
    #     my_question = f"""
    #        SELECT ?list_three ?car ?cdr WHERE {{
    #        ?s1 <{OPERATION}> <{VAL}cons> .
    #        ?s1 <{VAL}variable_x> <{VAL}nine> .
    #        ?s1 <{VAL}variable_y> <{VAL}nil> .
    #        ?s1 <{VAL}variable_z> ?list_nine .
    #        ?s2 <{OPERATION}> <{VAL}next_list_number> .
    #        ?s2 <{VAL}variable_x> ?list_nine .
    #        ?s2 <{VAL}variable_y> ?list_ten .
    #        ?s3 <{OPERATION}> <{VAL}cons> .
    #        ?s3 <{VAL}variable_x> ?car_ten .
    #        ?s3 <{VAL}variable_y> ?cdr_ten .
    #        ?s3 <{VAL}variable_z> ?list_ten .
    #        ?s4 <{OPERATION}> <{VAL}cons> .
    #        ?s4 <{VAL}variable_x> ?car .
    #        ?s4 <{VAL}variable_y> ?cdr .
    #        ?s4 <{VAL}variable_z> ?cdr_ten .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #
    #     # next(?ans, [2])
    #     my_question = f"""
    #        SELECT ?list_one ?car ?cdr WHERE {{
    #        ?s3 <{OPERATION}> <{VAL}cons> .
    #        ?s3 <{VAL}variable_x> <{VAL}two> .
    #        ?s3 <{VAL}variable_y> <{VAL}nil> .
    #        ?s3 <{VAL}variable_z> ?list_two .
    #        ?s2 <{OPERATION}> <{VAL}next_list_number> .
    #        ?s2 <{VAL}variable_x> ?list_one .
    #        ?s2 <{VAL}variable_y> ?list_two .
    #        ?s4 <{OPERATION}> <{VAL}cons> .
    #        ?s4 <{VAL}variable_x> ?car .
    #        ?s4 <{VAL}variable_y> ?cdr .
    #        ?s4 <{VAL}variable_z> ?list_one .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #
    #     # next(?ans, [3])
    #     my_question = f"""
    #        SELECT ?list_two ?car ?cdr WHERE {{
    #        ?s3 <{OPERATION}> <{VAL}cons> .
    #        ?s3 <{VAL}variable_x> <{VAL}three> .
    #        ?s3 <{VAL}variable_y> <{VAL}nil> .
    #        ?s3 <{VAL}variable_z> ?list_three .
    #        ?s2 <{OPERATION}> <{VAL}next_list_number> .
    #        ?s2 <{VAL}variable_x> ?list_two .
    #        ?s2 <{VAL}variable_y> ?list_three .
    #        ?s4 <{OPERATION}> <{VAL}cons> .
    #        ?s4 <{VAL}variable_x> ?car .
    #        ?s4 <{VAL}variable_y> ?cdr .
    #        ?s4 <{VAL}variable_z> ?list_two .
    #        }}"""
    #     my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    #     # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    #
    #     # next(?ans, [3])
    #     my_question = f"""
    #        SELECT ?list_two ?car ?cdr WHERE {{
    #        ?s1 <{OPERATION}> <{VAL}cons> .
    #        ?s1 <{VAL}variable_x> <{VAL}two> .
    #        ?s1 <{VAL}variable_y> <{VAL}nil> .
    #        ?s1 <{VAL}variable_z> ?list_dummy .
    #        ?s3 <{OPERATION}> <{VAL}cons> .
    #        ?s3 <{VAL}variable_x> <{VAL}three> .
    #        ?s3 <{VAL}variable_y> <{VAL}nil> .
    #        ?s3 <{VAL}variable_z> ?list_three .
    #        ?s2 <{OPERATION}> <{VAL}next_list_number> .
    #        ?s2 <{VAL}variable_x> ?list_two .
    #        ?s2 <{VAL}variable_y> ?list_three .
    #        ?s4 <{OPERATION}> <{VAL}cons> .
    #        ?s4 <{VAL}variable_x> ?car .
    #        ?s4 <{VAL}variable_y> ?cdr .
    #        ?s4 <{VAL}variable_z> ?list_two .
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
            ?s1 <{OPERATION}> <{VAL}next_list_number> . 
            ?s1 <{VAL}variable_x> <{VAL}list_one> . 
            ?s1 <{VAL}variable_y> ?ans . 
            ?s2 <{OPERATION}> <{VAL}cons> . 
            ?s2 <{VAL}variable_x> ?car . 
            ?s2 <{VAL}variable_y> ?cdr . 
            ?s2 <{VAL}variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # next([9, 9], ?ans) = [0, 0, 1] means 100
        my_question = f"""
            SELECT ?car_one_hundred ?car ?cdr WHERE {{
            ?s1 <{OPERATION}> <{VAL}cons> .
            ?s1 <{VAL}variable_x> <{VAL}nine> .
            ?s1 <{VAL}variable_y> <{VAL}nil> .
            ?s1 <{VAL}variable_z> ?list_nine .
            ?s1b <{OPERATION}> <{VAL}cons> .
            ?s1b <{VAL}variable_x> <{VAL}nine> .
            ?s1b <{VAL}variable_y> ?list_nine .
            ?s1b <{VAL}variable_z> ?list_ninety_nine .
            ?s2 <{OPERATION}> <{VAL}next_list_number> .
            ?s2 <{VAL}variable_x> ?list_ninety_nine .
            ?s2 <{VAL}variable_y> ?list_one_hundred .
            ?s3 <{OPERATION}> <{VAL}cons> .
            ?s3 <{VAL}variable_x> ?car_one_hundred .
            ?s3 <{VAL}variable_y> ?cdr_one_hundred .
            ?s3 <{VAL}variable_z> ?list_one_hundred .
            ?s4 <{OPERATION}> <{VAL}cons> .
            ?s4 <{VAL}variable_x> ?car .
            ?s4 <{VAL}variable_y> ?cdr .
            ?s4 <{VAL}variable_z> ?cdr_one_hundred .
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

    # list number add
    if True:
        # rdf_prolog = RdfProlog(rules_folder='../rules/rules_list_number_add')
        # add(1, 1, ?ans)
        my_question = f"""
           SELECT ?ans ?car ?cdr WHERE {{
           ?s1 <{OPERATION}> <{VAL}list_add> . 
           ?s1 <{VAL}variable_x> <{VAL}list_one> . 
           ?s1 <{VAL}variable_y> <{VAL}list_one> . 
           ?s1 <{VAL}variable_z> ?ans . 
           ?s2 <{OPERATION}> <{VAL}cons> . 
           ?s2 <{VAL}variable_x> ?car . 
           ?s2 <{VAL}variable_y> ?cdr . 
           ?s2 <{VAL}variable_z> ?ans . 
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # add(2, 1, ?ans)
        my_question = f"""
           SELECT ?ans ?car ?cdr WHERE {{
           ?s1 <{OPERATION}> <{VAL}list_add> . 
           ?s1 <{VAL}variable_x> <{VAL}list_two> . 
           ?s1 <{VAL}variable_y> <{VAL}list_one> . 
           ?s1 <{VAL}variable_z> ?ans . 
           ?s2 <{OPERATION}> <{VAL}cons> . 
           ?s2 <{VAL}variable_x> ?car . 
           ?s2 <{VAL}variable_y> ?cdr . 
           ?s2 <{VAL}variable_z> ?ans . 
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # add(1, 2, ?ans)
        my_question = f"""
           SELECT ?ans ?car ?cdr WHERE {{
           ?s1 <{OPERATION}> <{VAL}list_add> . 
           ?s1 <{VAL}variable_x> <{VAL}list_one> . 
           ?s1 <{VAL}variable_y> <{VAL}list_two> . 
           ?s1 <{VAL}variable_z> ?ans . 
           ?s2 <{OPERATION}> <{VAL}cons> . 
           ?s2 <{VAL}variable_x> ?car . 
           ?s2 <{VAL}variable_y> ?cdr . 
           ?s2 <{VAL}variable_z> ?ans . 
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # add(9, 1, ?ans)
        my_question = f"""
           SELECT ?ans ?car ?cdr WHERE {{
           ?s1 <{OPERATION}> <{VAL}list_add> . 
           ?s1 <{VAL}variable_x> <{VAL}list_nine> . 
           ?s1 <{VAL}variable_y> <{VAL}list_one> . 
           ?s1 <{VAL}variable_z> ?ans . 
           ?s2 <{OPERATION}> <{VAL}cons> . 
           ?s2 <{VAL}variable_x> ?car . 
           ?s2 <{VAL}variable_y> ?cdr . 
           ?s2 <{VAL}variable_z> ?ans . 
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # add(1, ?ans, 2)
        my_question = f"""
           SELECT ?ans ?car ?cdr WHERE {{
           ?s1 <{OPERATION}> <{VAL}list_add> . 
           ?s1 <{VAL}variable_x> <{VAL}list_one> . 
           ?s1 <{VAL}variable_y> ?ans . 
           ?s1 <{VAL}variable_z> <{VAL}list_two> . 
           ?s2 <{OPERATION}> <{VAL}cons> . 
           ?s2 <{VAL}variable_x> ?car . 
           ?s2 <{VAL}variable_y> ?cdr . 
           ?s2 <{VAL}variable_z> ?ans . 
           }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # add(1, ?ans, 3)
        my_question = f"""
           SELECT ?ans ?car ?cdr WHERE {{
           ?s <{OPERATION}> <{VAL}list_add> . 
           ?s <{VAL}variable_x> <{VAL}list_one> . 
           ?s <{VAL}variable_y> ?ans . 
           ?s <{VAL}variable_z> <{VAL}list_three> . 
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
            ?s1 <{OPERATION}> <{VAL}cons> .
            ?s1 <{VAL}variable_x> <{VAL}nine> .
            ?s1 <{VAL}variable_y> <{VAL}nil> .
            ?s1 <{VAL}variable_z> ?list_nine .
            ?s1b <{OPERATION}> <{VAL}cons> .
            ?s1b <{VAL}variable_x> <{VAL}nine> .
            ?s1b <{VAL}variable_y> ?list_nine .
            ?s1b <{VAL}variable_z> ?list_ninety_nine .
            ?s2 <{OPERATION}> <{VAL}next_list_number> .
            ?s2 <{VAL}variable_x> ?list_ninety_nine .
            ?s2 <{VAL}variable_y> ?list_one_hundred .
            ?s3 <{OPERATION}> <{VAL}cons> .
            ?s3 <{VAL}variable_x> ?car_one_hundred .
            ?s3 <{VAL}variable_y> ?cdr_one_hundred .
            ?s3 <{VAL}variable_z> ?list_one_hundred .
            ?s4 <{OPERATION}> <{VAL}cons> .
            ?s4 <{VAL}variable_x> ?car .
            ?s4 <{VAL}variable_y> ?cdr .
            ?s4 <{VAL}variable_z> ?cdr_one_hundred .
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # next([1], ?ans) = [2]
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s1 <{OPERATION}> <{VAL}next_list_number> .
            ?s1 <{VAL}variable_x> <{VAL}list_one> .
            ?s1 <{VAL}variable_y> ?ans .
            ?s2 <{OPERATION}> <{VAL}cons> .
            ?s2 <{VAL}variable_x> ?car .
            ?s2 <{VAL}variable_y> ?cdr .
            ?s2 <{VAL}variable_z> ?ans .
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # add(2, ?ans, 3)
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s <{OPERATION}> <{VAL}list_add> . 
            ?s <{VAL}variable_x> <{VAL}list_two> . 
            ?s <{VAL}variable_y> ?ans . 
            ?s <{VAL}variable_z> <{VAL}list_three> . 
            ?s2 <{OPERATION}> <{VAL}cons> . 
            ?s2 <{VAL}variable_x> ?car . 
            ?s2 <{VAL}variable_y> ?cdr . 
            ?s2 <{VAL}variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # subtract(4, 2, ?ans)
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s <{OPERATION}> <{VAL}list_subtract> . 
            ?s <{VAL}variable_x> <{VAL}list_four> . 
            ?s <{VAL}variable_y> <{VAL}list_two> . 
            ?s <{VAL}variable_z> ?ans . 
            ?s2 <{OPERATION}> <{VAL}cons> . 
            ?s2 <{VAL}variable_x> ?car . 
            ?s2 <{VAL}variable_y> ?cdr . 
            ?s2 <{VAL}variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)

        # multiply(2, 1, ?ans) -> ?ans = 2
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s <{OPERATION}> <{VAL}list_multiply> . 
            ?s <{VAL}variable_x> <{VAL}list_three> . 
            ?s <{VAL}variable_y> <{VAL}list_one> . 
            ?s <{VAL}variable_z> ?ans . 
            ?s2 <{OPERATION}> <{VAL}cons> . 
            ?s2 <{VAL}variable_x> ?car . 
            ?s2 <{VAL}variable_y> ?cdr . 
            ?s2 <{VAL}variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)

        # multiply(3, 1, ?ans) -> ?ans = 3
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s <{OPERATION}> <{VAL}list_multiply> . 
            ?s <{VAL}variable_x> <{VAL}list_three> . 
            ?s <{VAL}variable_y> <{VAL}list_one> . 
            ?s <{VAL}variable_z> ?ans . 
            ?s2 <{OPERATION}> <{VAL}cons> . 
            ?s2 <{VAL}variable_x> ?car . 
            ?s2 <{VAL}variable_y> ?cdr . 
            ?s2 <{VAL}variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)

        # multiply(3, 2, ?ans) -> ?ans = 6
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s <{OPERATION}> <{VAL}list_multiply> . 
            ?s <{VAL}variable_x> <{VAL}list_three> . 
            ?s <{VAL}variable_y> <{VAL}list_two> . 
            ?s <{VAL}variable_z> ?ans . 
            ?s2 <{OPERATION}> <{VAL}cons> . 
            ?s2 <{VAL}variable_x> ?car . 
            ?s2 <{VAL}variable_y> ?cdr . 
            ?s2 <{VAL}variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)

        # multiply(3, ?ans, 3) -> ?ans = 1
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s <{OPERATION}> <{VAL}list_multiply> . 
            ?s <{VAL}variable_x> <{VAL}list_three> . 
            ?s <{VAL}variable_y> ?ans . 
            ?s <{VAL}variable_z> <{VAL}list_three> . 
            ?s2 <{OPERATION}> <{VAL}cons> . 
            ?s2 <{VAL}variable_x> ?car . 
            ?s2 <{VAL}variable_y> ?cdr . 
            ?s2 <{VAL}variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)

        # multiply(3, ?ans, 9) -> ?ans = 3
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s <{OPERATION}> <{VAL}list_multiply> . 
            ?s <{VAL}variable_x> <{VAL}list_three> . 
            ?s <{VAL}variable_y> ?ans . 
            ?s <{VAL}variable_z> <{VAL}list_nine> . 
            ?s2 <{OPERATION}> <{VAL}cons> . 
            ?s2 <{VAL}variable_x> ?car . 
            ?s2 <{VAL}variable_y> ?cdr . 
            ?s2 <{VAL}variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=150)

        # divide(6, 2, ?ans) -> ?ans = [3]
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s1 <{OPERATION}> <{VAL}cons> . 
            ?s1 <{VAL}variable_x> <{VAL}six> . 
            ?s1 <{VAL}variable_y> <{VAL}nil> . 
            ?s1 <{VAL}variable_z> ?list_15 . 
            ?s2 <{OPERATION}> <{VAL}list_divide> . 
            ?s2 <{VAL}variable_x> ?list_15 . 
            ?s2 <{VAL}variable_y> <{VAL}list_two> . 
            ?s2 <{VAL}variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=50)

        # divide(5, 2, ?ans)
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s <{OPERATION}> <{VAL}list_divide> .
            ?s <{VAL}variable_x> <{VAL}list_five> .
            ?s <{VAL}variable_y> <{VAL}list_two> .
            ?s <{VAL}variable_z> ?ans .
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=200)

        # fibinacci(1, ?ans) -> ?ans = 1
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s1 <{OPERATION}> <{VAL}fibonacci_number> . 
            ?s1 <{VAL}variable_x> <{VAL}list_one> . 
            ?s1 <{VAL}variable_y> ?ans . 
            ?s2 <{OPERATION}> <{VAL}cons> . 
            ?s2 <{VAL}variable_x> ?car . 
            ?s2 <{VAL}variable_y> ?cdr . 
            ?s2 <{VAL}variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=100)

        # fibinacci(3, ?ans) -> ?ans = 2
        my_question = f"""
            SELECT ?ans ?car ?cdr WHERE {{
            ?s1 <{OPERATION}> <{VAL}fibonacci_number> . 
            ?s1 <{VAL}variable_x> <{VAL}list_three> . 
            ?s1 <{VAL}variable_y> ?ans . 
            ?s2 <{OPERATION}> <{VAL}cons> . 
            ?s2 <{VAL}variable_x> ?car . 
            ?s2 <{VAL}variable_y> ?cdr . 
            ?s2 <{VAL}variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=300)

        # function_cons()
        my_question = f"""
            SELECT ?ans WHERE {{
            ?s1 <{OPERATION}> <{VAL}function_cons> . 
            ?s1 <{VAL}variable_x> <{VAL}three> . 
            ?s1 <{VAL}variable_y> <{VAL}list_two> . 
            ?s1 <{VAL}variable_z> ?ans . 
            ?s2 <{OPERATION}> <{VAL}cons> . 
            ?s2 <{VAL}variable_x> ?car . 
            ?s2 <{VAL}variable_y> ?cdr . 
            ?s2 <{VAL}variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=300)
        pass

        # function_add()
        my_question = f"""
            SELECT ?ans WHERE {{
            ?s1 <{OPERATION}> <{VAL}function_add> . 
            ?s1 <{VAL}variable_x> <{VAL}list_three> . 
            ?s1 <{VAL}variable_y> <{VAL}list_two> . 
            ?s1 <{VAL}variable_z> ?ans . 
            ?s2 <{OPERATION}> <{VAL}cons> . 
            ?s2 <{VAL}variable_x> ?car . 
            ?s2 <{VAL}variable_y> ?cdr . 
            ?s2 <{VAL}variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=300)
        pass

        # function_add()
        my_question = f"""
            SELECT ?ans WHERE {{
            ?s3 <{OPERATION}> <{VAL}cons> . 
            ?s3 <{VAL}variable_x> <{VAL}seven> . 
            ?s3 <{VAL}variable_y> <{VAL}list_one> . 
            ?s3 <{VAL}variable_z> ?list_seventeen . 
            ?s4 <{OPERATION}> <{VAL}cons> . 
            ?s4 <{VAL}variable_x> <{VAL}nine> . 
            ?s4 <{VAL}variable_y> <{VAL}list_one> . 
            ?s4 <{VAL}variable_z> ?list_nineteen . 
            ?s1 <{OPERATION}> <{VAL}function_add> . 
            ?s1 <{VAL}variable_x> ?list_seventeen . 
            ?s1 <{VAL}variable_y> ?list_nineteen . 
            ?s1 <{VAL}variable_z> ?ans . 
            ?s2 <{OPERATION}> <{VAL}cons> . 
            ?s2 <{VAL}variable_x> ?car . 
            ?s2 <{VAL}variable_y> ?cdr . 
            ?s2 <{VAL}variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=300)
        pass

    # rational number
    if True:
        rdf_prolog = RdfProlog(rules_folder='../rules/rules_rational_number')

        # rational number 2
        my_question = f"""
                    SELECT ?m ?n WHERE {{
                    ?s1 <{OPERATION}> <{VAL}rational_number> . 
                    ?s1 <{VAL}variable_x> ?m . 
                    ?s1 <{VAL}variable_y> ?n . 
                    ?s1 <{VAL}variable_z> <{VAL}rational_2> . 
                    }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=5, depth_limit=300)

        # rational number 3/5
        my_question = f"""
                            SELECT ?m ?n WHERE {{
                            ?s1 <{OPERATION}> <{VAL}rational_number> . 
                            ?s1 <{VAL}variable_x> <{VAL}3> . 
                            ?s1 <{VAL}variable_y> <{VAL}5> . 
                            ?s1 <{VAL}variable_z> ?z .
                            ?s2 <{OPERATION}> <{VAL}rational_number> . 
                            ?s2 <{VAL}variable_x> ?m . 
                            ?s2 <{VAL}variable_y> ?n . 
                            ?s2 <{VAL}variable_z> ?z . 
                            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=1, depth_limit=20)

        # rational number 13/19
        my_question = f"""
                            SELECT ?m ?n WHERE {{
                            ?s1 <{OPERATION}> <{VAL}rational_number> . 
                            ?s1 <{VAL}variable_x> <{VAL}13> . 
                            ?s1 <{VAL}variable_y> <{VAL}19> . 
                            ?s1 <{VAL}variable_z> ?z .
                            ?s2 <{OPERATION}> <{VAL}rational_number> . 
                            ?s2 <{VAL}variable_x> ?m . 
                            ?s2 <{VAL}variable_y> ?n . 
                            ?s2 <{VAL}variable_z> ?z . 
                            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=1, depth_limit=300)

        # rational multiply 3/5 * 7/11
        my_question = f"""
                            SELECT ?m ?n WHERE {{
                            ?s1 <{OPERATION}> <{VAL}rational_number> . 
                            ?s1 <{VAL}variable_x> <{VAL}3> . 
                            ?s1 <{VAL}variable_y> <{VAL}5> . 
                            ?s1 <{VAL}variable_z> ?x . 
                            ?s2 <{OPERATION}> <{VAL}rational_number> . 
                            ?s2 <{VAL}variable_x> <{VAL}7> . 
                            ?s2 <{VAL}variable_y> <{VAL}11> . 
                            ?s2 <{VAL}variable_z> ?y . 
                            ?s3 <{OPERATION}> <{VAL}rational_multiply> . 
                            ?s3 <{VAL}variable_x> ?x . 
                            ?s3 <{VAL}variable_y> ?y . 
                            ?s3 <{VAL}variable_z> ?z . 
                            ?s4 <{OPERATION}> <{VAL}rational_number> . 
                            ?s4 <{VAL}variable_x> ?m . 
                            ?s4 <{VAL}variable_y> ?n . 
                            ?s4 <{VAL}variable_z> ?z . 
                            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=1, depth_limit=20)

        # contradiction of even(?x), odd(?x)
        my_question = f"""
                    SELECT ?x WHERE {{
                    ?s1 <{OPERATION}> <{VAL}even> . 
                    ?s1 <{VAL}variable_x> ?x . 
                    ?s2 <{OPERATION}> <{VAL}odd> . 
                    ?s2 <{VAL}variable_x> ?x . 
                    }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=1, depth_limit=30)

        # square root of 2 is not a rational number
        my_question = f"""
                    SELECT ?m ?n WHERE {{
                    ?s1 <{OPERATION}> <{VAL}rational_multiply> . 
                    ?s1 <{VAL}variable_x> ?root2 . 
                    ?s1 <{VAL}variable_y> ?root2 . 
                    ?s1 <{VAL}variable_z> <{VAL}rational_2> . 
                    ?s2 <{OPERATION}> <{VAL}rational_number> . 
                    ?s2 <{VAL}variable_x> ?m . 
                    ?s2 <{VAL}variable_y> ?n . 
                    ?s2 <{VAL}variable_z> ?root2 . 
                    }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=1, depth_limit=20)
        pass


if __name__ == '__main__':
    main()  # execute the main function
