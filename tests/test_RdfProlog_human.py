# import numpy as np
from src.RdfProlog import RdfProlog, Resolution, ClassSparqlQuery
from src.PR import PR
# from rdflib import URIRef


def test_graph():
    rdf_prolog = RdfProlog()
    resolution = Resolution(rdf_prolog.g_rules, rdf_prolog.rules)
    # assert len(rdf_prolog.g_rules) == 168
    # assert len(rdf_prolog.rules.list_of_rules) == 8
    query = f'SELECT ?s ?o WHERE {{ ?s <{PR.operation}> <{PR.human}>. ?s <{PR.variable_x}> ?o .}}'
    my_sparql_query = ClassSparqlQuery().set(query).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?o'] == f'<{str(PR.socrates)}>'


def test_answer_question1():
    rdf_prolog = RdfProlog()

    # mortal(?ans).
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.mortal}> . ' \
        f'?s <{PR.variable_x}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'<{str(PR.socrates)}>'


def test_answer_question2():
    rdf_prolog = RdfProlog()

    # mortal(socrates).
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.mortal}> . ' \
        f'?s <{PR.variable_x}> <{PR.socrates}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 1


def test_answer_question3():
    rdf_prolog = RdfProlog()

    # mortal(platon).
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.mortal}> . ' \
        f'?s <{PR.variable_x}> <{PR.platon}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 0
