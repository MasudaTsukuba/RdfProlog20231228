"""
RdfClass.py
Classes supporting RdfProlog reasoning
T. Masuda, 2023/10/30
"""
import sys
import logging
import rdflib
from rdflib import Graph, URIRef  # , BNode, Variable
from lark import Lark, Transformer, Token  # , Tree


def uri_ref(key_word: str, extension=False, ref=True) -> URIRef:
    reference = f'http://example.org/{key_word}'
    if extension:
        reference = f'<{reference}>'
    if ref:
        reference = URIRef(reference)
    return reference


def uri_ref_ext(key_word: str) -> URIRef:
    return URIRef(f'<http://example.org/{key_word}>')


class ClassClauses:
    """
    ClassClauses holds a set of clauses
    Used for the right sides of a rule
    Since the clauses are stored in a list, they are sorted with the priorities.
    """
    variable_modifier = 1000

    def __init__(self):
        self.list_of_clauses: list[ClassClause] = []
        self.list_of_variables = []
        pass

    def build(self, graph, results):
        pass

    def split_clauses(self):
        """
        Split the clauses into the first clause and the rest of clauses
        Returns:
             first clause (ClassClause)
             rest clauses (ClassClauses)
        """
        if len(self.list_of_clauses) > 0:
            rest_clauses = ClassClauses()
            rest_clauses.list_of_clauses = self.list_of_clauses[1:]
            return self.list_of_clauses[0], rest_clauses
        else:
            return None, []

    def combine(self, clauses):
        combined_clauses = ClassClauses()
        combined_clauses.list_of_clauses = self.list_of_clauses + clauses.list_of_clauses
        return combined_clauses

    def apply_bindings(self, bindings):
        return_clauses = ClassClauses()
        return_clauses.list_of_clauses = [clause.apply_bindings(bindings) for clause in self.list_of_clauses]
        return return_clauses

    def update_variables(self):
        clauses_updated = ClassClauses()
        for clause in self.list_of_clauses:
            clause_updated = clause.update_variables()
            clauses_updated.list_of_clauses.append(clause_updated)
        ClassClauses.variable_modifier += 1
        return clauses_updated


