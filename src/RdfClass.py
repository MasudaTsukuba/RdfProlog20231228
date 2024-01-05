"""Classes for handling RDF info for Prolog
RdfClass.py
Classes supporting RdfProlog reasoning.
T. Masuda, 2023/10/30
"""

# import sys
import logging
import sys

import rdflib
from rdflib import Graph, URIRef, Variable  # , BNode
from lark import Lark, Transformer, Token  # , Tree


VAL = 'http://value.org/'
VAR = 'http://variable.org/'
SOME = 'http://some.org/'
OPERATION = 'http://value.org/operation'

def print_and_log(message: str):  # print to console and log file
    print(message)
    logging.debug(message)


# utility functions
def uri_ref(key_word: str, extension: bool = False, ref: bool = True) -> URIRef:
    """Convert a key word into an uri string or an URIRef object

    Args:
        key_word (str): input uri string
        extension (bool): enclose with < and >
        ref (bool): convert to URIRef object

    Returns:
        URIRef:

    """
    reference = f'{VAL}{key_word}'
    if extension:
        reference = f'<{reference}>'
    if ref:
        reference = URIRef(reference)  # get URIRef object
    return reference


def uri_ref_ext(key_word: str) -> URIRef:
    """Use uri_ref function

    Args:
        key_word:

    Returns:

    """
    return URIRef(f'<{VAL}{key_word}>')


class ClassClauses:
    """Class for handling clauses (a list of clauses)
    ClassClauses holds a list of clauses.
    Also, sed for the right sides of a rule.
    Since the clauses are stored in a list, they are sorted according to the priorities.

    Attributes:
        list_of_clauses (list[ClassClause]): List of clauses
        list_of_variables (list[]): Variables contained in the clauses
    """
    variable_modifier = 1000  # number for updating temporal variables

    def __init__(self):
        self.list_of_clauses: list[ClassClause] = []
        self.list_of_variables = []
        pass

    def build(self, graph, results):  # not used at the moment
        pass

    def split_clauses(self):
        """Split the clauses into the first clause and the rest of clauses.

        Returns:
             ClassClause: first clause
             ClassClauses: rest clauses
        """
        if len(self.list_of_clauses) > 0:
            rest_clauses = ClassClauses()  # create a new instance of ClassClauses
            rest_clauses.list_of_clauses = self.list_of_clauses[1:]  # copy the rest clauses
            return self.list_of_clauses[0], rest_clauses  # first and rest
        else:
            return None, None  # contains no clauses

    def combine(self, clauses: 'ClassClauses'):
        """Combine other clauses to the current clauses.

        Args:
            clauses (ClassClauses):

        Returns:
            ClassClauses: combined clauses
        """
        combined_clauses = ClassClauses()  # create a new instance of ClassClauses
        combined_clauses.list_of_clauses = self.list_of_clauses + clauses.list_of_clauses  # merge the clauses
        return combined_clauses  # return the new instance

    def apply_bindings(self, bindings: dict[str, str]):
        """Apply bindings to the current clauses and returns a new ClassClauses instance.

        Args:
            bindings (dict[str, str]): bindings of variables and values

        Returns:
             ClassClauses: clauses after applying the bindings
        """
        return_clauses = ClassClauses()  # create a new instance of ClassClauses
        return_clauses.list_of_clauses = [clause.apply_bindings(bindings) for clause in self.list_of_clauses]  # apply bindings to each clause
        return return_clauses

    def update_variables(self):
        """Modify the names of variables contained in the current clauses and returns a new instance of ClassClauses.
        Variables are modified such as _x -> _x1000.

        Args:

        Returns:
             ClassClauses: modified variables
        """
        clauses_updated = ClassClauses()  # create a new instance of ClassClauses to be returned
        for clause in self.list_of_clauses:
            clause_updated = clause.update_variables()  # update the variables in each clause
            clauses_updated.list_of_clauses.append(clause_updated)  # append to the new instance
        ClassClauses.variable_modifier += 1  # after modifying the variables, increment the modifier
        return clauses_updated  # return the new instance


