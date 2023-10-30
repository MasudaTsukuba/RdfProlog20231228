from RdfProlog import RdfProlog, ClassSparqlQuery
from PR import PR
from rdflib import URIRef


def test_answer_question1():
    rdf_prolog = RdfProlog()

    # grandfather(taro, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.grandfather}> . ' \
        f'?s <{PR.variable_x}> <{PR.taro}> . ' \
        f'?s <{PR.variable_y}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'<{str(PR.ichiro)}>'


def test_answer_question2():
    rdf_prolog = RdfProlog()

    # grandfather(taro, ichiro)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.grandfather}> . ' \
        f'?s <{PR.variable_x}> <{PR.taro}> . ' \
        f'?s <{PR.variable_y}> <{PR.ichiro}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 1


def test_answer_question3():
    rdf_prolog = RdfProlog()

    # grandfather(taro, jiro)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.grandfather}> . ' \
        f'?s <{PR.variable_x}> <{PR.taro}> . ' \
        f'?s <{PR.variable_y}> <{PR.jiro}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 0
