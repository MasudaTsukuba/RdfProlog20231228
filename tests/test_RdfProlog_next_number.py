from src.RdfProlog import RdfProlog, ClassSparqlQuery
from src.PR import PR


def test_answer_question1():
    rdf_prolog = RdfProlog()

    # next(1, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.next_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.one}> . ' \
        f'?s <{PR.variable_y}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'<{str(PR.two)}>'


def test_answer_question2():
    rdf_prolog = RdfProlog()

    # next(?ans, 3)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.next_number}> . ' \
        f'?s <{PR.variable_x}> ?ans . ' \
        f'?s <{PR.variable_y}> <{PR.three}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'<{str(PR.two)}>'


def test_answer_question3():
    rdf_prolog = RdfProlog()

    # next(1, 2)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <{PR.operation}> <{PR.next_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.one}> . ' \
        f'?s <{PR.variable_y}> <{PR.two}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 1


def test_answer_question4():
    rdf_prolog = RdfProlog()

    # next(1, 3)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <{PR.operation}> <{PR.next_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.one}> . ' \
        f'?s <{PR.variable_y}> <{PR.three}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 0


def test_answer_question5():
    rdf_prolog = RdfProlog()

    # next(1, ?z),next(?z, ?x)
    my_question = \
        f'SELECT ?x WHERE {{' \
        f'?s1 <{PR.operation}> <{PR.next_number}> . ' \
        f'?s1 <{PR.variable_x}> <{PR.one}> . ' \
        f'?s1 <{PR.variable_y}> ?z . ' \
        f'?s2 <{PR.operation}> <{PR.next_number}> . ' \
        f'?s2 <{PR.variable_x}> ?z . ' \
        f'?s2 <{PR.variable_y}> ?x . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?x'] == f'<{str(PR.three)}>'