class ClassClause:
    """Class for a clause.
    A clause is a list of triples that have the same subject.
    One of the triples indicates the operation such as add or next.

    Attributes:
        list_of_triple (list[ClassTriple]): a list of triples
        operation_name_uri (str): ex. http://value.org/add_number
        predicate_object_dict (dict[str, str]): subject is unnamed and common among triples
        set_of_variables_in_query (set[tuple[str, str]]): [(object_variable, predicate)]
        set_of_half_variables (set[tuple[str, str]]): SOME:x
        variables_of_interest (set[str]):
        id (int): id of this clause
    """
    def __init__(self):
        self.list_of_triple: list[ClassTriple] = []
        self.operation_name_uri: str = ''  # ex. http://value.org/add_number
        self.predicate_object_dict: dict[str, str] = {}  # subject is unnamed and common among triples
        self.set_of_variables_in_query: set[tuple[str, str]] = set()  # [(object_variable, predicate)]
        self.set_of_half_variables: set[tuple[str, str]] = set()  # SOME:x
        self.variables_of_interest: set[str] = set()
        self.id: int = 0  # id of this clause

    def from_triples(self, list_of_triple):
        """Create a ClassClause from a list of triples.

        Args:
            list_of_triple (list[ClassTriple]): list of triples that have the same subject.

        Returns:

        """
        self.list_of_triple: list[ClassTriple] = list_of_triple  # [s-p-o, s-p-o, ..., s-p-o]
        len_effective_rdfs = 0
        g_temp: Graph = Graph()  # temporary graph for storing the query
        g_temp_debug: list[tuple[URIRef, URIRef, URIRef]] = []  # debug for g_temp
        self.predicate_object_dict: dict[str, str] = {}  # subject is unnamed and common among triples
        self.set_of_variables_in_query: set[tuple[str, str]] = set()  # [(object_variable, predicate)]

        for triple in self.list_of_triple:
            subj = triple.subject  # ClassTerm for subject
            predicate = triple.predicate  # predicate
            object_ = triple.object  # object
            subject_uri = subj.to_uri(drop=True)  # http://variable.org/s
            predicate_uri = predicate.to_uri(drop=True)  # http://value.org/operation
            object_uri = object_.to_uri(drop=True)  # http://value.org/add_number
            g_temp.add((URIRef(subject_uri), URIRef(predicate_uri), URIRef(object_uri)))  # add to the temporary graph
            g_temp_debug.append((URIRef(subject_uri), URIRef(predicate_uri), URIRef(object_uri)))  # for debug
            self.predicate_object_dict[predicate_uri] = object_uri  # build predicate-object pairs
            len_effective_rdfs += 1
            if not object_.is_variable:  # .find(VAR) < 0:
                pass  # skip if the object is a variable
            else:  # object is a variable
                self.set_of_variables_in_query.add((object_uri, predicate_uri))  # add as a tuple of object-predicate pair
            if predicate_uri == OPERATION:  # then the object is operation name
                operation_name = object_uri.replace(VAL, '')  # extract operation name
                self.operation_name_uri = uri_ref(operation_name)  # keep it as URIRef

    def from_query(self, graph: Graph, subject: rdflib.term.URIRef, id_: rdflib.term.URIRef = URIRef('0')):
        """Create a ClassClause from a SPARQL query.

        Args:
            graph (Graph): RDF graph.
            subject (rdflib.term.URIRef): subject term common to triples.
            id_ (rdflib.term.URIRef): id of this clause.

        Returns:
            self (ClassClause): return the self (instance of ClassClause)

        """
        self.id = int(id_)
        query_for_clause = f"""
            SELECT ?p ?o WHERE {{ <{subject}> ?p ?o . }}
        """
        results_for_clause = graph.query(query_for_clause)  # find triples that have the specified subject.
        self.list_of_triple: list[ClassTriple] = []  # list of triples such as [s-p-o, s-p-o, ..., s-p-o]
        len_effective_rdfs = 0  # length of effective RDF triples
        self.predicate_object_dict: dict[str, str] = {}  # subject is unnamed and common among triples
        self.set_of_variables_in_query: set[tuple[str, str]] = set()  # [(object_variable, predicate)]

        subj: URIRef = subject  # subject is an instance of ClassTerm
        subject_uri: str = str(subj)  # convert to an uri string such as http://variable.org/s
        for binding in results_for_clause.bindings:  # extract predicate - object pair
            predicate = binding[Variable('?p')]  # predicate
            object_ = binding[Variable('?o')]  # object
            predicate_uri = str(predicate)  # http://value.org/operation
            object_uri = str(object_)  # http://value.org/add_number
            triple = ClassTriple()  # create an instance of ClassTriple
            triple.build_from_spo(subject_uri, predicate_uri, object_uri)  # set up the triple
            self.list_of_triple.append(triple)  # append to the list
            self.predicate_object_dict[predicate_uri] = object_uri  # build predicate - object pairs
            len_effective_rdfs += 1
            if object_uri.find(VAR) >= 0:  # object is a variable
                self.set_of_variables_in_query.add((object_uri, predicate_uri))  # add the variable
            if object_uri.find(SOME) >= 0:  # object is a semi-variable
                self.set_of_half_variables.add((object_uri, predicate_uri))  # add the variable
            if predicate_uri == OPERATION:  # operation name
                operation_name = object_uri.replace(VAL, '')  # extract operation name
                self.operation_name_uri = uri_ref(operation_name)  # keep as UriRef
        return self

    def search_facts(self, rdf_prolog):
        """Search facts that may match this ClassClause.

        Args:
            rdf_prolog: instance of RdfProlog class

        Returns:

        """

        def match_fact(candidate_):
            """Test whether the argument candidate fact matches the request.

            Args:
                candidate_:

            Returns:

            """
            success_: bool = True  # assume the success
            bindings_ = {}  # prepare the bindings
            for predicate, object_ in self.predicate_object_dict.items():
                try:
                    if object_.find(VAR) >= 0:  # object is a variable
                        bindings_[object_] = candidate_.fact.predicate_object_dict[predicate]  # correspondence against the object
                    else:
                        if candidate_.fact.predicate_object_dict[predicate] == object_:
                            pass  # same constants are OK
                        else:
                            success_ = False  # different constants cause failure
                            break
                except Exception as e:
                    success_ = False  # KeyError?
                    break
            return success_, bindings_

        def generate_cons():
            """Generate a cons element.

            Args:

            Returns:

            """
            success_ = True  # assume the success
            bindings_ = {}  # prepare bindings
            variable_x = self.predicate_object_dict[uri_ref('variable_x', ref=False)]  # cons must have x, y and z
            variable_y = self.predicate_object_dict[uri_ref('variable_y', ref=False)]
            variable_z = self.predicate_object_dict[uri_ref('variable_z', ref=False)]
            if variable_x.find(VAL) >= 0 and variable_y.find(VAL) >= 0 and variable_z.find(VAR) >= 0:
                cons_node = uri_ref(f'cons_node{str(ClassFacts.cons_number)}', ref=False)  # create cons_nodeNNNNN
                cons_list = uri_ref(f'cons_list{str(ClassFacts.cons_number)}', ref=False)  # create cons_listNNNNN
                ClassFacts.cons_number += 1  # update the serial number

                triple1 = ClassTriple()  # build a new triple for cons fact
                triple1.build_from_spo(cons_node, uri_ref('operation', ref=False), uri_ref('cons', ref=False))
                triple2 = ClassTriple()
                triple2.build_from_spo(cons_node, uri_ref('variable_x', ref=False), variable_x)
                triple3 = ClassTriple()
                triple3.build_from_spo(cons_node, uri_ref('variable_y', ref=False), variable_y)
                triple4 = ClassTriple()
                triple4.build_from_spo(cons_node, uri_ref('variable_z', ref=False), cons_list)
                fact = ClassFact()
                fact.build_from_triples([triple1, triple2, triple3, triple4])  # build a new fact
                rdf_prolog.facts.add_fact(fact)  # add to the facts set
                bindings_[variable_z] = cons_list  # cons result is cons_list
            else:  # x or y or both are not a constant
                success_ = False  # then cons creates nothing
            return success_, bindings_  # end of generate_cons

        operation_name_uri = self.operation_name_uri
        return_bindings = []  # prepare a list of bindings for return
        try:
            candidates = rdf_prolog.facts.fact_dict[operation_name_uri]  # get fact candidates
            for candidate in candidates:
                success, bindings = match_fact(candidate)  # test whether this candidate matches this clause
                if success:
                    return_bindings.append(bindings)  # add to the return_bindings
        except KeyError:  # no entry for this operation_name_uri
            pass
        if len(return_bindings) == 0 and operation_name_uri == uri_ref('cons'):  # no cons is registered
            success, bindings = generate_cons()  # try to generate cons
            if success:
                return_bindings = [bindings]  # this binding is the only element of return_bindings
        return return_bindings  # end and return of search_facts

    # def match_rule(self, rule):  # NOT USED at this moment,
    #     """Test whether the argument rule matches the request.
    #
    #     Args:
    #         rule (ClassRule):
    #
    #     Returns:
    #
    #     """
    #     matched = True  # first assume the success
    #     forward_bindings = {}  # clause has constant, rule has variable. query: add(2, ?ans, 3) -> ?x: 2, ?y: 3
    #     backward_bindings = {}  # clause has variable, rule has constant. rule_left: add(?x, 1, ?y) -> ?ans: 1
    #     for rule_predicate, rule_object in rule.rule_left.predicate_object_dict.items():
    #         rule_object_drop = rule_object.replace('<', '').replace('>', '')
    #         try:
    #             query_object = self.predicate_object_dict[str(rule_predicate)]
    #             if rule_object_drop.find('http://value.org') >= 0:  # rule side is a const
    #                 if query_object.find('http://value.org') >= 0:  # query side is a const
    #                     if rule_object_drop == query_object:  # then they must be the same
    #                         pass  # go through
    #                     else:
    #                         matched = False  # if different, the match fails
    #                         continue
    #                 else:  # object in the query is a variable
    #                     backward_bindings['?' + query_object.replace(VAR, '')] = f'<{rule_object_drop}>'
    #             else:  # rule object is a variable
    #                 forward_bindings[
    #                     rdflib.term.Variable(rule_object_drop.replace(VAR, ''))] = query_object
    #         except KeyError:  # rule_predicate is not in the predicate_object_dict
    #             matched = False
    #             continue
    #     return matched, rule.rule_right_clauses(), forward_bindings, backward_bindings

    def match_application(self, rdf_prolog, application):
        """Test whether the argument application matches with this clause.

        Args:
            rdf_prolog:
            application (ClassApplication):

        Returns:

        """
        def append_to_bindings(bindings, key_, value_):
            """Append a value to the list specified by key.

            Args:
                bindings (dict[str, list[str]]):
                key_ (str):
                value_ (str):

            Returns:
                dict[str, list[str]]: revised bindings

            """
            try:
                xxx = bindings[key_]  # search an entry
            except KeyError:  # no entry found
                bindings[key_] = []  # value of the dict is an empty list
            bindings[key_].append(value_)
            return bindings

        def apply_internal_bindings(forward_multiple: dict[str, list[str]], backward_multiple: dict[str, list[str]]):
            """Apply forward and backward bindings to this clause.

            Args:
                forward_multiple:
                backward_multiple:

            Returns:

            """
            def is_constant(term: str) -> bool:
                """Check whether term is a variable or not.

                Args:
                    term (str):

                Returns:
                    bool: True if constant

                """
                if term.find(VAL) >= 0:
                    return True  # constant
                return False  # variable, not constant

            success_: bool = True  # assume a success
            forward_binding_: dict[str, str] = {}  # forward bindings
            backward_binding_: dict[str, str] = {}  # backward bindings, query is variable and rule is constant
            for key_, values in forward_multiple.items():
                if len(values) == 1:   # this is the only element in the list
                    forward_binding_[key_] = values[0]  # just copy the first element
                elif len(values) > 1:
                    first_constant: str = ''  # start from empty string
                    for value_ in values:
                        if is_constant(value_):  # value is a constant
                            if first_constant == '':  # first_constant is not yet assigned
                                first_constant = value_  # set the constant value
                            else:
                                if first_constant == value_:  # same value
                                    pass
                                else:  # different constants are assigned to a variable
                                    success_ = False  # failure
                                    break  # skip the rest
                    first_element = first_constant
                    if first_constant == '':  # no constant value is found
                        for value_ in values:
                            if not is_constant(value_):
                                first_element = value_  # variable
                    for value_ in values:  # scan for the variables
                        if not is_constant(value_):  # the value is a variable
                            backward_binding_[value_] = first_element  # variable
                else:  # len(values)==0 => error
                    sys.exit(-1)  # stop the program

            if not success_:
                return success_, forward_binding_, backward_binding_  # no further processing

            first_constant = ''
            for key_, values in backward_multiple.items():  # process the backward bindings
                if len(values) == 1:  # this is the only element in the list
                    backward_binding_[key_] = values[0]  # just copy the first element
                elif len(values) > 1:
                    first_constant: str = ''  # start from empty string
                    for value_ in values:
                        if is_constant(value_):  # value is a constant
                            if first_constant == '':  # first_constant is not yet assigned
                                first_constant = value_  # set the constant value
                            else:
                                if first_constant == value_:  # same value
                                    pass
                                else:  # different constants are assigned to a variable
                                    success_ = False
                                    break
                    if first_constant == '':  # no constant value is found
                        break
                    for value_ in values:  # scan for the variables
                        if not is_constant(value_):  # the value is a variable
                            backward_binding_[value_] = first_constant
                else:  # len(values)==0 => error
                    sys.exit(-1)  # stop the program

            return success_, forward_binding_, backward_binding_  # end and return of apply_internal_bindings

        # try to match the pattern of an application
        pattern = application.pattern  # extract the pattern in the application
        matched = True  # first assume the success
        forward_binding_multiple = {}  # query is constant, rule is variable
        backward_binding_multiple = {}  # query is variable, rule is either constant or variable
        for key, value in self.predicate_object_dict.items():  # key: predicate, value: object
            if value.find(VAR) >= 0:  # object of this clause is a variable
                try:
                    pattern_value = pattern.predicate_object_dict[key]
                    if pattern_value.find(VAR) >= 0:  # application side is also a variable
                        # forward_binding[pattern_value] = value
                        forward_binding_multiple = append_to_bindings(forward_binding_multiple, pattern_value, value)  # 2023/12/12
                    elif pattern_value.find(SOME) >= 0:  # application side is a semi-variable
                        matched = False  # a semi-variable only matches with a constant
                        break
                    else:  # application side is a constant
                        # backward_binding[value] = pattern_value  # application side is a constant
                        backward_binding_multiple = append_to_bindings(backward_binding_multiple, value, pattern_value)  # 2023/12/12
                except KeyError:  # no entry for this key (=predicate)
                    matched = False  # match failed
                    break  # skip the rest of for loop
            else:  # object of this clause is a constant
                try:
                    pattern_value = pattern.predicate_object_dict[key]
                    if pattern_value.find(VAR) >= 0:  # application side is a variable
                        # forward_binding[pattern_value] = value
                        forward_binding_multiple = append_to_bindings(forward_binding_multiple, pattern_value, value)  # 2023/12/12
                    elif pattern_value.find(SOME) >= 0:  # application side is a semi-variable
                        # forward_binding[pattern_value] = value  # also create a binding
                        forward_binding_multiple = append_to_bindings(forward_binding_multiple, pattern_value, value)  # 2023/12/12
                    else:  # application side is a constant
                        if pattern_value == value:
                            pass  # if both sides are constants, they must be the same
                        else:
                            matched = False  # match failed
                            break  # skip the rest of for loop
                except KeyError:
                    matched = False  # match failed
                    break  # skip the rest of for loop

        # apply the bindings to the controls contained in the application
        list_of_clauses = []
        list_of_forward_bindings = []
        list_of_backward_bindings = []
        if matched:
            success, forward_binding, backward_binding = apply_internal_bindings(forward_binding_multiple, backward_binding_multiple)  # 2023/12/12
            if not success:
                matched = False  # match failed
                return matched, list_of_clauses, list_of_forward_bindings, list_of_backward_bindings

            matched = False  # assume a failure

            def try_controls(matched_):
                """Try controls in application.list_of_controls.

                Args:
                    matched_ (bool): Modify in this function and return the modified value.

                Returns:
                    bool: matched_

                """
                controls = application.list_of_controls  # names (uri) of controls
                for control_uri in controls:  # try each control
                    control: ClassControl = rdf_prolog.controls.operation_name_dict[control_uri]  # get the ClassControl instance from its name
                    left_side: ClassClause = control.rule.left_side.update_variables()  # update variable name ?x -> ?x1000, etc. before establishing bindings
                    restrictions = control.left_side
                    forward_binding_control_multiple: dict[str, list[str]] = {}
                    backward_binding_control_multiple: dict[str, list[str]] = {}
                    match_control = True  # assume a success
                    for key_, value_ in self.predicate_object_dict.items():
                        if value_.find(VAR) >= 0:  # object is a variable
                            try:
                                left_value = left_side.predicate_object_dict[key_]
                                if left_value.find(VAR) >= 0:  # control side is also a variable
                                    try:
                                        restriction = restrictions[key_]
                                        match_control = False  # semi-variable only matches a constant
                                        break  # match failed, no further matching in useless
                                    except KeyError:
                                        # forward_binding_control[left_value] = value
                                        forward_binding_control_multiple = append_to_bindings(forward_binding_control_multiple, left_value, value_)  # 2023/12/12
                                # elif left_value.find(SOME) >= 0:  # control side is a semi-variable
                                #     match_control = False  # semi-variable only matches a constant
                                #     break  # match failed, no further matching in useless
                                else:  # control side is a constant
                                    # backward_binding_control[value] = left_value
                                    backward_binding_control_multiple = append_to_bindings(backward_binding_control_multiple, value_, left_value)  # 2023/12/12
                            except KeyError:
                                match_control = False  # match failed
                                break  # no further matching is useless
                        else:  # value in key-value pair is a constant, therefore the argument in the control must be a variable, a semi-variable or the same constant value
                            try:
                                left_value = left_side.predicate_object_dict[key_]  # control side
                                if left_value.find(VAR) >= 0:  # is variable
                                    try:
                                        restriction = restrictions[key_]
                                        # forward_binding_control[left_value] = value
                                        forward_binding_control_multiple = append_to_bindings(forward_binding_control_multiple, left_value, value_)  # 2023/12/12
                                    except KeyError:
                                        # forward_binding_control[left_value] = value
                                        forward_binding_control_multiple = append_to_bindings(forward_binding_control_multiple, left_value, value_)  # 2023/12/12
                                # elif left_value.find(SOME) >= 0:  # semi-variable
                                #     # forward_binding_control[left_value] = value
                                #     forward_binding_control_multiple = append_to_bindings(forward_binding_control_multiple, left_value, value_)  # 2023/12/12
                                else:  # constant
                                    if left_value == value_:  # same value
                                        pass  # if the constant has the same value, match is OK.
                                    else:
                                        match_control = False  # match failed
                                        break  # no further matching is useless
                            except KeyError:
                                match_control = False  # match failed
                                break  # no further matching is useless
                    if match_control:  # the arguments of this control match with the values in the current clause
                        success_, forward_binding_control, backward_binding_control = apply_internal_bindings(forward_binding_control_multiple, backward_binding_control_multiple)
                        if success_:
                            matched_ = True  # return value
                            list_of_forward_bindings.append({**forward_binding, **forward_binding_control})
                            list_of_backward_bindings.append({**backward_binding, **backward_binding_control})
                            clauses = ClassClauses()
                            for index in control.right_sides:
                                right: ClassClause = control.rule.right_sides.list_of_clauses[index-1]
                                right_updated: ClassClause = right.update_variables()
                                clauses.list_of_clauses.append(right_updated)
                            list_of_clauses.append(clauses)
                            ClassClauses.variable_modifier += 1
                return matched_

            matched = try_controls(matched)  # try controls

            def try_functions(matched_: bool):
                """Try functions.

                Args:
                    matched_ (bool): Modified in this function and returned.

                Returns:
                    bool: matched_, result of matching

                """
                def exec_function(function_: ClassFunction, forward_binding_: dict[str, str]):
                    """Execute Python code for the function.

                    Args:
                        function_ (ClassFunction): an instance of ClassFunction to be executed.
                        forward_binding_ (dict[str, str]): argument bindings

                    Returns:
                        dict[str, str]: results bindings

                    """
                    code_to_execute: str = function_.code  # code contains teh Python code to be executed.
                    local_vars = {'bindings': forward_binding_, 'rdf_prolog': rdf_prolog}  # variable bindings
                    # for key1, value1 in forward_binding_.items():
                    #     key_modified = key1.replace(f'{SOME}_', '').replace(f'{VAR}_', '')  # -> x
                    #     value_modified = value1.replace(VAL, '').replace(VAR, '')
                    #     local_vars[key_modified] = value_modified  # arguments for exec
                    exec(code_to_execute, {}, local_vars)  # execution of Python code
                    # result_bindings_: dict[str, str] = local_vars.get('result', None)  # the results are contained in result variable as dict object
                    return_bindings: dict[str, str] = local_vars.get('results', None)  # the results are contained in result variable as dict object
                    # for key2, value2 in result_bindings_.items():  # convert back to uri representations
                    #     key_modified = f'{VAR}{key2}'
                    #     value_modified = f'{VAL}{str(value2)}'
                    #     return_bindings[key_modified] = value_modified
                    return return_bindings  # end and return of exec_function
                    pass

                functions = application.list_of_functions  # get a list of function name uri
                for function_uri in functions:  # try each function
                    function: ClassFunction = rdf_prolog.functions.operation_name_dict[URIRef(function_uri)]  # get the ClassFunction instance from uri name
                    left_side: ClassClause = function.rule.left_side  # .update_variables()  # ?x -> ?x1000, etc.
                    restrictions = function.left_side
                    forward_binding_function_multiple = {}
                    backward_binding_function_multiple = {}
                    match_function = True  # assume a success
                    for key_, value_ in self.predicate_object_dict.items():
                        if value_.find(VAR) >= 0:  # clause side is a variable
                            try:
                                left_value = left_side.predicate_object_dict[key_]  # get the corresponding value in function
                                if left_value.find(VAR) >= 0:  # function side is a variable
                                    try:
                                        restriction = restrictions[key_]
                                        match_function = False  # semi-variable only matches with a constant
                                        break  # match failed, no further matching in useless
                                    except KeyError:
                                        # forward_binding_function[left_value] = value
                                        forward_binding_function_multiple = append_to_bindings(forward_binding_function_multiple, left_value, value_)  # 2023/12/12
                                # elif left_value.find(SOME) >= 0:  # function side is a semi-variable
                                #     match_function = False  # semi-variable only matches with a constant
                                #     break  # match failed, no further matching in useless
                                else:  # function side is a constant
                                    # backward_binding_control[value] = left_value
                                    backward_binding_function_multiple = append_to_bindings(backward_binding_function_multiple, value_, left_value)  # 2023/12/12
                            except KeyError:
                                match_function = False# match failed
                                break  # no further matching in useless
                        else:  # value in key-value pair is a constant, therefore the argument in the control must be a variable, a semi-variable or the same constant value
                            try:
                                left_value = left_side.predicate_object_dict[key_]
                                if left_value.find(VAR) >= 0:  # function side is a variable
                                    try:
                                        restriction = restrictions[key_]
                                        # forward_binding_control[left_value] = value
                                        forward_binding_function_multiple = append_to_bindings(forward_binding_function_multiple, left_value, value_)  # 2023/12/12
                                    except KeyError:
                                        # forward_binding_control[left_value] = value
                                        forward_binding_function_multiple = append_to_bindings(forward_binding_function_multiple, left_value, value_)  # 2023/12/12
                                # elif left_value.find(SOME) >= 0:  # function side is a semi-variable
                                #     # forward_binding_control[left_value] = value
                                #     forward_binding_function_multiple = append_to_bindings(forward_binding_function_multiple, left_value, value_)  # 2023/12/12
                                else:    # function side is a constant
                                    if left_value == value_:
                                        pass  # if the constant has the same value, match is OK.
                                    else:
                                        match_function = False  # match failed
                                        break  # no further matching in useless
                            except KeyError:
                                match_function = False  # match failed
                                break  # no further matching in useless
                    if match_function:  # the arguments of this control match with the values in the current clause
                        success_, forward_binding_function, backward_binding_function = apply_internal_bindings(forward_binding_function_multiple, backward_binding_function_multiple)
                        if success_:
                            matched_ = True  # match result to be returned
                            # list_of_clauses.append(function.right_sides.update_variables())
                            result_bindings = exec_function(function, forward_binding_function)
                            list_of_forward_bindings.append({**forward_binding, **forward_binding_function, **result_bindings})
                            list_of_backward_bindings.append({**backward_binding, **backward_binding_function})
                return matched_  # end and return of try_functions

            matched = try_functions(matched)

        return matched, list_of_clauses, list_of_forward_bindings, list_of_backward_bindings  # end and return of match_application

    def apply_bindings(self, bindings: dict[str, str]):
        """Apply bindings to this clause.

        Args:
            bindings dict[str, str]: bindings to be applied.

        Returns:
            ClassClause: a clause after the application of the bindings.

        """
        clause_applied = ClassClause()  # create an instance of ClassClause to be returned
        clause_applied.list_of_triple = []  # clear the triples
        clause_applied.predicate_object_dict = {}  # clear the predicate_object_dict
        for triple in self.list_of_triple:  # apply to each triple
            triple_applied = triple.apply_bindings(bindings)  # apply the bindings to a triple
            clause_applied.list_of_triple.append(triple_applied)  # append to the new clause to be returned
            clause_applied.predicate_object_dict[triple_applied.predicate.to_uri(drop=True)] = triple_applied.object.to_uri(drop=True)
            if triple.predicate.to_uri(drop=True) == OPERATION:
                clause_applied.operation_name_uri = rdflib.term.URIRef(triple_applied.object.to_uri(drop=True))  # set the operation name
        return clause_applied

    def update_variables(self):
        """Update variables in this clause

        Args:

        Returns:
            ClassClause: ClassClause instance with updated variables

        """
        clause_updated = ClassClause()  # create a new instance of ClassClause to be returned
        list_of_triple = []
        for triple in self.list_of_triple:
            triple_updated = triple.update_variables()  # update each triple
            list_of_triple.append(triple_updated)
        clause_updated.from_triples(list_of_triple)
        return clause_updated  # return the new instance


