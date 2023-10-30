"""
RdfClass.py
T. Masuda, 2023/10/30
"""

import rdflib
from rdflib import Graph, URIRef  # , BNode, Variable
from src.PR import PR
from src.ConvertQuery import convert_question


class ClassRules:  # list of rules
    """
    list of rules
    """
    def __init__(self, graph):
        """
        initialize ClassRules class
        :param graph:
        """
        self.list_of_rules = []
        query_for_rules = f'SELECT ?s ?o WHERE {{ ' \
                          f'?s <{PR.left_side}> ?o . ' \
                          f'OPTIONAL {{ ?s <{PR.priority}> ?priority .}} }}' \
                          f'ORDER BY ?priority '  # query for extracting left side rules
        results_for_rule_left = graph.query(query_for_rules)  # execute query and extract
        for binding_for_left in results_for_rule_left.bindings:
            instance_rule = ClassRule()  # create a rule instance
            instance_rule.build(graph, binding_for_left['s'], binding_for_left['o'])
            self.list_of_rules.append(instance_rule)  # append the rule to the list


class ClassRule:  # class for individual rule
    """
    class for individual rule
    """
    serial_number = 1000  # a variable to convert variables: x -> x1000

    def __init__(self):
        """
        initialize ClassRule class
        """
        self.label = ''
        self.rule_left = ClassRuleLeft()
        self.rule_right = []
        self.variables_dict = {}

    def build(self, graph, rule_label, rule_left_label):
        """
        build
        :param graph:
        :param rule_label:
        :param rule_left_label:
        :return:
        """
        # print('DETECTED RULE: ', rule_label)  # left side rule returned as an object  # debug
        self.label = rule_label
        self.rule_left.build(graph, rule_left_label)
        self.rule_right = []
        query = f'SELECT ?o WHERE {{ <{self.label}> <{PR.right_side}> ?o . ' \
                f'?o <{PR.priority}> ?priority . }} ORDER BY (?priority) '
        results = graph.query(query)
        # print('NUMBER OF CHILD RULES: ' + str(len(results)))  # debug
        for result in results:
            rr = ClassRuleRight().build(graph, result)
            self.rule_right.append(rr)
        return self

    def modify_variables(self):  # x -> x1000, etc.
        """
        x -> x1000, etc.
        :return:
        """
        self.variables_dict = {}
        for var in self.rule_left.var_list:
            self.variables_dict[var] = var + str(ClassRule.serial_number)  # x -> x1000
        for rule in self.rule_right:
            for grand_child in rule.child.grandchildren:
                triple = grand_child.triple
                if triple.subject.is_variable:  # subject
                    var = triple.subject.to_var()
                    try:
                        value = self.variables_dict[var]
                        triple.subject.build(value)
                    except KeyError:
                        self.variables_dict[var] = var + str(ClassRule.serial_number)  # convert free variable
                        triple.subject.build(self.variables_dict[var])
                if triple.object.is_variable:  # object
                    var = triple.object.to_var()
                    try:
                        value = self.variables_dict[var]
                        triple.object.build(value)
                    except KeyError:
                        self.variables_dict[var] = var + str(ClassRule.serial_number)  # convert free variable
                        triple.object.build(self.variables_dict[var])
        ClassRule.serial_number += 1  # prepare for the next conversion
        pass


