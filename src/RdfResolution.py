"""Module for reasoning
RdfResolution.py
Execute Prolog on RDF query system
2022/12/20, 2023/3/16, 2023/10/30, 2023/11/6, 2023/11/28
T. Masuda
"""

import os
from rdflib import BNode  # , Graph, URIRef, Variable
from itertools import permutations  # 2023/12/28
from src.RdfClass import *


# ClassClauses, ClassClause, ClassRule, ClassRules, ClassRuleRight, ClassSparqlQuery, ClassTerm


def start_log():
    # set up the log file
    log_file_path = '../logs/debug.log'
    if os.path.exists(log_file_path):
        os.remove(log_file_path)  # remove the existing og file
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug('Starting debug log')


class RdfProlog:  # Prolog Class, prepare a graph and available rules
    """Prolog Class
    Prepare a graph and available rules, and also execute a query.

    Attributes:
        # find_all (bool): stop the search if the first result is obtained.
        facts (ClassFacts): facts
        rules (ClassRules): set the rules in ClassRules class
        controls (ClassControls): controls
        functions (ClassFunctions): functions
        applications (ClassApplications): applications

    """

    def __init__(self, rules_folder: str ='../rules/rules_human'):
        """Initialize the RdfProlog class.
        Create a graph g_rules for storing facts and rules.
        Prepare applicable rules from the left sides of the rules.

        Args:
            rules_folder (str): Folder where the RDFs describing rules exist.

        Returns:
            None
        """
        # print('$$$$$$$$$$ PREPARING $$$$$$$$$$')  # debug
        print_and_log('$$$$$$$$$$ PREPARATION STARTED $$$$$$$$$$')  # debug
        # self.find_all: bool = False  # stop the search if the first result is obtained.  # NOT USED anymore.
        # self.find_all = True  # find all the results using inferences.  # NOT USED anymore.

        graph: Graph = Graph()  # graph for facts and rules
        g_temp: Graph = Graph()  # temporary graph for reading RDF files
        # self.rules_folder: str = rules_folder  # folder where the RDFs describing rules exist.
        # NO NEED to store as an instance variable.
        files: list[str] = os.listdir(rules_folder)  # get all the files in the folder.
        for file in files:  # read all the turtle files in rules folder
            if file.endswith('.ttl'):
                g_temp.parse(f'{rules_folder}/{file}')  # read into a graph object

        results = g_temp.query('SELECT ?s ?p ?o WHERE { ?s ?p ?o . }')  # retrieve all the triples read in
        for result in results:
            ss = result['s']  # subject
            pp = result['p']  # predicate
            oo = result['o']  # object
            if isinstance(ss, BNode):  # convert blank node to URI
                ss = f'{VAL}{str(ss)}'
            if isinstance(oo, BNode):  # also, for the object
                oo = f'{VAL}{str(oo)}'
            graph.add((URIRef(ss), URIRef(pp), URIRef(oo)))  # finally store in an RDF graph.
        self.facts: ClassFacts = ClassFacts(graph)  # facts
        self.rules: ClassRules = ClassRules(graph)  # set the rules in ClassRules class
        self.controls: ClassControls = ClassControls(self, graph)  # controls
        self.functions: ClassFunctions = ClassFunctions(self, graph, rules_folder)  # functions
        self.applications: ClassApplications = ClassApplications(graph)  # applications
        # print('$$$$$$$$$$ PREPARATION COMPLETED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')  # debug
        print_and_log('$$$$$$$$$$ PREPARATION COMPLETED $$$$$$$$')  # debug
        # print()  # line feed
        print_and_log('')  # line feed

    def answer_question(self, sparql_query, results_limit: int = 1, depth_limit: int = 30):
        """Answer a SPARQL query with multiple clauses.

        Args:
            sparql_query (ClassSparqlQuery): an instance of ClassSparqlQuery
            # find_all (bool): if true, find all the possible answers.
            results_limit (int): maximum number of bindings in results.
            depth_limit (int): maximum depth of resolution.

        Returns:
            list[dict[str, str]]: list of bindings
        """
        # self.find_all = find_all  # if true, find all the possible answers
        # resolution = Resolution(self.rules, self.find_all, depth_limit)
        # create an instance of Resolution class, left_rules: ClassLeftRules
        # resolve_succeeded, resolve_bindings \
        #     = resolution.resolve_rule(sparql_query.rule)  # execute the resolution / resolve rule
        reasoner: Reasoner = Reasoner(self, results_limit=results_limit, depth_limit=depth_limit)
        # create an instance of Reasoner class
        clauses_in: ClassClauses = sparql_query.to_clauses()  # convert a sparql_query instance to ClassClauses object
        resolve_succeeded, resolve_bindings_temp, contradiction \
            = reasoner.reasoner(clauses_in, depth_current=0)  # start the reasoner with depth = 0
        resolve_bindings = []  # receive the query results
        for binding in resolve_bindings_temp:
            binding_revised = {}  # receiver dict object
            for key, value in binding.items():
                binding_revised[key.replace(VAR, '?')] = value  # ?ans -> http://variable.org/ans
            resolve_bindings.append(binding_revised)  # resolve_bindings holds the correspondences

        if resolve_succeeded:  # if succeeded, print the results
            print_and_log('answer_complex_question: RESOLVE SUCCEEDED')
            # print('sparql_query: ', sparql_query.query)  # print the input query on a console
            print_and_log(f'sparql_query: {sparql_query.query}')  # print the input query to the log file
            # print('resolve_bindings: ', resolve_bindings)  # results
            print_and_log(f'resolve_bindings: {resolve_bindings}')  # results
            for binding in resolve_bindings:  # print the values of variables in the query input.
                try:
                    for var in clauses_in.list_of_variables:  # ClassClauses holds the list of variables in that clauses
                        var_name = var.to_var_string()  # get the name of the variable
                        # print(var_name, ': ', binding[var_name])  # if the query contains a variable ?ans
                        print_and_log(f'{var_name}: {binding[var_name]}')  # if the query contains a variable ?ans
                except KeyError:
                    pass
                except Exception as e:
                    # print(e)
                    print_and_log(str(e))
                    pass
        else:  # reasoner failed
            # print('answer_complex_question: RESOLVE FAILED')
            print_and_log('answer_complex_question: RESOLVE FAILED')
            if contradiction:
                print_and_log('============================>> Contradiction found.')
            # print('resolve_bindings: ', resolve_bindings)
            print_and_log(f'resolve_bindings: {resolve_bindings}')
            resolve_bindings = []

        # print('Depth reached: ', reasoner.depth_reached)  # record the depth reached during the search  # 2023/12/19
        print_and_log(f'Depth reached: {reasoner.depth_reached}')  # record the depth reached during the search
        print_and_log(f'Width reached: {reasoner.width_reached}')  # record the width reached during the search
        # print('==============================================================================================')
        print_and_log('==============================================================================================')
        return resolve_bindings

    def search_order(self, sparql_query, results_limit: int = 1, depth_limit: int = 30):
        """Search the optimal order of executing clauses in a rule

        Returns:

        """

        reasoner: Reasoner = Reasoner(self, results_limit=results_limit, depth_limit=depth_limit)
        # create an instance of Reasoner class
        clauses_in: ClassClauses = sparql_query.to_clauses()  # convert a sparql_query instance to ClassClauses object
        control_target: ClassControl = self.controls.operation_name_dict[f'{VAL}control_add_number_x_y_z']
        # get the control for add(x, y, z)
        execution_order: list[int] = control_target.right_sides
        permuted_order = permutations(execution_order)
        for order in permuted_order:
            # order = (3, 2, 1)  # debug
            control_target.right_sides = list(order)
            resolve_succeeded, resolve_bindings_temp, contradiction = reasoner.reasoner(clauses_in, depth_current=0)
            # start the reasoner with depth = 0
            width_reached: int = reasoner.width_reached
            depth_reached: int = reasoner.depth_reached
            if depth_reached < depth_limit:
                pass
            print_and_log(f'>>>{order}, {depth_reached}, {width_reached}')
            pass
        return []