class ClassFacts:
    """This class holds a set of facts extracted from the RDF graph.

    Attributes:
        facts (set[ClassFact]): a set of facts.
        fact_dict (dict[str, set[ClassFact]): a dict of facts.
    """
    cons_number = 10000  # serial number for cons_node and cons_list

    def __init__(self, graph):
        self.facts: set[ClassFact] = set()  # set of ClassFact
        self.fact_dict: dict[str, set[ClassFact]] = {}  # also store in a dict object

        # register facts
        query_for_facts = f"""
            SELECT ?subject WHERE {{ ?subject {uri_ref_ext('type')} {uri_ref_ext('fact')} . }}
            """
        results_for_facts = graph.query(query_for_facts)  # find subjects that are marked as 'fact'
        for binding in results_for_facts.bindings:
            subject = binding['subject']  # extract the subject
            fact = ClassFact()  # a new instance
            fact.build(graph, subject)  # create a fact instance from the subject
            self.add_fact(fact)  # add to the set

        # register inferences in a graph
        query_for_inferences = f"""
            SELECT ?subject WHERE {{ ?subject {uri_ref_ext('type')} {uri_ref_ext('inference')} . }}
            """
        results_for_inferences = graph.query(query_for_inferences)  # get inferences
        for binding in results_for_inferences.bindings:
            subject = binding['subject']
            inference = ClassFact()  # inference is treated as a Fact
            inference.build(graph, subject)
            self.add_fact(inference)
        pass

    def add_fact(self, fact):
        """Add and register a fact to facts set.

        Args:
            fact (ClassFact): a fact to be added to the set and to the fact_dict

        Returns:

        """
        self.facts.add(fact)  # register the new fact
        # operation_name = fact.operation_name_uri
        try:
            self.fact_dict[fact.operation_name_uri].add(fact)  # try to register the new fact into a dict
        except KeyError:  # a dict entry for this operation name does not exit
            self.fact_dict[fact.operation_name_uri] = set()  # create an entry for this operation name as an empty set
            self.fact_dict[fact.operation_name_uri].add(fact)  # and register the fact