class ClassClause:
    """
    Clause is a list of triples that have the same subject.
    One of the triples indicates the operation such as add or next.

    """
    def __init__(self):
        self.list_of_triple: list[ClassTriple] = []
        self.operation_name_uri: str = ''  # ex. http://example.org/add_number
        self.predicate_object_dict: dict[str, str] = {}  # subject is unnamed and common among triples
        self.set_of_variables_in_query: set[tuple[str, str]] = set()  # [(object_variable, predicate)]
        self.set_of_half_variables: set[tuple[str, str]] = set()  # SOME:x
        self.variables_of_interest: set[str] = set()

    def from_triples(self, list_of_triple):
        self.list_of_triple: list[ClassTriple] = list_of_triple  # [s-p-o, s-p-o, ..., s-p-o]
        len_effective_rdfs = 0
        g_temp: Graph = Graph()  # temporary graph for storing the query
        g_temp_debug: list[tuple[URIRef, URIRef, URIRef]] = []  # debug for g_temp
        self.predicate_object_dict: dict[str, str] = {}  # subject is unnamed and common among triples
        self.set_of_variables_in_query: set[tuple[str, str]] = set()  # [(object_variable, predicate)]

        for triple in self.list_of_triple:
            subj = triple.subject  # ClassTerm
            pred = triple.predicate
            obje = triple.object
            subj_uri = subj.to_uri(drop=True)  # http://variable.org/s
            pred_uri = pred.to_uri(drop=True)  # http://example.org/operation
            obje_uri = obje.to_uri(drop=True)  # http://example.org/add_number
            g_temp.add((URIRef(subj_uri), URIRef(pred_uri), URIRef(obje_uri)))  # add to the temporary graph
            g_temp_debug.append((URIRef(subj_uri), URIRef(pred_uri), URIRef(obje_uri)))
            self.predicate_object_dict[pred_uri] = obje_uri  # build predicate-object pairs
            len_effective_rdfs += 1
            if not obje.is_variable:  # .find('http://variable.org/') < 0:
                pass  # skip if the object is a variable
            else:
                self.set_of_variables_in_query.add((obje_uri, pred_uri))
            if pred_uri == 'http://example.org/operation':
                operation_name = obje_uri.replace('http://example.org/', '')  # extract operation name
                self.operation_name_uri = uri_ref(operation_name)  # keep as UriRef

    def from_query(self, graph: Graph, subject: rdflib.term.URIRef):
        query_for_clause = f"""
            SELECT ?p ?o WHERE {{ <{subject}> ?p ?o . }}
        """
        results_for_clause = graph.query(query_for_clause)
        self.list_of_triple: list[ClassTriple] = []  # [s-p-o, s-p-o, ..., s-p-o]
        len_effective_rdfs = 0
        self.predicate_object_dict: dict[str, str] = {}  # subject is unnamed and common among triples
        self.set_of_variables_in_query: set[tuple[str, str]] = set()  # [(object_variable, predicate)]

        subj = subject  # ClassTerm
        subj_uri = str(subj)  # http://variable.org/s
        for binding in results_for_clause.bindings:
            pred = binding['?p']
            obje = binding['?o']
            pred_uri = str(pred)  # http://example.org/operation
            obje_uri = str(obje)  # http://example.org/add_number
            triple = ClassTriple()
            triple.build_from_spo(subj_uri, pred_uri, obje_uri)
            self.list_of_triple.append(triple)
            self.predicate_object_dict[pred_uri] = obje_uri  # build predicate-object pairs
            len_effective_rdfs += 1
            if obje_uri.find('http://variable.org/') >= 0:
                self.set_of_variables_in_query.add((obje_uri, pred_uri))
            if obje_uri.find('http://some.org/') >= 0:
                self.set_of_half_variables.add((obje_uri, pred_uri))
            if pred_uri == 'http://example.org/operation':
                operation_name = obje_uri.replace('http://example.org/', '')  # extract operation name
                self.operation_name_uri = uri_ref(operation_name)  # keep as UriRef
        return self

    def search_facts(self, rdf_prolog):  # search facts that may match this clause
        # def build_query():  # build a sparql query from a clause
        #     # sparql_query = ClassSparqlQuery()
        #     # clauses = ClassClauses()
        #     # clauses.list_of_clauses = [self]
        #     # sparql_query.from_clauses(clauses)
        #     query = 'SELECT $VAR_LIST WHERE {'
        #     var_set = set()
        #     for triple in self.list_of_triples:
        #         subj = triple.subject
        #         subj_uri = subj.to_var_string()
        #         if subj.is_variable:
        #             var_set.add(subj_uri)
        #         pred = triple.predicate
        #         pred_uri = pred.to_uri()
        #         obje = triple.object
        #         obje_uri = obje.to_var_string()
        #         if obje.is_variable:
        #             var_set.add(obje_uri)
        #         query += f'{subj_uri} {pred_uri} {obje_uri} . '
        #     query += '}'
        #     var_list = ''
        #     for var in var_set:
        #         var_list += f'{var} '
        #     query_out = query.replace('$VAR_LIST', var_list)
        #     return query_out
        #
        # query = build_query()
        # results = ClassRules.graph.query(query)  # execute a query
        # return_bindings = []
        # for bindings in results.bindings:
        #     bindings_dict = {}
        #     for key, value in bindings.items():
        #         if type(key) == rdflib.term.Variable:
        #             key_string = f'?{str(key)}'
        #         else:
        #             key_string = f'<{str(key)}>'
        #         if type(value) == rdflib.term.URIRef:
        #             value_string = f'<{str(value)}>'
        #         else:
        #             value_string = f'?{str(value)}'
        #         bindings_dict[key_string] = value_string
        #     return_bindings.append(bindings_dict)
        def match_fact(candidate):
            success = True
            bindings = {}
            for predicate, object in self.predicate_object_dict.items():
                try:
                    if object.find('http://variable.org/') >= 0:
                        bindings[object] = candidate.fact.predicate_object_dict[predicate]
                    else:
                        if candidate.fact.predicate_object_dict[predicate] == object:
                            pass
                        else:
                            success = False
                            break
                except Exception as e:
                    success = False
                    break
            return success, bindings

        def generate_cons():
            success = True  # assume the success
            bindings = {}
            variable_x = self.predicate_object_dict[uri_ref('variable_x', ref=False)]
            variable_y = self.predicate_object_dict[uri_ref('variable_y', ref=False)]
            variable_z = self.predicate_object_dict[uri_ref('variable_z', ref=False)]
            if variable_x.find('http://example.org/') >= 0 and variable_y.find('http://example.org/') >= 0 and variable_z.find('http://variable.org/') >= 0:
                cons_node = uri_ref(f'cons_node{str(ClassFacts.cons_number)}', ref=False)
                cons_list = uri_ref(f'cons_list{str(ClassFacts.cons_number)}', ref=False)
                ClassFacts.cons_number += 1

                triple1 = ClassTriple()
                triple1.build_from_spo(cons_node, uri_ref('operation', ref=False), uri_ref('cons', ref=False))
                triple2 = ClassTriple()
                triple2.build_from_spo(cons_node, uri_ref('variable_x', ref=False), variable_x)
                triple3 = ClassTriple()
                triple3.build_from_spo(cons_node, uri_ref('variable_y', ref=False), variable_y)
                triple4 = ClassTriple()
                triple4.build_from_spo(cons_node, uri_ref('variable_z', ref=False), cons_list)
                fact = ClassFact()
                fact.build_from_triples([triple1, triple2, triple3, triple4])
                rdf_prolog.facts.add_fact(fact)
                bindings[variable_z] = cons_list
            else:
                success = False
            return success, bindings

        operation_name_uri = self.operation_name_uri
        return_bindings = []
        try:
            candidates = rdf_prolog.facts.fact_dict[operation_name_uri]
            for candidate in candidates:
                success, bindings = match_fact(candidate)
                if success:
                    return_bindings.append(bindings)
        except KeyError:
            pass
        if len(return_bindings) == 0 and operation_name_uri == uri_ref('cons'):
            success, bindings = generate_cons()  # try to generate cons
            if success:
                return_bindings = [bindings]
        return return_bindings

    def match_rule(self, rule):
        matched = True  # assume the success
        forward_bindings = {}  # clause has constant, rule has variable. query: add(2, ?ans, 3) -> ?x: 2, ?y: 3
        backward_bindings = {}  # clause has variable, rule has constant. rule_left: add(?x, 1, ?y) -> ?ans: 1
        for rule_predicate, rule_object in rule.rule_left.predicate_object_dict.items():
            rule_object_drop = rule_object.replace('<', '').replace('>', '')
            try:
                query_object = self.predicate_object_dict[str(rule_predicate)]
                if rule_object_drop.find('http://example.org') >= 0:  # rule side is const
                    if query_object.find('http://example.org') >= 0:  # query side is const
                        if rule_object_drop == query_object:  # then they must be the same
                            pass
                        else:
                            matched = False  # if different, the match fails
                            continue
                    else:  # object in query is variable
                        backward_bindings['?' + query_object.replace('http://variable.org/', '')] = f'<{rule_object_drop}>'
                else:  # rule object is variable
                    forward_bindings[
                        rdflib.term.Variable(rule_object_drop.replace('http://variable.org/', ''))] = query_object
            except KeyError:
                matched = False
                continue
        return matched, rule.rule_right_clauses(), forward_bindings, backward_bindings

    def match_application(self, application):
        pattern = application.pattern
        matched = True  # assume the success
        forward_binding = {}  # query is constant, rule is variable
        backward_binding = {}  # query is variable, rule is either constant or variable
        for key, value in self.predicate_object_dict.items():
            if value.find('http://variable.org/') >= 0:
                try:
                    pattern_value = pattern.predicate_object_dict[key]
                    if pattern_value.find('http://variable.org/') >= 0:
                        forward_binding[pattern_value] = value
                    elif pattern_value.find('http://some.org/') >= 0:
                        matched = False
                        break
                    else:
                        backward_binding[value] = pattern_value
                except KeyError:
                    matched = False
                    break
            else:
                try:
                    pattern_value = pattern.predicate_object_dict[key]
                    if pattern_value.find('http://variable.org/') >= 0:
                        forward_binding[pattern_value] = value
                    elif pattern_value.find('http://some.org/') >= 0:
                        forward_binding[pattern_value] = value
                    else:
                        if pattern_value == value:
                            pass
                        else:
                            matched = False
                            break
                except KeyError:
                    matched = False
                    break
        list_of_clauses = []
        list_of_forward_bindings = []
        list_of_backward_bindings = []
        if matched:
            controls = application.list_of_controls
            for control in controls:
                left_side = control.left_side.update_variables()
                forward_binding_control = {}
                backward_binding_control = {}
                match_control = True
                for key, value in self.predicate_object_dict.items():
                    if value.find('http://variable.org/') >= 0:
                        try:
                            left_value = left_side.predicate_object_dict[key]
                            if left_value.find('http://variable.org/') >= 0:
                                forward_binding_control[left_value] = value
                            elif left_value.find('http://some.org/') >= 0:
                                match_control = False
                                break
                            else:
                                backward_binding_control[value] = left_value
                        except KeyError:
                            match_control = False
                            break
                    else:
                        try:
                            left_value = left_side.predicate_object_dict[key]
                            if left_value.find('http://variable.org/') >= 0:
                                forward_binding_control[left_value] = value
                            elif left_value.find('http://some.org/') >= 0:
                                forward_binding_control[left_value] = value
                            else:
                                if left_value == value:
                                    pass
                                else:
                                    match_control = False
                                    break
                        except KeyError:
                            match_control = False
                            break
                if match_control:
                    list_of_forward_bindings.append({**forward_binding, **forward_binding_control})
                    list_of_backward_bindings.append({**backward_binding, **backward_binding_control})
                    list_of_clauses.append(control.right_sides.update_variables())
        return matched, list_of_clauses, list_of_forward_bindings, list_of_backward_bindings

    def apply_bindings(self, bindings):
        clause_applied = ClassClause()
        clause_applied.list_of_triple = []
        clause_applied.predicate_object_dict = {}
        for triple in self.list_of_triple:
            triple_applied = triple.apply_bindings(bindings)
            clause_applied.list_of_triple.append(triple_applied)
            clause_applied.predicate_object_dict[triple_applied.predicate.to_uri(drop=True)] = triple_applied.object.to_uri(drop=True)
            if triple.predicate.to_uri(drop=True) == 'http://example.org/operation':
                clause_applied.operation_name_uri = rdflib.term.URIRef(triple_applied.object.to_uri(drop=True))
        return clause_applied

    def update_variables(self):
        clause_updated = ClassClause()
        list_of_triple = []
        for triple in self.list_of_triple:
            triple_updated = triple.update_variables()
            list_of_triple.append(triple_updated)
        clause_updated.from_triples(list_of_triple)
        return clause_updated


class ClassFacts:
    """
    This class holds a set of facts extracted from the rdf graph
    """
    cons_number = 10000  # serial number for cons_node and cons_list

    def __init__(self, graph):
        self.facts: set[ClassFact] = set()
        self.fact_dict = {}

        # register facts
        query_for_facts = f"""
            SELECT ?subject WHERE {{ ?subject {uri_ref_ext('type')} {uri_ref_ext('fact')} . }}
        """
        results_for_facts = graph.query(query_for_facts)
        for binding in results_for_facts.bindings:
            subject = binding['subject']
            fact = ClassFact()
            fact.build(graph, subject)
            self.add_fact(fact)

        # register inferences in a graph
        query_for_inferences = f"""
            SELECT ?subject WHERE {{ ?subject {uri_ref_ext('type')} {uri_ref_ext('inference')} . }}
        """
        results_for_inferences = graph.query(query_for_inferences)
        for binding in results_for_inferences.bindings:
            subject = binding['subject']
            inference = ClassFact()
            inference.build(graph, subject)
            self.add_fact(inference)
        pass

    def add_fact(self, fact):  # add and register a fact to facts
        self.facts.add(fact)
        operation_name = fact.operation_name_uri
        try:
            self.fact_dict[fact.operation_name_uri].add(fact)
        except KeyError:
            self.fact_dict[fact.operation_name_uri] = set()
            self.fact_dict[fact.operation_name_uri].add(fact)


