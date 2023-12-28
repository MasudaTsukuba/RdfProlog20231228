"""
test_010_RdfProlog_human.py
test for classic human -> mortal reasoning
T. Masuda, 2023/11/28
"""

from src.RdfResolution import *

rdf_prolog = RdfProlog('../rules/rules_human')  # create an instance of RdfProlog class specifying the rule folder


def test_graph():
    # human(?ans)  find people who are human. ?ans -> socrates
    query = f"""
        SELECT ?s ?o WHERE {{ ?s <{OPERATION}> <{VAL}human>. ?s <{VAL}variable_x> ?o .}}
        """
    my_sparql_query = ClassSparqlQuery().set(query).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?o'] == f'{VAL}socrates'


def test_answer_question1():
    # mortal(?ans).  find people who are mortal
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <{OPERATION}> <{VAL}mortal> . 
        ?s <{VAL}variable_x> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert resolve_bindings[0]['?ans'] == f'{VAL}socrates'


def test_answer_question2():
    # mortal(socrates).  socrates is mortal because socrates is human.
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <{OPERATION}> <{VAL}mortal> . 
        ?s <{VAL}variable_x> <{VAL}socrates> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 1


def test_answer_question3():
    # mortal(platon).  platon is not registered.
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <{OPERATION}> <{VAL}mortal> . 
        ?s <{VAL}variable_x> <{VAL}platon> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
    assert len(resolve_bindings) == 0