class Reasoner:
    """Class for reasoning.

    Attributes:
        # find_all (bool): find all the possible answers.  # NOT USED anymore.
        results_limit (int): limit of bindings in results.
        depth_limit (int): maximum depth of recursive call.
        number_of_results_obtained (int): number of successful results obtained.
        depth_reached (int): depth reached while executing reasoning.
        width_reached (int): number of max answers reached while executing reasoning.
    """

    def __init__(self, rdf_prolog, results_limit: int = 10, depth_limit: int = 30):
        self.rdf_prolog: RdfProlog = rdf_prolog
        # self.find_all: bool = find_all  # find all the possible answers  # NOT USED anymore.
        self.results_limit: int = results_limit  # limit of bindings in results
        self.depth_limit: int = depth_limit  # maximum depth of recursive call
        self.depth_reached: int = 0  # depth reached while executing reasoning
        self.width_reached: int = 0  # number of max answers reached while executing reasoning
        self.number_of_results_obtained: int = 0  # number of successful results obtained

    def reasoner(self, clauses: ClassClauses, depth_current: int = 0):
        """Execute the depth first search.

        Args:
            clauses (ClassClauses): clauses to be resolved
            # bindings_in:  # NOT USED anymore.
            depth_current (int): recursive call depth of reasoner

        Returns:
            bool: success or failure
            dict[str, str]: results bindings
        """
        contradiction: bool = False  # 2024/2/6
        if depth_current == 0:  # if this is the start of reasoner
            self.depth_reached = 0  # reset depth_reached
            self.width_reached = 0  # reset width_reached
        print_and_log(f'reasoner: depth={depth_current}')  # for debug
        if depth_current > self.depth_reached:  # if depth exceeds depth_reached
            self.depth_reached = depth_current  # update depth_reached
        if depth_current > self.depth_limit:  # if the depth reaches the depth_limit, return with failure
            # print(f'Depth limit reached: {depth}')  # debug
            print_and_log(f'Depth limit reached: {depth_current}')  # debug
            return False, [], contradiction  # success = False, list_of_bindings = None
        first_clause, rest_clauses = clauses.split_clauses(index=0)  # split the clauses into the first and the remainder
        if first_clause is None or len(first_clause.list_of_triple) == 0:  # first clause is empty
            self.number_of_results_obtained += 1  # successful result is obtained
            return True, [{}], contradiction  # success = True, list_of_bindings = [{}]
        if first_clause.operation_name_uri == URIRef(f'{VAL}nil'):
            return False, [{}], True  # contradiction
        list_of_bindings_return = []  # list of bindings to be returned
        success_out: bool = False  # flag for success
        # print('first clause: ', first_clause.predicate_object_dict)  # debug
        print_and_log(f'first clause: {dict(sorted(first_clause.predicate_object_dict.items()))}')  # debug

        def try_facts(first_clause_, rest_clauses_, depth_, success_out_, list_of_bindings_return_):
            # try facts
            contradiction_: bool = False  # 2024/2/6
            list_of_bindings_current = first_clause_.search_facts(self.rdf_prolog)
            # find facts that match the first clause
            # print('search facts: ', len(list_of_bindings_current), list_of_bindings_current)  # debug
            print_and_log(f'search facts: {len(list_of_bindings_current)}, {list_of_bindings_current}')  # debug
            if len(list_of_bindings_current) > self.width_reached:
                self.width_reached = len(list_of_bindings_current)  # update the width
            for bindings_current in list_of_bindings_current:  # repeat for multiple possibilities
                rest_clauses_applied = rest_clauses_.apply_bindings(bindings_current)
                # apply the bindings to the remainder of clauses
                success, list_of_bindings_fact, contradiction_ = self.reasoner(rest_clauses_applied, depth_ + 1)
                # recursive call
                if success:  # find some results
                    success_out_ = True  # at least one trial is successful
                    list_of_bindings_out \
                        = [{**bindings_current, **bindings_fact} for bindings_fact in list_of_bindings_fact]
                    # combine the bindings
                    list_of_bindings_return_ += list_of_bindings_out  # add to the list
                    # if not self.find_all:  # at least one trial is successful
                    if self.number_of_results_obtained >= self.results_limit or contradiction_:  # 2023/12/19
                        return success_out_, list_of_bindings_return_, contradiction_  # return the answer
            return success_out_, list_of_bindings_return_, contradiction_  # return the answer

        success_out, list_of_bindings_return, contradiction \
            = try_facts(first_clause, rest_clauses, depth_current, success_out, list_of_bindings_return)  # try facts
        if self.number_of_results_obtained >= self.results_limit or contradiction:  # 2024/2/2
            print_and_log(f'return, depth={depth_current}')
            return success_out, list_of_bindings_return, contradiction  # return the answer without try_applications

        def try_applications(first_clause_, rest_clauses_, depth_, success_out_, list_of_bindings_return_):
            # try applications
            def match_application(rdf_prolog__, application__, first_clause__, rest_clauses__):  # 2024/2/5
                """
                match an application to query clauses
                an application has more than 1 input patterns

                Args:
                    rdf_prolog__:
                    application__ (ClassApplication): application to be matched
                    first_clause__ (ClassClause): first clause in the query
                    rest_clauses__ (ClassClauses): remaining clauses in the query

                Returns:
                    matched, list_of_application_clauses, list_of_bindings_forward,
                    list_of_bindings_backward, rest_clauses_, contradiction

                """

                def match_clause_clause(
                        application_clause_____: ClassClause,
                        query_clause_____: ClassClause,
                        rest_of_application_clauses_____: ClassClauses,
                        rest_of_query_clauses_____: ClassClauses,
                        list_of_rest_of_query_clauses_____: list[ClassClauses],
                        list_of_bindings_forward_multiple_____: list[dict[str, list[str]]],
                        list_of_bindings_backward_multiple_____: list[dict[str, list[str]]],
                        bindings_forward_multiple_in_____: dict[str, list[str]],
                        bindings_backward_multiple_in_____: dict[str, list[str]]):
                    """

                    Args:
                        application_clause_____ (ClassClause):
                        query_clause_____ (ClassClause):
                        rest_of_application_clauses_____ (ClassClauses):
                        rest_of_query_clauses_____ (ClassClauses):
                        list_of_rest_of_query_clauses_____ (list[ClassClauses]):
                        list_of_bindings_forward_multiple_____:
                        list_of_bindings_backward_multiple_____:
                        bindings_forward_multiple_in_____:
                        bindings_backward_multiple_in_____:

                    Returns:

                    """

                    def append_to_bindings(bindings_, key_, value_):
                        """Append a value to the list specified by key.
                        For bindings multiple.

                        Args:
                            bindings_ (dict[str, list[str]]):
                            key_ (str):
                            value_ (str):

                        Returns:
                            dict[str, list[str]]: revised bindings

                        """
                        try:
                            xxx: str = bindings_[key_]  # search an entry
                        except KeyError:  # no entry found
                            bindings_[key_] = []  # value of the dict is an empty list
                        bindings_[key_].append(value_)
                        return bindings_

                    # application vs query clauses matching
                    matched_____: bool = True  # assume the success
                    bindings_forward_multiple_____ = {}  # forward: query is constant, rule is variable
                    bindings_backward_multiple_____ = {}  # backward: query is variable, rule is either constant or variable
                    bindings_forward_out_____ = {}
                    bindings_backward_out_____ = {}
                    for application_key_____, application_value_____ in (
                            application_clause_____.predicate_object_dict.items()):  # key: predicate, value: object
                        try:
                            query_value_____ = query_clause_____.predicate_object_dict[application_key_____]
                            # get the corresponding value in query clause
                            if query_value_____.find(VAR) >= 0:  # object of this clause is a variable
                                if application_value_____.find(VAR) >= 0:  # application side is also a variable
                                    bindings_forward_multiple_____ \
                                        = append_to_bindings(
                                            bindings_forward_multiple_____,
                                            application_value_____, query_value_____)  # append to forward bindings
                                elif application_value_____.find(SOME) >= 0:  # application side is a semi-variable
                                    matched_____ = False  # a semi-variable only matches with a constant
                                    # break  # skip the rest of the loop
                                    return (
                                        False,  # match failed
                                        list_of_rest_of_query_clauses_____,
                                        list_of_bindings_forward_multiple_____,
                                        list_of_bindings_backward_multiple_____)
                                else:  # application side is a constant
                                    bindings_backward_multiple_____ \
                                        = append_to_bindings(
                                            bindings_backward_multiple_____,
                                            query_value_____,
                                            application_value_____)  # append to backward bindings
                            else:  # query side is constant
                                if application_value_____.find(VAR) >= 0:  # application side is a variable
                                    bindings_forward_multiple_____ \
                                        = append_to_bindings(
                                            bindings_forward_multiple_____,
                                            application_value_____,
                                            query_value_____)  # append to forward bindings
                                elif application_value_____.find(SOME) >= 0:  # application side is a semi-variable
                                    bindings_forward_multiple_____ \
                                        = append_to_bindings(
                                            bindings_forward_multiple_____,
                                            application_value_____,
                                            query_value_____)  # append to forward bindings
                                else:  # application side is a constant
                                    if application_value_____ == query_value_____:
                                        pass  # if both sides are constants, they must be the same
                                    else:
                                        matched_____ = False  # match failed
                                        # break  # skip the rest of the loop
                                        return (
                                            False,
                                            list_of_rest_of_query_clauses_____,
                                            list_of_bindings_forward_multiple_____,
                                            list_of_bindings_backward_multiple_____)
                        except KeyError:
                            matched_____ = False  # match failed
                            # break  # skip the rest of the loop
                            return (
                                False,
                                list_of_rest_of_query_clauses_____,
                                list_of_bindings_forward_multiple_____,
                                list_of_bindings_backward_multiple_____)

                    def bindings_join(bindings_multiple_in, bindings_multiple):
                        bindings_out = {}
                        for key, value in bindings_multiple_in.items():
                            bindings_out[key] = value
                        for key, value in bindings_multiple.items():
                            try:
                                value_in = bindings_out[key]
                                bindings_out[key] = value_in + value
                            except KeyError:  # no key exists in bindings_out
                                bindings_out[key] = value
                        return bindings_out

                    bindings_forward_out_____ \
                        = bindings_join(bindings_forward_multiple_in_____, bindings_forward_multiple_____)
                    bindings_backward_out_____ \
                        = bindings_join(bindings_backward_multiple_in_____, bindings_backward_multiple_____)
                    rest_of_query_clauses_____.apply_bindings(bindings_backward_out_____)
                    (matched_____,
                     list_of_rest_of_query_clauses___,
                     list_of_bindings_forward_multiple_____,
                     list_of_bindings_backward_multiple_____) \
                        = match_clauses_clauses(
                            rest_of_application_clauses_____,
                            rest_of_query_clauses_____,
                            list_of_rest_of_query_clauses_____,
                            list_of_bindings_forward_multiple_____,
                            list_of_bindings_backward_multiple_____,
                            bindings_forward_out_____,
                            bindings_backward_out_____)  # recursively process the remained application clauses
                    return (
                        matched_____,  # matched____ is not used
                        list_of_rest_of_query_clauses___,
                        list_of_bindings_forward_multiple_____,
                        list_of_bindings_backward_multiple_____)

                def match_clause_clauses(
                        application_clause____: ClassClause,
                        rest_of_application_clauses____: ClassClauses,
                        query_clauses____: ClassClauses,
                        list_of_rest_of_query_clauses____: list[ClassClauses],
                        list_of_bindings_forward_multiple____: list[dict[str, list[str]]],
                        list_of_bindings_backward_multiple____: list[dict[str, list[str]]],
                        bindings_forward_multiple____: dict[str, list[str]],
                        bindings_backward_multiple____: dict[str, list[str]]):
                    """

                    Args:
                        application_clause____ (ClassClause):
                        rest_of_application_clauses____ (ClassClauses):
                        query_clauses____ (ClassClauses):
                        list_of_rest_of_query_clauses____:
                        list_of_bindings_forward_multiple____:
                        list_of_bindings_backward_multiple____:
                        bindings_forward_multiple____:
                        bindings_backward_multiple____:

                    Returns:

                    """
                    matched____: bool = True
                    if len(query_clauses____.list_of_clauses) == 0:
                        # no more query clauses against the application clause
                        return (
                            False,
                            list_of_rest_of_query_clauses____,
                            list_of_bindings_forward_multiple____,
                            list_of_bindings_backward_multiple____)
                    for index____, query_clause____ in enumerate(query_clauses____.list_of_clauses):
                        rest_of_query_clauses____ = ClassClauses()
                        rest_of_query_clauses____.list_of_clauses \
                            = [clause____ for clause____ in query_clauses____.list_of_clauses]
                        rest_of_query_clauses____.list_of_clauses.pop(index____)
                        (matched____,
                         list_of_rest_of_query_clauses___,
                         list_of_bindings_forward_multiple____,
                         list_of_bindings_backward_multiple____) \
                            = match_clause_clause(
                            application_clause____,
                            query_clause____,
                            rest_of_application_clauses____,
                            rest_of_query_clauses____,
                            list_of_rest_of_query_clauses____,
                            list_of_bindings_forward_multiple____,
                            list_of_bindings_backward_multiple____,
                            bindings_forward_multiple____,
                            bindings_backward_multiple____)
                        # if not matched____:
                        #     return False, [], [{}], [{}]
                    return (
                        matched____,  # matched___ is not used
                        list_of_rest_of_query_clauses____,
                        list_of_bindings_forward_multiple____,
                        list_of_bindings_backward_multiple____)

                def match_clauses_clauses(
                        application_clauses___: ClassClauses,
                        query_clauses___: ClassClauses,
                        list_of_rest_of_query_clauses___: list[ClassClauses],
                        list_of_bindings_forward_multiple___: list[dict[str, list[str]]],
                        list_of_bindings_backward_multiple___: list[dict[str, list[str]]],
                        bindings_forward_multiple___: dict[str, list[str]],
                        bindings_backward_multiple___: dict[str, list[str]]):
                    """
                    Matching between application clauses and query clauses.

                    Args:
                        application_clauses___ (ClassClauses):
                        query_clauses___ (ClassClauses):
                        list_of_rest_of_query_clauses___ (list[ClassClauses]):
                        list_of_bindings_forward_multiple___ (list[dict[str, list[str]]]):
                        list_of_bindings_backward_multiple___ (list[dict[str, list[str]]]):
                        bindings_forward_multiple___ (dict[str, list[str]]):
                        bindings_backward_multiple___ (dict[str, list[str]]):

                    Returns:

                    """
                    matched___ = True
                    if len(application_clauses___.list_of_clauses) == 0:
                        # all the clause in application clauses have been satisfied
                        list_of_bindings_forward_multiple___.append(bindings_forward_multiple___)
                        list_of_bindings_backward_multiple___.append(bindings_backward_multiple___)
                        list_of_rest_of_query_clauses___.append(query_clauses___)
                        return (
                            True, list_of_rest_of_query_clauses___,
                            list_of_bindings_forward_multiple___,
                            list_of_bindings_backward_multiple___)  # recursive call ends
                    rest_of_application_clauses___ = None
                    application_clause___: ClassClause \
                        = application_clauses___.list_of_clauses[0]
                    # choose first one of the remaining application clauses
                    rest_of_application_clauses___: ClassClauses = ClassClauses()
                    rest_of_application_clauses___.list_of_clauses \
                        = application_clauses___.list_of_clauses[1:]
                    (matched___,
                     list_of_rest_of_query_clauses___,
                     list_of_bindings_forward_multiple___,
                     list_of_bindings_backward_multiple___) \
                        = match_clause_clauses(
                        application_clause___,
                        rest_of_application_clauses___,
                        query_clauses___,
                        list_of_rest_of_query_clauses___,
                        list_of_bindings_forward_multiple___,
                        list_of_bindings_backward_multiple___,
                        bindings_forward_multiple___,
                        bindings_backward_multiple___)
                    # if not matched___:  # match failed
                    #     return False, [], [{}], [{}]
                    return (
                        matched___,  # matched__ is not used
                        list_of_rest_of_query_clauses___,  # return the remained query clauses
                        list_of_bindings_forward_multiple___,
                        list_of_bindings_backward_multiple___)

                application_pattern_clauses__: ClassClauses = application__.patterns
                query_clauses__: ClassClauses = ClassClauses()
                query_clauses__.list_of_clauses.append(first_clause__)  # merge the first clause and the rest clauses
                for clause__ in rest_clauses__.list_of_clauses:  # do not modify rest_clauses__, but copy them
                    query_clauses__.list_of_clauses.append(clause__)
                list_of_bindings_forward_multiple__: list[dict[str, list[str]]] = []
                list_of_bindings_backward_multiple__: list[dict[str, list[str]]] = []
                list_of_rest_of_query_clauses__: list[ClassClauses] = []
                bindings_forward_multiple__: dict[str, list[str]] = {}  # initial states
                bindings_backward_multiple__: dict[str, list[str]] = {}
                (matched__,
                 list_of_rest_of_query_clauses__,
                 list_of_bindings_forward_multiple__,
                 list_of_bindings_backward_multiple__) \
                    = match_clauses_clauses(
                        application_pattern_clauses__,
                        query_clauses__,
                        list_of_rest_of_query_clauses__,
                        list_of_bindings_forward_multiple__,
                        list_of_bindings_backward_multiple__,
                        bindings_forward_multiple__,
                        bindings_backward_multiple__)
                matched__ = True
                # returned value of matched__ is not used, but is created from list_of_bindings_forward_multiple__
                if list_of_bindings_forward_multiple__ is None or len(list_of_bindings_forward_multiple__) == 0:
                    matched__ = False

                def apply_internal_bindings(
                        forward_multiple: dict[str, list[str]],
                        backward_multiple: dict[str, list[str]]):
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
                        if len(values) == 1:  # this is the only element in the list
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
                            first_element: str = first_constant
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

                    first_constant: str = ''
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

                    return (
                        success_,
                        forward_binding_,
                        backward_binding_)  # end and return of apply_internal_bindings

                def try_controls(matched___):
                    controls___: list[str] \
                        = application__.list_of_controls  # names (uri) of controls
                    for control_uri___ in controls___:  # try each control
                        control___: ClassControl \
                            = rdf_prolog__.controls.operation_name_dict[control_uri___]
                        rule_left_sides___: ClassClauses \
                            = control___.rule.left_sides.update_variables()
                        restrictions___ = control___.left_side
                        forward_bindings_control_multiple___: dict[str, list[str]] = {}
                        backward_bindings_control_multiple___: dict[str, list[str]] = {}
                        match_control___ = True  # assume a success

                        list_of_rest_of_query_clauses___: list[ClassClauses] = []
                        list_of_bindings_forward_multiple___: list[dict[str, list[str]]] = []
                        list_of_bindings_backward_multiple___: list[dict[str, list[str]]] = []
                        bindings_forward_multiple___: dict[str, list[str]] = {}  # initial states
                        bindings_backward_multiple___: dict[str, list[str]] = {}

                        (match_control___,
                         list_of_rest_of_query_clauses___,
                         list_of_bindings_forward_multiple___,
                         list_of_bindings_backward_multiple___) \
                            = match_clauses_clauses(
                            rule_left_sides___,
                            query_clauses__,
                            list_of_rest_of_query_clauses___,
                            list_of_bindings_forward_multiple___,
                            list_of_bindings_backward_multiple___,
                            bindings_forward_multiple___,
                            bindings_backward_multiple___)
                        if (list_of_bindings_forward_multiple___ is None or
                                len(list_of_bindings_forward_multiple___) == 0):
                            # match_control___ = False
                            return False

                        if len(list_of_bindings_forward_multiple___) == 1:
                            another_bindings_forward_multiple___ = list_of_bindings_forward_multiple___[0]
                            another_bindings_backward_multiple___ = list_of_bindings_backward_multiple___[0]
                            success___, another_bindings_forward___, another_bindings_backward___ \
                                = apply_internal_bindings(
                                another_bindings_forward_multiple___,
                                another_bindings_backward_multiple___)
                            if not success___:
                                # match_control___ = False
                                return False
                            else:  # success___ == True
                                matched_ = True  # return value
                                list_of_bindings_forward__.append(
                                    {**another_bindings_forward__, **another_bindings_forward___})
                                list_of_bindings_backward__.append(
                                    {**another_bindings_backward__, **another_bindings_backward___})
                                clauses___ = ClassClauses()
                                for index___ in control___.right_sides:
                                    right___: ClassClause \
                                        = control___.rule.right_sides.list_of_clauses[index___ - 1]
                                    # index starts with 1
                                    right_updated___: ClassClause \
                                        = right___.update_variables()
                                    clauses___.list_of_clauses.append(right_updated___)
                                list_of_query_clauses__.append(clauses___)
                                ClassClauses.variable_modifier += 1

                        else:
                            for another_bindings_forward_multiple___, another_bindings_backward_multiple___ \
                                    in zip(list_of_bindings_forward_multiple___, list_of_bindings_backward_multiple___):
                                success___, another_bindings_forward___, another_bindings_backward___ \
                                    = apply_internal_bindings(
                                        another_bindings_forward_multiple___,
                                        another_bindings_backward_multiple___)
                                if not success___:
                                    # match_control___ = False
                                    # return False
                                    pass  # 2024/4/23
                                else:  # success___ == True
                                    matched_ = True  # return value
                                    list_of_bindings_forward__.append(
                                        {**another_bindings_forward__, **another_bindings_forward___})
                                    list_of_bindings_backward__.append(
                                        {**another_bindings_backward__, **another_bindings_backward___})
                                    clauses___ = ClassClauses()
                                    for index___ in control___.right_sides:
                                        right___: ClassClause \
                                            = control___.rule.right_sides.list_of_clauses[index___ - 1]
                                        # index starts with 1
                                        right_updated___: ClassClause \
                                            = right___.update_variables()
                                        clauses___.list_of_clauses.append(right_updated___)
                                    list_of_query_clauses__.append(clauses___)
                                    ClassClauses.variable_modifier += 1
                        pass  # end of if len(list_of_bindings_forward_multiple___) == 1:
                    return matched___
                    # end of try_controls

                list_of_query_clauses__: list[ClassClauses] = []
                list_of_bindings_forward__: list[dict[str, str]] = []
                list_of_bindings_backward__: list[dict[str, str]] = []
                if matched__:
                    matched__: bool = False  # assume a failure
                    if len(list_of_bindings_forward_multiple__) == 1:
                        rest_of_query_clauses__ = list_of_rest_of_query_clauses__[0]
                        another_bindings_forward_multiple__: dict[str, list[str]] \
                            = list_of_bindings_forward_multiple__[0]
                        another_bindings_backward_multiple__: dict[str, list[str]] \
                            = list_of_bindings_backward_multiple__[0]

                        success__, another_bindings_forward__, another_bindings_backward__ \
                            = apply_internal_bindings(
                                another_bindings_forward_multiple__,
                                another_bindings_backward_multiple__)
                        if success__:
                            matched__ = True
                        else:
                            matched__ = False
                            return (
                                False, list_of_query_clauses__,
                                list_of_bindings_forward__, list_of_bindings_backward__)

                        matched__ = try_controls(matched__)  # try controls

                    else:
                        matched__ = False
                        for \
                            rest_of_query_clauses__, \
                            another_bindings_forward_multiple__, \
                            another_bindings_backward_multiple__ \
                            in zip(list_of_rest_of_query_clauses__,
                                   list_of_bindings_forward_multiple__,
                                   list_of_bindings_backward_multiple__):

                            success__, another_bindings_forward__, another_bindings_backward__ \
                                = apply_internal_bindings(
                                    another_bindings_forward_multiple__,
                                    another_bindings_backward_multiple__)
                            if success__:
                                matched__ = True
                            # else:
                            #     matched__ = False
                            #     return (
                            #         False, list_of_query_clauses__,
                            #         list_of_bindings_forward__, list_of_bindings_backward__)
                        if matched__:
                            matched__ = try_controls(matched__)  # try controls

                pass  # end of if matched__:
                return (
                    matched__,
                    list_of_query_clauses__,
                    list_of_bindings_forward__,
                    list_of_bindings_backward__)
                # end of match_application

            # print('trying applications')
            print_and_log('trying applications')  # debug
            contradiction_: bool = False  # 2024/2/6
            # applications = []  # start the rule search
            try:
                applications \
                    = self.rdf_prolog.applications.operation_names_dict[first_clause_.operation_name_uri]
                # possible rules are already summarized in ClassApplications object
                # print('number of applications: ', len(applications))
                print_and_log(f'number of applications: {len(applications)}')
                spaces = ''
                for d in range(depth_):
                    spaces += spaces + '  '
                for index, application in enumerate(applications):  # repeat for each candidate application
                    print_and_log(f'{spaces}{index}/{len(applications)} trying: {application.application_label}')  # 2024/2/20
                    matched = False
                    list_of_query_clauses = []
                    list_of_bindings_forward = []
                    list_of_bindings_backward = []
                    if len(application.patterns.list_of_clauses) == 1:  # conventional match, 2024/2/5
                        matched, list_of_query_clauses, list_of_bindings_forward, list_of_bindings_backward \
                            = first_clause_.match_application(self.rdf_prolog, application)
                        # match the rule against the query
                        index = 0  # index for loop
                        for bindings_forward, bindings_backward \
                                in zip(list_of_bindings_forward, list_of_bindings_backward):
                            try:
                                application_clauses: ClassClauses = list_of_query_clauses[index]
                                combined_clauses: ClassClauses = application_clauses.combine(rest_clauses_)  # combine the clauses
                            except IndexError:  # no list_of_application_clauses found  # 2023/12/21
                                combined_clauses: ClassClauses = rest_clauses_  # just use the rest clauses

                            query_clauses_applied \
                                = combined_clauses.apply_bindings(
                                    {**bindings_forward, **bindings_backward})  # apply the bindings
                            for clause in query_clauses_applied.list_of_clauses:  # debug
                                # print(clause.predicate_object_dict)
                                print_and_log(str(dict(sorted(clause.predicate_object_dict.items()))))  # debug
                            success, list_of_bindings_application, contradiction_ \
                                = self.reasoner(query_clauses_applied, depth_ + 1)  # recursive call with +1 depth
                            if contradiction_:
                                return False, list_of_bindings_return_, contradiction_  # return without further search
                            if success:  # reasoner succeeded
                                success_out_ = True  # success flag for return
                                list_of_bindings_out = [
                                    {**bindings_forward, **bindings_backward, **bindings_application}
                                    for bindings_application in list_of_bindings_application]
                                list_of_bindings_return_ += list_of_bindings_out  # merge list for return
                                # if not self.find_all:  # NOT USED anymore
                                if self.number_of_results_obtained >= self.results_limit or contradiction_:
                                    # number of results reached the limit # 2023/12/19
                                    return (
                                        True,
                                        list_of_bindings_return_,
                                        contradiction_)  # return without further search
                            index += 1  # try next bindings

                    else:  # more than 1 clause in patterns, 2024/2/6
                        print_and_log('more than 1 clause in patterns')  # 2024/4/22
                        if application.application_label == 'http://value.org/application_square_integer_factor2_even':
                            pass
                        matched, list_of_query_clauses, list_of_bindings_forward, list_of_bindings_backward \
                            = match_application(self.rdf_prolog, application, first_clause_, rest_clauses_)
                        print_and_log('result of matched: ' + str(matched))
                        if matched:  # 2024/4/22
                            index = 0  # index for loop
                            combined_clauses = ClassClauses()  # empty clauses
                            for bindings_forward, bindings_backward \
                                    in zip(list_of_bindings_forward, list_of_bindings_backward):
                                try:
                                    combined_clauses = list_of_query_clauses[index]

                                except IndexError:  # no list_of_application_clauses found  # 2023/12/21
                                    pass

                                query_clauses_applied = combined_clauses.apply_bindings(
                                    {**bindings_forward, **bindings_backward})  # apply the bindings
                                for clause in query_clauses_applied.list_of_clauses:  # debug
                                    # print(clause.predicate_object_dict)
                                    print_and_log(str(dict(sorted(clause.predicate_object_dict.items()))))  # debug
                                success, list_of_bindings_application, contradiction_ \
                                    = self.reasoner(query_clauses_applied, depth_ + 1)  # recursive call with +1 depth
                                if contradiction_:
                                    return False, list_of_bindings_return_, contradiction_  # return without further search
                                if success:  # reasoner succeeded
                                    success_out_ = True  # success flag for return
                                    list_of_bindings_out = [
                                        {**bindings_forward, **bindings_backward, **bindings_application}
                                        for bindings_application in list_of_bindings_application]
                                    list_of_bindings_return_ += list_of_bindings_out  # merge list for return
                                    # if not self.find_all:  # NOT USED anymore
                                    if self.number_of_results_obtained >= self.results_limit or contradiction_:
                                        # number of results reached the limit # 2023/12/19
                                        return (
                                            True,
                                            list_of_bindings_return_,
                                            contradiction_)  # return without further search
                                index += 1  # try next bindings

            except KeyError as e:
                print_and_log(f'applications not found {e}')
            return (
                success_out_,
                list_of_bindings_return_,
                contradiction_)  # return of try_applications
            # end of try_applications

        success_out, list_of_bindings_return, contradiction \
            = try_applications(
                first_clause, rest_clauses,
                depth_current, success_out,
                list_of_bindings_return)  # try applications

        print_and_log(f'return, depth={depth_current}')
        if success_out and len(list_of_bindings_return) > self.width_reached:
            self.width_reached = len(list_of_bindings_return)  # update the width
        return success_out, list_of_bindings_return, contradiction  # return of reasoner
        # end of reasoner
    # end of Reasoner class