class ClassFact:
    """
    A clause asserted as a fact in rdf graph
    """
    def __init__(self):
        self.fact = ClassClause()
        self.operation_name_uri = ''

    def build(self, graph, subject):
        self.fact = ClassClause()
        self.fact.from_query(graph, subject)
        self.operation_name_uri = self.fact.operation_name_uri

    def build_from_triples(self, list_of_triple):
        clause = ClassClause()
        clause.from_triples(list_of_triple)
        self.fact = clause
        self.operation_name_uri = clause.operation_name_uri


class ClassApplications:
    def __init__(self, graph: Graph):
        self.applications: list[ClassApplication] = []
        self.operation_names_dict = {}
        query_for_applications = f"""
            SELECT ?application WHERE {{ 
            ?application {uri_ref_ext('type')} {uri_ref_ext('application')} . 
            OPTIONAL {{ ?application {uri_ref_ext('priority')} ?priority . }}
            }} ORDER BY ?priority
        """
        results_for_applications = graph.query(query_for_applications)
        for binding in results_for_applications.bindings:
            application = ClassApplication(graph, binding['application'])
            self.applications.append(application)
            operation_name = application.operation_name_uri
            try:
                self.operation_names_dict[operation_name].append(application)
            except Exception as e:
                self.operation_names_dict[operation_name] = []
                self.operation_names_dict[operation_name].append(application)
        pass


    def build(self):
        pass


class ClassApplication:
    def __init__(self, graph: Graph, subject: rdflib.term.URIRef):
        query_for_application = f"""
            SELECT ?program ?pattern WHERE {{ <{subject}> {uri_ref_ext('program')} ?program ; {uri_ref_ext('pattern')} ?pattern . }}
        """
        results_for_application = graph.query(query_for_application)
        if len(results_for_application.bindings) > 0:
            self.program = str(results_for_application.bindings[0]['program']).find(f'{uri_ref("true")}') >= 0
            self.pattern = ClassClause()
            self.pattern.from_query(graph, results_for_application.bindings[0]['pattern'])
        self.operation_name_uri = self.pattern.operation_name_uri
        query_for_application_use = f"""
            SELECT ?control WHERE {{ <{subject}> {uri_ref_ext('use')} ?use . 
            ?use {uri_ref_ext('control')} ?control .
            OPTIONAL {{ ?use {uri_ref_ext('priority')} ?priority . }} }} ORDER BY ?priority 
        """
        results_for_application_use = graph.query(query_for_application_use)
        self.list_of_controls = []
        for binding in results_for_application_use.bindings:
            subject = binding['control']
            control = ClassControl(graph, subject)
            self.list_of_controls.append(control)
        pass


class ClassControls:
    def __init__(self, graph: Graph):
        self.controls: list[ClassControl] = []
        self.operation_name_dict = {}
        query_for_controls = f"""
            SELECT ?s WHERE {{
            ?s {uri_ref_ext('type')} {uri_ref_ext('control')} . 
            OPTIONAL {{ ?s {uri_ref_ext('priority')} ?priority . }}
            }} ORDER BY ?priority
        """
        results_for_controls = graph.query(query_for_controls)
        for binding in results_for_controls.bindings:
            control = ClassControl(graph, binding['s'])
            self.controls.append(control)
            operation_name = control.left_side.operation_name_uri
            try:
                self.operation_name_dict[operation_name].append(control)
            except Exception as e:
                self.operation_name_dict[operation_name] = []
                self.operation_name_dict[operation_name].append(control)
        pass


class ClassControl:
    def __init__(self, graph, subject: rdflib.term.URIRef):
        query_for_control_left = f"""
        SELECT ?left_side  WHERE {{ <{subject}> {uri_ref_ext('left_side')} ?left_side . }}
        """
        results_for_control_left = graph.query(query_for_control_left)
        subject_left = results_for_control_left.bindings[0]['left_side']
        clause = ClassClause()
        self.left_side = clause.from_query(graph, subject_left)
        self.right_sides = ClassClauses()
        query_for_control_right = f"""
        SELECT ?child  WHERE {{ 
        <{subject}> {uri_ref_ext('right_side')} ?right_side . 
        ?right_side {uri_ref_ext('child')} ?child .
        OPTIONAL {{ ?right_side {uri_ref_ext('priority')} ?priority . }}
        }} ORDER BY ?priority
        """

        results_for_control_right = graph.query(query_for_control_right)
        for binding in results_for_control_right.bindings:
            clause = ClassClause()
            right_side = clause.from_query(graph, binding['child'])
            self.right_sides.list_of_clauses.append(right_side)
        pass


class ClassRules:  # list of rules
    """
    Holds a list of all rules

    Attributes:
        list_of_rules (list[ClassRule]): List of rule instances
        dict_of_rules (dict[str, set[ClassRule]]): dict of rule instances
    """
    graph = None

    def __init__(self, graph):
        """
        initialize ClassRules class
        :param graph:
        """
        ClassRules.graph = graph
        self.list_of_rules = []
        # query_for_rules = SELECT ?s ?left WHERE {{ ' \
        #                   ?s <{uri_ref("left_side")}> ?left .
        #                   f'OPTIONAL {{ ?s <{uri_ref("priority")}> ?priority .}} }}' \
        #                   f'ORDER BY ?priority '  # query for extracting rules and their left side. Rules always have left_side. Use the priority values to order the rules.
        # results_for_rule_left = graph.query(query_for_rules)  # execute query and extract
        # for binding_for_left in results_for_rule_left.bindings:
        #     instance_rule = ClassRule()  # create a rule instance
        #     instance_rule.build(graph, binding_for_left['s'], binding_for_left['left'])  # s: rule id, o: rule pattern
        #     self.list_of_rules.append(instance_rule)  # append the rule to the list

        self.dict_of_rules = {}  # dict of rules. operation name as a key
        query_for_rules = f"""
            SELECT ?rule WHERE {{ ?rule {uri_ref_ext('type')} {uri_ref_ext('rule')} }}
        """ # query for extracting rules and their left side. Rules always have left_side. Use the priority values to order the rules.
        results_for_rule = graph.query(query_for_rules)  # execute query and extract
        for binding in results_for_rule.bindings:
            subject = binding['rule']
            instance_rule = ClassRule(graph, subject)  # create a rule instance
            operation_name = instance_rule.rule_left.operation_name_uri
            try:
                self.dict_of_rules[operation_name].add(instance_rule)
            except KeyError:
                self.dict_of_rules[operation_name] = set()
                self.dict_of_rules[operation_name].add(instance_rule)
        pass


