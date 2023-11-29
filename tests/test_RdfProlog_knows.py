from src.RdfPrologMain import RdfProlog
from src.RdfResolution import ClassSparqlQuery
# from src_not_used.PR import PR
import numpy as np


rdf_prolog = RdfProlog()


def test_answer_question1():
    # rdf_prolog = RdfProlog()

    # knows_direct(andy, bob)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://example.org/operation> <http://example.org/knows_direct> . 
        ?s <http://example.org/variable_x> <http://example.org/andy> . 
        ?s <http://example.org/variable_y> <http://example.org/bob> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1  # > 0


def test_answer_question1b():
    # rdf_prolog = RdfProlog()

    # knows_direct(andy, chris)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://example.org/operation> <http://example.org/knows_direct> . 
        ?s <http://example.org/variable_x> <http://example.org/andy> . 
        ?s <http://example.org/variable_y> <http://example.org/chris> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 0  # > 0


def test_answer_question1c():
    # rdf_prolog = RdfProlog()

    # knows_indirect(andy, chris)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://example.org/operation> <http://example.org/knows_indirect> . 
        ?s <http://example.org/variable_x> <http://example.org/andy> . 
        ?s <http://example.org/variable_y> <http://example.org/chris> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1  # > 0


def test_answer_question1e():
    # rdf_prolog = RdfProlog()

    # knows(andy, chris)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://example.org/operation> <http://example.org/knows> . 
        ?s <http://example.org/variable_x> <http://example.org/andy> . 
        ?s <http://example.org/variable_y> <http://example.org/chris> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1  # > 0


def test_answer_question2():
    # rdf_prolog = RdfProlog()

    # knows_direct(andy, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://example.org/operation> <http://example.org/knows_direct> . 
        ?s <http://example.org/variable_x> <http://example.org/andy> . 
        ?s <http://example.org/variable_y> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=True)
    assert np.logical_or(resolve_bindings[0]['?ans'] == 'http://example.org/bob',
                         resolve_bindings[1]['?ans'] == 'http://example.org/bob')
    assert np.logical_or(resolve_bindings[0]['?ans'] == 'http://example.org/david',
                         resolve_bindings[1]['?ans'] == 'http://example.org/david')


def test_answer_question3():
    # rdf_prolog = RdfProlog()

    # knows(andy, ?ans)
    my_question = f"""
        SELECT ?s WHERE {{ 
        ?s <http://example.org/operation> <http://example.org/knows> . 
        ?s <http://example.org/variable_x> <http://example.org/andy> . 
        ?s <http://example.org/variable_y> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, True)
    assert len(resolve_bindings) == 4  # > 0


def test_answer_question4():
    # rdf_prolog = RdfProlog()

    # knows_indirect(andy, edgar)
    my_question = f"""
        SELECT ?s WHERE {{ 
        ?s <http://example.org/operation> <http://example.org/knows_indirect> . 
        ?s <http://example.org/variable_x> <http://example.org/andy> . 
        ?s <http://example.org/variable_y> <http://example.org/edgar> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1