# class Resolution:  # main class for resolution
#     """Main class for resolution.
#
#     Attributes:
#         graph (Graph): set the knowledge graph
#         rules (ClassRules): ClassRules created from a graph
#         find_all (bool): if true, find all the possible answers, else find the first answer.
#     """
#     resolve_right_recursive_count = 0  # indicate the depth of recursive call.  # for debug
#
#     def __init__(self, rules, find_all: bool, depth_limit: int):
#         """
#         initialize Resolution class
#
#         """
#         # self.graph = graph  # set the knowledge graph
#         self.rules = rules  # ClassRules(graph)
#         self.find_all = find_all  # find all possible answers
#         self.depth_limit = depth_limit  # maximum depth of resolution
#         pass
#
#     def resolve_recursive(self, right_clauses: ClassClauses) -> (bool, list[dict[str, str]]):
#         resolve_bindings_in 辞書の配列
#         """
#         resolve_recursiveはルールの右側のclauseを順番に再帰呼び出しで処理する。
#
#         １つのclauseが複数の結果を返す場合があるので、処理がツリー状に分岐する。
#
#         第２戻り値は辞書の配列
#
#         入力：
#             right_clauses (ClassRuleRight): 処理するルールの右側
#
#         出力：
#             succeeded: 結果が得られた時True
#
#             bindings: 変数と値を結びつける辞書の配列
#
#         Resolve right side clauses recursively.
#         If there are no clauses, return with success.
#         If there are clauses, resolve the first clause with "resolve_clause".
#         The rest of the clauses are recursively processed by this function.
#
#         Args:
#
#             right_clauses (ClassRuleRight): right side clauses of a rule
#
#         Returns:
#
#             bool: succeeded
#
#             list[dict[str, str]]: a list of bindings:
#         """
#         print_and_log('++++++++++ resolve_recursive ++++++++++')  # debug
#         print_and_log('++++++++++ resolve_recursive ++++++++++')  # debug
#         if len(right_clauses) == 0:  # clauseが無くなったら再帰呼び出しを終了して戻る。
#             return True, []  # resolution=success, 辞書の配列の配列を返す。
#         else:  # 右側にまだclauseがある時。
#             # print('[', Resolution.resolve_right_recursive_count, '] ENTERING resolve_recursive')  # debug
#             print_and_log(f'[{Resolution.resolve_right_recursive_count}] ENTERING resolve_recursive')  # debug
#             Resolution.resolve_right_recursive_count += 1  # 再帰呼び出しの深さをup。debug
#             if Resolution.resolve_right_recursive_count > self.depth_limit:
#                 exceeds depth_limit of resolution  # 2023/11/7
#                 Resolution.resolve_right_recursive_count -= 1
#                 return False, []
#             grandchild_rules, right_clauses_sub = right_clauses.split_clauses()
#                 first clauseを取り出す, rest of clausesは後で処理する。
#             built_query = ClassSparqlQuery().set('SELECT ?s ?p ?o WHERE {?s ?p ?o .}')  # dummy query
#             built_query.build_query(grandchild_rules)  # resolveを呼び出すためのクエリ
#             succeeded, bindings_array = self.resolve_clause(built_query)  # execute resolve
#             # 戻り値のbindings_arrayは辞書の配列
#             if len(bindings_array) > 1:  # debug
#                 pass  # debug
#             if not succeeded:  # resolve failed
#                 # print('---------- resolve_right_recursive-1 ---------')  # debug for execution trace
#                 print_and_log('---------- resolve_right_recursive-1 ---------')  # debug for execution trace
#                 Resolution.resolve_right_recursive_count -= 1  # debug 再帰呼び出しの深さを戻す
#                 return False, []  # 失敗で戻る
#
#             resolve_bindings_out = []  # 戻り値の初期化
#             return_succeeded = False  # succeeded  # 戻り値  # initially assume False
#             # print('%%% bindings_array: ', bindings_array)  # debug  # return value of resolve_clause
#             print_and_log(f'%%% bindings_array: {bindings_array}')  # debug  # return value of resolve_clause
#             iteration = 1  # 横方向の分岐の数 debug
#
#             for bindings in bindings_array:  # bindings は辞書、bindings_arrayは辞書の配列、resolve_clauseの戻り値
#                 # print(iteration, '??? bindings: ', bindings, '<<< ', bindings_array)  # debug
#                 print_and_log(f'{iteration} ??? bindings: {bindings}<<< {bindings_array}')  # debug
#                 iteration += 1  # 横方向の分岐のレベルup  debug
#                 return_bindings = [bindings]
#                 right_clauses_sub_revised = []  # 右辺の修正したもの initialize
#                 for right_clause in right_clauses_sub:  # 右辺の各項を修正
#                     right_clause_revised = ClassClause()  # 新規にインスタンスを作る
#                     right_clause_revised.revise(right_clause, bindings)  # 修正の実行
#                     right_clauses_sub_revised += [right_clause_revised]  # 修正したものを追加。
#                     pass  # debug
#                 resolve_succeeded, resolve_bindings_array \
#                     = self.resolve_recursive(right_clauses_sub_revised)  # 再帰呼び出し
#                 if resolve_succeeded:
#                     return_succeeded = True  # at least one trial was successful
#                     for r_bindings in return_bindings:
#                         # print('r_bindings: ', r_bindings)  # results of the first clause
#                         print_and_log(f'r_bindings: {r_bindings}')  # results of the first clause
#                         temp = [r_bindings]
#                         if resolve_bindings_array:  # results of the rest clauses, if it is not null
#                             temp = []
#                             for bindings1 in resolve_bindings_array:
#                                 r_bindings1 = r_bindings.copy()  # 2023/11/6
#                                 # print('+++', bindings1)  # debug
#                                 print_and_log(f'+++{bindings1}')  # debug
#                                 if bindings1:
#                                     r_bindings1.update(bindings1)  # append to the dict
#                                     temp.append(r_bindings1)  # append to the list
#                         resolve_bindings_out += temp
#                 else:
#                     pass  # do nothing
#             # print('[', Resolution.resolve_right_recursive_count,
#                   '] ==resolve_bindings_out IN resolve_right_recursive: ',
#                   resolve_bindings_out)  # debug
#             print_and_log(f'[{Resolution.resolve_right_recursive_count}] == resolve_bindings_out
#             IN resolve_right_recursive: {resolve_bindings_out}')  # debug
#             # print('---------- resolve_right_recursive-2 ---------')  # debug
#             print_and_log('---------- resolve_right_recursive-2 ---------')  # debug
#             Resolution.resolve_right_recursive_count -= 1  # depth of recursive call down.  # debug
#             return return_succeeded, resolve_bindings_out
#
#     def resolve_rule(self, rule: ClassRule) -> (bool, list[dict[str, str]]):  # resolve multiple clauses
#         """resolve_ruleはルールを処理する。
#
#         ルールとして呼び出された場合には左側が評価されてargument_bindingsが生成される。
#
#         クエリとして呼び出された場合には、左側は評価されない。ルールに左側が設定されていない。
#
#         実際の処理はresolve_right_recursiveが行う。
#
#         入力：
#             rule: 処理するルール
#
#             resolve_bindings_in: 変数と値を結びつける辞書の配列
#         出力：
#             succeeded: 結果が得られた時True
#
#             bindings: 変数と値を結びつける辞書  ####の配列
#
#         This function resolves a rule.
#         First, the left side part of the rule is evaluated with the forward_bindings associated with the left.
#         The bindings are then applied to the right side clauses of the rule.
#         Then the right side clauses are evaluated by "resolve_recursive".
#
#         Using this function, a question with multiple clauses is also processed without forward_bindings.
#
#         Args:
#             rule (ClassRule): a rule instance to be processed
#
#         Returns:
#             bool: resolution succeeded.
#
#             list[dict[str, str]]: resolve_bindings_array, a list of bindings. list because of multiple answers.
#         """
#         # ルールの左辺と一致するようの変数をbindingする。戻り値は辞書型。
#         # print('++++++++++ resolve_rule ++++++++++')  # debug
#         print_and_log('++++++++++ resolve_rule ++++++++++')  # debug
#
#         def build_argument_bindings_for_left(bindings_for_left: dict[rdflib.term.Variable, str]) -> dict[str, str]:
#             """
#             左辺の変数をチェック
#
#             Args:
#                 bindings_for_left (dict[rdflib.term.Variable, str]): {x: 'http://value.org/two',
#                 y: 'http://value.org/two', z: 'http://value.org/z'}
#
#             Returns:
#                 dict[str, str]: {'x1000': '<http://value.org/two>',
#                 '?y1000': '<http://value.org/two>'. '?z1000': '?z'}
#             """
#             # print('BINDINGS FOR LEFT: ' + str(bindings_for_left))  # debug
#             print_and_log(f'BINDINGS FOR LEFT: {str(bindings_for_left)}')  # debug
#             argument_bindings_built = {}  # initialize a dict
#             # print('(DEBUG) TYPE OF BINDING[0]: '+str(type(binding)))  # debug
#             # print('(DEBUG) LENGTH OF BINDING: ', len(binding))  # debug
#             for item in bindings_for_left:
#                 my_key = str(item)  # x
#                 if isinstance(item, Variable):
#                     my_key = '?' + my_key  # ?x
#                     try:
#                         my_key = rule.variables_dict[my_key]  # ?x ->?x1000, etc.
#                     except KeyError:
#                         pass
#                 my_term = ClassTerm().build(my_key)  # build a ClassTerm  instance from a string my_key
#                 my_value = ClassTerm().build(str(bindings_for_left[item]))
#                 my_value is also an instance of ClassTerm
#                 argument_bindings_built[my_term.to_var_string()] = my_value.to_var_string()  # return value
#             # print('ARGUMENT BINDINGS: ' + str(argument_bindings_built))
#             print_and_log(f'ARGUMENT BINDINGS: {str(argument_bindings_built)}')
#             return argument_bindings_built
#
#         # argument_binding = build_argument_bindings_for_left(rule.rule_left.bindings)  # argument_bindingは辞書型
#         argument_binding = build_argument_bindings_for_left(rule.rule_left.forward_bindings)  # argument_bindingは辞書型
#         right_clauses_sub_revised = ClassClauses() # argument_bindingに基づいて右辺を修正する。
#         for right_clause in rule.rule_right.list_of_clauses:  # 右側には複数の節が含まれる可能性がある。
#             right_clause_revised = ClassClauses().revise(right_clause, argument_binding)  # 新規に節を作り直す。
#             right_clauses_sub_revised.list_of_clauses += right_clause_revised  # 修正した項を追加していく。
#             pass
#         # resolve_right_bindings_in = []  # [argument_binding]  右辺の項を修正したのでbindingsは不要。
#         right_side_succeeded, resolve_bindings_array \
#             = self.resolve_recursive(right_clauses_sub_revised)  # ルールの右辺を評価
#         return right_side_succeeded, resolve_bindings_array
#
#     def resolve_clause(self, resolve_query: ClassSparqlQuery) -> (bool, list[dict[str, str]]):
#         resolve a single clause
#         """
#         resolve_clauseは１つのclauseを対象にする。
#
#         戻り値のbindings[]は２つ以上の辞書を含む場合がある。
#
#         knows_direct(andy, ?ans)に対する、bob, davidのような場合。
#
#         入力：
#             resolve_query: 処理するクエリ＝節
#
#         出力：
#             succeeded (bool): 結果が得られた時True
#
#             bindings: 変数と値を結びつける辞書の配列
#
#         Resolve a single clause.
#         First, try to find a direct match in the graph.
#         Next, search for applicable rules and appy them to the clause using 'resolve_rule'.
#         If find_all is false and direct search is successful, return the results.
#         Also, if there are no applicable rules, return without results.
#         Lastly if 'resolve_rule' is succeeded, return the results of 'resolve_rule'.
#
#         Args:
#             resolve_query (ClassSparqlQuery): an input single clause represented as a sparql query
#
#         Returns:
#             bool: if true, the resolution is succeeded.
#
#             list[dict[str, str]]: list of bindings
#
#         """
#         # print('++++++++++ resolve_clause ++++++++++')  # debug
#         print_and_log('++++++++++ resolve_clause ++++++++++')  # debug
#         # global find_all  # if True, find all the results.
#         succeeded = False  # final result of success. firstly assumed to be failed.
#         resolve_bindings_out: list[dict[str, str]] = []  # initialize bindings to be returned
#         direct_search_succeeded, returned_direct_search_bindings = resolve_query.direct_search()  # direct search
#         if direct_search_succeeded:
#             succeeded = True  # final result is also set succeeded.
#             resolve_bindings_out += returned_direct_search_bindings
#         if not direct_search_succeeded:
#             # print('DIRECT ANSWERS WERE NOT FOUND. TRYING TO FIND APPLICABLE RULES. ')  # debug
#             print_and_log('DIRECT ANSWERS WERE NOT FOUND. TRYING TO FIND APPLICABLE RULES. ')  # debug
#         if not self.find_all:
#             if direct_search_succeeded:
#                 # print('======= LEAVING RESOLVE, AFTER FINDING DIRECT ANSWER =======')  # debug
#                 print_and_log('======= LEAVING RESOLVE, AFTER FINDING DIRECT ANSWER =======')  # debug
#                 # print('---------- resolve_clause-1 ---------')  # debug
#                 print_and_log('---------- resolve_clause-1 ---------')  # debug
#                 return True, resolve_bindings_out  # 辞書の配列
#         rules = resolve_query.find_applicable_rules(self.rules)  # set left side bindings
#         if len(rules) == 0:
#             # print('NO APPLICABLE RULES FOUND.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')  # debug
#             print_and_log('NO APPLICABLE RULES FOUND.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')  # debug
#             # print('---------- resolve_clause-2 ---------')  # debug
#             print_and_log('---------- resolve_clause-2 ---------')  # debug
#             return succeeded, resolve_bindings_out
#         # print('APPLICABLE RULES WERE FOUND. NUMBER WAS ' + str(len(rules)))  # debug
#         print_and_log(f'APPLICABLE RULES WERE FOUND. NUMBER WAS {str(len(rules))}')  # debug
#         for rule_template in rules:
#             if rule_template.label.find('list_number_add_x_y_z') >= 0:  # debug
#                 pass  # debug
#             rule = ClassRule().build(ClassRules.graph, rule_template.label, rule_template.rule_left.label)
#             copy a rule
#             rule.modify_variables()  # x -> x1000, etc.
#             rule.rule_left.bindings = rule_template.rule_left.bindings
#             rule.rule_left.forward_bindings = rule_template.rule_left.forward_bindings
#             rule.rule_left.backward_bindings = rule_template.rule_left.backward_bindings
#             right_side_succeeded, resolve_bindings_array = self.resolve_rule(rule)
#             if right_side_succeeded:
#                 succeeded = True  # at least one rule is succeeded.
#                 # print('==RESOLVE BINDINGS: ', resolve_bindings_array)  # debug
#                 print_and_log(f'==RESOLVE BINDINGS: {resolve_bindings_array}')  # debug
#                 # print('=======RESOLVE SUCCEEDED=======')  # debug
#                 print_and_log('=======RESOLVE SUCCEEDED=======')  # debug
#                 resolve_bindings_array2 = []
#                 for resolve_bindings in resolve_bindings_array:
#                     resolve_bindings2 = {**resolve_bindings, **rule.rule_left.backward_bindings}  # merge two dict
#                     resolve_bindings_array2.append(resolve_bindings2)
#                 rule_return_bindings = []  # 不要なbindingを削除する。左辺の変数だけを返す。
#                 for binding in resolve_bindings_array2:
#                     return_dict = {}  # 戻り値の要素
#                     for var in resolve_query.list_of_variables:  # var: ClassTerm instance
#                         var_temp = var.to_var_string()  # 繰り返し置き換える。
#                         try:
#                             value_temp = binding[var_temp]  # key -> value (String)
#                             value_temp2 = ClassTerm().build(value_temp)  # string -> ClassTerm
#                             return_dict[var_temp] = value_temp2.to_var_string()  # stringに戻す。辞書に追加。
#                         except KeyError:
#                             pass
#                         except TypeError:
#                             pass
#                     rule_return_bindings += [return_dict]  # リストに追加
#                 if not rule_return_bindings:
#                     rule_return_bindings = [{'?dummy_key': 'dummy_value'}]
#                 if not self.find_all:
#                     # print('---------- resolve_clause-3 ---------')  # debug
#                     print_and_log('---------- resolve_clause-3 ---------')  # debug
#                     return succeeded, rule_return_bindings
#                 else:
#                     for bindings in rule_return_bindings:
#                         resolve_bindings_out.append(bindings)
#         # print('---------- resolve_clause-4 ---------')  # debug
#         print_and_log('---------- resolve_clause-4 ---------')  # debug
#         for bindings in resolve_bindings_out:
#             try:
#                 # xxx = bindings['?v1007']  # debug
#                 pass
#             except KeyError:
#                 pass
#         return succeeded, resolve_bindings_out
#     # end of resolve_clause
class FunctionHelper:
    """Class for function helper methods.
    All the methods are static.
    """

    @staticmethod
    def list_to_num(rdf_prolog: RdfProlog, list_number: str):
        """Convert a list number to an integer.
        http://value.org/list_five -> 5

        Args:
            rdf_prolog (RdfProlog): RdfProlog instance
            list_number (str): an integer represented as a list number

        Returns:
            int: an integer number

        """
        number_list = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
                       'eight': 8, 'nine': 9}  # conversion table
        return_number = 0  # initial value of an integer to be returned
        multiplier = 1  # multiplier for each digit of the integer
        while True:
            my_question_ \
                = f"""
                    SELECT ?car ?cdr WHERE {{
                    ?s1 <{OPERATION}> <{VAL}cons> . 
                    ?s1 <{VAL}variable_x> ?car . 
                    ?s1 <{VAL}variable_y> ?cdr . 
                    ?s1 <{VAL}variable_z> <{list_number}> . 
                    }}"""
            my_sparql_query = ClassSparqlQuery().set(my_question_).build_rule()
            resolve_bindings \
                = rdf_prolog.answer_question(
                    my_sparql_query,
                    depth_limit=300)  # get the car and cdr of the list number
            car = resolve_bindings[0]['?car']  # car part
            car_value = number_list[car.replace(VAL, '')]  # convert to an integer
            return_number += car_value * multiplier  # 345 = 5*1 + 4*10 + 3*100
            multiplier *= 10
            cdr = resolve_bindings[0]['?cdr']  # cdr part
            if cdr == f'{VAL}nil':  # no more digit exists
                break  # leave the while loop
            list_number = cdr  # repeat for the remaining, 345 -> 5 and 34
        return return_number

    @staticmethod
    def num_to_list(rdf_prolog: RdfProlog, num: int):
        """Convert integer number to a list number.

        Args:
            rdf_prolog (RdfProlog): RdfProlog instance holding all the info of list numbers
            num (int): an integer number to be converted

        Returns:
            str: list number

        """
        number_list = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven',
                       8: 'eight', 9: 'nine'}  # conversion table
        if num < 10:  # no more upper digits
            list_number = f'{VAL}{number_list[num]}'  # 2 -> http://value.org/two
            my_question_ = f"""
                    SELECT ?ans WHERE {{
                    ?s1 <{OPERATION}> <{VAL}cons> . 
                    ?s1 <{VAL}variable_x> <{list_number}> . 
                    ?s1 <{VAL}variable_y> <{VAL}nil> . 
                    ?s1 <{VAL}variable_z> ?ans . 
                    }}"""
            my_sparql_query = ClassSparqlQuery().set(my_question_).build_rule()
            resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=300)
            return resolve_bindings[0]['?ans']  # create a cons and return it
        else:  # num >=10, more digits exist
            quotient, remainder = divmod(num, 10)
            quotient_number = FunctionHelper.num_to_list(rdf_prolog, quotient)  # recursive call
            remainder_number = f'{VAL}{number_list[remainder]}'  # least significant digit
            my_question_ = f"""
                    SELECT ?ans WHERE {{
                    ?s1 <{OPERATION}> <{VAL}cons> . 
                    ?s1 <{VAL}variable_x> <{remainder_number}> . 
                    ?s1 <{VAL}variable_y> <{quotient_number}> . 
                    ?s1 <{VAL}variable_z> ?ans . 
                    }}"""
            my_sparql_query = ClassSparqlQuery().set(my_question_).build_rule()
            resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=300)
            return resolve_bindings[0]['?ans']  # create a cons and return it
        pass

    @staticmethod
    def function_list_cons(rdf_prolog: RdfProlog, bindings: dict[str, str]):
        """Execute cons operation for list numbers.
        Function called from function_function_cons.py

        Args:
            rdf_prolog (RdfProlog):
            bindings (dict[str, str]):

        Returns:
            str: list number of cons results

        """

        x = bindings[f'{VAR}_x']  # extract an argument x
        y = bindings[f'{VAR}_y']  # extract an argument y
        print(f'x: {x}')  # just for debug
        print(f'y: {y}')
        my_question_ = f"""
            SELECT ?car ?cdr WHERE {{
            ?s1 <{OPERATION}> <{VAL}cons> . 
            ?s1 <{VAL}variable_x> <{x}> . 
            ?s1 <{VAL}variable_y> <{y}> . 
            ?s1 <{VAL}variable_z> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question_).build_rule()
        resolve_bindings = rdf_prolog.answer_question(my_sparql_query, depth_limit=300)
        print(resolve_bindings[0]['?ans'])
        results = {bindings[f'{VAR}_z']: resolve_bindings[0]['?ans']}  # return the result
        return results

    @staticmethod
    def function_list_add(rdf_prolog: RdfProlog, bindings: dict[str, str]):
        """Execute add operation for list numbers.
        Function called from function_function_add.py

        Args:
            rdf_prolog (RdfProlog):
            bindings (dict[str, str]):

        Returns:
            str: list number of add results

        """

        x = bindings[f'{VAR}_x']  # extract an argument x
        y = bindings[f'{VAR}_y']  # extract an argument y
        print(f'x: {x}')  # just for debug
        print(f'y: {y}')
        x_num = FunctionHelper.list_to_num(rdf_prolog, x)  # convert a list number to an integer
        y_num = FunctionHelper.list_to_num(rdf_prolog, y)
        z_num = x_num + y_num  # add
        z = FunctionHelper.num_to_list(rdf_prolog, z_num)  # convert back to a list number

        results = {bindings[f'{VAR}_z']: z}  # return the result
        return results

    @staticmethod
    def function_list_multiply(rdf_prolog: RdfProlog, bindings: dict[str, str]):
        """Execute multiplication operation for list numbers.
        Function called from function_function_multiply.py

        Args:
            rdf_prolog (RdfProlog):
            bindings (dict[str, str]):

        Returns:
            str: list number of multiplication results

        """

        x = bindings[f'{VAR}_x']  # extract an argument x
        y = bindings[f'{VAR}_y']  # extract an argument y
        print(f'x: {x}')  # just for debug
        print(f'y: {y}')
        x_num = FunctionHelper.list_to_num(rdf_prolog, x)  # convert a list number to an integer
        y_num = FunctionHelper.list_to_num(rdf_prolog, y)
        z_num = x_num * y_num  # add
        z = FunctionHelper.num_to_list(rdf_prolog, z_num)  # convert back to a list number

        results = {bindings[f'{VAR}_z']: z}  # return the result
        return results


def main():
    """Main function for RdfProlog (This is just for test).
    True main entry is in RdfPrologMain.py

    Args:

    Returns:

    """
    start_log()
    # test search_order()
    if True:
        rdf_prolog = RdfProlog(rules_folder='../rules/rules_number_10')

        my_question_ = f"""
                      SELECT ?ans WHERE {{ 
                      ?s <{OPERATION}> <{VAL}add_number> . 
                      ?s <{VAL}variable_x> <{VAL}one> . 
                      ?s <{VAL}variable_y> ?ans . 
                      ?s <{VAL}variable_z> <{VAL}three> . 
                      }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question_).build_rule()
        # rdf_prolog.answer_question(my_sparql_query)

        my_question_ = f"""
              SELECT ?ans WHERE {{ 
                      ?s <{OPERATION}> <{VAL}add_number> . 
                      ?s <{VAL}variable_x> <{VAL}one> . 
                      ?s <{VAL}variable_y> ?ans . 
                      ?s <{VAL}variable_z> <{VAL}three> . 
                      }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question_).build_rule()
        # resolve_bindings = rdf_prolog.search_order(my_sparql_query, results_limit=30, depth_limit=30)
        # search the optimal order of processing clauses

        my_question_ = f"""
              SELECT ?ans WHERE {{ 
                      ?s <{OPERATION}> <{VAL}add_number> . 
                      ?s <{VAL}variable_x> ?ans . 
                      ?s <{VAL}variable_y> <{VAL}two> . 
                      ?s <{VAL}variable_z> <{VAL}four> . 
                      }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question_).build_rule()
        resolve_bindings = rdf_prolog.search_order(my_sparql_query, results_limit=30,
                                                   depth_limit=30)  # search the optimal order of processing clauses

        pass

    # rules_number
    if True:
        # rdf_prolog = RdfProlog(rules_folder='../rules/rules_number')

        # next(1, ?ans)
        my_question_ = f"""
            SELECT ?ans WHERE {{ 
            ?s <{OPERATION}> <{VAL}next_number> . 
            ?s <{VAL}variable_x> <{VAL}one> . 
            ?s <{VAL}variable_y> ?ans . 
            }}"""
        my_sparql_query = ClassSparqlQuery().set(my_question_).build_rule()
        # resolve_bindings = rdf_prolog.answer_question(my_sparql_query)
        pass

        # # next(?ans, 3)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s <{OPERATION}> <{VAL}next_number> .
        #     ?s <{VAL}variable_x> ?ans .
        #     ?s <{VAL}variable_y> <{VAL}three> .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
        # pass
        #
        # # next(1, 2)
        # my_question = f"""
        #     SELECT ?s WHERE {{
        #     ?s <{OPERATION}> <{VAL}next_number> .
        #     ?s <{VAL}variable_x> <{VAL}one> .
        #     ?s <{VAL}variable_y> <{VAL}two> .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
        # pass
        #
        # # next(1, 3)
        # my_question = f"""
        #     SELECT ?s WHERE {{
        #     ?s <{OPERATION}> <{VAL}next_number> .
        #     ?s <{VAL}variable_x> <{VAL}one> .
        #     ?s <{VAL}variable_y> <{VAL}three> .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
        # pass
        #
        # # next(1, ?z),next(?z, ?ans)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s1 <{OPERATION}> <{VAL}next_number> .
        #     ?s1 <{VAL}variable_x> <{VAL}one> .
        #     ?s1 <{VAL}variable_y> ?z .
        #     ?s2 <{OPERATION}> <{VAL}next_number> .
        #     ?s2 <{VAL}variable_x> ?z .
        #     ?s2 <{VAL}variable_y> ?ans .
        #     }}"""
        #
        # # next(1, ?z),next(?z, ?x)
        # my_question = f"""
        #     SELECT ?x WHERE {{
        #     ?s1 <{OPERATION}> <{VAL}next_number> .
        #     ?s1 <{VAL}variable_x> <{VAL}one> .
        #     ?s1 <{VAL}variable_y> ?z .
        #     ?s2 <{OPERATION}> <{VAL}next_number> .
        #     ?s2 <{VAL}variable_x> ?z .
        #     ?s2 <{VAL}variable_y> ?x .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
        # pass
        #
        # # next(?x, ?y)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s <{OPERATION}> <{VAL}next_number> .
        #     ?s <{VAL}variable_x> ?x .
        #     ?s <{VAL}variable_y> ?y .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
        # pass
        #
        # # add(3, 1, ?ans)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s <{OPERATION}> <{VAL}add_number> .
        #     ?s <{VAL}variable_x> <{VAL}three> .
        #     ?s <{VAL}variable_y> <{VAL}one> .
        #     ?s <{VAL}variable_z> ?ans .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
        #
        # # add(3, 1, ?z)
        # my_question = f"""
        #     SELECT ?z WHERE {{
        #     ?s <{OPERATION}> <{VAL}add_number> .
        #     ?s <{VAL}variable_x> <{VAL}three> .
        #     ?s <{VAL}variable_y> <{VAL}one> .
        #     ?s <{VAL}variable_z> ?z .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
        # pass
        #
        # # add(2, 2, ?ans)
        # my_question = f"""
        #     SELECT ?ans WHERE {{ ?s <{OPERATION}> <{VAL}add_number> .
        #     ?s <{VAL}variable_x> <{VAL}two> .
        #     ?s <{VAL}variable_y> <{VAL}two> .
        #     ?s <{VAL}variable_z> ?z .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
        # # pass
        #
        # # add(3, 2, ?ans)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s <{OPERATION}> <{VAL}add_number> .
        #     ?s <{VAL}variable_x> <{VAL}three> .
        #     ?s <{VAL}variable_y> <{VAL}two> .
        #     ?s <{VAL}variable_z> ?ans .
        #     }}"""
        #
        # # add(3, 2, ?z)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s <{OPERATION}> <{VAL}add_number> .
        #     ?s <{VAL}variable_x> <{VAL}three> .
        #     ?s <{VAL}variable_y> <{VAL}two> .
        #     ?s <{VAL}variable_z> ?z .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
        # pass
        #
        # # add(3, 2, ?z), next(?z, ?ans)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s1 <{OPERATION}> <{VAL}add_number> .
        #     ?s1 <{VAL}variable_x> <{VAL}three> .
        #     ?s1 <{VAL}variable_y> <{VAL}two> .
        #     ?s1 <{VAL}variable_z> ?z .
        #     ?s2 <{OPERATION}> <{VAL}next_number> .
        #     ?s2 <{VAL}variable_x> ?z .
        #     ?s2 <{VAL}variable_y> ?ans .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
        # pass
        #
        # # add(3, 2, ?z), add(?z, 2, ?ans) -> 3+2+2 = 7
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s1 <{OPERATION}> <{VAL}add_number> .
        #     ?s1 <{VAL}variable_x> <{VAL}three> .
        #     ?s1 <{VAL}variable_y> <{VAL}two> .
        #     ?s1 <{VAL}variable_z> ?z .
        #     ?s2 <{OPERATION}> <{VAL}add_number> .
        #     ?s2 <{VAL}variable_x> ?z .
        #     ?s2 <{VAL}variable_y> <{VAL}two> .
        #     ?s2 <{VAL}variable_z> ?ans .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
        # pass
        #
        # # add(2, ?ans, 3)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s <{OPERATION}> <{VAL}add_number> .
        #     ?s <{VAL}variable_x> <{VAL}two> .
        #     ?s <{VAL}variable_y> ?ans .
        #     ?s <{VAL}variable_z> <{VAL}three> .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # rdf_prolog.answer_complex_question(my_sparql_query)
        #
        # # add(3, ?ans, 5)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s <{OPERATION}> <{VAL}add_number> .
        #     ?s <{VAL}variable_x> <{VAL}three> .
        #     ?s <{VAL}variable_y> ?ans .
        #     ?s <{VAL}variable_z> <{VAL}five> .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # rdf_prolog.answer_complex_question(my_sparql_query)
        #
        # # add(1, ?y, ?z)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s <{OPERATION}> <{VAL}add_number> .
        #     ?s <{VAL}variable_x> <{VAL}one> .
        #     ?s <{VAL}variable_y> ?y .
        #     ?s <{VAL}variable_z> ?z .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query, results_limit=10)
        # pass
        #
        # # add(9, ?y, ?z)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s <{OPERATION}> <{VAL}add_number> .
        #     ?s <{VAL}variable_x> <{VAL}nine> .
        #     ?s <{VAL}variable_y> ?y .
        #     ?s <{VAL}variable_z> ?z .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query, results_limit=10)
        # pass
        #
        # # grandfather(taro, ?ans)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s <{OPERATION}> <{VAL}grandfather> .
        #     ?s <{VAL}variable_x> <{VAL}taro> .
        #     ?s <{VAL}variable_y> ?ans .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # rdf_prolog.answer_complex_question(my_sparql_query)
        #
        # # mortal(?ans)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s <{OPERATION}> <{VAL}mortal> .
        #     ?s <{VAL}variable_x> ?ans .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # rdf_prolog.answer_complex_question(my_sparql_query)
        #
        # # knows(andy, bob)
        # my_question = f"""
        #     SELECT ?s WHERE {{
        #     ?s <{OPERATION}> <{VAL}knows_direct> .
        #     ?s <{VAL}variable_x> <{VAL}andy> .
        #     ?s <{VAL}variable_y> <{VAL}bob> .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # rdf_prolog.answer_complex_question(my_sparql_query)
        #
        # # knows_direct(andy, chris)
        # my_question = f"""
        #     SELECT ?s WHERE {{
        #     ?s <{OPERATION}> <{VAL}knows_direct> .
        #     ?s <{VAL}variable_x> <{VAL}andy> .
        #     ?s <{VAL}variable_y> <{VAL}chris> .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # rdf_prolog.answer_complex_question(my_sparql_query)
        #
        # # knows_direct(andy, ?ans)
        # my_question = f"""
        #     SELECT ?s ?ans WHERE {{
        #     ?s <{OPERATION}> <{VAL}knows_direct> .
        #     ?s <{VAL}variable_x> <{VAL}andy> .
        #     ?s <{VAL}variable_y> ?ans .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # rdf_prolog.answer_complex_question(my_sparql_query)
        #
        # # knows_indirect(andy, chris)
        # my_question = f"""
        #     SELECT ?s WHERE {{
        #     ?s <{OPERATION}> <{VAL}knows_indirect> .
        #     ?s <{VAL}variable_x> <{VAL}andy> .
        #     ?s <{VAL}variable_y> <{VAL}chris> .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # rdf_prolog.answer_complex_question(my_sparql_query)
        #
        # # knows_indirect(andy, edgar)
        # my_question = f"""
        #     SELECT ?s WHERE {{
        #     ?s <{OPERATION}> <{VAL}knows_indirect> .
        #     ?s <{VAL}variable_x> <{VAL}andy> .
        #     ?s <{VAL}variable_y> <{VAL}edgar> .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # rdf_prolog.answer_complex_question(my_sparql_query)
        #
        # # knows_indirect(andy, ?ans)
        # my_question = f"""
        #     SELECT ?s WHERE {{
        #     ?s <{OPERATION}> <{VAL}knows_indirect> .
        #     ?s <{VAL}variable_x> <{VAL}andy> .
        #     ?s <{VAL}variable_y> ?ans .
        #     }}"""
        # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
        # # rdf_prolog.answer_complex_question(my_sparql_query)
        #
        # # knows(andy, ?ans)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s <{OPERATION}> <{VAL}knows> . ' \
        #     ?s <{VAL}variable_x> <{VAL}andy> . ' \
        #     ?s <{VAL}variable_y> ?ans . ' \
        #     }}"""
        # my_sparql_query = ClassSparqlQuery(rdf_prolog.g_rules).set(my_question).build_rule()
        # # rdf_prolog.answer_complex_question(my_sparql_query)
        #
        # # subtract(5, 3, ?ans)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s <{OPERATION}> <{VAL}subtract_number> . ' \
        #     ?s <{VAL}variable_x> <{VAL}five> . ' \
        #     ?s <{VAL}variable_y> <{VAL}three> . ' \
        #     ?s <{VAL}variable_z> ?ans . ' \
        #     }}"""
        # my_sparql_query = ClassSparqlQuery(rdf_prolog.g_rules).set(my_question).build_rule()
        # # rdf_prolog.answer_complex_question(my_sparql_query)
        #
        # # subtract(3, 2, ?ans)
        # my_question = f"""
        #     SELECT ?ans WHERE {{
        #     ?s <{OPERATION}> <{VAL}subtract_number> . ' \
        #     ?s <{VAL}variable_x> <{VAL}three> . ' \
        #     ?s <{VAL}variable_y> <{VAL}two> . ' \
        #     ?s <{VAL}variable_z> ?ans . ' \
        #     }}"""
        # my_sparql_query = ClassSparqlQuery(rdf_prolog.g_rules).set(my_question).build_rule()
        # # rdf_prolog.answer_complex_question(my_sparql_query)
        pass


if __name__ == '__main__':  # test execution
    main()  # execute the main function
