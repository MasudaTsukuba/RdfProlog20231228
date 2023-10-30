from RdfProlog import RdfProlog, ClassSparqlQuery
from PR import PR
from rdflib import URIRef
import numpy as np


def test_answer_question1():
    rdf_prolog = RdfProlog()

    # add(3, 1, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.add_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.three}> . ' \
        f'?s <{PR.variable_y}> <{PR.one}> . ' \
        f'?s <{PR.variable_z}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'<{PR.four}>'


def test_answer_question2():
    rdf_prolog = RdfProlog()

    # add(2, 2, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{ ?s <{PR.operation}> <{PR.add_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.two}> . ' \
        f'?s <{PR.variable_y}> <{PR.two}> . ' \
        f'?s <{PR.variable_z}> ?ans . ' \
        f'}} '
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'<{PR.four}>'


def test_answer_question3():
    rdf_prolog = RdfProlog()

    # # add(3, 2, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.add_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.three}> . ' \
        f'?s <{PR.variable_y}> <{PR.two}> . ' \
        f'?s <{PR.variable_z}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'<{PR.five}>'


def test_answer_question3b():
    rdf_prolog = RdfProlog()

    # add(3, 2, ?z), next(?z, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s1 <{PR.operation}> <{PR.add_number}> . ' \
        f'?s1 <{PR.variable_x}> <{PR.three}> . ' \
        f'?s1 <{PR.variable_y}> <{PR.two}> . ' \
        f'?s1 <{PR.variable_z}> ?z . ' \
        f'?s2 <{PR.operation}> <{PR.next_number}> . ' \
        f'?s2 <{PR.variable_x}> ?z . ' \
        f'?s2 <{PR.variable_y}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'<{PR.six}>'


def test_answer_question4():
    rdf_prolog = RdfProlog()

    # add(3, ?ans, 5)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.add_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.three}> . ' \
        f'?s <{PR.variable_y}> ?ans . ' \
        f'?s <{PR.variable_z}> <{PR.five}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'<{PR.two}>'


def test_answer_complex_question1():
    rdf_prolog = RdfProlog()

    # add(3, 2, ?z), next(?z, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s1 <{PR.operation}> <{PR.add_number}> . ' \
        f'?s1 <{PR.variable_x}> <{PR.three}> . ' \
        f'?s1 <{PR.variable_y}> <{PR.two}> . ' \
        f'?s1 <{PR.variable_z}> ?z . ' \
        f'?s2 <{PR.operation}> <{PR.next_number}> . ' \
        f'?s2 <{PR.variable_x}> ?z . ' \
        f'?s2 <{PR.variable_y}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)  # ###################
    assert resolve_bindings[0]['?ans'] == f'<{PR.six}>'


def test_answer_complex_question2():
    rdf_prolog = RdfProlog()

    # add(3, 2, ?z), add(?z, 2, ?ans)
    my_question = \
        my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s1 <{PR.operation}> <{PR.add_number}> . ' \
        f'?s1 <{PR.variable_x}> <{PR.three}> . ' \
        f'?s1 <{PR.variable_y}> <{PR.two}> . ' \
        f'?s1 <{PR.variable_z}> ?z . ' \
        f'?s2 <{PR.operation}> <{PR.add_number}> . ' \
        f'?s2 <{PR.variable_x}> ?z . ' \
        f'?s2 <{PR.variable_y}> <{PR.two}> . ' \
        f'?s2 <{PR.variable_z}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)  # ###################
    assert resolve_bindings[0]['?ans'] == f'<{PR.seven}>'