class ClassRule:  # class for individual rule
    """
    class for an individual rule

    Attributes:
        label (str): label of the rule
        rule_left (ClassRuleLeft): left part of the rule
        rule_right (list[ClassRuleRight]): right part of the class consisting of a list of ClassRuleRight
        variables_dict (dict[str, str]): dict of the variables in the rule
    """
    serial_number = 1000  # a variable to convert variables: x -> x1000

    def __init__(self, graph, subject):
        """
        initialize ClassRule class
        """
        self.label = ''
        self.rule_left = ClassRuleLeft(graph, subject)
        self.rule_right: ClassRuleRight = ClassRuleRight()
        self.variables_dict = {}
        # self.build(graph, subject)


    # def build(self, graph, rule_label):
    #     """
    #     build a rule from rule label and rule left label.
    #
    #     Args:
    #         graph: RDF graph holding all info of rules
    #         rule_label: label of this rule
    #         rule_left_label: label of the left part of the rule
    #
    #     Returns:
    #         ClassRule: return the self as a ClassRule
    #     """
    #     # print('DETECTED RULE: ', rule_label)  # left side rule returned as an object  # debug
    #     self.label = rule_label
    #     self.rule_left.build(graph, rule_left_label)  # build the left parts of the rule from the left label.
    #     self.rule_right = []
    #     # get the right parts of the rule while considering the priorities to apply the sub goal.
    #     query = SELECT ?o WHERE {{ <{self.label}> <{uri_ref("right_side")}> ?o .
    #             f'?o <{uri_ref("priority")}> ?priority . }} ORDER BY (?priority) '
    #     results = graph.query(query)
    #     # print('NUMBER OF CHILD RULES: ' + str(len(results)))  # debug
    #     for result in results:
    #         right_clause = ClassClauses().build(graph, result)  # build the right side part of the rule
    #         self.rule_right.append(right_clause)  # save into a list
    #     return self

    def modify_variables(self):  # x -> x1000, etc.
        """
        x -> x1000, etc.
        This function is used to avoid confusion between classes that have variables with the same name.

        Returns:
            None: This function just modifies the internal variables.
        """
        self.variables_dict = {}  # The variables are held in this list.
        for var in self.rule_left.set_of_variables_in_query:
            self.variables_dict[var] = var + str(ClassRule.serial_number)  # x -> x1000
        for right_clause in self.rule_right:
            for grand_child in right_clause.child.grandchildren:
                triple = grand_child.triple
                if triple.subject.is_variable:  # subject
                    var = triple.subject.to_var_string()  # rdflib.term.Variable -> ?x
                    try:
                        value = self.variables_dict[var]  # already registered
                        triple.subject.build(value)
                    except KeyError:
                        self.variables_dict[var] = var + str(ClassRule.serial_number)  # convert free variable
                        triple.subject.build(self.variables_dict[var])
                if triple.object.is_variable:  # object
                    var = triple.object.to_var_string()
                    try:
                        value = self.variables_dict[var]  # already registered
                        triple.object.build(value)
                    except KeyError:
                        self.variables_dict[var] = var + str(ClassRule.serial_number)  # convert free variable
                        triple.object.build(self.variables_dict[var])
        ClassRule.serial_number += 1  # update the serial number to prepare for the next conversion
        pass

    def rule_right_clauses(self):
        clauses = []
        for right_clause in self.rule_right:
            clause = ClassClause()
            clause.list_of_triple = [triple for triple in right_clause.child.grandchildren]
            clauses.append(clause)
        return clauses


class ClassRuleLeft(ClassClause):  # left side of a rule
    """
    left side of a rule

    Attributes:
        label: id for the left part of the rule
        content: sparql query for finding applicable rules
        bindings:
        var_list: a list of variables in the triple
        const_dict: dict of constants in object with the correspondent predicate
        predicate_object_dict: dict for finding object from predicate as a key
        forward_bindings:
        backward_bindings:
    """
    def __init__(self, graph, subject):
        """
        initialize ClassRuleLeft class
        """
        super().__init__()
        self.list_of_triples: list[ClassTriple] = []
        self.operation_name_uri: str = ''  # ex. http://example.org/add_number
        self.predicate_object_dict: dict[str, str] = {}  # subject is unnamed and common among triples
        self.set_of_variables_in_query: set[tuple[str, str]] = set()  # [(object_variable, predicate)]
        self.set_of_half_variables: set[tuple[str, str]] = set()  # SOME:x
        self.variables_of_interest: set[str] = set()

        self.label = None  # id for the left part of the rule
        self.content = None  # sparql query for finding applicable rules
        self.bindings = {}
        # self.var_list = []  # a list of variables in the triple
        self.const_dict = {}  # dict of constants in object with the correspondent predicate
        self.forward_bindings = {}
        self.backward_bindings = {}
        query_for_rule_left = f"""
            SELECT ?left WHERE {{ <{subject}> {uri_ref_ext('left_side')} ?left }}
        """
        results_for_rule_left = graph.query(query_for_rule_left)
        bindings = results_for_rule_left.bindings
        if len(bindings) > 0:
            self.from_query(graph, bindings[0]['left'])
        pass

    def build(self, graph, rule_left_label):  # executed at the initial stage
        """
        Build the left side part of a rule from the label
        executed at the initial stage

        Args:
            graph:
            rule_left_label:

        Returns:

        """
        self.label = None  # label for the left side part of a rule
        self.content = None
        self.bindings = {}
        self.var_list = []
        self.const_dict = {}  # dict of constants in object with the corresponding predicate
        self.predicate_object_dict = {}  # dict for finding object from predicate as a key

        # print('DETECTED LEFT RULE: ', rule_left_label)  # left side rule in returned as an object  # debug
        # get the actual rules of the left side
        query_for_left_content = f"""
            SELECT ?p ?o WHERE {{ 
            <{str(rule_left_label)}> ?p ?o . }}"""  # extract content of left side rule from the label
        results_for_left_content = graph.query(query_for_left_content)  # execute a query

        var_list_string = '?s '  # build VAR_LIST of sparql query for left side rule
        # self.var_list.append('?s')  # also store the variables in a list
        sparql_query = f"""SELECT VAR_LIST WHERE {{ """  # VAR_LIST will be replaced at the end
        for bindings_for_left_content in results_for_left_content.bindings:  # analyze the query results
            triple_predicate = bindings_for_left_content['p']  # predicate part of the left side of a rule
            triple_object0 = bindings_for_left_content['o']  # object part of the left side of a rule
            triple_object = f'<{triple_object0}>'  # convert object to URI string
            self.predicate_object_dict[triple_predicate] = triple_object
            try:
                if triple_object.find('http://variable.org/') >= 0:
                    triple_object = triple_object.replace('<http://variable.org/', '?').replace('>', '')
                    var_list_string += str(triple_object) + ' '  # register the variable to a list
                    # self.var_list.append(str(triple_object))  # also append the variable to a list
                else:
                    self.const_dict[triple_predicate] = triple_object
            except KeyError:
                pass  # object is not a variable
            if triple_predicate.find('http://example.org/operation') >= 0 or triple_object.find('?') >= 0:
                sparql_query += f""" ?s <{triple_predicate}> {triple_object} . """

        sparql_query += f'}}'  # close the sparql query
        sparql_query = sparql_query.replace('VAR_LIST', var_list_string)  # insert variables list
        self.label = str(rule_left_label)
        self.var_list = var_list_string.strip().split(' ')
        self.content = sparql_query
        self.bindings = results_for_left_content.bindings
        return self


class ClassRuleRight(ClassClauses):  # right side of a rule
    """
    right side of a rule

    Attributes:
        child (ClassRuleRightChild): child of the right side clause
    """
    def __init__(self):
        """
        initialize ClassRuleRight class
        """
        super().__init__()
        # self.child = ClassRuleRightChild()  # right side clause has one child, which in turn has one or more grandchild

    def build(self, graph, right_side_for_child):  # executed at the initial stage
        """
        Build the right side clause of a rule
        executed at the initial stage

        Args:
            graph:
            right_side_for_child:

        Returns:
        """
        # print('CHILD RULE: ' + str(right_side_for_child[0]))  # debug
        query_for_child = f"""SELECT ?o WHERE {{ <{str(right_side_for_child[0])}> <{uri_ref("child")}> ?o .}} """
        results_of_right_side_child = graph.query(query_for_child)  # query by the child name

        self.child.build(graph, results_of_right_side_child.bindings[0])  # build a child from the query results
        return self

    def revise(self, right_clauses, bindings):  # bindingsは辞書型
        """
        bindingsは辞書型
        :param right_clauses:
        :param bindings:
        :return:
        """
        for grandchild in right_clauses.child.grandchildren:
            pass
            # grandchild_revised = ClassRightGrandChild()  # create a new grandchild
            # new_term = grandchild.triple.subject.revise(bindings)
            # grandchild_revised.triple.subject.build(new_term)  # subject
            # new_term = grandchild.triple.predicate.revise(bindings)
            # grandchild_revised.triple.predicate.build(new_term)  # predicate
            # new_term = grandchild.triple.object.revise(bindings)
            # grandchild_revised.triple.object.build(new_term)  # object
            # self.child.grandchildren.append(grandchild_revised)  # append the grandchild to the grandchildren
        return self


