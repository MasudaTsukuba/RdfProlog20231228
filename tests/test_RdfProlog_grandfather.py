from src.RdfPrologMain import RdfProlog
from src.RdfResolution import ClassSparqlQuery
# from src_not_used.PR import PR


def test_answer_question1():
    rdf_prolog = RdfProlog()

    # grandfather(taro, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://example.org/operation> <http://example.org/grandfather> . 
        ?s <http://example.org/variable_x> <http://example.org/taro> . 
        ?s <http://example.org/variable_y> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == 'http://example.org/ichiro'


def test_answer_question2():
    rdf_prolog = RdfProlog()

    # grandfather(taro, ichiro)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://example.org/operation> <http://example.org/grandfather> . 
        ?s <http://example.org/variable_x> <http://example.org/taro> . 
        ?s <http://example.org/variable_y> <http://example.org/ichiro> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1


def test_answer_question3():
    rdf_prolog = RdfProlog()

    # grandfather(taro, jiro)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://example.org/operation> <http://example.org/grandfather> . 
        ?s <http://example.org/variable_x> <http://example.org/taro> . 
        ?s <http://example.org/variable_y> <http://example.org/jiro> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 0
