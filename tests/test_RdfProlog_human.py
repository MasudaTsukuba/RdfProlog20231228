# import numpy as np
from src.RdfProlog import RdfProlog, Resolution, ClassSparqlQuery
# from src_not_used.PR import PR
# from rdflib import URIRef


def test_graph():
    rdf_prolog = RdfProlog()
    resolution = Resolution(rdf_prolog.g_rules, rdf_prolog.rules, False)
    # assert len(rdf_prolog.g_rules) == 168
    # assert len(rdf_prolog.rules.list_of_rules) == 8
    query = f'SELECT ?s ?o WHERE {{ ?s <http://example.org/operation> <http://example.org/human>. ?s <http://example.org/variable_x> ?o .}}'
    my_sparql_query = ClassSparqlQuery().set(query).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?o'] == '<http://example.org/socrates>'


def test_answer_question1():
    rdf_prolog = RdfProlog()

    # mortal(?ans).
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/mortal> . ' \
        f'?s <http://example.org/variable_x> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == '<http://example.org/socrates>'


def test_answer_question2():
    rdf_prolog = RdfProlog()

    # mortal(socrates).
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/mortal> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/socrates> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 1


def test_answer_question3():
    rdf_prolog = RdfProlog()

    # mortal(platon).
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/mortal> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/platon> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 0
