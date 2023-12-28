"""
test_020_RdfProlog_grandfather.py
test for family relationships
T. Masuda, 2023/11/28
"""

from src.RdfResolution import *

rdf_prolog = RdfProlog()


def test_answer_question1():
    # grandfather(taro, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <{OPERATION}> <{VAL}grandfather> . 
        ?s <{VAL}variable_x> <{VAL}taro> . 
        ?s <{VAL}variable_y> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}ichiro'


def test_answer_question2():
    # grandfather(taro, ichiro)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <{OPERATION}> <{VAL}grandfather> . 
        ?s <{VAL}variable_x> <{VAL}taro> . 
        ?s <{VAL}variable_y> <{VAL}ichiro> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1


def test_answer_question3():
    # grandfather(taro, jiro)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <{OPERATION}> <{VAL}grandfather> . 
        ?s <{VAL}variable_x> <{VAL}taro> . 
        ?s <{VAL}variable_y> <{VAL}jiro> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 0
