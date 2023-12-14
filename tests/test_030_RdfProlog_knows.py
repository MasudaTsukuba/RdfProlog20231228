"""
test_030_RdfProlog_knows.py
test the relationships of knowing others
knows_direct is based on facts
if A knows B directly and B knows C directly, then A knows C indirectly
A knows B, if A knows B directly or indirectly
T. Masuda, 2023/11/28
"""

from src.RdfPrologMain import RdfProlog
from src.RdfResolution import ClassSparqlQuery
import numpy as np  # for logical OR


rdf_prolog = RdfProlog()


def test_answer_question1():
   # knows_direct(andy, bob)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://value.org/operation> <http://value.org/knows_direct> . 
        ?s <http://value.org/variable_x> <http://value.org/andy> . 
        ?s <http://value.org/variable_y> <http://value.org/bob> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1  # > 0


def test_answer_question1b():
    # knows_direct(andy, chris)  andy -> bob -> chris
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://value.org/operation> <http://value.org/knows_direct> . 
        ?s <http://value.org/variable_x> <http://value.org/andy> . 
        ?s <http://value.org/variable_y> <http://value.org/chris> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 0  # > 0


def test_answer_question1c():
    # knows_indirect(andy, chris)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://value.org/operation> <http://value.org/knows_indirect> . 
        ?s <http://value.org/variable_x> <http://value.org/andy> . 
        ?s <http://value.org/variable_y> <http://value.org/chris> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1  # > 0


def test_answer_question1e():
    # knows(andy, chris)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://value.org/operation> <http://value.org/knows> . 
        ?s <http://value.org/variable_x> <http://value.org/andy> . 
        ?s <http://value.org/variable_y> <http://value.org/chris> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1  # > 0


def test_answer_question2():
    # knows_direct(andy, ?ans)  find people who Andy knows directly -> bob, david
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://value.org/operation> <http://value.org/knows_direct> . 
        ?s <http://value.org/variable_x> <http://value.org/andy> . 
        ?s <http://value.org/variable_y> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=True)
    assert np.logical_or(resolve_bindings[0]['?ans'] == 'http://value.org/bob',
                         resolve_bindings[1]['?ans'] == 'http://value.org/bob')
    assert np.logical_or(resolve_bindings[0]['?ans'] == 'http://value.org/david',
                         resolve_bindings[1]['?ans'] == 'http://value.org/david')


def test_answer_question3():
    # knows(andy, ?ans) -> bob, chris, david edgar
    my_question = f"""
        SELECT ?s WHERE {{ 
        ?s <http://value.org/operation> <http://value.org/knows> . 
        ?s <http://value.org/variable_x> <http://value.org/andy> . 
        ?s <http://value.org/variable_y> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, True)
    assert len(resolve_bindings) == 4  # > 0


def test_answer_question4():
    # knows_indirect(andy, edgar) -> yes returns empty bindings
    my_question = f"""
        SELECT ?s WHERE {{ 
        ?s <http://value.org/operation> <http://value.org/knows_indirect> . 
        ?s <http://value.org/variable_x> <http://value.org/andy> . 
        ?s <http://value.org/variable_y> <http://value.org/edgar> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
