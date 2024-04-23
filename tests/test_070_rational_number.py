"""
test_070_rational_numer.py
test for rational numbers
T. Masuda, 2024/2/5
"""

from src.RdfResolution import *

rdf_prolog = RdfProlog(rules_folder='../rules/rules_rational_number')


def test_rational_number_m_n_2():
    # rational_number(?m, ?n, rational_2) = [2, 1], [4, 2]
    my_question = f"""
        SELECT ?m ?n WHERE {{
        ?s1 <{OPERATION}> <{VAL}rational_number> . 
        ?s1 <{VAL}variable_x> ?m . 
        ?s1 <{VAL}variable_y> ?n . 
        ?s1 <{VAL}variable_z> <{VAL}rational_2> . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=4, depth_limit=10)
    assert len(resolve_bindings) == 1  # 2
    assert resolve_bindings[0]['?m'] == f'{VAL}2' or resolve_bindings[0]['?m'] == f'{VAL}4'
    assert resolve_bindings[0]['?n'] == f'{VAL}1' or resolve_bindings[0]['?n'] == f'{VAL}2'


def test_rational_number_3_5_z():
    # rational number 3/5
    my_question = f"""
        SELECT ?m ?n WHERE {{
        ?s1 <{OPERATION}> <{VAL}rational_number> . 
        ?s1 <{VAL}variable_x> <{VAL}3> . 
        ?s1 <{VAL}variable_y> <{VAL}5> . 
        ?s1 <{VAL}variable_z> ?z .
        ?s2 <{OPERATION}> <{VAL}rational_number> . 
        ?s2 <{VAL}variable_x> ?m . 
        ?s2 <{VAL}variable_y> ?n . 
        ?s2 <{VAL}variable_z> ?z . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=1, depth_limit=10)
    assert resolve_bindings[0]['?m'] == f'{VAL}3'
    assert resolve_bindings[0]['?n'] == f'{VAL}5'


def test_rational_number_13_19_z():
    # rational number 13/19
    my_question = f"""
        SELECT ?m ?n WHERE {{
        ?s1 <{OPERATION}> <{VAL}rational_number> . 
        ?s1 <{VAL}variable_x> <{VAL}13> . 
        ?s1 <{VAL}variable_y> <{VAL}19> . 
        ?s1 <{VAL}variable_z> ?z .
        ?s2 <{OPERATION}> <{VAL}rational_number> . 
        ?s2 <{VAL}variable_x> ?m . 
        ?s2 <{VAL}variable_y> ?n . 
        ?s2 <{VAL}variable_z> ?z . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=1, depth_limit=10)
    assert resolve_bindings[0]['?m'] == f'{VAL}13'
    assert resolve_bindings[0]['?n'] == f'{VAL}19'


def test_rational_multiply_3_5_7_11_z():
    # rational multiply 3/5 * 7/11
    my_question = f"""
        SELECT ?m ?n WHERE {{
        ?s1 <{OPERATION}> <{VAL}rational_number> . 
        ?s1 <{VAL}variable_x> <{VAL}3> . 
        ?s1 <{VAL}variable_y> <{VAL}5> . 
        ?s1 <{VAL}variable_z> ?x . 
        ?s2 <{OPERATION}> <{VAL}rational_number> . 
        ?s2 <{VAL}variable_x> <{VAL}7> . 
        ?s2 <{VAL}variable_y> <{VAL}11> . 
        ?s2 <{VAL}variable_z> ?y . 
        ?s3 <{OPERATION}> <{VAL}rational_multiply> . 
        ?s3 <{VAL}variable_x> ?x . 
        ?s3 <{VAL}variable_y> ?y . 
        ?s3 <{VAL}variable_z> ?z . 
        ?s4 <{OPERATION}> <{VAL}rational_number> . 
        ?s4 <{VAL}variable_x> ?m . 
        ?s4 <{VAL}variable_y> ?n . 
        ?s4 <{VAL}variable_z> ?z . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    resolve_bindings = rdf_prolog.answer_question(my_sparql_query, results_limit=1, depth_limit=20)
    assert resolve_bindings[0]['?m'] == f'{VAL}21'
    assert resolve_bindings[0]['?n'] == f'{VAL}55'