class ClassFact:
    """A clause asserted as a fact in the RDF graph.

    Attributes:
        fact (ClassClause):
        operation_name_uri (str):
    """
    def __init__(self):
        self.fact = ClassClause()  # fact has ClassClause
        self.operation_name_uri = ''  # and operation name

    def build(self, graph: Graph, subject):
        """Build a fact from the subject term.

        Args:
            graph (Graph): RDF graph contains all the necessary info for the facts
            subject:

        Returns:
            None: just update the internal variables in the class instance.
        """
        self.fact = ClassClause()
        self.fact.from_query(graph, subject)
        self.operation_name_uri = self.fact.operation_name_uri

    def build_from_triples(self, list_of_triple: list['ClassTriple']):
        """Build an instance of ClassFact from a list of triples.

        Args:
            list_of_triple (list[ClassTriple]):

        Returns:

        """
        clause = ClassClause()
        clause.from_triples(list_of_triple)
        self.fact = clause
        self.operation_name_uri = clause.operation_name_uri


class ClassApplications:
    """Class for handling applications.

    Attributes:
        applications (list[ClassApplication]): a list of ClassApplication
        operation_names_dict (dict[]): summarize the applications with the operation name as a key
    """
    def __init__(self, graph: Graph):
        self.applications: list[ClassApplication] = []  # has a list of application
        self.operation_names_dict: dict[str, list[ClassApplication]] = {}  # Also store in a dict object
        query_for_applications = f"""
            SELECT ?application WHERE {{ 
            ?application {uri_ref_ext('type')} {uri_ref_ext('application')} . 
            OPTIONAL {{ ?application {uri_ref_ext('priority')} ?priority . }}
            }} ORDER BY ?priority
        """
        results_for_applications = graph.query(query_for_applications)
        for binding in results_for_applications.bindings:
            application: ClassApplication = ClassApplication(graph, URIRef(binding[Variable('application')]))  # create an instance of ClassApplication
            self.applications.append(application)  # append to the list
            operation_name = application.operation_name_uri  # get the operation name
            try:
                self.operation_names_dict[operation_name].append(application)
            except Exception as e:
                self.operation_names_dict[operation_name] = []
                self.operation_names_dict[operation_name].append(application)
        pass

    def build(self):
        pass  # not used at this moment


class ClassApplication:
    """Class for handling an application.

    Attributes:
        program (bool): True if this application is a program without back tracking.
        pattern (ClassClause): Acceptable query pattern
        operation_name_uri (str): Operation name such as VAL:add in uri form
        list_of_controls (list[ClassControl]): List of controls included in this application with priorities
    """
    def __init__(self, graph: Graph, subject: rdflib.term.URIRef):
        query_for_application = f"""
            SELECT ?program ?pattern WHERE {{ 
            <{subject}> {uri_ref_ext('pattern')} ?pattern . 
            OPTIONAL {{ <{subject}> {uri_ref_ext('program')} ?program . }}
            }}
        """
        results_for_application = graph.query(query_for_application)
        if len(results_for_application.bindings) > 0:
            self.program = str(results_for_application.bindings[0][Variable('program')]).find(f'{uri_ref("true")}') >= 0
            self.pattern = ClassClause()  # pattern is an instance ClassClause
            self.pattern.from_query(graph, URIRef(results_for_application.bindings[0][Variable('pattern')]))
        self.operation_name_uri = self.pattern.operation_name_uri

        query_for_application_use = f"""
            SELECT ?control WHERE {{ <{subject}> {uri_ref_ext('use')} ?use . 
            ?use {uri_ref_ext('control')} ?control .
            OPTIONAL {{ ?use {uri_ref_ext('priority')} ?priority . }} }} ORDER BY ?priority 
        """
        results_for_application_use = graph.query(query_for_application_use)  # search controls
        self.list_of_controls: list[str] = []
        for binding in results_for_application_use.bindings:
            control_uri: str = str(binding[Variable('control')])
            # control = ClassControl(graph, control_uri)
            self.list_of_controls.append(control_uri)

        query_for_application_use = f"""
                    SELECT ?function WHERE {{ <{subject}> {uri_ref_ext('use')} ?use . 
                    ?use {uri_ref_ext('function')} ?function .
                    OPTIONAL {{ ?use {uri_ref_ext('priority')} ?priority . }} }} ORDER BY ?priority 
                """
        results_for_application_use = graph.query(query_for_application_use)  # search functions
        self.list_of_functions: list[str] = []
        for binding in results_for_application_use.bindings:
            function_uri: str = str(binding[Variable('function')])  # get the function name uri
            # function = ClassFunction(graph, function_uri)
            # self.list_of_functions.append(function)
            self.list_of_functions.append(function_uri)  # register the function name
        pass


class ClassControls:
    """Class for handling controls.

    Attributes:
        list_of_controls (list[ClassControl]):
        operation_name_dict (dict[str, ClassControl]):
    """
    def __init__(self, rdf_prolog, graph: Graph):
        self.list_of_controls: list[ClassControl] = []  # controls has a list of ClassControl
        # self.operation_name_dict: dict[str, set[ClassControl]] = {}  # also has a dict object to store
        self.operation_name_dict: dict[str, ClassControl] = {}  # also has a dict object to store, operation name is unique to each control
        query_for_controls = f"""
            SELECT ?s ?rule_name WHERE {{
            ?s {uri_ref_ext('type')} {uri_ref_ext('control')} . 
            ?s {uri_ref_ext('rule')} ?rule_name . 
            OPTIONAL {{ ?s {uri_ref_ext('priority')} ?priority . }}
            }} ORDER BY ?priority
        """
        results_for_controls = graph.query(query_for_controls)
        for binding in results_for_controls.bindings:
            control: ClassControl = ClassControl(rdf_prolog, graph, URIRef(binding[Variable('s')]), URIRef(binding[Variable('rule_name')]))  # create an instance of ClassControl
            self.list_of_controls.append(control)  # register to the list
            operation_name: str = control.control_uri
            # try:
            #     self.operation_name_dict[operation_name].add(control)
            # except Exception as e:
            #     self.operation_name_dict[operation_name] = set()
            #     self.operation_name_dict[operation_name].add(control)
            self.operation_name_dict[operation_name] = control
        pass  # end of __init__ of ClassControls


class ClassControl:
    """Class for handling a control object.

    Attributes:
        control_uri (str): subject of this control
        rule (ClassRule): rule
        left_side (dict[str, str]): left side of a control, variable restriction, VAL:variable_x "some".
        right_sides (list[int]): list of ids of rule's right sides

    """
    def __init__(self, rdf_prolog, graph: Graph, subject: rdflib.term.URIRef, rule: rdflib.term.URIRef):
        self.control_uri: str = str(subject)
        self.rule = rdf_prolog.rules.dict_of_rules[str(rule)]
        self.left_side: dict[str, str] = {}
        query_for_control_left = f"""
        SELECT ?var ?restriction  WHERE {{ 
        <{subject}> {uri_ref_ext('left_side')} ?left_side . 
        ?left_side ?var ?restriction .
        }}
        """
        results_for_control_left = graph.query(query_for_control_left)  # get the left side of a control
        try:
            for binding in results_for_control_left.bindings:
                self.left_side[binding[Variable('var')]] = binding[Variable('restriction')]  # create the left side
            self.right_sides: list[int] = []  # create the right sides
            query_for_control_right: str = f"""
            SELECT ?id WHERE {{ 
            <{subject}> {uri_ref_ext('right_side')} ?right_side . 
            ?right_side {uri_ref_ext('id')} ?id . 
            ?right_side {uri_ref_ext('priority')} ?priority . 
            }} ORDER BY ?priority
            """
            results_for_control_right = graph.query(query_for_control_right)  # get the right side
            if len(results_for_control_right.bindings) == 1:
                pass
            for binding in results_for_control_right.bindings:
                # clause = ClassClause()  # create a new instance
                # right_side = clause.from_query(graph, binding['child'])
                self.right_sides.append(int(binding[Variable('id')]))  #.list_of_clauses.append(right_side)  # append to the right sides
        except KeyError:
            pass  # error
        except Exception as e:  # unknown and unexpected exception
            pass  # error
        pass  # end of __init__ of ClassControl


class ClassFunctions:
    """Class for handling functions.

    Attributes:
        functions (list[ClassFunction]):
        operation_name_dict (dict[str,ClassFunction]): dict for retrieving ClassFunction instance from its label.

    """
    def __init__(self, rdf_prolog, graph: Graph, rules_folder: str):
        """

        Args:
            graph (Graph): RDF graph containing info on functions.
            rules_folder (str): Path to the folder containing rules and function definitions.

        """
        self.functions: list[ClassFunction] = []
        self.operation_name_dict: dict[str, ClassFunction] = {}
        query_for_functions = f"""
             SELECT ?s ?rule_name WHERE {{
             ?s {uri_ref_ext('type')} {uri_ref_ext('function')} . 
             ?s {uri_ref_ext('rule')} ?rule_name . 
             OPTIONAL {{ ?s {uri_ref_ext('priority')} ?priority . }}
             }} ORDER BY ?priority
         """
        results_for_functions = graph.query(query_for_functions)  # execute query
        for binding in results_for_functions.bindings:
            function: ClassFunction = ClassFunction(rdf_prolog, graph, URIRef(binding[Variable('s')]), URIRef(binding[Variable('rule_name')]))
            self.functions.append(function)
            # operation_name_dict = function.left_side.operation_name_uri
            function_uri: str = function.function_uri
            # try:
            #     self.operation_name_dict[function_uri].append(function)
            # except Exception as e:
            #     self.operation_name_dict[function_uri] = []
            #     self.operation_name_dict[function_uri].append(function)
            self.operation_name_dict[function_uri] = function
        for function in self.functions:  # read the function codes
            function_name: str = function.rule.left_side.operation_name_uri
            function_name: str = f'function_{function_name.replace(VAL, "")}.py'
            with open(f'{rules_folder}/{function_name}', 'r') as function_file:
                code: str = function_file.read()
                function.code = code
        pass  # end of __init__ of ClassFUnctions
    pass  # end of ClassFunctions


class ClassFunction:
    """Class for handling a function object.

    Attributes:
        code (str): Python code string of function.
        function_uri (str): subject of this function.
        rule (ClassRule): rule for this function.
        left_side (dict[str, str]): left side of a control, variable restriction, VAL:variable_x "some".
        right_sides (list[int]): list of ids of rule's right sides

    """
    def __init__(self, rdf_prolog, graph, function_uri: rdflib.term.URIRef, rule_name: rdflib.term.URIRef):
        self.code: str = ''  # Python code string
        self.function_uri = function_uri
        self.rule = rdf_prolog.rules.dict_of_rules[str(rule_name)]  # set the rule for this function
        self.left_side = {}
        query_for_function_left: str = f"""
        SELECT ?var ?restriction  WHERE {{ 
        <{function_uri}> {uri_ref_ext('left_side')} ?left_side . 
        ?left_side ?var ?restriction . 
        }}
        """
        results_for_function_left = graph.query(query_for_function_left)  # get the left side of a function

        try:
            for binding in results_for_function_left.bindings:
                self.left_side[binding[Variable('var')]] = binding[Variable('restriction')]  # create the left side
            self.right_sides: list[int] = []  # create the right sides
            query_for_function_right: str = f"""
                        SELECT ?child ?id WHERE {{ 
                        <{function_uri}> {uri_ref_ext('right_side')} ?right_side . 
                        ?right_side {uri_ref_ext('id')} ?id . 
                        ?right_side {uri_ref_ext('priority')} ?priority . 
                        }} ORDER BY ?priority
                        """
            results_for_function_right = graph.query(query_for_function_right)  # get the right side
            for binding in results_for_function_right.bindings:
                self.right_sides.append(
                    int(binding[Variable('id')]))  # .list_of_clauses.append(right_side)  # append to the right sides
        except KeyError:
            pass  # error
        except Exception:
            pass  # error

        pass  # end of __init__


