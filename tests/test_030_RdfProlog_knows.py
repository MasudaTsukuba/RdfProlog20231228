"""
test_030_RdfProlog_knows.py
test the relationships of knowing others
knows_direct is based on facts
if A knows B directly and B knows C directly, then A knows C indirectly
A knows B, if A knows B directly or indirectly
T. Masuda, 2023/11/28
"""

from src.RdfResolution import *
import numpy as np  # for logical OR


rdf_prolog = RdfProlog()


def test_answer_question1():
   # knows_direct(andy, bob)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <{OPERATION}> <{VAL}knows_direct> . 
        ?s <{VAL}variable_x> <{VAL}andy> . 
        ?s <{VAL}variable_y> <{VAL}bob> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1  # > 0


def test_answer_question1b():
    # knows_direct(andy, chris)  andy -> bob -> chris
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <{OPERATION}> <{VAL}knows_direct> . 
        ?s <{VAL}variable_x> <{VAL}andy> . 
        ?s <{VAL}variable_y> <{VAL}chris> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 0  # > 0


def test_answer_question1c():
    # knows_indirect(andy, chris)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <{OPERATION}> <{VAL}knows_indirect> . 
        ?s <{VAL}variable_x> <{VAL}andy> . 
        ?s <{VAL}variable_y> <{VAL}chris> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1  # > 0


def test_answer_question1e():
    # knows(andy, chris)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <{OPERATION}> <{VAL}knows> . 
        ?s <{VAL}variable_x> <{VAL}andy> . 
        ?s <{VAL}variable_y> <{VAL}chris> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1  # > 0


def test_answer_question2():
    # knows_direct(andy, ?ans)  find people who Andy knows directly -> bob, david
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <{OPERATION}> <{VAL}knows_direct> . 
        ?s <{VAL}variable_x> <{VAL}andy> . 
        ?s <{VAL}variable_y> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=2)
    assert np.logical_or(resolve_bindings[0]['?ans'] == f'{VAL}bob',
                         resolve_bindings[1]['?ans'] == f'{VAL}bob')
    assert np.logical_or(resolve_bindings[0]['?ans'] == f'{VAL}david',
                         resolve_bindings[1]['?ans'] == f'{VAL}david')


def test_answer_question3():
    # knows(andy, ?ans) -> bob, chris, david edgar
    my_question = f"""
        SELECT ?s WHERE {{ 
        ?s <{OPERATION}> <{VAL}knows> . 
        ?s <{VAL}variable_x> <{VAL}andy> . 
        ?s <{VAL}variable_y> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=4)
    assert len(resolve_bindings) == 4  # > 0


def test_answer_question4():
    # knows_indirect(andy, edgar) -> yes returns empty bindings
    my_question = f"""
        SELECT ?s WHERE {{ 
        ?s <{OPERATION}> <{VAL}knows_indirect> . 
        ?s <{VAL}variable_x> <{VAL}andy> . 
        ?s <{VAL}variable_y> <{VAL}edgar> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