# class ClassRuleRightChild:  # right side child of a rule
#     """
#     right side child of a rule
#
#     Attributes:
#         grandchildren:
#     """
#     def __init__(self):  # child has grandchildren
#         """
#         child has a list of grandchildren
#         """
#         self.grandchildren = []
#
#     def build(self, graph, result_for_grandchild):  # build the right side of a rule
#         """
#         build the right side of a rule
#
#         Args:
#             graph:
#             result_for_grandchild:
#
#         Returns:
#             self:
#         """
#         self.grandchildren = []
#         query_for_grandchild = SELECT ?s ?p ?o WHERE ' \
#                                f'{{ <{result_for_grandchild["o"]}> ?p ?o . }}'  # find grandchildren of a rule
#         results_for_grandchild = graph.query(query_for_grandchild)  # execute the query
#         # get grand child rules from grand child name
#         # print('NUMBER OF GRAND CHILD RULES: ' + str(len(results_for_grandchild)))  # debug
#         for triple_for_grandchild in results_for_grandchild:
#             # print('PREDICATE AND OBJECT OF GRAND CHILD RULE WERE: '
#             #       + str(triple_for_grandchild['p']) + ' '
#             #       + str(triple_for_grandchild['o']))  # debug
#             triple = {'s': result_for_grandchild["o"], 'p': triple_for_grandchild['p'], 'o': triple_for_grandchild['o']}
#             grandchild = ClassRightGrandChild().build(triple)  # build a grandchild from the triple
#             self.grandchildren.append(grandchild)  # append the grandchild to the grandchildren
#         return self
#
#     def revise(self, clause, bindings):  # revise the right side of a rule
#         """
#         revise the right side of a rule
#
#         Args:
#             clause:
#             bindings:
#
#         Returns:
#             self:
#         """
#         for grandchild in clause.child.grandchildren:
#             grandchild_revised = ClassRightGrandChild()  # create a new grandchild
#             new_term = grandchild.triple.subject.revise(bindings)
#             grandchild_revised.triple.subject.build(new_term)  # revise the subject
#             grandchild_revised.triple.predicate.build(grandchild.triple.predicate.revise(bindings))  # predicate
#             grandchild_revised.triple.object.build(grandchild.triple.object.revise(bindings))  # object
#             self.grandchildren.append(grandchild_revised)  # append the revised grandchild
#
#
# class ClassRightGrandChild:  # grandchild of a rule having one triple
#     """
#     grandchild of a rule having one triple
#
#     Attributes:
#         triple: grandchild is an RF triple
#     """
#     def __init__(self):
#         """
#         triple: empty ClassTriple()
#         """
#         self.triple = ClassTriple()  # create an empty triple
#
#     def build(self, triple_for_grandchild):
#         """
#         build a grandchild of a rule
#
#         Args:
#             triple_for_grandchild:
#
#         Returns:
#             self:
#         """
#         self.triple.build(triple_for_grandchild)  # build a triple
#         return self


class ClassTriple:  # triple class
    """
    triple class

    Attributes:
        subject (ClassTerm)
        predicate = (ClassTerm)
        object = (ClassTerm)
    """
    def __init__(self):  # triple has subject, predicate and object
        """
        triple has subject, predicate and object
        """
        self.subject = ClassTerm()  # create an empty terms
        self.predicate = ClassTerm()
        self.object = ClassTerm()

    def build(self, triple):  # triple is a dict
        """
        build a triple

        Args:
            triple:

        Returns:
            None
        """
        self.subject.build(triple['s'])
        self.predicate.build(triple['p'])
        self.object.build(triple['o'])

    def build_from_spo(self, subject, predicate, object):
        self.subject.build(subject)
        self.predicate.build(predicate)
        self.object.build(object)

    def apply_bindings(self, bindings):
        triple_applied = ClassTriple()
        triple_applied.subject = self.subject.apply_bindings(bindings)
        triple_applied.predicate = self.predicate.apply_bindings(bindings)
        triple_applied.object = self.object.apply_bindings(bindings)
        return triple_applied

    def update_variables(self):
        triple_updated = ClassTriple()
        triple_updated.subject = self.subject.update_variables()
        triple_updated.predicate = self.predicate.update_variables()
        triple_updated.object = self.object.update_variables()
        return triple_updated


class ClassTerm:  # term is either subject, predicate or object
    """
    term is either subject, predicate or object

    Attributes:
        term_text (str): string name of this term, such as 'ans'
        is_variable (bool): True if this term represents a variable
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
        <http://variable.org/x> -> x

        Args:
            term_text:

        Returns:
            self:
        """
        self.term_text = str(term_text).replace(' ', '').replace('<', '').replace('>', '')
        self.is_variable = False
        if self.term_text.find('http://variable.org/') >= 0:  # <http://variable.org/x> -> x
            self.is_variable = True
            self.term_text = self.term_text.replace('<', '').replace('>', ''). \
                replace('http://variable.org/', '')  # .replace('variable_', '')
        if self.term_text.find('?') >= 0:  # ?x -> x
            self.is_variable = True
            self.term_text = self.term_text.replace('?', '')
        return self

    def to_uriref(self) -> URIRef:
        """
        Service function to produce URIRef from ClassTerm.
        'x' -> 'rdflib.term.URIRef('http://variable.org/x')

        Returns:
             uri_ref (URIRef)
        """
        if self.is_variable:
            return URIRef('http://variable.org/' + self.term_text)
        else:
            return URIRef(self.term_text)

    def to_uri(self, drop=False) -> str:
        """
        x -> <http://variable.org/x> for a variable
        http://example.org/andy -> <http://example.org/andy> for a constant
        Returns:
            str: uri_string
        """
        if self.is_variable:
            term_str = 'http://variable.org/' + self.term_text + ''  # x -> <http://variable.org/x>
        else:
            term_str = '' + self.term_text + ''  # http://example.org/andy -> <http://example.org/andy>
        if drop:
            return term_str
        else:
            return f'<{term_str}>'

    def to_var_string(self, drop=False) -> str:
        """
        http://variable.org/x -> ?x for a variable
        http://example.org/andy -> <http://example.org/andy> for a constant

        Returns:
            str:
        """
        if self.is_variable:
            return '?' + self.term_text  # http://variable.org/x -> ?x
        else:
            return self.to_uri(drop=drop)  # http://example.org/andy -> <http://example.org/andy>

    def force_to_var(self) -> str:
        """
        http://example.org/x -> ?x

        Returns:
            str:
        """
        return '?' + self.term_text.replace('http://example.org/', '')  # http://example.org/x -> ?x

    def revise(self, bindings):  # bindings: dict
        """
        Revise a term based on the bindings

        Args:
            bindings dict():

        Returns:

        """
        term_text = self.to_var_string()  # if VAR x -> ?x, else http://example.org/andy -> <http://example.org/andy>
        try:
            if len(bindings) > 0:  # if bindings contains maps
                try:
                    term_text2 = bindings[term_text]
                    return term_text2  # return the value in the dict
                except KeyError:  # term_text is not registered in the bindings
                    pass
                except Exception as e:  # unexpected error
                    print('In ClassTerm/revise, unexpected error', e)
                    logging.debug(f'In ClassTerm/revise, unexpected error {e}')
                    pass
        except Exception as e:  # unexpected error
            print('In ClassTerm/revise, unexpected error', e)
            logging.debug(f'In ClassTerm/revise, unexpected error {e}')
            pass
        return term_text  # if not in bindings, return as is

    def apply_bindings(self, bindings):
        term_applied = ClassTerm()
        if self.is_variable:
            try:
                value: str = bindings[f'?{self.term_text}']
                if value.startswith('?'):
                    term_applied.is_variable = True
                    term_applied.term_text = value.replace('?', '')
                else:
                    term_applied.is_variable = False
                    term_applied.term_text = value
            except Exception as e:
                term_applied.is_variable = True
                term_applied.term_text = self.term_text
            try:
                value: str = bindings[f'http://variable.org/{self.term_text}']
                if value.find('http://variable.org/') >= 0:
                    term_applied.is_variable = True
                    term_applied.term_text = value.replace('http://variable.org/', '')
                else:
                    term_applied.is_variable = False
                    term_applied.term_text = value
            except Exception as e:
                term_applied.is_variable = True
                term_applied.term_text = self.term_text
        else:
            term_applied.is_variable = False
            term_applied.term_text = self.term_text
        return term_applied

    def update_variables(self):
        term_updated = ClassTerm()
        term_updated.is_variable = self.is_variable
        if self.is_variable:
            term_updated.term_text = self.term_text + str(ClassClauses.variable_modifier)
        else:
            term_updated.term_text = self.term_text
        return term_updated


