from src.RdfPrologMain import RdfProlog, ClassSparqlQuery


def test_list_next_1_ans():
    rdf_prolog = RdfProlog(rules_folder='rules_list_number')

    # next([1], ?ans) = [2]
    my_question = \
        f'SELECT ?ans ?car ?cdr WHERE {{' \
        f'?s1 <http://example.org/operation> <http://example.org/next_list_number> . ' \
        f'?s1 <http://example.org/variable_x> <http://example.org/list_one> . ' \
        f'?s1 <http://example.org/variable_y> ?ans . ' \
        f'?s2 <http://example.org/operation> <http://example.org/cons> . ' \
        f'?s2 <http://example.org/variable_x> ?car . ' \
        f'?s2 <http://example.org/variable_y> ?cdr . ' \
        f'?s2 <http://example.org/variable_z> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == '<http://example.org/two>'
    assert resolve_bindings[0]['?cdr'] == '<http://example.org/nil>'


def test_list_next_2_ans():
    rdf_prolog = RdfProlog(rules_folder='rules_list_number')

    # next([2], ?ans) = [3]
    my_question = \
        f'SELECT ?list_three ?car ?cdr WHERE {{' \
        f'?s1 <http://example.org/operation> <http://example.org/cons> . ' \
        f'?s1 <http://example.org/variable_x> <http://example.org/two> . ' \
        f'?s1 <http://example.org/variable_y> <http://example.org/nil> . ' \
        f'?s1 <http://example.org/variable_z> ?list_two . ' \
        f'?s2 <http://example.org/operation> <http://example.org/next_list_number> . ' \
        f'?s2 <http://example.org/variable_x> ?list_two . ' \
        f'?s2 <http://example.org/variable_y> ?list_three . ' \
        f'?s3 <http://example.org/operation> <http://example.org/cons> . ' \
        f'?s3 <http://example.org/variable_x> ?car . ' \
        f'?s3 <http://example.org/variable_y> ?cdr . ' \
        f'?s3 <http://example.org/variable_z> ?list_three . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car'] == '<http://example.org/three>'
    assert resolve_bindings[0]['?cdr'] == '<http://example.org/nil>'


def test_list_next_9_ans():
    rdf_prolog = RdfProlog(rules_folder='rules_list_number')

    # next([9], ?ans) = [0 1]
    my_question = \
        f'SELECT ?list_three ?car ?cdr WHERE {{' \
        f'?s1 <http://example.org/operation> <http://example.org/cons> . ' \
        f'?s1 <http://example.org/variable_x> <http://example.org/nine> . ' \
        f'?s1 <http://example.org/variable_y> <http://example.org/nil> . ' \
        f'?s1 <http://example.org/variable_z> ?list_nine . ' \
        f'?s2 <http://example.org/operation> <http://example.org/next_list_number> . ' \
        f'?s2 <http://example.org/variable_x> ?list_nine . ' \
        f'?s2 <http://example.org/variable_y> ?list_ten . ' \
        f'?s3 <http://example.org/operation> <http://example.org/cons> . ' \
        f'?s3 <http://example.org/variable_x> ?car_ten . ' \
        f'?s3 <http://example.org/variable_y> ?cdr_ten . ' \
        f'?s3 <http://example.org/variable_z> ?list_ten . ' \
        f'?s4 <http://example.org/operation> <http://example.org/cons> . ' \
        f'?s4 <http://example.org/variable_x> ?car . ' \
        f'?s4 <http://example.org/variable_y> ?cdr . ' \
        f'?s4 <http://example.org/variable_z> ?cdr_ten . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?car_ten'] == '<http://example.org/zero>'
    assert resolve_bindings[0]['?car'] == '<http://example.org/one>'
    assert resolve_bindings[0]['?cdr'] == '<http://example.org/nil>'


def test_list_next_ans_2():
    rdf_prolog = RdfProlog(rules_folder='rules_list_number')

    # next(?ans, [2])
    my_question = \
        f'SELECT ?list_one ?car ?cdr WHERE {{' \
        f'?s3 <http://example.org/operation> <http://example.org/cons> . ' \
        f'?s3 <http://example.org/variable_x> <http://example.org/two> . ' \
        f'?s3 <http://example.org/variable_y> <http://example.org/nil> . ' \
        f'?s3 <http://example.org/variable_z> ?list_two . ' \
        f'?s2 <http://example.org/operation> <http://example.org/next_list_number> . ' \
        f'?s2 <http://example.org/variable_x> ?list_one . ' \
        f'?s2 <http://example.org/variable_y> ?list_two . ' \
        f'?s4 <http://example.org/operation> <http://example.org/cons> . ' \
        f'?s4 <http://example.org/variable_x> ?car . ' \
        f'?s4 <http://example.org/variable_y> ?cdr . ' \
        f'?s4 <http://example.org/variable_z> ?list_one . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query, find_all=False)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?list_one'] == '<http://example.org/list_one>'
    assert resolve_bindings[0]['?car'] == '<http://example.org/one>'
    assert resolve_bindings[0]['?cdr'] == '<http://example.org/nil>'