class ClassRules:  # list of rules
    """Class for handling rules.
    Holds a list of all rules.

    Attributes:
        list_of_rules (list[ClassRule]): List of rule instances.
        dict_of_rules (dict[str, ClassRule]):
        operation_name_dict (dict[str, set[ClassRule]]): dict of rule instances with the operation names as keys.
    """
    # graph = None

    def __init__(self, graph: Graph):
        """Initialize ClassRules class.

        Args:
            graph (Graph): RDF graph containing all the info on rules.
        """
        # ClassRules.graph = graph
        self.list_of_rules: list[ClassRule] = []
        # query_for_rules = SELECT ?s ?left WHERE {{ ' \
        #                   ?s <{uri_ref("left_side")}> ?left .
        #                   f'OPTIONAL {{ ?s <{uri_ref("priority")}> ?priority .}} }}' \
        #                   f'ORDER BY ?priority '  # query for extracting rules and their left side. Rules always have left_side. Use the priority values to order the rules.
        # results_for_rule_left = graph.query(query_for_rules)  # execute query and extract
        # for binding_for_left in results_for_rule_left.bindings:
        #     instance_rule = ClassRule()  # create a rule instance
        #     instance_rule.build(graph, binding_for_left['s'], binding_for_left['left'])  # s: rule id, o: rule pattern
        #     self.list_of_rules.append(instance_rule)  # append the rule to the list
        self.dict_of_rules: dict[str, ClassRule] = {}
        self.operation_name_dict: dict[str, set[ClassRule]] = {}  # dict of rules. operation name as a key
        query_for_rules = f"""
            SELECT ?rule_subject WHERE {{ ?rule_subject {uri_ref_ext('type')} {uri_ref_ext('rule')} }}
            """ # query for extracting rules and their left side. Rules always have left_side. Use the priority values to order the rules.
        results_for_rules = graph.query(query_for_rules)  # execute query and extract
        for binding in results_for_rules.bindings:
            rule_subject = URIRef(binding[Variable('rule_subject')])
            rule_instance: ClassRule = ClassRule(graph, rule_subject)  # create a rule instance
            self.list_of_rules.append(rule_instance)  # append the rule to the list
            self.dict_of_rules[str(rule_subject)] = rule_instance
            operation_name: str = rule_instance.left_side.operation_name_uri  # rule_left.operation_name_uri
            try:
                self.operation_name_dict[operation_name].add(rule_instance)
            except KeyError:
                self.operation_name_dict[operation_name] = set()
                self.operation_name_dict[operation_name].add(rule_instance)
        pass  # end of __init__ of ClassRules


class ClassRule:  # class for individual rule
    """Class for an individual rule.

    Attributes:
        rule_uri (str): subject of this rule.
        left_side (ClassClause): left side of a rule.
        right_sides (ClassClauses): right sides of a rule.
        # label (str): label of the rule
        # rule_left (ClassRuleLeft): left part of the rule
        # rule_right (list[ClassRuleRight]): right part of the class consisting of a list of ClassRuleRight
        # variables_dict (dict[str, str]): dict of the variables in the rule
    """
    # serial_number: int = 1000  # a variable to convert variables: x -> x1000

    def __init__(self, graph: Graph, subject: rdflib.term.URIRef):
        """Initialize ClassRule class.
        """
        self.rule_uri: str = str(subject)
        query_for_rule_left = f"""
        SELECT ?left_side  WHERE {{ <{subject}> {uri_ref_ext('left_side')} ?left_side . }}
        """
        results_for_rule_left = graph.query(query_for_rule_left)  # get the left side of a control
        try:
            subject_left = results_for_rule_left.bindings[0][Variable('left_side')]
            clause = ClassClause()  # create a new instance
            self.left_side = clause.from_query(graph, URIRef(subject_left))  # create the left side
            self.right_sides = ClassClauses()  # create the right sides
            query_for_rule_right = f"""
            SELECT ?child ?id WHERE {{ 
            <{subject}> {uri_ref_ext('right_side')} ?right_side . 
            ?right_side {uri_ref_ext('child')} ?child .
            ?right_side {uri_ref_ext('id')} ?id . }}
            ORDER BY ?id
            """
            results_for_rule_right = graph.query(query_for_rule_right)  # get the right side
            for binding in results_for_rule_right.bindings:
                clause = ClassClause()  # create a new instance
                right_side = clause.from_query(graph, URIRef(binding[Variable('child')]), URIRef(binding[Variable('id')]))
                self.right_sides.list_of_clauses.append(right_side)  # append to the right sides
        except KeyError:
            pass  # error
        except Exception:  # unknown and unexpected exception
            pass  # error

        # self.label: str = ''
        # self.rule_left: ClassRuleLeft = ClassRuleLeft(graph, subject)
        # self.rule_right: ClassRuleRight = ClassRuleRight()
        # self.variables_dict: dict[str, str] = {}
        # self.build(graph, subject)
        pass  # end of __init__ of ClassRule

    # def build(self, graph, rule_label):
    #     """Build a rule from rule label and rule left label.
    #
    #     Args:
    #         graph: RDF graph holding all info of rules
    #         rule_label: label of this rule
    #         # rule_left_label: label of the left part of the rule
    #
    #     Returns:
    #         ClassRule: return the self as a ClassRule
    #     """
    #     # print('DETECTED RULE: ', rule_label)  # left side rule returned as an object  # debug
    #     self.label = rule_label
    #     self.rule_left.build(graph, rule_left_label)  # build the left parts of the rule from the left label.
    #     self.rule_right = []
    #     # get the right parts of the rule while considering the priorities to apply the sub goal.
    #     query = f'SELECT ?o WHERE {{ <{self.label}> <{uri_ref("right_side")}> ?o . ' \
    #             f'?o <{uri_ref("priority")}> ?priority . }} ORDER BY (?priority) '
    #     results = graph.query(query)
    #     # print('NUMBER OF CHILD RULES: ' + str(len(results)))  # debug
    #     for result in results:
    #         right_clause = ClassClauses().build(graph, result)  # build the right side part of the rule
    #         self.rule_right.append(right_clause)  # save into a list
    #     return self

    # def modify_variables(self):  # x -> x1000, etc.
    #     """Modify a variable name by appending a unique serial number.
    #     x -> x1000, etc.
    #     This function is used to avoid confusion between classes that have variables with the same name.
    #
    #     Returns:
    #         None: This function just modifies the internal variables of a class instance.
    #     """
    #     self.variables_dict = {}  # The variables are held in this list.
    #     for var in self.rule_left.set_of_variables_in_query:
    #         self.variables_dict[var] = var + str(ClassRule.serial_number)  # x -> x1000
    #     for right_clause in self.rule_right:
    #         for grand_child in right_clause.child.grandchildren:
    #             triple = grand_child.triple
    #             if triple.subject.is_variable:  # subject
    #                 var = triple.subject.to_var_string()  # rdflib.term.Variable -> ?x
    #                 try:
    #                     value = self.variables_dict[var]  # already registered
    #                     triple.subject.build(value)
    #                 except KeyError:
    #                     self.variables_dict[var] = var + str(ClassRule.serial_number)  # convert free variable
    #                     triple.subject.build(self.variables_dict[var])
    #             if triple.object.is_variable:  # object
    #                 var = triple.object.to_var_string()
    #                 try:
    #                     value = self.variables_dict[var]  # already registered
    #                     triple.object.build(value)
    #                 except KeyError:
    #                     self.variables_dict[var] = var + str(ClassRule.serial_number)  # convert free variable
    #                     triple.object.build(self.variables_dict[var])
    #     ClassRule.serial_number += 1  # update the serial number to prepare for the next conversion
    #     pass

    # def rule_right_clauses(self):
    #     """
    #
    #     Returns:
    #
    #     """
    #     clauses = []
    #     for right_clause in self.rule_right:
    #         clause = ClassClause()
    #         clause.list_of_triple = [triple for triple in right_clause.child.grandchildren]
    #         clauses.append(clause)
    #     return clauses


class ClassRuleLeft(ClassClause):  # left side of a rule
    """Left side of a rule.

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
        Initialize ClassRuleLeft class.
        """
        super().__init__()
        self.list_of_triples: list[ClassTriple] = []
        self.operation_name_uri: str = ''  # ex. http://value.org/add_number
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

    def build(self, graph: Graph, rule_left_label):  # executed at the initial stage
        """Build the left side part of a rule from the label.
        Executed at the initial stage.

        Args:
            graph (Graph):
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
            triple_predicate = bindings_for_left_content[Variable('p')]  # predicate part of the left side of a rule
            triple_object0 = bindings_for_left_content[Variable('o')]  # object part of the left side of a rule
            triple_object = f'<{triple_object0}>'  # convert object to URI string
            self.predicate_object_dict[triple_predicate] = triple_object
            try:
                if triple_object.find(VAR) >= 0:
                    triple_object = triple_object.replace(f'<{VAR}', '?').replace('>', '')
                    var_list_string += str(triple_object) + ' '  # register the variable to a list
                    # self.var_list.append(str(triple_object))  # also append the variable to a list
                else:
                    self.const_dict[triple_predicate] = triple_object
            except KeyError:
                pass  # object is not a variable
            if triple_predicate.find(OPERATION) >= 0 or triple_object.find('?') >= 0:
                sparql_query += f""" ?s <{triple_predicate}> {triple_object} . """

        sparql_query += f'}}'  # close the sparql query
        sparql_query = sparql_query.replace('VAR_LIST', var_list_string)  # insert variables list
        self.label = str(rule_left_label)
        self.var_list = var_list_string.strip().split(' ')
        self.content = sparql_query
        self.bindings = results_for_left_content.bindings
        return self


# class ClassRuleRight:  # right side of a rule
#     """Right side of a rule.
#
#     Attributes:
#         child (ClassRuleRightChild): child of the right side clause.
#     """
#     def __init__(self):
#         """Initialize ClassRuleRight class.
#         """
#         super().__init__()
#         self.child = ClassRuleRightChild()  # right side clause has one child, which in turn has one or more grandchild
#
#     def build(self, graph: Graph, right_side_for_child):  # executed at the initial stage
#         """Build the right side clause of a rule.
#         Executed at the initial stage.
#
#         Args:
#             graph (Graph):
#             right_side_for_child:
#
#         Returns:
#
#         """
#         # print('CHILD RULE: ' + str(right_side_for_child[0]))  # debug
#         query_for_child = f"""SELECT ?o WHERE {{ <{str(right_side_for_child[0])}> <{uri_ref("child")}> ?o .}} """
#         results_of_right_side_child = graph.query(query_for_child)  # query by the child name
#
#         self.child.build(graph, results_of_right_side_child.bindings[0])  # build a child from the query results
#         return self
#
#     def revise(self, right_clauses, bindings):  # bindingsは辞書型
#         """
#
#         Args:
#             right_clauses:
#             bindings (dict[str, str]):
#
#         Returns:
#
#         """
#         for grandchild in right_clauses.child.grandchildren:
#             pass
#             # grandchild_revised = ClassRightGrandChild()  # create a new grandchild
#             # new_term = grandchild.triple.subject.revise(bindings)
#             # grandchild_revised.triple.subject.build(new_term)  # subject
#             # new_term = grandchild.triple.predicate.revise(bindings)
#             # grandchild_revised.triple.predicate.build(new_term)  # predicate
#             # new_term = grandchild.triple.object.revise(bindings)
#             # grandchild_revised.triple.object.build(new_term)  # object
#             # self.child.grandchildren.append(grandchild_revised)  # append the grandchild to the grandchildren
#         return self