class ClassSparqlQuery:  # Sparql Query Class
    """
    sparql query class

    Attributes:
        query:
        list_of_rdfs: rdfs is an array of clauses
        list_of_variables: list of variables
        rule (ClassRule): empty rule
    """
    cons_number = 10000

    def __init__(self):  # initialize the sparql query class instance
        """
        initialize the sparql query class instance
        """

        self.query = None  # sparql query string
        self.list_of_rdfs = []  # rdfs is an array of clauses
        self.list_of_variables = []  # list of variables in this query
        # self.rule = ClassRule()  # empty rule

    def set(self, sparql_query: str):  # convert from sparql query string to a sparql query class instance
        """
        convert from sparql query string to a sparql query class instance

        Args:
            sparql_query (str):

        Returns:
            list[list[ClassTriple]]
        """
        self.query = sparql_query.replace('\n', '').replace('  ', ' ').strip()  # sparql_query is a string
        self.list_of_rdfs = []  # rdfs is an array of clauses
        self.build_variable_list()  # list of variables in this query
        list_of_rdfs_temp: list[list[ClassTerm]] = convert_question(self.query)  # query string to a list of triples
        list_of_triples = []  # clause is an array of triples that have the same subject
        previous_subject = None
        first = True  # switch indicating the initial processing
        for rdf in list_of_rdfs_temp:  # rdf is an array of triples [s, p, o]
            # dummy = {'s': 'Dummy', 'p': 'Dummy', 'o': 'Dummy'}  # dummy dict
            triple = ClassTriple()  # an instance of an empty Triple Class
            if len(rdf) == 3:  # is indeed a triple
                triple.subject.build(rdf[0].to_var_string())  # assign into triple  # subject
                triple.predicate.build(rdf[1].to_var_string())  # predicate
                triple.object.build(rdf[2].to_var_string())  # object
                if triple.subject.to_uri() == previous_subject:  # has the same subject
                    list_of_triples += [triple]  # append to the clause list
                else:
                    if first:
                        first = False  # for the first time, do nothing
                    else:
                        self.list_of_rdfs += [list_of_triples]  # list of clauses ended. Append to the list
                    list_of_triples = [triple]  # start a new list of clauses
                    previous_subject = triple.subject.to_uri()  # update the previous subject
        self.list_of_rdfs += [list_of_triples]  # list of last clause ended
        return self

    def build_variable_list(self):  # create a list of variables
        """
        create a list of variables

        Returns:
            None: Just modify the internal state.
        """
        variable_str = self.query.replace('SELECT ', '')  # extract a string between 'SELECT' and 'WHERE'
        variable_str = variable_str[:variable_str.find(' WHERE')]
        list_of_variables_temp = variable_str.split(' ')  # split the string and convert to a list
        self.list_of_variables = [ClassTerm().build(var) for var in list_of_variables_temp]  # create a list of variables
        pass

    def build_query(self, results_for_build_query):  # build a query string
        """
        build a query string

        Args:
            results_for_build_query:

        Returns:

        """
        try:
            var_list = ''  # variables list for replacing $VAR_LIST
            query_for_resolve = f"""SELECT $VAR_LIST WHERE {{ """  # start the query string. $VAR_LIST will be replaced at the end.
            term_subject = None  # for suppressing the warning of not defined before assignment
            self.list_of_rdfs = []  # reset
            for triple_for_build_query in results_for_build_query.child.grandchildren:  # extract each triple of a rule
                term_subject = ClassTerm().build(triple_for_build_query.triple.subject.force_to_var())  # subject
                term_predicate = ClassTerm().build(triple_for_build_query.triple.predicate.to_uri())  # predicate
                term_object = ClassTerm().build(triple_for_build_query.triple.object.to_var_string())  # object
                print('PREDICATE AND OBJECT: ' + str(term_predicate.to_uri()) + ' ' + str(term_object.to_var_string()))  # debug
                logging.debug(f'PREDICATE AND OBJECT: {str(term_predicate.to_uri())} {str(term_object.to_var_string())}')  # debug
                # term_value1 = term_object
                if term_object.is_variable:  # object is a variable
                    print('OBJECT WAS A VARIABLE: ' + str(term_object.to_var_string()))  # debug
                    logging.debug(f'OBJECT WAS A VARIABLE: {str(term_object.to_var_string())}')  # debug
                    key1 = term_object.to_uri()  # convert the object to uri
                    try:
                        if key1.find('<http://variable.org/') >= 0:
                            key1 = key1.replace('<http://variable.org/', '?').replace('>', '')  # to ?var form
                            term_value1 = ClassTerm().build(key1)  # new object term
                            print('(1)OBJECT VARIABLE WAS CONVERTED TO: ' + str(term_value1.to_uri()))  # debug
                            logging.debug(f'(1)OBJECT VARIABLE WAS CONVERTED TO: {str(term_value1.to_uri())}')  # debug
                    except KeyError:
                        pass
                else:
                    pass

                temp_obj = term_object
                # my_var = term_value1

                if temp_obj.is_variable:
                    var_list += temp_obj.to_var_string() + ' '  # append to the variables list (string)
                ss = term_subject.to_var_string()
                pp = term_predicate.to_uri()
                oo = temp_obj.to_var_string()
                str1 = f'{ss} {pp} {oo} . '
                query_for_resolve += str1  # append the converted triple
                temp_triple = ClassTriple()
                temp_triple.subject = term_subject
                temp_triple.predicate = term_predicate
                temp_triple.object = term_object
                self.list_of_rdfs.append(temp_triple)
            query_for_resolve += f'}}'  # terminate the query string

            if term_subject.is_variable:  # such as ?s
                var_list += term_subject.to_var_string()  # last element  # to enable yes/no question
            query_for_resolve = query_for_resolve.replace('$VAR_LIST', var_list)
            print('CONVERTED QUERY FOR THE GRAND CHILD: ' + query_for_resolve)  # sub goal
            logging.debug(f'CONVERTED QUERY FOR THE GRAND CHILD: {query_for_resolve}')  # sub goal
            self.query = query_for_resolve  # set the query string in instance variable
            self.build_variable_list()  # previous function. set self.list_of_variables.
        except Exception as e:
            print('Something has happened in ClassSparqlQuery.build_query(). ', e)
            logging.debug(f'Something has happened in ClassSparqlQuery.build_query(). {e}')
            pass

    def direct_search(self):  # find a triple in the graph that directly matches the query
        """
        find a triple in the graph that directly matches the query

        Args:
            graph (Graph): an RDF graph holding all the info of facts and rules.

        Returns:
            bool: True, if search is successful.
            list[]:  a list of bindings.

        """

        results = ClassRules.graph.query(self.query)  # execute a query
        if len(results) > 0:  # direct search detected candidates. results.bindings are a list of dict
            def build_bindings(bindings_of_direct_search):
                print('BINDINGS OF DIRECT SEARCH: ', str(bindings_of_direct_search))  # debug
                logging.debug(f'BINDINGS OF DIRECT SEARCH: {str(bindings_of_direct_search)}')  # debug
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
            found_cons = True  # try creating cons node  # 2023/11/10
            var_x = None
            var_y = None
            var_z = None
            for rdf in self.list_of_rdfs:
                if rdf.predicate.term_text == 'http://example.org/operation':
                    if rdf.object.term_text != 'http://example.org/cons':
                        found_cons = False
                        break
                if rdf.predicate.term_text == 'http://example.org/variable_x':
                    if rdf.object.is_variable:
                        found_cons = False
                        break
                    else:
                        var_x = rdf.object.to_uriref()
                if rdf.predicate.term_text == 'http://example.org/variable_y':
                    if rdf.object.is_variable:
                        found_cons = False
                        break
                    else:
                        var_y = rdf.object.to_uriref()
                if rdf.predicate.term_text == 'http://example.org/variable_z':
                    if not rdf.object.is_variable:
                        found_cons = False
                        break
                    else:
                        var_z = rdf.object.to_var_string()
            if found_cons:

                cons_node = URIRef(f'http://example.org/cons_node{ClassSparqlQuery.cons_number}')
                cons_list = URIRef(f'http://example.org/cons_list{ClassSparqlQuery.cons_number}')
                ClassSparqlQuery.cons_number += 1

                ClassRules.graph.add((cons_node, URIRef('http://example.org/operation'), URIRef('http://example.org/cons')))
                ClassRules.graph.add((cons_node, URIRef('http://example.org/variable_x'), var_x))
                ClassRules.graph.add((cons_node, URIRef('http://example.org/variable_y'), var_y))
                ClassRules.graph.add((cons_node, URIRef('http://example.org/variable_z'), cons_list))
                return True, [{var_z: f'<{str(cons_list)}>'}]

            return False, []  # no direct match was found. return False (Not Found) and an empty list

    def find_applicable_rules(self, rules):  # find rules applicable to this query
        """
        find rules applicable to this query

        Args:
            rules (ClassRules): a class holding info of rules.

        Returns:

        """
        list_of_rdfs: list[list[ClassTerm]] = convert_question(self.query)  # convert query to a list of triples
        len_effective_rdfs = 0
        g_temp: Graph = Graph()  # temporary graph for storing the query
        g_temp_debug: list[tuple[URIRef, URIRef, URIRef]] = []
        predicate_object_dict: dict[str, str] = {}
        set_of_variables_in_query: set[tuple[str, str]] = set()
        operation_name_uri: str = ''

        for clause in list_of_rdfs:  # repeat for the triples
            if len(clause) == 3:  # clause is indeed a triple
                subj = clause[0]  # .to_uri(drop=True)  # clause[0].replace('<', '').replace('>', '')
                pred = clause[1]  # .to_uri(drop=True)  # clause[1].replace('<', '').replace('>', '')
                obje = clause[2]  # .to_uri(drop=True)  # clause[2].replace('<', '').replace('>', '')
                subj_uri = subj.to_uri(drop=True)
                pred_uri = pred.to_uri(drop=True)
                obje_uri = obje.to_uri(drop=True)
                g_temp.add((URIRef(subj_uri), URIRef(pred_uri), URIRef(obje_uri)))
                g_temp_debug.append((URIRef(subj_uri), URIRef(pred_uri), URIRef(obje_uri)))
                predicate_object_dict[pred_uri] = obje_uri
                len_effective_rdfs += 1
                if not obje.is_variable:  # .find('http://variable.org/') < 0:  # skip if the object is a variable
                    # g_temp.add((URIRef(subj), URIRef(pred), URIRef(obje)))
                    # g_temp_debug.append((URIRef(subj), URIRef(pred), URIRef(obje)))
                    # len_effective_rdfs += 1
                    pass
                else:
                    set_of_variables_in_query.add((obje_uri, pred_uri))
                # g_temp.add((URIRef(clause[0].replace('<', '').replace('>', '')),
                #             URIRef(clause[1].replace('<', '').replace('>', '')),
                #             URIRef(clause[2].replace('<', '').replace('>', ''))))  # store the triple into the graph
                if pred_uri == 'http://example.org/operation':
                    operation_name = obje_uri.replace('http://example.org/', '')
                    operation_name_uri = uri_ref(operation_name)

        # list_of_applicable_rules = []  # start building a list of applicable rules
        # for rule in rules.list_of_rules:  # rules.list_of_rules contains all the rules
        #     # results_for_left = g_temp.query(rule.rule_left.content)  # query against the temporary graph
        #     match = True
        #     forward_bindings = {}
        #     backward_bindings = {}
        #     for rule_predicate, rule_object0 in rule.rule_left.predicate_object_dict.items():
        #         rule_object = rule_object0.replace('<', '').replace('>', '')
        #         try:
        #             query_object = predicate_object_dict[str(rule_predicate)]
        #             if rule_object.find('http://example.org') >= 0:  # const
        #                 if query_object.find('http://example.org') >= 0:  # const
        #                     if rule_object == query_object:
        #                         pass
        #                     else:
        #                         match = False
        #                         continue
        #                 else:  # object in query is variable
        #                     backward_bindings['?'+query_object.replace('http://variable.org/', '')] = f'<{rule_object}>'
        #             else:  # rule object is variable
        #                 forward_bindings[rdflib.term.Variable(rule_object.replace('http://variable.org/', ''))] = query_object
        #         except KeyError:
        #             match = False
        #             continue
        #
        #     # if len(results_for_left) > 0:  # applicable rule exists
        #     #     # if len(results_for_left.bindings[0]) == len_effective_rdfs:
        #     #     forward_bindings = results_for_left.bindings[0]
        #     #     backward_bindings = {}
        #     #     dict_of_rule_left = {}
        #     #     for variable in set_of_variables_in_query:
        #     #         pred = variable[1]
        #     #         obje_in_rule_left = rule.rule_left.predicate_object_dict[URIRef(pred)]
        #     #         backward_bindings['?'+variable[0]] = obje_in_rule_left
        #     if match:
        #         rule.rule_left.forward_bindings = forward_bindings
        #         rule.rule_left.backward_bindings = backward_bindings
        #         list_of_applicable_rules.append(rule)  # append the found rule
        #         print('LIST OF APPLICABLE RULES: ', str(rule.label))  # print the rule on the console

        # THe code below causes error in pytest. The reason is unknown. 2023/11/7.
        list_of_applicable_rules2 = []  # start building a list of applicable rules
        try:
            set_of_rules = rules.dict_of_rules[operation_name_uri]
            for rule in list(set_of_rules):  # rules.list_of_rules contains all the rules
                # results_for_left = g_temp.query(rule.rule_left.content)  # query against the temporary graph
                match = True
                forward_bindings = {}
                backward_bindings = {}
                for rule_predicate, rule_object0 in rule.rule_left.predicate_object_dict.items():
                    rule_object = rule_object0.replace('<', '').replace('>', '')
                    try:
                        query_object = predicate_object_dict[str(rule_predicate)]
                        if rule_object.find('http://example.org') >= 0:  # const
                            if query_object.find('http://example.org') >= 0:  # const
                                if rule_object == query_object:
                                    pass
                                else:
                                    match = False
                                    continue
                            else:  # object in query is variable
                                backward_bindings['?'+query_object.replace('http://variable.org/', '')] = f'<{rule_object}>'
                        else:  # rule object is variable
                            forward_bindings[rdflib.term.Variable(rule_object.replace('http://variable.org/', ''))] = query_object
                    except KeyError:
                        match = False
                        continue
                if match:
                    rule.rule_left.forward_bindings = forward_bindings
                    rule.rule_left.backward_bindings = backward_bindings
                    list_of_applicable_rules2.append(rule)  # append the found rule
                    print('LIST OF APPLICABLE RULES: ', str(rule.label))  # print the rule on the console
                    logging.debug(f'LIST OF APPLICABLE RULES: {str(rule.label)}')  # print the rule on the console
                    if str(rule.label).find('list_number_add_x_y_z') >= 0:  # debug
                        pass  # debug
        except KeyError:
            pass  # operation_name not found in dict_of_rules
        # if len(list_of_applicable_rules) != len(list_of_applicable_rules2):
        #     print(list_of_applicable_rules, list_of_applicable_rules2)
        #     pass  # debug
        #     sys.exit(-1)
        # else:
        #     for rule1, rule2 in zip(list_of_applicable_rules, list_of_applicable_rules2):
        #         if rule1.label != rule2.label:
        #             print(rule1.label, rule2.label)
        #             pass  # debug
        #             sys.exit(-2)
        return list_of_applicable_rules2  # return the applicable rules

    def build_rule(self):  # build the right side of a rule
        """
        build the right side of a rule
        :return:
        """
        for clause in self.list_of_rdfs:
            rule_right = ClassClauses()  # create right side of a rule
            for triple in clause:
                gc = ClassClause()  # create a grandchild
                tp = ClassTriple()  # create a triple
                tp.subject = triple.subject  # copy the subject
                tp.predicate = triple.predicate  # copy the predicate
                tp.object = triple.object  # copy the object
                gc.triple = tp  # set the created triple into the grandchild
                # rule_right.list_of_clauses += gc  # append to the grandchildren
            # self.rule.rule_right = rule_right  # append to the right side
        return self

    def to_clauses(self):
        clauses = ClassClauses()
        clauses.list_of_variables = self.list_of_variables  # list of ClassTerm
        clauses.list_of_clauses = []
        for list_of_triples in self.list_of_rdfs:
            clause = ClassClause()
            clause.from_triples(list_of_triples)
            clauses.list_of_clauses.append(clause)
        return clauses

    def from_clauses(self, clauses):
        self.list_of_variables = clauses.list_of_variables
        self.list_of_rdfs = []
        for clause in clauses.list_of_clauses:
            list_of_triples = clause.list_of_triple
            self.list_of_rdfs.append(list_of_triples)
        return self


