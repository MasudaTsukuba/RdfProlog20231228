"""
test_010_RdfProlog_human.py
test for classic human -> mortal reasoning
T. Masuda, 2023/11/28
"""

from src.RdfPrologMain import RdfProlog
from src.RdfResolution import ClassSparqlQuery

rdf_prolog = RdfProlog('../rules/rules_human')


def test_graph():
    # human(?ans)  find people who are human -> socrates
    query = f"""
    SELECT ?s ?o WHERE {{ ?s <http://value.org/operation> <http://value.org/human>. ?s <http://value.org/variable_x> ?o .}}
    """
    my_sparql_query = ClassSparqlQuery().set(query).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?o'] == 'http://value.org/socrates'


def test_answer_question1():
    # mortal(?ans).  find people who are mortal
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://value.org/operation> <http://value.org/mortal> . 
        ?s <http://value.org/variable_x> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == 'http://value.org/socrates'


def test_answer_question2():
    # mortal(socrates).  socrates is mortal because socrates is human.
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://value.org/operation> <http://value.org/mortal> . 
        ?s <http://value.org/variable_x> <http://value.org/socrates> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1


def test_answer_question3():
    # mortal(platon).  platon is not registered.
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://value.org/operation> <http://value.org/mortal> . 
        ?s <http://value.org/variable_x> <http://value.org/platon> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 0