class ClassRuleLeft:  # left side of a rule
    """
    left side of a rule
    """
    def __init__(self):
        """
        initialize ClassRuleLeft class
        """
        self.label = None
        self.content = None
        self.bindings = {}
        self.var_list = []

    def build(self, graph, rule_left_label):  # executed at the initial stage
        """
        executed at the initial stage
        :param graph:
        :param rule_left_label:
        :return:
        """
        self.label = None
        self.content = None
        self.bindings = {}
        self.var_list = []
        # print('DETECTED LEFT RULE: ', rule_left_label)  # left side rule in returned as an object  # debug
        # get the actual rules of the left side
        query_for_left_content = \
            f'SELECT ?p ?o WHERE {{ ' \
            f'<{str(rule_left_label)}> ?p ?o . }}'  # extract content of left side rule from the label
        results_for_left_content = graph.query(query_for_left_content)  # execute a query
        var_list = '?s '  # build sparql query for left side rule
        self.var_list.append('?s')
        sparql_query = f'SELECT VAR_LIST WHERE {{ '  # VAR_LIST will be replaced at the end
        for bindings_for_left_content in results_for_left_content.bindings:
            triple_predicate = bindings_for_left_content['p']  # predicate part of the left side of a rule
            triple_object = bindings_for_left_content['o']  # object part of the left side of a rule
            triple_object = f'<{triple_object}>'  # convert object to URI string
            try:
                if triple_object.find('http://variable.org/variable_') >= 0:
                    triple_object = triple_object.replace('<http://variable.org/variable_', '?').replace('>', '')
                    var_list += str(triple_object) + ' '  # register the variable to a list
                    self.var_list.append(str(triple_object))
            except KeyError:
                pass  # object is not a variable
            sparql_query += f'?s <{triple_predicate}> {triple_object} . '
        sparql_query += f'}}'  # close the sparql query
        sparql_query = sparql_query.replace('VAR_LIST', var_list)  # insert variables list
        self.label = str(rule_left_label)
        self.content = sparql_query
        self.bindings = results_for_left_content.bindings
        return self


class ClassRuleRight:  # right side of a rule
    """
    right side of a rule
    """
    def __init__(self):
        """
        initialize ClassRuleRight class
        """
        self.child = ClassRuleRightChild()  # right side has one child, which in turn has one or more grandchild

    def build(self, graph, right_side_for_child):  # executed at the initial stage
        """
        executed at the initial stage
        :param graph:
        :param right_side_for_child:
        :return:
        """
        # print('CHILD RULE: ' + str(right_side_for_child[0]))  # debug
        query_for_child = f'SELECT ?o where {{ <{str(right_side_for_child[0])}> <{PR.child}> ?o .}} '
        results_of_right_side_child = graph.query(query_for_child)  # query by the child name
        self.child.build(graph, results_of_right_side_child.bindings[0])
        return self

    def revise(self, right_clauses, bindings):  # bindingsは辞書型
        """
        bindingsは辞書型
        :param right_clauses:
        :param bindings:
        :return:
        """
        for grandchild in right_clauses.child.grandchildren:
            grandchild_revised = ClassRightGrandChild()  # create a new grandchild
            new_term = grandchild.triple.subject.revise(bindings)
            grandchild_revised.triple.subject.build(new_term)  # subject
            new_term = grandchild.triple.predicate.revise(bindings)
            grandchild_revised.triple.predicate.build(new_term)  # predicate
            new_term = grandchild.triple.object.revise(bindings)
            grandchild_revised.triple.object.build(new_term)  # object
            self.child.grandchildren.append(grandchild_revised)  # append the grandchild to the grandchildren
        return self


class ClassRuleRightChild:  # right side child of a rule
    """
    right side child of a rule
    """
    def __init__(self):  # child has grandchildren
        """
        child has a list of grandchildren
        """
        self.grandchildren = []

    def build(self, graph, result_for_grandchild):  # build the right side of a rule
        """
        build the right side of a rule
        :param graph:
        :param result_for_grandchild:
        :return:
        """
        self.grandchildren = []
        query_for_grandchild = f'SELECT ?s ?p ?o WHERE ' \
                               f'{{ <{result_for_grandchild["o"]}> ?p ?o . }}'  # find grandchildren of a rule
        results_for_grandchild = graph.query(query_for_grandchild)  # execute the query
        # get grand child rules from grand child name
        # print('NUMBER OF GRAND CHILD RULES: ' + str(len(results_for_grandchild)))  # debug
        for triple_for_grandchild in results_for_grandchild:
            # print('PREDICATE AND OBJECT OF GRAND CHILD RULE WERE: '
            #       + str(triple_for_grandchild['p']) + ' '
            #       + str(triple_for_grandchild['o']))  # debug
            triple = {'s': result_for_grandchild["o"], 'p': triple_for_grandchild['p'], 'o': triple_for_grandchild['o']}
            gc = ClassRightGrandChild().build(triple)  # build a grandchild from the triple
            self.grandchildren.append(gc)  # append the grandchild to the grandchildren
        return self

    def revise(self, clause, bindings):  # revise the right side of a rule
        """
        revise the right side of a rule
        :param clause:
        :param bindings:
        :return:
        """
        for grandchild in clause.child.grandchildren:
            grandchild_revised = ClassRightGrandChild()  # create a new grandchild
            new_term = grandchild.triple.subject.revise(bindings)
            grandchild_revised.triple.subject.build(new_term)  # revise the subject
            grandchild_revised.triple.predicate.build(grandchild.triple.predicate.revise(bindings))  # predicate
            grandchild_revised.triple.object.build(grandchild.triple.object.revise(bindings))  # object
            self.grandchildren.append(grandchild_revised)  # append the revised grandchild