"""
ConvertQuery.py
T. Masuda, 2023/10/30

convert a sparql query into a list of rdf triples

For example, if the input sparql query is
SELECT ?ans WHERE {
?s <http://example.org/operation> <http://example.org/add_number> .
?s <http://example.org/variable_x> <http://example.org/three> .
?s <http://example.org/variable_y> <http://example.org/two> .
?s <http://example.org/variable_z> ?ans . }'

The return list is
[['<http://variable.org/s>', '<http://example.org/operation>', '<http://example.org/add_number>'],
['<http://variable.org/s>', '<http://example.org/variable_x>', '<http://example.org/three>'],
['<http://variable.org/s>', '<http://example.org/variable_y>', '<http://example.org/two>'],
['<http://variable.org/s>', '<http://example.org/variable_z>', '<http://variable.org/ans>']]

where ?s and ?ans are transformed into <http://variable.org/s> and <http://variable.org/ans>, respectively.
"""


grammar = """
sparql : "SELECT " (var)+ where
where : "WHERE {" (" ")* (triple)+ "}" (" ")* 
var : VAR
VAR : "?" WORD (" ")+
triple : subject predicate object "." (" ")* 
WORD : CHAR (CHAR | NUMBER | "_")*
CHAR : "a".."z" | "A".."Z"
NUMBER : "0".."9"
subject   : (VAR | HTTP) 
predicate : (VAR | HTTP)
object    : (VAR | HTTP)
HTTP : "<http://" HTTP_WORD ">" (" ")* 
HTTP_WORD : CHAR (CHAR | NUMBER | "." | "/" | "_" | "-")*
"""


