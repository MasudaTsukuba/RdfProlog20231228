"""
test_020_RdfProlog_grandfather.py
test for family relationships
T. Masuda, 2023/11/28
"""

from src.RdfPrologMain import RdfProlog
from src.RdfResolution import ClassSparqlQuery

rdf_prolog = RdfProlog()


def test_answer_question1():
    # grandfather(taro, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://value.org/operation> <http://value.org/grandfather> . 
        ?s <http://value.org/variable_x> <http://value.org/taro> . 
        ?s <http://value.org/variable_y> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == 'http://value.org/ichiro'


def test_answer_question2():
    # grandfather(taro, ichiro)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://value.org/operation> <http://value.org/grandfather> . 
        ?s <http://value.org/variable_x> <http://value.org/taro> . 
        ?s <http://value.org/variable_y> <http://value.org/ichiro> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1


def test_answer_question3():
    # grandfather(taro, jiro)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://value.org/operation> <http://value.org/grandfather> . 
        ?s <http://value.org/variable_x> <http://value.org/taro> . 
        ?s <http://value.org/variable_y> <http://value.org/jiro> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 0