class ClassRightGrandChild:  # grandchild of a rule having one triple
    """
    grandchild of a rule having one triple
    """
    def __init__(self):
        """
        triple: empty ClassTriple()
        """
        self.triple = ClassTriple()

    def build(self, triple_for_grandchild):
        """
        build a grandchild of a rule
        :param triple_for_grandchild:
        :return:
        """
        self.triple.build(triple_for_grandchild)
        return self


class ClassTriple:  # triple class
    """
    triple class
    """
    def __init__(self):  # triple has subject, predicate and object
        """
        triple has subject, predicate and object
        """
        self.subject = ClassTerm()
        self.predicate = ClassTerm()
        self.object = ClassTerm()

    def build(self, triple):  # triple is a dict
        """
        build a triple
        :param triple:
        :return:
        """
        self.subject.build(triple['s'])
        self.predicate.build(triple['p'])
        self.object.build(triple['o'])


class ClassTerm:  # term is either subject, predicate or object
    """
    term is either subject, predicate or object
    """
    def __init__(self):  # initialize
        """
        initialize ClassTerm class
        """
        self.term_text = ''
        self.is_variable = False

    def build(self, term_text):  # extract text element
        """
        build a term from term text
        :param term_text:
        :return:
        """
        self.term_text = str(term_text).replace(' ', '').replace('<', '').replace('>', '')
        self.is_variable = False
        if self.term_text.find('http://variable.org/') >= 0:  # <http://variable.org/variable_x> -> x
            self.is_variable = True
            self.term_text = self.term_text.replace('<', '').replace('>', ''). \
                replace('http://variable.org/', '').replace('variable_', '')
        if self.term_text.find('?') >= 0:  # ?x -> x
            self.is_variable = True
            self.term_text = self.term_text.replace('?', '')
        return self

    def to_uriref(self) -> URIRef:
        """

        :return uri_ref: URIRef
        """
        return URIRef('http://variable.org/variable_' + self.term_text)

    def to_uri(self) -> str:
        """

        :return
            uri_string: str
        """
        if self.is_variable:
            return '<http://variable.org/variable_' + self.term_text + '>'  # x -> <http://variable.org/variable_x>
        else:
            return '<' + self.term_text + '>'  # http://example.org/andy -> <http://example.org/andy>

    def to_var(self) -> str:
        """

        :return:
        """
        if self.is_variable:
            return '?' + self.term_text  # http://variable.org/x -> ?x
        else:
            return self.to_uri()  # http://example.org/andy -> <http://example.org/andy>

    def force_to_var(self) -> str:
        """

        :return:
        """
        return '?' + self.term_text.replace('http://example.org/', '')  # http://example.org/x -> ?x

    def revise(self, bindings):  # bindings: dict
        """

        :param bindings:
        :return:
        """
        term_text = self.to_var()  # if VAR x -> ?x, else http://example.org/andy -> <http://example.org/andy>
        try:
            if len(bindings) > 0:
                try:
                    term_text2 = bindings[term_text]
                    return term_text2  # return the value in the dict
                except KeyError:
                    pass
                except Exception as e:
                    print(e)
                    pass
        except Exception as e:
            print(e)
            pass
        return term_text  # if not in bindings, return as is