# class ClassRuleRightChild:  # right side child of a rule
#     """
#     right side child of a rule
#
#     Attributes:
#         clause (ClassClause): triples contained in this right child
#
#     """
#     def __init__(self):  # child has grandchildren
#         """
#         child has a list of grandchildren
#         """
#         self.clause: ClassClause | None = None
#
#     def build(self, graph, result_for_clause):  # build the right side of a rule
#         """Build the right side of a rule
#
#         Args:
#             graph:
#             result_for_clause:
#
#         Returns:
#             self:
#         """
#         self.clause = None
#         query_for_clause = f'SELECT ?s ?p ?o WHERE ' \
#                                f'{{ <{result_for_clause["o"]}> ?p ?o . }}'  # find grandchildren of a rule
#         results_for_clause = graph.query(query_for_clause)  # execute the query
#         # get grand child rules from grand child name
#         # print('NUMBER OF GRAND CHILD RULES: ' + str(len(results_for_grandchild)))  # debug
#         for triple_for_grandchild in results_for_clause:
#             # print('PREDICATE AND OBJECT OF GRAND CHILD RULE WERE: '
#             #       + str(triple_for_grandchild['p']) + ' '
#             #       + str(triple_for_grandchild['o']))  # debug
#             triple = {'s': result_for_clause["o"], 'p': triple_for_grandchild['p'], 'o': triple_for_grandchild['o']}
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
    """Triple class.

    Attributes:
        subject (ClassTerm): subject of a triple
        predicate (ClassTerm): predicate of a triple
        object (ClassTerm): object of a triple
    """
    def __init__(self):  # triple has subject, predicate and object
        """Triple has subject, predicate and object.
        """
        self.subject = ClassTerm()  # create an empty terms
        self.predicate = ClassTerm()
        self.object = ClassTerm()

    def build(self, triple: dict[str, str]):  # triple is a dict
        """Build a triple.

        Args:
            triple (dict[str, str]):

        Returns:
            None
        """
        self.subject.build(triple['s'])  # build a subject
        self.predicate.build(triple['p'])  # build a predicate
        self.object.build(triple['o'])  # build an object

    def build_from_spo(self, subject, predicate, object_):
        """Build a triple from subject, predicate and object.

        Args:
            subject:
            predicate:
            object_:

        Returns:

        """
        self.subject.build(subject)  # build a subject
        self.predicate.build(predicate)  # build a predicate
        self.object.build(object_)  # build an object

    def apply_bindings(self, bindings: dict[str, str]):
        """Apply bindings to a triple

        Args:
            bindings (dict[str, str]):

        Returns:
            ClassTriple: an instance of ClassTriple

        """
        triple_applied = ClassTriple()  # create a new instance
        triple_applied.subject = self.subject.apply_bindings(bindings)  # build a subject
        triple_applied.predicate = self.predicate.apply_bindings(bindings)  # build a predicate
        triple_applied.object = self.object.apply_bindings(bindings)  # build an object
        return triple_applied

    def update_variables(self):
        """Update variables in this triple.
        ?_x -> ?_x1000, etc.

        Args:

        Returns:

        """
        triple_updated = ClassTriple()  # create a new instance
        triple_updated.subject = self.subject.update_variables()  # update a subject
        triple_updated.predicate = self.predicate.update_variables()  # update a predicate
        triple_updated.object = self.object.update_variables()  # update an object
        return triple_updated


class ClassTerm:  # term is either subject, predicate or object
    """Class for a term.
    Term is either subject, predicate or object.

    Attributes:
        term_text (str): string name of this term, such as 'ans'
        is_variable (bool): True if this term represents a variable
    """
    def __init__(self):  # initialize
        """Initialize ClassTerm instance.
        """
        self.term_text: str = ''  # Initially term_text is null
        self.is_variable: bool = False  # and assumed to be a constant

    def build(self, term_text: str):  # extract text element
        """Build a term from term text.
        <http://variable.org/x> -> x.

        Args:
            term_text (str):

        Returns:
            self:
        """
        self.term_text = str(term_text).replace(' ', '').replace('<', '').replace('>', '')
        self.is_variable = False
        if self.term_text.find(VAR) >= 0:  # <http://variable.org/x> -> x
            self.is_variable = True
            self.term_text = self.term_text.replace('<', '').replace('>', ''). \
                replace(VAR, '')  # .replace('variable_', '')
        if self.term_text.find(SOME) >= 0:  # <http://some.org/x> -> x
            self.is_variable = True
            self.term_text = self.term_text.replace('<', '').replace('>', ''). \
                replace(SOME, '')  # .replace('variable_', '')
        if self.term_text.find('?') >= 0:  # ?x -> x
            self.is_variable = True
            self.term_text = self.term_text.replace('?', '')
        return self

    def to_uriref(self) -> URIRef:  # NOT USED at this moment
        """Service function to produce URIRef from ClassTerm.
        'x' -> 'rdflib.term.URIRef('http://variable.org/x')

        Args:

        Returns:
             URIRef:
        """
        if self.is_variable:
            return URIRef(VAR + self.term_text)  # x -> http://variable.org/x
        else:
            return URIRef(self.term_text)

    def to_uri(self, drop=False) -> str:
        """Service function to produce URIRef from ClassTerm.
        x -> <http://variable.org/x> for a variable.
        http://value.org/andy -> <http://value.org/andy> for a constant.

        Args:
            drop (bool): if True, http://..., else <http://...>

        Returns:
            str: uri_string
        """
        if self.is_variable:
            term_str = VAR + self.term_text + ''  # x -> <http://variable.org/x>
        else:
            term_str = '' + self.term_text + ''  # http://value.org/andy -> <http://value.org/andy>
        if drop:  # drop < and >
            return term_str
        else:
            return f'<{term_str}>'

    def to_var_string(self, drop=False) -> str:
        """
        http://variable.org/x -> ?x for a variable.
        http://value.org/andy -> <http://value.org/andy> for a constant.

        Returns:
            str:
        """
        if self.is_variable:
            return '?' + self.term_text  # http://variable.org/x -> ?x
        else:
            return self.to_uri(drop=drop)  # http://value.org/andy -> <http://value.org/andy>

    def force_to_var(self) -> str:
        """Force conversion.
        http://value.org/x -> ?x

        Returns:
            str:
        """
        return '?' + self.term_text.replace(VAL, '')  # http://value.org/x -> ?x

    def revise(self, bindings: dict[str, str]):  # bindings: dict
        """Revise a term based on the bindings.

        Args:
            bindings (dict[str, str]):

        Returns:

        """
        term_text = self.to_var_string()  # if VAR x -> ?x, else http://value.org/andy -> <http://value.org/andy>
        try:
            if len(bindings) > 0:  # if bindings contain maps
                try:
                    term_text2 = bindings[term_text]
                    return term_text2  # return the value in the dict
                except KeyError:  # term_text is not registered in the bindings
                    pass
                except Exception as e:  # unexpected error
                    # print ('In ClassTerm/revise, unexpected error', e)
                    print_and_log(f'In ClassTerm/revise, unexpected error {e}')
                    pass
        except Exception as e:  # unexpected error
            # print ('In ClassTerm/revise, unexpected error', e)
            print_and_log(f'In ClassTerm/revise, unexpected error {e}')
            pass
        return term_text  # if not in bindings, return as is

    def apply_bindings(self, bindings: dict[str, str]):
        """Apply bindings to this ClassTerm.

        Args:
            bindings (dic[str, str]):

        Returns:
            ClassTerm: term after applied the bindings

        """
        term_applied = ClassTerm()  # create a new instance
        if self.is_variable:
            try:
                value: str = bindings[f'?{self.term_text}']  # get the bound value
                if value.startswith('?'):  # bound to a variable
                    term_applied.is_variable = True
                    term_applied.term_text = value.replace('?', '')  # remove '?' from variable name
                else:  # bound to a constant
                    term_applied.is_variable = False
                    term_applied.term_text = value  # value itself
            except Exception as e:  # no entry in bindings
                term_applied.is_variable = True
                term_applied.term_text = self.term_text  # copy the current variable name
            try:
                value: str = bindings[f'{VAR}{self.term_text}']  # uri variable
                if value.find(VAR) >= 0:  # bound to a variable
                    term_applied.is_variable = True
                    term_applied.term_text = value.replace(VAR, '')  # remove prefix
                else:  # bound to a constant
                    term_applied.is_variable = False
                    term_applied.term_text = value
            except Exception as e:  # no entry in the bindings
                term_applied.is_variable = True
                term_applied.term_text = self.term_text  # copy the current variable name
        else:  # the current term is a constant
            term_applied.is_variable = False
            term_applied.term_text = self.term_text  # copy the current variable name
        return term_applied  #return the created instance

    def update_variables(self):
        """Update variables in this term.
        x -> x1000

        Args:

        Returns:
            ClassTerm: updated term

        """
        term_updated = ClassTerm()  # create a new instance
        term_updated.is_variable = self.is_variable  # copy the is_variable property
        if self.is_variable:  # is a variable
            term_updated.term_text = self.term_text + str(ClassClauses.variable_modifier)  # append a modifier number
        else:  # is a constant
            term_updated.term_text = self.term_text
        return term_updated  # return the updated term


