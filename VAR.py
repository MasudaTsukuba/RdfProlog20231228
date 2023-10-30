from rdflib import URIRef


class VAR:
    var_url = 'http://variable.org/'
    variable_u = URIRef(var_url + 'variable_u')
    variable_v = URIRef(var_url + 'variable_v')
    variable_w = URIRef(var_url + 'variable_w')
    variable_x = URIRef(var_url + 'variable_x')
    variable_y = URIRef(var_url + 'variable_y')
    variable_z = URIRef(var_url + 'variable_z')
    # variables_mapping = {'<'+str(variable_u)+'>': '?u', '<'+str(variable_v)+'>': '?v', '<'+str(variable_w)+'>': '?w',
    #                      '<'+str(variable_x)+'>': '?x', '<'+str(variable_y)+'>': '?y', '<'+str(variable_z)+'>': '?z'}