class ClassSparqlQuery:  # Sparql Query Class
    """
    sparql query class
    """
    def __init__(self):  # initialize the sparql query class instance
        """
        initialize the sparql query class instance
        """
        self.query = None
        self.list_of_rdfs = []  # rdfs is an array of clauses
        self.list_of_variables = []  # list of variables
        self.rule = ClassRule()  # empty rule

    def set(self, sparql_query):  # convert from sparql query string
        """
        convert from sparql query string
        :param sparql_query:
        :return:
        """
        self.query = sparql_query  # sparql_query is a string
        self.list_of_rdfs = []  # rdfs is an array of clauses
        self.build_variable_list()
        list_of_rdfs_temp = convert_question(self.query)
        list_of_clauses = []  # clause is an array of triples that have the same subject
        previous_subject = None
        first = True  # switch indicating the initial processing
        for rdf in list_of_rdfs_temp:  # rdf is an array of [s, p, o]
            # dummy = {'s': 'Dummy', 'p': 'Dummy', 'o': 'Dummy'}  # dummy dict
            triple = ClassTriple()  # instance of Triple Class
            if len(rdf) == 3:  # is indeed a triple
                triple.subject.build(rdf[0])  # assign into triple  # subject
                triple.predicate.build(rdf[1])  # predicate
                triple.object.build(rdf[2])  # object
                if triple.subject.to_uri() == previous_subject:  # has the same subject
                    list_of_clauses += [triple]  # append to the clause list
                else:
                    if first:
                        first = False  # for the first time, do nothing
                    else:
                        self.list_of_rdfs += [list_of_clauses]  # list of clauses ended. Append to the list
                    list_of_clauses = [triple]  # start a new list of clauses
                    previous_subject = triple.subject.to_uri()  # update the previous subject
        self.list_of_rdfs += [list_of_clauses]  # list of last clause ended
        return self

    def build_variable_list(self):  # create a list of variables
        """
        create a list of variables
        :return:
        """
        variable_str = self.query.replace('SELECT ', '')  # extract a string between 'SELECT' and 'WHERE'
        variable_str = variable_str[:variable_str.find(' WHERE')]
        list_of_variables_temp = variable_str.split(' ')  # split the string and convert to a list
        self.list_of_variables = [ClassTerm().build(var) for var in list_of_variables_temp]  # create a list of variables
        pass

    def build_query(self, results_for_build_query):  # build a query string
        """
        build a query string
        :param results_for_build_query:
        :return:
        """
        try:
            var_list = ''  # variables list for replacing $VAR_LIST
            query_for_resolve = f'SELECT $VAR_LIST WHERE {{ '  # start the query string
            term_subject = None  # for suppressing the warning of not defined before assignment
            for triple_for_build_query in results_for_build_query.child.grandchildren:  # extract each triple of a rule
                term_subject = ClassTerm().build(triple_for_build_query.triple.subject.force_to_var())  # subject
                term_predicate = ClassTerm().build(triple_for_build_query.triple.predicate.to_uri())  # predicate
                term_object = ClassTerm().build(triple_for_build_query.triple.object.to_var())  # object
                print('PREDICATE AND OBJECT: ' + str(term_predicate.to_uri()) + ' ' + str(term_object.to_var()))  # debug
                # term_value1 = term_object
                if term_object.is_variable:  # object is a variable
                    print('OBJECT WAS A VARIABLE: ' + str(term_object.to_var()))  # debug
                    key1 = term_object.to_uri()  # convert the object to uri
                    try:
                        if key1.find('<http://variable.org/variable_') >= 0:
                            key1 = key1.replace('<http://variable.org/variable_', '?').replace('>', '')  # to ?var form
                            term_value1 = ClassTerm().build(key1)  # new object term
                            print('(1)OBJECT VARIABLE WAS CONVERTED TO: ' + str(term_value1.to_uri()))  # debug
                    except KeyError:
                        pass
                else:
                    pass

                temp_obj = term_object
                # my_var = term_value1

                if temp_obj.is_variable:
                    var_list += temp_obj.to_var() + ' '  # append to the variables list (string)
                ss = term_subject.to_var()
                pp = term_predicate.to_uri()
                oo = temp_obj.to_var()
                str1 = f'{ss} {pp} {oo} . '
                query_for_resolve += str1  # append the converted triple
            query_for_resolve += f'}}'  # terminate the query string
            if term_subject.is_variable:  # such as ?s
                var_list += term_subject.to_var()  # last element  # to enable yes/no question
            query_for_resolve = query_for_resolve.replace('$VAR_LIST', var_list)
            print('CONVERTED QUERY FOR THE GRAND CHILD: ' + query_for_resolve)  # sub goal
            self.query = query_for_resolve  # set the query string in instance variable
            self.build_variable_list()  # previous function. set self.list_of_variables.
        except Exception as e:
            print('Something has happened in ClassSparqlQuery.build_query(). ', e)
            pass

    def direct_search(self, graph):  # find a triple in the graph that directly matches the query
        """
        find a triple in the graph that directly matches the query
        :param graph:
        :return:
        """
        results = graph.query(self.query)  # execute a query
        if len(results) > 0:  # direct search detected candidates. results.bindings are list of dict
            def build_bindings(bindings_of_direct_search):
                print('BINDINGS OF DIRECT SEARCH: ', str(bindings_of_direct_search))  # debug
                success = False  # assume a failure
                direct_search_bindings = []  # initialize the returned value
                for binding_of_direct_search in bindings_of_direct_search:  # extract an element in the list
                    success_for_each = True  # assume a success
                    return_bindings_temp = {}  # temporary bindings to be returned
                    for key in binding_of_direct_search:  # get a key in dict
                        key_string = str(key)  # get a key string
                        if isinstance(key, rdflib.term.Variable):  # in the case of a variable
                            key_string = '?' + key_string.replace('?', '')  # the key was a variable
                        my_value = str(binding_of_direct_search[key])  # get a value
                        if my_value.find('?') < 0:  # in the case the value is not a variable
                            my_value = '<' + my_value.replace('<', '').replace('>', '') + '>'  # convert to uri
                            # not a variable, change to uri
                            if my_value.find('variable.org') >= 0:  # value is a variable, not a true uri
                                success_for_each = False  # failed
                                break  # exit the for loop
                        return_bindings_temp[key_string] = my_value  # store in a dictionary
                    if success_for_each:
                        return_bindings = {}  # bindings to be returned
                        for key, value in return_bindings_temp.items():
                            return_bindings[key] = value  # copy the dict
                        direct_search_bindings.append(return_bindings)  # add to the list
                        success = True  # at least one element is succeeded
                return success, direct_search_bindings

            succeeded, bindings = build_bindings(results.bindings)  # create bindings to be returned
            return succeeded, bindings
        else:
            return False, []  # no direct match was found

    def find_applicable_rules(self, rules):  # find rules applicable to this query
        """
        find rules applicable to this query
        :param rules:
        :return:
        """
        g_temp = Graph()  # temporary graph for storing the query
        list_of_rdfs = convert_question(self.query)  # convert query to rdfs
        for clause in list_of_rdfs:  # repeat for the triple
            if len(clause) == 3:  # clause is indeed a triple
                g_temp.add((URIRef(clause[0].replace('<', '').replace('>', '')),
                            URIRef(clause[1].replace('<', '').replace('>', '')),
                            URIRef(clause[2].replace('<', '').replace('>', ''))))  # store the triple into the graph
        list_of_applicable_rules = []
        for rule in rules.list_of_rules:  # rules.list_of_rules contains all the rules
            results_for_left = g_temp.query(rule.rule_left.content)  # query against the temporary graph
            if len(results_for_left) > 0:  # applicable rule exists
                rule.rule_left.bindings = results_for_left.bindings[0]
                list_of_applicable_rules.append(rule)  # append the found rule
                print('LIST OF APPLICABLE RULES: ', str(rule.label))  # print the rule on the console
        return list_of_applicable_rules  # return the applicable rule(s)

    def build_rule(self):  # build the right side of a rule
        """
        build the right side of a rule
        :return:
        """
        for clause in self.list_of_rdfs:
            rule_right = ClassRuleRight()  # create right side of a rule
            for triple in clause:
                gc = ClassRightGrandChild()  # create a grandchild
                tp = ClassTriple()  # create a triple
                tp.subject = triple.subject  # copy the subject
                tp.predicate = triple.predicate  # copy the predicate
                tp.object = triple.object  # copy the object
                gc.triple = tp  # set the created triple into the grandchild
                rule_right.child.grandchildren += [gc]  # append to the grandchildren
            self.rule.rule_right += [rule_right]  # append to the right side
        return self