class ClassSparqlQuery:  # Sparql Query Class
    """Sparql query class.

    Attributes:
        query (str): sparql query string
        list_of_rdfs: rdfs is an array of clauses
        list_of_variables: list of variables
        # rule (ClassRule): empty rule
    """
    cons_number = 10000  # unique number for every cons object.

    def __init__(self):  # initialize the sparql query class instance
        """Initialize the sparql query class instance.
        """

        self.query: str = ''  # sparql query string
        self.list_of_rdfs: list[list[ClassTriple]] = []  # rdfs is an array of clauses
        self.list_of_variables: list[str] = []  # list of variables in this query
        # self.rule = ClassRule()  # empty rule

    def set(self, sparql_query: str) -> 'ClassSparqlQuery':  # convert from sparql query string to a sparql query class instance
        """Convert from SPARQL query string to a SPARQL query class instance.

        Args:
            sparql_query (str):

        Returns:
            ClassSparqlQuery:
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
        """Create a list of variables.

        Returns:
            None: Just modify the internal state.
        """
        variable_str = self.query.replace('SELECT ', '')  # extract a string between 'SELECT' and 'WHERE'
        variable_str = variable_str[:variable_str.find(' WHERE')]
        list_of_variables_temp = variable_str.split(' ')  # split the string and convert to a list
        self.list_of_variables = [ClassTerm().build(var) for var in list_of_variables_temp]  # create a list of variables
        pass  # end of build_variable_list

    # def build_query(self, results_for_build_query):  # build a query string  # NOT USED at this moment
    #     """Build a query string.
    #
    #     Args:
    #         results_for_build_query:
    #
    #     Returns:
    #
    #     """
    #     try:
    #         var_list = ''  # variables list for replacing $VAR_LIST
    #         query_for_resolve = f"""SELECT $VAR_LIST WHERE {{ """  # start the query string. $VAR_LIST will be replaced at the end.
    #         term_subject = None  # for suppressing the warning of not defined before assignment
    #         self.list_of_rdfs = []  # reset
    #         for triple_for_build_query in results_for_build_query.child.grandchildren:  # extract each triple of a rule
    #             term_subject = ClassTerm().build(triple_for_build_query.triple.subject.force_to_var())  # subject
    #             term_predicate = ClassTerm().build(triple_for_build_query.triple.predicate.to_uri())  # predicate
    #             term_object = ClassTerm().build(triple_for_build_query.triple.object.to_var_string())  # object
    #             # print ('PREDICATE AND OBJECT: ' + str(term_predicate.to_uri()) + ' ' + str(term_object.to_var_string()))  # debug
    #             print_and_log(f'PREDICATE AND OBJECT: {str(term_predicate.to_uri())} {str(term_object.to_var_string())}')  # debug
    #             # term_value1 = term_object
    #             if term_object.is_variable:  # object is a variable
    #                 # print ('OBJECT WAS A VARIABLE: ' + str(term_object.to_var_string()))  # debug
    #                 print_and_log(f'OBJECT WAS A VARIABLE: {str(term_object.to_var_string())}')  # debug
    #                 key1 = term_object.to_uri()  # convert the object to uri
    #                 try:
    #                     if key1.find(f'<{VAR}') >= 0:
    #                         key1 = key1.replace(f'<{VAR}', '?').replace('>', '')  # to ?var form
    #                         term_value1 = ClassTerm().build(key1)  # new object term
    #                         # print ('(1)OBJECT VARIABLE WAS CONVERTED TO: ' + str(term_value1.to_uri()))  # debug
    #                         print_and_log(f'(1)OBJECT VARIABLE WAS CONVERTED TO: {str(term_value1.to_uri())}')  # debug
    #                 except KeyError:
    #                     pass
    #             else:
    #                 pass
    #
    #             temp_obj = term_object
    #             # my_var = term_value1
    #
    #             if temp_obj.is_variable:
    #                 var_list += temp_obj.to_var_string() + ' '  # append to the variables list (string)
    #             ss = term_subject.to_var_string()
    #             pp = term_predicate.to_uri()
    #             oo = temp_obj.to_var_string()
    #             str1 = f'{ss} {pp} {oo} . '
    #             query_for_resolve += str1  # append the converted triple
    #             temp_triple = ClassTriple()
    #             temp_triple.subject = term_subject
    #             temp_triple.predicate = term_predicate
    #             temp_triple.object = term_object
    #             self.list_of_rdfs.append(temp_triple)
    #         query_for_resolve += f'}}'  # terminate the query string
    #
    #         if term_subject.is_variable:  # such as ?s
    #             var_list += term_subject.to_var_string()  # last element  # to enable yes/no question
    #         query_for_resolve = query_for_resolve.replace('$VAR_LIST', var_list)
    #         # print ('CONVERTED QUERY FOR THE GRAND CHILD: ' + query_for_resolve)  # sub goal
    #         print_and_log(f'CONVERTED QUERY FOR THE GRAND CHILD: {query_for_resolve}')  # sub goal
    #         self.query = query_for_resolve  # set the query string in instance variable
    #         self.build_variable_list()  # previous function. set self.list_of_variables.
    #     except Exception as e:
    #         # print ('Something has happened in ClassSparqlQuery.build_query(). ', e)
    #         print_and_log(f'Something has happened in ClassSparqlQuery.build_query(). {e}')
    #         pass

    # def direct_search(self):  # find a triple in the graph that directly matches the query
    #     """Find a triple in the graph that directly matches the query.
    #
    #     Args:
    #         # graph (Graph): an RDF graph holding all the info of facts and rules.
    #
    #     Returns:
    #         bool: True, if search is successful.
    #         list[]: a list of bindings.
    #
    #     """
    #
    #     results = ClassRules.graph.query(self.query)  # execute a query
    #     if len(results) > 0:  # direct search detected candidates. results.bindings are a list of dict
    #         def build_bindings(bindings_of_direct_search):
    #             print('BINDINGS OF DIRECT SEARCH: ', str(bindings_of_direct_search))  # debug
    #             print_and_log(f'BINDINGS OF DIRECT SEARCH: {str(bindings_of_direct_search)}')  # debug
    #             success = False  # assume a failure
    #             direct_search_bindings = []  # initialize the returned value
    #             for binding_of_direct_search in bindings_of_direct_search:  # extract an element in the list
    #                 success_for_each = True  # assume a success
    #                 return_bindings_temp = {}  # temporary bindings to be returned
    #                 for key in binding_of_direct_search:  # get a key in dict
    #                     key_string = str(key)  # get a key string
    #                     if isinstance(key, rdflib.term.Variable):  # in the case of a variable
    #                         key_string = '?' + key_string.replace('?', '')  # the key was a variable
    #                     my_value = str(binding_of_direct_search[key])  # get a value
    #                     if my_value.find('?') < 0:  # in the case the value is not a variable
    #                         my_value = '<' + my_value.replace('<', '').replace('>', '') + '>'  # convert to uri
    #                         # not a variable, change to uri
    #                         if my_value.find(VAR) >= 0:  # value is a variable, not a true uri
    #                             success_for_each = False  # failed
    #                             break  # exit the for loop
    #                     return_bindings_temp[key_string] = my_value  # store in a dictionary
    #                 if success_for_each:
    #                     return_bindings = {}  # bindings to be returned
    #                     for key, value in return_bindings_temp.items():
    #                         return_bindings[key] = value  # copy the dict
    #                     direct_search_bindings.append(return_bindings)  # add to the list
    #                     success = True  # at least one element is succeeded
    #             return success, direct_search_bindings
    #
    #         succeeded, bindings = build_bindings(results.bindings)  # create bindings to be returned
    #         return succeeded, bindings
    #     else:  # len(results) == 0
    #         found_cons = True  # try creating cons node  # 2023/11/10
    #         var_x = None
    #         var_y = None
    #         var_z = None
    #         for rdf in self.list_of_rdfs:
    #             if rdf.predicate.term_text == OPERATION:
    #                 if rdf.object.term_text != f'{VAL}cons':
    #                     found_cons = False
    #                     break
    #             if rdf.predicate.term_text == f'{VAL}variable_x':
    #                 if rdf.object.is_variable:
    #                     found_cons = False
    #                     break
    #                 else:
    #                     var_x = rdf.object.to_uriref()
    #             if rdf.predicate.term_text == f'{VAL}variable_y':
    #                 if rdf.object.is_variable:
    #                     found_cons = False
    #                     break
    #                 else:
    #                     var_y = rdf.object.to_uriref()
    #             if rdf.predicate.term_text == f'{VAL}variable_z':
    #                 if not rdf.object.is_variable:
    #                     found_cons = False
    #                     break
    #                 else:
    #                     var_z = rdf.object.to_var_string()
    #         if found_cons:
    #
    #             cons_node = URIRef(f'{VAL}cons_node{ClassSparqlQuery.cons_number}')
    #             cons_list = URIRef(f'{VAL}cons_list{ClassSparqlQuery.cons_number}')
    #             ClassSparqlQuery.cons_number += 1  # update the unique number for cons
    #
    #             ClassRules.graph.add((cons_node, URIRef(OPERATION), URIRef('{VAL}cons')))
    #             ClassRules.graph.add((cons_node, URIRef('{VAL}variable_x'), var_x))
    #             ClassRules.graph.add((cons_node, URIRef('{VAL}variable_y'), var_y))
    #             ClassRules.graph.add((cons_node, URIRef('{VAL}variable_z'), cons_list))
    #             return True, [{var_z: f'<{str(cons_list)}>'}]
    #
    #         return False, []  # no direct match was found. return False (Not Found) and an empty list

    # def find_applicable_rules(self, rules):  # find rules applicable to this query
    #     """Find rules applicable to this query.
    #
    #     Args:
    #         rules (ClassRules): a class holding info of rules.
    #
    #     Returns:
    #
    #     """
    #     list_of_rdfs: list[list[ClassTerm]] = convert_question(self.query)  # convert query to a list of triples
    #     len_effective_rdfs = 0
    #     g_temp: Graph = Graph()  # temporary graph for storing the query
    #     g_temp_debug: list[tuple[URIRef, URIRef, URIRef]] = []
    #     predicate_object_dict: dict[str, str] = {}
    #     set_of_variables_in_query: set[tuple[str, str]] = set()
    #     operation_name_uri: str = ''
    #
    #     for clause in list_of_rdfs:  # repeat for the triples
    #         if len(clause) == 3:  # clause is indeed a triple
    #             subj = clause[0]  # .to_uri(drop=True)  # clause[0].replace('<', '').replace('>', '')
    #             predicate = clause[1]  # .to_uri(drop=True)  # clause[1].replace('<', '').replace('>', '')
    #             object_ = clause[2]  # .to_uri(drop=True)  # clause[2].replace('<', '').replace('>', '')
    #             subj_uri = subj.to_uri(drop=True)
    #             predicate_uri = predicate.to_uri(drop=True)
    #             object_uri = object_.to_uri(drop=True)
    #             g_temp.add((URIRef(subj_uri), URIRef(predicate_uri), URIRef(object_uri)))
    #             g_temp_debug.append((URIRef(subj_uri), URIRef(predicate_uri), URIRef(object_uri)))
    #             predicate_object_dict[predicate_uri] = object_uri
    #             len_effective_rdfs += 1
    #             if not object_.is_variable:  # .find(VAR) < 0:  # skip if the object is a variable
    #                 # g_temp.add((URIRef(subj), URIRef(predicate), URIRef(object_)))
    #                 # g_temp_debug.append((URIRef(subj), URIRef(predicate), URIRef(object_)))
    #                 # len_effective_rdfs += 1
    #                 pass
    #             else:
    #                 set_of_variables_in_query.add((object_uri, predicate_uri))
    #             # g_temp.add((URIRef(clause[0].replace('<', '').replace('>', '')),
    #             #             URIRef(clause[1].replace('<', '').replace('>', '')),
    #             #             URIRef(clause[2].replace('<', '').replace('>', ''))))  # store the triple into the graph
    #             if predicate_uri == OPERATION:
    #                 operation_name = object_uri.replace(VAL, '')
    #                 operation_name_uri = uri_ref(operation_name)
    #
    #     # list_of_applicable_rules = []  # start building a list of applicable rules
    #     # for rule in rules.list_of_rules:  # rules.list_of_rules contains all the rules
    #     #     # results_for_left = g_temp.query(rule.rule_left.content)  # query against the temporary graph
    #     #     match = True
    #     #     forward_bindings = {}
    #     #     backward_bindings = {}
    #     #     for rule_predicate, rule_object0 in rule.rule_left.predicate_object_dict.items():
    #     #         rule_object = rule_object0.replace('<', '').replace('>', '')
    #     #         try:
    #     #             query_object = predicate_object_dict[str(rule_predicate)]
    #     #             if rule_object.find(VAL) >= 0:  # const
    #     #                 if query_object.find(VAL) >= 0:  # const
    #     #                     if rule_object == query_object:
    #     #                         pass
    #     #                     else:
    #     #                         match = False
    #     #                         continue
    #     #                 else:  # object in query is variable
    #     #                     backward_bindings['?'+query_object.replace(VAR, '')] = f'<{rule_object}>'
    #     #             else:  # rule object is variable
    #     #                 forward_bindings[rdflib.term.Variable(rule_object.replace(VAR, ''))] = query_object
    #     #         except KeyError:
    #     #             match = False
    #     #             continue
    #     #
    #     #     # if len(results_for_left) > 0:  # applicable rule exists
    #     #     #     # if len(results_for_left.bindings[0]) == len_effective_rdfs:
    #     #     #     forward_bindings = results_for_left.bindings[0]
    #     #     #     backward_bindings = {}
    #     #     #     dict_of_rule_left = {}
    #     #     #     for variable in set_of_variables_in_query:
    #     #     #         predicate = variable[1]
    #     #     #         object_in_rule_left = rule.rule_left.predicate_object_dict[URIRef(predicate)]
    #     #     #         backward_bindings['?'+variable[0]] = object_in_rule_left
    #     #     if match:
    #     #         rule.rule_left.forward_bindings = forward_bindings
    #     #         rule.rule_left.backward_bindings = backward_bindings
    #     #         list_of_applicable_rules.append(rule)  # append the found rule
    #     #         print('LIST OF APPLICABLE RULES: ', str(rule.label))  # print the rule on the console
    #
    #     # THe code below causes error in pytest. The reason is unknown. 2023/11/7.
    #     list_of_applicable_rules2 = []  # start building a list of applicable rules
    #     try:
    #         set_of_rules = rules.dict_of_rules[operation_name_uri]
    #         for rule in list(set_of_rules):  # rules.list_of_rules contains all the rules
    #             # results_for_left = g_temp.query(rule.rule_left.content)  # query against the temporary graph
    #             match = True
    #             forward_bindings = {}
    #             backward_bindings = {}
    #             for rule_predicate, rule_object0 in rule.rule_left.predicate_object_dict.items():
    #                 rule_object = rule_object0.replace('<', '').replace('>', '')
    #                 try:
    #                     query_object = predicate_object_dict[str(rule_predicate)]
    #                     if rule_object.find(VAL) >= 0:  # const
    #                         if query_object.find(VAL) >= 0:  # const
    #                             if rule_object == query_object:
    #                                 pass
    #                             else:
    #                                 match = False
    #                                 continue
    #                         else:  # object in query is variable
    #                             backward_bindings['?'+query_object.replace(VAR, '')] = f'<{rule_object}>'
    #                     else:  # rule object is variable
    #                         forward_bindings[rdflib.term.Variable(rule_object.replace(VAR, ''))] = query_object
    #                 except KeyError:
    #                     match = False
    #                     continue
    #             if match:
    #                 rule.rule_left.forward_bindings = forward_bindings
    #                 rule.rule_left.backward_bindings = backward_bindings
    #                 list_of_applicable_rules2.append(rule)  # append the found rule
    #                 print('LIST OF APPLICABLE RULES: ', str(rule.label))  # print the rule on the console
    #                 print_and_log(f'LIST OF APPLICABLE RULES: {str(rule.label)}')  # print the rule on the console
    #                 if str(rule.label).find('list_number_add_x_y_z') >= 0:  # debug
    #                     pass  # debug
    #     except KeyError:
    #         pass  # operation_name not found in dict_of_rules
    #     # if len(list_of_applicable_rules) != len(list_of_applicable_rules2):
    #     #     print(list_of_applicable_rules, list_of_applicable_rules2)
    #     #     pass  # debug
    #     #     sys.exit(-1)
    #     # else:
    #     #     for rule1, rule2 in zip(list_of_applicable_rules, list_of_applicable_rules2):
    #     #         if rule1.label != rule2.label:
    #     #             print(rule1.label, rule2.label)
    #     #             pass  # debug
    #     #             sys.exit(-2)
    #     return list_of_applicable_rules2  # return the applicable rules

    def build_rule(self):  # build the right side of a rule
        """Build the right side of a rule.

        Args:

        Returns:

        """
        for list_of_triples in self.list_of_rdfs:
            # rule_right = ClassClauses()  # create right side of a rule
            for triple in list_of_triples:
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
        """Convert sparql query to clauses

        Args:

        Returns:
            ClassClauses: clauses that contain triple in the sparql query

        """
        clauses = ClassClauses()  # create a new instance
        clauses.list_of_variables = self.list_of_variables  # list of ClassTerm
        clauses.list_of_clauses = []  # clear list of clauses
        for list_of_triples in self.list_of_rdfs:  # convert rdfs to clauses
            clause = ClassClause()
            clause.from_triples(list_of_triples)
            clauses.list_of_clauses.append(clause)
        return clauses  # return the created ClassClauses

    def from_clauses(self, clauses):
        """Convert clauses to a sparql query

        Args:
            clauses (ClassClauses):

        Returns:

        """
        self.list_of_variables = clauses.list_of_variables  # copy the list of variables
        self.list_of_rdfs = []  # clear the list of rdfs
        for clause in clauses.list_of_clauses:  # for each clause in clauses
            list_of_triples = clause.list_of_triple  # extract list of triples
            self.list_of_rdfs.append(list_of_triples)  # store in list of rdfs
        return self


