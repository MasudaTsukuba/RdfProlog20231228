"""Generate cons within a function
rules_list_number_math/function_function_cons.py
called from exec()
T. Masuda, 2023/12/28
"""

from src.RdfResolution import *

local_bindings = {}
print('Facts in RdfProlog.Fatcs: ', len(rdf_prolog.facts.facts))

for key_, value_ in bindings.items():
    key_modified = key_.replace(f'http://some.org/_', '').replace(f'http://variable.org/_', '')  # -> x
    # value_modified = value1.replace('http://value.org/', '').replace('http://variable.org/', '')
    local_bindings[key_modified] = value_  # value_modified  # arguments for exec

x = local_bindings['x']
y = local_bindings['y']
print(f'x: {x}')
print(f'y: {y}')

my_question = f"""
    SELECT ?car ?cdr WHERE {{
    ?s1 <{OPERATION}> <{VAL}cons> . 
    ?s1 <{VAL}variable_x> <{x}> . 
    ?s1 <{VAL}variable_y> <{y}> . 
    ?s1 <{VAL}variable_z> ?ans . 
    }}"""
my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
# rdf_prolog_local = RdfProlog(rules_folder='../rules/rules_list_number_math')
# resolve_bindings = rdf_prolog_local.answer_question(my_sparql_query, depth_limit=300)
resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=300)
print(resolve_bindings[0]['?ans'])

results = {'http://variable.org/ans': resolve_bindings[0]['?ans']}
