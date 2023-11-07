from src.RdfProlog import RdfProlog, ClassSparqlQuery
# from src_not_used.PR import PR


def test_answer_question1_next_1_ans():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # next(1, ?ans) = 2
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/one> . ' \
        f'?s <http://example.org/variable_y> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == '<http://example.org/two>'


def test_answer_question2_next_ans_3():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # next(?ans, 3) = 2
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s <http://example.org/variable_x> ?ans . ' \
        f'?s <http://example.org/variable_y> <http://example.org/three> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == '<http://example.org/two>'


def test_answer_question3_next_1_2():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # next(1, 2) = True
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/one> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/two> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 1


def test_answer_question4_next_1_3():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # next(1, 3) = False
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/one> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/three> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 0


def test_answer_question5_next_1_z_next_z_x():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # next(1, ?z),next(?z, ?x)->z:2, x:3
    my_question = \
        f'SELECT ?x WHERE {{' \
        f'?s1 <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s1 <http://example.org/variable_x> <http://example.org/one> . ' \
        f'?s1 <http://example.org/variable_y> ?z . ' \
        f'?s2 <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s2 <http://example.org/variable_x> ?z . ' \
        f'?s2 <http://example.org/variable_y> ?x . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?x'] == '<http://example.org/three>'


def test_answer_next_x_y():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # next(?x, ?y)->(1,2), (2,3), ..., (9,10)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s <http://example.org/variable_x> ?x . ' \
        f'?s <http://example.org/variable_y> ?y . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert len(resolve_bindings) == 9