"""
ConvertQuery.py
T. Masuda, 2023/10/30

convert a sparql query into a list of rdf triples

For example, if the input sparql query is
SELECT ?ans WHERE {
?s <http://value.org/operation> <http://value.org/add_number> .
?s <http://value.org/variable_x> <http://value.org/three> .
?s <http://value.org/variable_y> <http://value.org/two> .
?s <http://value.org/variable_z> ?ans . }'

The return list is
[['<http://variable.org/s>', '<http://value.org/operation>', '<http://value.org/add_number>'],
['<http://variable.org/s>', '<http://value.org/variable_x>', '<http://value.org/three>'],
['<http://variable.org/s>', '<http://value.org/variable_y>', '<http://value.org/two>'],
['<http://variable.org/s>', '<http://value.org/variable_z>', '<http://variable.org/ans>']]

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

        Args:

        Returns:

        """
        super().__init__()
        self.list_of_rdf_triples = []  # This is what we actually want to get.
        self.list_of_each_triple = []  # working variable.
        # self.predicate_object_pair = {}

    @staticmethod
    def sparql(tree: list[str]) -> str:
        """Build a sparql query string.

        Args:
             tree (list[str]): a list of lark tree strings.

        Returns:
             sparql query string (str)
        """
        sparql_string = 'SELECT '
        sparql_string += ''.join(tree)
        return sparql_string

    @staticmethod
    def where(tree: list[str]) -> str:
        """Build the WHERE clause of a sparql query string.

        Args:
            tree (list[str]): lark tree string

        Returns:
             str: where_string
        """
        where_string = ''.join(tree)
        return 'WHERE { ' + where_string + '}'

    @staticmethod
    def var(tree: list[Token]) -> str:
        """

        Args:
            tree (list[Token]): list of tokens

        Returns:
            str: token for a variable:
        """
        # print('### ', tree[0].type, tree[0].value)
        return f'{tree[0]}'

    def triple(self, tree: list[str]) -> str:
        """Build a triple in a sparql query string.

        Args:
            tree (list[str]):

        Returns:
            str:
        """
        self.list_of_each_triple = []  # initialize the list of a triple
        return_str = ''.join(tree)
        # self.predicate_object_pair[tree[1]] = tree[2]
        return return_str + '. '

    def subject(self, tree: list[Token]) -> str:
        """Build a subject of a triple in a sparql query string.

        Args:
            tree (list[Token]): list of Tokens

        Returns:
            str:
        """
        # print('¥¥¥ ', tree)  # debug
        if tree[0].type == 'VAR':
            ret = f'<{VAR}{tree[0].value.replace("?", "").strip()}>'
            # ret = tree[0].value  # '<{VAL}subj> '
        else:
            ret = tree[0].value  # '<http://value.org/subj> '  # tree[0].value
        self.list_of_each_triple = []  # initialize the list of a triple
        self.list_of_each_triple.append(ClassTerm().build(ret.strip()))  # subject of a triple
        return ret + ','  # ret is just for debug

    def predicate(self, tree: list[Token]) -> str:
        """Build a predicate of a triple in a sparql query string.

        Args:
            tree (list[Token]):

        Returns:
            str:
        """
        if tree[0].type == 'VAR':
            ret = tree[0].value  # TODO
        else:
            ret = tree[0].value
        # if tree[0].value == '<{OPERATION}> ':
        #     MyTransformer.predicate_is_operation = True
        # else:
        #     MyTransformer.predicate_is_operation = False
        self.list_of_each_triple.append(ClassTerm().build(ret.strip()))  # predicate of a triple
        return ret+','

    def object(self, tree: list[Token]) -> str:
        """Build an object part of a triple in a sparql query string.

        Args:
            tree (list[Token]):

        Returns:

        """
        my_value = tree[0].value
        ret = my_value
        if tree[0].type == 'VAR':
            ret = f'<{VAR}{my_value.replace("?", "").strip()}>'  # ?ans -> <http://variable.org/ans>
        self.list_of_each_triple.append(ClassTerm().build(ret.strip()))  # element holds a triple as a list # remove unnecessary spaces
        self.list_of_rdf_triples.append(self.list_of_each_triple)  # append the triple to the list
        return ret  # return value is for debug


def convert_question(question: str) -> list[list[ClassTerm]]:
    """Convert a sparql query string into a list of triples.

    Args:
        question(str): SPARQL query string

    Returns:
        list[list[ClassTerm]]: a list of triples
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


if __name__ == '__main__':  # This main() is for a test purpose.
    # my_query = 'SELECT ?ss WHERE { ?ss <{OPERATION}> <{VAL}add_number> . ' + \
    #            '?s <{VAL}PP> ?o . }'
    # conv_query, var_dict, predicate_object_pair = convert_query(my_query)

    my_question = f""" SELECT ?ans WHERE {{ ?s <{OPERATION}> <{VAL}add_number> . 
                  ?s <{VAL}variable_x> <{VAL}three> . 
                  ?s <{VAL}variable_y> <{VAL}two> . 
                  ?s <{VAL}variable_z> ?ans . 
                  }}"""
    list_of_rdf_triples = convert_question(my_question)
    print_and_log(str(list_of_rdf_triples))
