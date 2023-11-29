from src.RdfPrologMain import RdfProlog, ClassSparqlQuery


rdf_prolog = RdfProlog(rules_folder='rules_number')


def test_answer_question1_add_3_1():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(3, 1, ?ans) = 4
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://example.org/operation> <http://example.org/add_number> . 
        ?s <http://example.org/variable_x> <http://example.org/three> . 
        ?s <http://example.org/variable_y> <http://example.org/one> . 
        ?s <http://example.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://example.org/four'


def test_answer_question2_add_2_2_ans():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(2, 2, ?ans) = 4
    my_question = f"""
        SELECT ?ans WHERE {{ ?s <http://example.org/operation> <http://example.org/add_number> . 
        ?s <http://example.org/variable_x> <http://example.org/two> . 
        ?s <http://example.org/variable_y> <http://example.org/two> . 
        ?s <http://example.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://example.org/four'


def test_answer_question3_add_3_2_ans():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(3, 2, ?ans) = 5
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://example.org/operation> <http://example.org/add_number> . 
        ?s <http://example.org/variable_x> <http://example.org/three> . 
        ?s <http://example.org/variable_y> <http://example.org/two> . 
        ?s <http://example.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://example.org/five'


def test_answer_question4_add_3_ans_5():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(3, ?ans, 5)->ans:2
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://example.org/operation> <http://example.org/add_number> . 
        ?s <http://example.org/variable_x> <http://example.org/three> . 
        ?s <http://example.org/variable_y> ?ans . 
        ?s <http://example.org/variable_z> <http://example.org/five> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'http://example.org/two'


def test_answer_question4b_add_2_ans_3():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(2, ?ans, 3)->ans:1
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://example.org/operation> <http://example.org/add_number> . 
        ?s <http://example.org/variable_x> <http://example.org/two> . 
        ?s <http://example.org/variable_y> ?ans . 
        ?s <http://example.org/variable_z> <http://example.org/three> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, max_depth=10)
    assert resolve_bindings[0]['?ans'] == f'http://example.org/one'


def test_answer_complex_question1():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(3, 2, ?z), next(?z, ?ans)->z:5, ans:6
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <http://example.org/operation> <http://example.org/add_number> . 
        ?s1 <http://example.org/variable_x> <http://example.org/three> . 
        ?s1 <http://example.org/variable_y> <http://example.org/two> . 
        ?s1 <http://example.org/variable_z> ?z . 
        ?s2 <http://example.org/operation> <http://example.org/next_number> . 
        ?s2 <http://example.org/variable_x> ?z . 
        ?s2 <http://example.org/variable_y> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)  # ###################
    assert resolve_bindings[0]['?ans'] == f'http://example.org/six'


def test_answer_complex_question2():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(3, 2, ?z), add(?z, 2, ?ans)->z:5, ans:7
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s1 <http://example.org/operation> <http://example.org/add_number> . 
        ?s1 <http://example.org/variable_x> <http://example.org/three> . 
        ?s1 <http://example.org/variable_y> <http://example.org/two> . 
        ?s1 <http://example.org/variable_z> ?z . 
        ?s2 <http://example.org/operation> <http://example.org/add_number> . 
        ?s2 <http://example.org/variable_x> ?z . 
        ?s2 <http://example.org/variable_y> <http://example.org/two> . 
        ?s2 <http://example.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)  # ###################
    assert resolve_bindings[0]['?ans'] == f'http://example.org/seven'


def test_add_1_y_z():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(1, ?y, ?z)->(1,2),(2,3),...,(9,10)
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://example.org/operation> <http://example.org/add_number> . 
        ?s <http://example.org/variable_x> <http://example.org/one> . 
        ?s <http://example.org/variable_y> ?y . 
        ?s <http://example.org/variable_z> ?z . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=True, max_depth=30)
    assert len(resolve_bindings) == 9


def test_add_9_y_z():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')
    # add(9, ?y, ?z)->(1,10)
    my_question = f"""
        SELECT ?y ?z WHERE {{
        ?s <http://example.org/operation> <http://example.org/add_number> . 
        ?s <http://example.org/variable_x> <http://example.org/nine> . 
        ?s <http://example.org/variable_y> ?y . 
        ?s <http://example.org/variable_z> ?z . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=True, max_depth=20)
    assert resolve_bindings[0]['?y'] == f'http://example.org/one'
    assert resolve_bindings[0]['?z'] == f'http://example.org/ten'


def test_add_x_1_z():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(?x, 1, ?z)->(1,2),(2,3),...,(9,10)
    my_question = f"""
        SELECT ?x ?z WHERE {{
        ?s <http://example.org/operation> <http://example.org/add_number> . 
        ?s <http://example.org/variable_x> ?x . 
        ?s <http://example.org/variable_y> <http://example.org/one> . 
        ?s <http://example.org/variable_z> ?z . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=True)
    assert len(resolve_bindings) == 9


def test_add_x_9_z():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(?x, 9, ?z)->(1,10)
    my_question = f"""
        SELECT ?x ?z WHERE {{
        ?s <http://example.org/operation> <http://example.org/add_number> . 
        ?s <http://example.org/variable_x> ?x . 
        ?s <http://example.org/variable_y> <http://example.org/nine> . 
        ?s <http://example.org/variable_z> ?z . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=True)
    assert resolve_bindings[0]['?x'] == 'http://example.org/one'
    assert resolve_bindings[0]['?z'] == 'http://example.org/ten'


def test_add_x_y_2():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(?x, ?y, 2)->(1,1)
    my_question = f"""
        SELECT ?x ?y WHERE {{
        ?s <http://example.org/operation> <http://example.org/add_number> . 
        ?s <http://example.org/variable_x> ?x . 
        ?s <http://example.org/variable_y> ?y . 
        ?s <http://example.org/variable_z> <http://example.org/two> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=True)
    assert resolve_bindings[0]['?x'] == 'http://example.org/one'
    assert resolve_bindings[0]['?y'] == 'http://example.org/one'


def test_add_x_y_3():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(?x, ?y, 3)->(1,2),(2,1)
    my_question = f"""
        SELECT ?x ?y WHERE {{
        ?s <http://example.org/operation> <http://example.org/add_number> . 
        ?s <http://example.org/variable_x> ?x . 
        ?s <http://example.org/variable_y> ?y . 
        ?s <http://example.org/variable_z> <http://example.org/three> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=True, max_depth=10)
    assert len(resolve_bindings) == 2


def test_max_depth_add_3_1_ans():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(3, 1, ?ans) max_depth=0
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://example.org/operation> <http://example.org/add_number> . 
        ?s <http://example.org/variable_x> <http://example.org/three> . 
        ?s <http://example.org/variable_y> <http://example.org/one> . 
        ?s <http://example.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False, max_depth=1)
    assert len(resolve_bindings) == 0


def test_max_depth_add_3_1_ans_2():
    # rdf_prolog = RdfProlog(rules_folder='rules_number')

    # add(3, 1, ?ans) max_depth=1
    my_question = f"""
        SELECT ?ans WHERE {{
        ?s <http://example.org/operation> <http://example.org/add_number> . 
        ?s <http://example.org/variable_x> <http://example.org/three> . 
        ?s <http://example.org/variable_y> <http://example.org/one> . 
        ?s <http://example.org/variable_z> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, find_all=False, max_depth=2)
    assert len(resolve_bindings) == 1
    assert resolve_bindings[0]['?ans'] == 'http://example.org/four'
