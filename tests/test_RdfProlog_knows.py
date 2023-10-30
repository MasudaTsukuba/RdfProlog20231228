from src.RdfProlog import RdfProlog, ClassSparqlQuery
from src.PR import PR
import numpy as np


def test_answer_question1():
    rdf_prolog = RdfProlog()

    # knows_direct(andy, bob)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.knows_direct}> . ' \
        f'?s <{PR.variable_x}> <{PR.andy}> . ' \
        f'?s <{PR.variable_y}> <{PR.bob}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 1  # > 0


def test_answer_question1b():
    rdf_prolog = RdfProlog()

    # knows_direct(andy, chris)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.knows_direct}> . ' \
        f'?s <{PR.variable_x}> <{PR.andy}> . ' \
        f'?s <{PR.variable_y}> <{PR.chris}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 0  # > 0


def test_answer_question1c():
    rdf_prolog = RdfProlog()

    # knows_indirect(andy, chris)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.knows_indirect}> . ' \
        f'?s <{PR.variable_x}> <{PR.andy}> . ' \
        f'?s <{PR.variable_y}> <{PR.chris}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 1  # > 0


def test_answer_question1e():
    rdf_prolog = RdfProlog()

    # knows(andy, chris)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.knows}> . ' \
        f'?s <{PR.variable_x}> <{PR.andy}> . ' \
        f'?s <{PR.variable_y}> <{PR.chris}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 1  # > 0


def test_answer_question2():
    rdf_prolog = RdfProlog()

    # knows_direct(andy, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.knows_direct}> . ' \
        f'?s <{PR.variable_x}> <{PR.andy}> . ' \
        f'?s <{PR.variable_y}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert np.logical_or(resolve_bindings[0]['?ans'] == f'<{str(PR.bob)}>',
                         resolve_bindings[1]['?ans'] == f'<{str(PR.bob)}>')
    assert np.logical_or(resolve_bindings[0]['?ans'] == f'<{str(PR.david)}>',
                         resolve_bindings[1]['?ans'] == f'<{str(PR.david)}>')


def test_answer_question3():
    rdf_prolog = RdfProlog()

    # knows(andy, ?ans)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <{PR.operation}> <{PR.knows}> . ' \
        f'?s <{PR.variable_x}> <{PR.andy}> . ' \
        f'?s <{PR.variable_y}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) > 0


def test_answer_question4():
    rdf_prolog = RdfProlog()

    # knows_indirect(andy, edgar)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <{PR.operation}> <{PR.knows_indirect}> . ' \
        f'?s <{PR.variable_x}> <{PR.andy}> . ' \
        f'?s <{PR.variable_y}> <{PR.edgar}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 1
