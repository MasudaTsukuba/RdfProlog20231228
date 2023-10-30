from rdflib import Graph, URIRef, BNode
from PR import PR

g_temp = Graph()
g_temp.parse('rules/rules_human.ttl')
results = g_temp.query('SELECT ?s ?p ?o WHERE { ?s ?p ?o . }')
g = Graph()
# g.parse('rules_human.ttl')
for result in results:
    ss = result['s']
    pp = result['p']
    oo = result['o']
    if type(ss) == BNode:
        ss = f'http://example.org/{str(ss)}'
    if type(oo) == BNode:
        oo = f'http://example.org/{str(oo)}'
    g.add((URIRef(ss), URIRef(pp), URIRef(oo)))
results = g.query('SELECT ?s ?p ?o WHERE { ?s ?p ?o . } ')
for result in results:
    print(result)
query = 'SELECT ?s ?o ?p1 ?o1 WHERE {?s <http://example.org/left_side> ?o . ' \
        '?o ?p1 ?o1}'
results = g.query(query)
# for result in results:
#     print(result)
query1 = f'SELECT ?o WHERE {{ ' \
         f'?s <http://example.org/left_side> ?o . ' \
         f'OPTIONAL {{ ?s <{PR.priority}> ?priority .}} }}' \
         f'ORDER BY ?priority '  # query for extracting left side rules
results1 = g.query(query1)  # execute query and extract
for result1 in results1:
    print(result1)
    query2 = f'SELECT ?p ?o WHERE {{ ?s <http://example.org/left_side> ?oo . ?oo ?p ?o . }}'  # extract content of left side rule
    results2 = g.query(query2)
    for result2 in results2:
        print(result2)

print('============================================')
query2 = f'SELECT ?s WHERE {{ ?s <{PR.operation}> <{PR.human}> . ?s <{PR.variable_x}> <{PR.socrates}> . }} '
results2 = g.query(query2)
for result2 in results2:
    print(result2)