class MyTransformer(Transformer):
    """

    Attributes:
        list_of_rdf_triples (list[list[str]]): a list of triples.

        list_of_each_triple (list[str]): a list of each triple.
    """
    def __init__(self):
        """

        """
        super().__init__()
        self.list_of_rdf_triples = []  # This is what we actually want to get.
        self.list_of_each_triple = []  # working variable.
        # self.predicate_object_pair = {}

    @staticmethod
    def sparql(tree: list[str]) -> str:
        """
        build a sparql query string

        Args:
             tree: a list of lark tree strings

        Returns:
             sparql query string (str)
        """
        sparql_string = 'SELECT '
        sparql_string += ''.join(tree)
        return sparql_string

    @staticmethod
    def where(tree: list[str]) -> str:
        """
        build where clause of a sparql query string

        Args:
            tree: lark tree string

        Returns:
             str: where_string
        """
        where_string = ''.join(tree)
        return 'WHERE { ' + where_string + '}'

    @staticmethod
    def var(tree: list[Token]) -> str:
        """

        Args:
            tree: list of tokens

        Returns:
            token for a variable:
        """
        # print('### ', tree[0].type, tree[0].value)
        return f'{tree[0]}'

    def triple(self, tree: list[str]) -> str:
        """
        build a triple in a sparql query string

        Args:
            tree:

        Returns:

        """
        self.list_of_each_triple = []  # initialize the list of a triple
        return_str = ''.join(tree)
        # self.predicate_object_pair[tree[1]] = tree[2]
        return return_str + '. '

    def subject(self, tree: list[Token]) -> str:
        """
        build a subject of a triple in a sparql query string
        :param tree: list of Tokens
        :return:
        """
        # print('¥¥¥ ', tree)  # debug
        if tree[0].type == 'VAR':
            ret = f'<http://variable.org/{tree[0].value.replace("?", "").strip()}>'
            # ret = tree[0].value  # '<http://example.org/subj> '
        else:
            ret = tree[0].value  # '<http://example.org/subj> '  # tree[0].value
        self.list_of_each_triple = []  # initialize the list of a triple
        self.list_of_each_triple.append(ClassTerm().build(ret.strip()))  # subject of a triple
        return ret + ','  # ret is just for debug

    def predicate(self, tree: list[Token]) -> str:
        """
        build a predicate of a triple in a sparql query string
        :param tree:
        :return:
        """
        if tree[0].type == 'VAR':
            ret = tree[0].value  # TODO
        else:
            ret = tree[0].value
        # if tree[0].value == '<http://example.org/operation> ':
        #     MyTransformer.predicate_is_operation = True
        # else:
        #     MyTransformer.predicate_is_operation = False
        self.list_of_each_triple.append(ClassTerm().build(ret.strip()))  # predicate of a triple
        return ret+','

    def object(self, tree: list[Token]) -> str:
        """
        build an object part of a triple in a sparql query string
        :param tree:
        :return:
        """
        my_value = tree[0].value
        ret = my_value
        if tree[0].type == 'VAR':
            ret = f'<http://variable.org/{my_value.replace("?", "").strip()}>'  # ?ans -> <http://variable.org/ans>
        self.list_of_each_triple.append(ClassTerm().build(ret.strip()))  # element holds a triple as a list # remove unnecessary spaces
        self.list_of_rdf_triples.append(self.list_of_each_triple)  # append the triple to the list
        return ret  # return value is for debug


def convert_question(question: str) -> list[list[ClassTerm]]:
    """
    convert a sparql query string into a list of triples

    Args:
        question(str): sparql query string

    Returns:
        list[str]: a list of triples
    """
    parser = Lark(grammar, start='sparql')  # create a Lark parser with 'sparql' as a root
    my_tree = parser.parse(question)  # convert the input sparql query into a lark tree
    # print(my_tree)  # debug
    my_transformer2 = MyTransformer()  # create an instance of MyTransformer2
    my_transformer2.list_of_rdfs = []  # initialize the list of rdfs
    # trans =
    my_transformer2.transform(my_tree)  # transform a lark tree to a list of rdf triples
    # print(trans)  # debug
    # print(my_transformer2.list_of_rdfs)  # debug
    return my_transformer2.list_of_rdf_triples  # list[list[ClassTerm]]


if __name__ == '__main__':  # for a test purpose
    # my_query = 'SELECT ?ss WHERE { ?ss <http://example.org/operation> <http://example.org/add_number> . ' + \
    #            '?s <http://example.org/PP> ?o . }'
    # conv_query, var_dict, predicate_object_pair = convert_query(my_query)

    my_question = f""" SELECT ?ans WHERE {{ ?s <http://example.org/operation> <http://example.org/add_number> . 
                  ?s <http://example.org/variable_x> <http://example.org/three> . 
                  ?s <http://example.org/variable_y> <http://example.org/two> . 
                  ?s <http://example.org/variable_z> ?ans . 
                  }}"""
    list_of_rdf_triples = convert_question(my_question)
    print(list_of_rdf_triples)
