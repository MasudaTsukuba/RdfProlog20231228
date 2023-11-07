from src.RdfProlog import RdfProlog, ClassSparqlQuery


def test_answer_question1_add_3_1():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(3, 1, ?ans) = 4
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/three> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/one> . ' \
        f'?s <http://example.org/variable_z> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'<http://example.org/four>'


def test_answer_question2_add_2_2():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(2, 2, ?ans) = 4
    my_question = \
        f'SELECT ?ans WHERE {{ ?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/two> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/two> . ' \
        f'?s <http://example.org/variable_z> ?ans . ' \
        f'}} '
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'<http://example.org/four>'


def test_answer_question3_add_3_2():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(3, 2, ?ans) = 5
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/three> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/two> . ' \
        f'?s <http://example.org/variable_z> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'<http://example.org/five>'


def test_answer_question4_add_3_ans_5():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(3, ?ans, 5)->ans:2
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/three> . ' \
        f'?s <http://example.org/variable_y> ?ans . ' \
        f'?s <http://example.org/variable_z> <http://example.org/five> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'<http://example.org/two>'


def test_answer_question4b_add_2_ans_3():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(2, ?ans, 3)->ans:1
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/two> . ' \
        f'?s <http://example.org/variable_y> ?ans . ' \
        f'?s <http://example.org/variable_z> <http://example.org/three> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'<http://example.org/one>'


def test_answer_complex_question1():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(3, 2, ?z), next(?z, ?ans)->z:5, ans:6
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s1 <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s1 <http://example.org/variable_x> <http://example.org/three> . ' \
        f'?s1 <http://example.org/variable_y> <http://example.org/two> . ' \
        f'?s1 <http://example.org/variable_z> ?z . ' \
        f'?s2 <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s2 <http://example.org/variable_x> ?z . ' \
        f'?s2 <http://example.org/variable_y> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)  # ###################
    assert resolve_bindings[0]['?ans'] == f'<http://example.org/six>'


def test_answer_complex_question2():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(3, 2, ?z), add(?z, 2, ?ans)->z:5, ans:7
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s1 <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s1 <http://example.org/variable_x> <http://example.org/three> . ' \
        f'?s1 <http://example.org/variable_y> <http://example.org/two> . ' \
        f'?s1 <http://example.org/variable_z> ?z . ' \
        f'?s2 <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s2 <http://example.org/variable_x> ?z . ' \
        f'?s2 <http://example.org/variable_y> <http://example.org/two> . ' \
        f'?s2 <http://example.org/variable_z> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)  # ###################
    assert resolve_bindings[0]['?ans'] == f'<http://example.org/seven>'


def test_add_1_y_z():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(1, ?y, ?z)->(1,2),(2,3),...,(9,10)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/one> . ' \
        f'?s <http://example.org/variable_y> ?y . ' \
        f'?s <http://example.org/variable_z> ?z . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query, find_all=True)
    assert len(resolve_bindings) == 9


def test_add_9_y_z():
    rdf_prolog = RdfProlog(rules_folder='rules_number')
    # add(9, ?y, ?z)->(1,10)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/nine> . ' \
        f'?s <http://example.org/variable_y> ?y . ' \
        f'?s <http://example.org/variable_z> ?z . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query, find_all=True)
    assert resolve_bindings[0]['?y'] == f'<http://example.org/one>'
    assert resolve_bindings[0]['?z'] == f'<http://example.org/ten>'


def test_add_x_1_z():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(?x, 1, ?z)->(1,2),(2,3),...,(9,10)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> ?x . ' \
        f'?s <http://example.org/variable_y> <http://example.org/one> . ' \
        f'?s <http://example.org/variable_z> ?z . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query, find_all=True)
    assert len(resolve_bindings) == 9


def test_add_x_9_z():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(?x, 9, ?z)->(1,10)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> ?x . ' \
        f'?s <http://example.org/variable_y> <http://example.org/nine> . ' \
        f'?s <http://example.org/variable_z> ?z . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query, find_all=True)
    assert resolve_bindings[0]['?x'] == '<http://example.org/one>'
    assert resolve_bindings[0]['?z'] == '<http://example.org/ten>'


def test_add_x_y_2():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(?x, ?y, 2)->(1,1)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> ?x . ' \
        f'?s <http://example.org/variable_y> ?y . ' \
        f'?s <http://example.org/variable_z> <http://example.org/two> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query, find_all=True)
    assert resolve_bindings[0]['?x'] == '<http://example.org/one>'
    assert resolve_bindings[0]['?y'] == '<http://example.org/one>'


def test_add_x_y_3():
    rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(?x, ?y, 3)->(1,2),(2,1)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> ?x . ' \
        f'?s <http://example.org/variable_y> ?y . ' \
        f'?s <http://example.org/variable_z> <http://example.org/three> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query, find_all=True)
    assert len(resolve_bindings) == 2
