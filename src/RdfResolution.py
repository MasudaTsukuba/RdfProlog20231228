"""Module for reasoning
RdfResolution.py
Execute Prolog on RDF query system
2022/12/20, 2023/3/16, 2023/10/30, 2023/11/6, 2023/11/28
T. Masuda
"""

import os
import rdflib.term
from rdflib import Graph, URIRef, BNode, Variable
from src.RdfClass import *  # ClassClauses, ClassClause, ClassRule, ClassRules, ClassRuleRight, ClassSparqlQuery, ClassTerm


class RdfProlog:  # Prolog Class, prepare a graph and available rules
    """Prolog Class, prepare a graph and available rules.

    Attributes:

    """
    def __init__(self, rules_folder='../rules/rules_human'):
        """Initialize the RdfProlog class.

        Create a Graph g_rules for storing facts and rules.

        Prepare applicable rules from the left sides of the rules.

        Args:
            rules_folder (str): Folder where the RDFs describing rules exist.

        Returns:
            None
        """
        # print('$$$$$$$$$$ PREPARING $$$$$$$$$$')  # debug
        logging.debug('$$$$$$$$$$ PREPARING $$$$$$$$$$')  # debug
        self.find_all = False  # stop the search if the first result is obtained.
        # self.find_all = True  # find all the results using inferences.

        graph = Graph()  # graph for facts and rules
        g_temp = Graph()  # temporary graph for reading RDF files
        self.rules_folder: str = rules_folder  # folder where the RDFs describing rules exist.
        files = os.listdir(self.rules_folder)
        for file in files:  # read all the turtle files in rules folder
            if file.endswith('.ttl'):
                g_temp.parse(f'{self.rules_folder}/{file}')

        results = g_temp.query('SELECT ?s ?p ?o WHERE { ?s ?p ?o . }')  # retrieve all the triples read in
        for result in results:
            ss = result['s']
            pp = result['p']
            oo = result['o']
            if isinstance(ss, BNode):  # convert blank node to URI
                ss = f'http://value.org/{str(ss)}'
            if isinstance(oo, BNode):
                oo = f'http://value.org/{str(oo)}'
            graph.add((URIRef(ss), URIRef(pp), URIRef(oo)))
        self.facts = ClassFacts(graph)
        self.rules = ClassRules(graph)  # set the rules in ClassRules class
        self.controls = ClassControls(graph)
        self.applications = ClassApplications(graph)
        print('$$$$$$$$$$ PREPARATION COMPLETED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')  # debug
        logging.debug('$$$$$$$$$$ PREPARATION COMPLETED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')  # debug
        # print()  # line feed
        logging.debug('')  # line feed

    def answer_question(self, sparql_query, find_all: bool = False, max_depth: int = 30):  # answer a sparql query with multiple clauses
        """Answer a SPARQL query with multiple clauses.

        Args:
            sparql_query
            find_all (bool): if true, find all the possible answers.
            max_depth (int): maximum depth of resolution.

        Returns:
            list[dict[str, str]]: list of binding
        """
        self.find_all = find_all  # if true, find all the possible answers
        # resolution = Resolution(self.rules, self.find_all, max_depth)  # create an instance of Resolution class, left_rules: ClassLeftRules
        # resolve_succeeded, resolve_bindings \
        #     = resolution.resolve_rule(sparql_query.rule)  # execute the resolution / resolve rule
        reasoner = Reasoner(self, self.find_all, max_depth)
        clauses_in = sparql_query.to_clauses()
        resolve_succeeded, resolve_bindings_temp = reasoner.reasoner(clauses_in, depth=1)  # start from depth = 1
        resolve_bindings = []
        for binding in resolve_bindings_temp:
            binding_revised = {}
            for key, value in binding.items():
                binding_revised[key.replace('http://variable.org/', '?')] = value
            resolve_bindings.append(binding_revised)

        if resolve_succeeded:
            print('answer_complex_question: RESOLVE SUCCEEDED')
            logging.debug('answer_complex_question: RESOLVE SUCCEEDED')
            print('sparql_query: ', sparql_query.query)  # input query
            logging.debug(f'sparql_query: {sparql_query.query}')  # input query
            print('resolve_bindings: ', resolve_bindings)  # results
            logging.debug(f'resolve_bindings: {resolve_bindings}')  # results
            for binding in resolve_bindings:
                try:
                    for var in clauses_in.list_of_variables:
                        var_name = var.to_var_string()
                        print(var_name, ': ', binding[var_name])  # if the query contains a variable ?ans
                        logging.debug(f'{var_name}: {binding[var_name]}')  # if the query contains a variable ?ans
                except KeyError:
                    pass
                except Exception as e:
                    print(e)
                    logging.debug(e)
                    pass
            print('===================================================================================================')
            logging.debug('===================================================================================================')
            return resolve_bindings
        else:  # failed
            print('answer_complex_question: RESOLVE FAILED xxxxxxxxxxxxx')
            logging.debug('answer_complex_question: RESOLVE FAILED xxxxxxxxxxxxx')
            print('resolve_bindings: ', resolve_bindings)
            logging.debug(f'resolve_bindings: {resolve_bindings}')
            print('===================================================================================================')
            logging.debug('===================================================================================================')
            return []


class Reasoner:
    """Execute the depth first search for reasoning.

    Attributes:
        find_all (bool): find all the possible answers.
        max_depth (int): maximum depth of recursive call.
    """
    def __init__(self, rdf_prolog, find_all=False, max_depth: int = 30):
        self.rdf_prolog = rdf_prolog
        self.find_all = find_all  # find all the possible answers
        self.max_depth = max_depth  # maximum depth of recursive call

    def reasoner(self, clauses: ClassClauses, depth=0):
        """Execute the depth first search.

        Args:
            clauses (ClassClauses):
            # bindings_in:
            depth:

        Returns:

        """
        print('reasoner: depth=', depth)  # for debug
        if depth > self.max_depth:  # if the depth reaches the max_depth, return with failure
            print(f'Max depth reached: {depth}')  #
            return False, []  # success = False, list_of_bindings = None
        first_clause, rest_clauses = clauses.split_clauses()  # split the clauses into the first and the remainder
        if first_clause is None or len(first_clause.list_of_triple) == 0:
            return True, [{}]  # success = True, list_of_bindings = [{}]
        list_of_bindings_return = []  # list of bindings to be returned
        success_out = False  # flag for success
        print('first clause: ', first_clause.predicate_object_dict)  # debug

        # try facts
        list_of_bindings_current = first_clause.search_facts(self.rdf_prolog)  # find facts that match the first clause
        print('search facts: ', len(list_of_bindings_current), list_of_bindings_current)  # debug
        for bindings_current in list_of_bindings_current:  # repeat for multiple possibilities
            rest_clauses_applied = rest_clauses.apply_bindings(bindings_current)  # apply the bindings to the remainder of clauses
            success, list_of_bindings_fact = self.reasoner(rest_clauses_applied, depth)  # recursive call
            if success:  # find some results
                success_out = True  # at least one trial is successful
                list_of_bindings_out = [{**bindings_current, **bindings_fact} for bindings_fact in list_of_bindings_fact]  # combine the bindings
                list_of_bindings_return += list_of_bindings_out  # add to the list
                if not self.find_all:  # at least one trial is successful
                    return success_out, list_of_bindings_out  # return the first answer

        # try applications
        print('trying applications')
        applications = []  # start the rule search
        try:
            applications = self.rdf_prolog.applications.operation_names_dict[first_clause.operation_name_uri]  # possible rules are already summarized in ClassRules object
            print('number of applications: ', len(applications))
            for application in applications:  # repeat for each rule
                matched, list_of_application_clauses, list_of_bindings_forward, list_of_bindings_backward = first_clause.match_application(application)  # match the rule against the query
                for application_clauses, bindings_forward, bindings_backward in zip(list_of_application_clauses, list_of_bindings_forward, list_of_bindings_backward):
                    combined_clauses = application_clauses.combine(rest_clauses)  # combine the clauses
                    application_clauses_applied = combined_clauses.apply_bindings({**bindings_forward, **bindings_backward})  # apply the bindings
                    for clause in application_clauses_applied.list_of_clauses:  # debug
                        print(clause.predicate_object_dict)
                    success, list_of_bindings_application = self.reasoner(application_clauses_applied, depth+1)  # recursive call with +1 depth
                    if success:
                        success_out = True
                        list_of_bindings_out = [{**bindings_backward, **bindings_application} for bindings_application in list_of_bindings_application]
                        list_of_bindings_return += list_of_bindings_out
                        if not self.find_all:
                            return True, list_of_bindings_out
        except KeyError as e:
            print('applications not found', e)
        print('return, depth=', depth)
        return success_out, list_of_bindings_return


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
#     def __init__(self, rules, find_all: bool, max_depth: int):
#         """
#         initialize Resolution class
#
#         """
#         # self.graph = graph  # set the knowledge graph
#         self.rules = rules  # ClassRules(graph)
#         self.find_all = find_all  # find all possible answers
#         self.max_depth = max_depth  # maximum depth of resolution
#         pass
#
#     def resolve_recursive(self, right_clauses: ClassClauses) -> (bool, list[dict[str, str]]):  # resolve_bindings_in 辞書の配列
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
#         print('++++++++++ resolve_recursive ++++++++++')  # debug
#         logging.debug('++++++++++ resolve_recursive ++++++++++')  # debug
#         if len(right_clauses) == 0:  # clauseが無くなったら再帰呼び出しを終了して戻る。
#             return True, []  # resolution=success, 辞書の配列の配列を返す。
#         else:  # 右側にまだclauseがある時。
#             print('[', Resolution.resolve_right_recursive_count, '] ENTERING resolve_recursive')  # debug
#             logging.debug(f'[{Resolution.resolve_right_recursive_count}] ENTERING resolve_recursive')  # debug
#             Resolution.resolve_right_recursive_count += 1  # 再帰呼び出しの深さをup。debug
#             if Resolution.resolve_right_recursive_count > self.max_depth:  # exceeds max_depth of resolution  # 2023/11/7
#                 Resolution.resolve_right_recursive_count -= 1
#                 return False, []
#             grandchild_rules, right_clauses_sub = right_clauses.split_clauses()  # first clauseを取り出す, rest of clausesは後で処理する。
#             built_query = ClassSparqlQuery().set('SELECT ?s ?p ?o WHERE {?s ?p ?o .}')  # dummy query
#             built_query.build_query(grandchild_rules)  # resolveを呼び出すためのクエリ
#             succeeded, bindings_array = self.resolve_clause(built_query)  # execute resolve
#             # 戻り値のbindings_arrayは辞書の配列
#             if len(bindings_array) > 1:  # debug
#                 pass  # debug
#             if not succeeded:  # resolve failed
#                 print('---------- resolve_right_recursive-1 ---------')  # debug for execution trace
#                 logging.debug('---------- resolve_right_recursive-1 ---------')  # debug for execution trace
#                 Resolution.resolve_right_recursive_count -= 1  # debug 再帰呼び出しの深さを戻す
#                 return False, []  # 失敗で戻る
#
#             resolve_bindings_out = []  # 戻り値の初期化
#             return_succeeded = False  # succeeded  # 戻り値  # initially assume False
#             print('%%% bindings_array: ', bindings_array)  # debug  # return value of resolve_clause
#             logging.debug(f'%%% bindings_array: {bindings_array}')  # debug  # return value of resolve_clause
#             iteration = 1  # 横方向の分岐の数 debug
#
#             for bindings in bindings_array:  # bindings は辞書、bindings_arrayは辞書の配列、resolve_clauseの戻り値
#                 print(iteration, '??? bindings: ', bindings, '<<< ', bindings_array)  # debug
#                 logging.debug(f'{iteration} ??? bindings: {bindings}<<< {bindings_array}')  # debug
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
#                         print('r_bindings: ', r_bindings)  # results of the first clause
#                         logging.debug(f'r_bindings: {r_bindings}')  # results of the first clause
#                         temp = [r_bindings]
#                         if resolve_bindings_array:  # results of the rest clauses, if it is not null
#                             temp = []
#                             for bindings1 in resolve_bindings_array:
#                                 r_bindings1 = r_bindings.copy()  # 2023/11/6
#                                 print('+++', bindings1)  # debug
#                                 logging.debug(f'+++{bindings1}')  # debug
#                                 if bindings1:
#                                     r_bindings1.update(bindings1)  # append to the dict
#                                     temp.append(r_bindings1)  # append to the list
#                         resolve_bindings_out += temp
#                 else:
#                     pass  # do nothing
#             print('[', Resolution.resolve_right_recursive_count,
#                   '] ==resolve_bindings_out IN resolve_right_recursive: ',
#                   resolve_bindings_out)  # debug
#             logging.debug(f'[{Resolution.resolve_right_recursive_count}] ==resolve_bindings_out IN resolve_right_recursive: {resolve_bindings_out}')  # debug
#             print('---------- resolve_right_recursive-2 ---------')  # debug
#             logging.debug('---------- resolve_right_recursive-2 ---------')  # debug
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
#         print('++++++++++ resolve_rule ++++++++++')  # debug
#         logging.debug('++++++++++ resolve_rule ++++++++++')  # debug
#
#         def build_argument_bindings_for_left(bindings_for_left: dict[rdflib.term.Variable, str]) -> dict[str, str]:  # 左辺の変数をチェック
#             """
#             左辺の変数をチェック
#
#             Args:
#                 bindings_for_left (dict[rdflib.term.Variable, str]): {x: 'http://value.org/two', y: 'http://value.org/two', z: 'http://variable.org/z'}
#
#             Returns:
#                 dict[str, str]: {'x1000': '<http://value.org/two>', '?y1000': '<http://value.org/two>'. '?z1000': '?z'}
#             """
#             print('BINDINGS FOR LEFT: ' + str(bindings_for_left))  # debug
#             logging.debug(f'BINDINGS FOR LEFT: {str(bindings_for_left)}')  # debug
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
#                 my_value = ClassTerm().build(str(bindings_for_left[item]))  # my_value is also an instance of ClassTerm
#                 argument_bindings_built[my_term.to_var_string()] = my_value.to_var_string()  # return value
#             print('ARGUMENT BINDINGS: ' + str(argument_bindings_built))
#             logging.debug(f'ARGUMENT BINDINGS: {str(argument_bindings_built)}')
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
#     def resolve_clause(self, resolve_query: ClassSparqlQuery) -> (bool, list[dict[str, str]]):  # resolve a single clause
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
#         print('++++++++++ resolve_clause ++++++++++')  # debug
#         logging.debug('++++++++++ resolve_clause ++++++++++')  # debug
#         # global find_all  # if True, find all the results.
#         succeeded = False  # final result of success. firstly assumed to be failed.
#         resolve_bindings_out: list[dict[str, str]] = []  # initialize bindings to be returned
#         direct_search_succeeded, returned_direct_search_bindings = resolve_query.direct_search()  # direct search
#         if direct_search_succeeded:
#             succeeded = True  # final result is also set succeeded.
#             resolve_bindings_out += returned_direct_search_bindings
#         if not direct_search_succeeded:
#             print('DIRECT ANSWERS WERE NOT FOUND. TRYING TO FIND APPLICABLE RULES. ')  # debug
#             logging.debug('DIRECT ANSWERS WERE NOT FOUND. TRYING TO FIND APPLICABLE RULES. ')  # debug
#         if not self.find_all:
#             if direct_search_succeeded:
#                 print('======= LEAVING RESOLVE, AFTER FINDING DIRECT ANSWER =======')  # debug
#                 logging.debug('======= LEAVING RESOLVE, AFTER FINDING DIRECT ANSWER =======')  # debug
#                 print('---------- resolve_clause-1 ---------')  # debug
#                 logging.debug('---------- resolve_clause-1 ---------')  # debug
#                 return True, resolve_bindings_out  # 辞書の配列
#         rules = resolve_query.find_applicable_rules(self.rules)  # set left side bindings
#         if len(rules) == 0:
#             print('NO APPLICABLE RULES FOUND.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')  # debug
#             logging.debug('NO APPLICABLE RULES FOUND.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')  # debug
#             print('---------- resolve_clause-2 ---------')  # debug
#             logging.debug('---------- resolve_clause-2 ---------')  # debug
#             return succeeded, resolve_bindings_out
#         print('APPLICABLE RULES WERE FOUND. NUMBER WAS ' + str(len(rules)))  # debug
#         logging.debug(f'APPLICABLE RULES WERE FOUND. NUMBER WAS {str(len(rules))}')  # debug
#         for rule_template in rules:
#             if rule_template.label.find('list_number_add_x_y_z') >= 0:  # debug
#                 pass  # debug
#             rule = ClassRule().build(ClassRules.graph, rule_template.label, rule_template.rule_left.label)  # copy a rule
#             rule.modify_variables()  # x -> x1000, etc.
#             rule.rule_left.bindings = rule_template.rule_left.bindings
#             rule.rule_left.forward_bindings = rule_template.rule_left.forward_bindings
#             rule.rule_left.backward_bindings = rule_template.rule_left.backward_bindings
#             right_side_succeeded, resolve_bindings_array = self.resolve_rule(rule)
#             if right_side_succeeded:
#                 succeeded = True  # at least one rule is succeeded.
#                 print('==RESOLVE BINDINGS: ', resolve_bindings_array)  # debug
#                 logging.debug(f'==RESOLVE BINDINGS: {resolve_bindings_array}')  # debug
#                 print('=======RESOLVE SUCCEEDED=======')  # debug
#                 logging.debug('=======RESOLVE SUCCEEDED=======')  # debug
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
#                     print('---------- resolve_clause-3 ---------')  # debug
#                     logging.debug('---------- resolve_clause-3 ---------')  # debug
#                     return succeeded, rule_return_bindings
#                 else:
#                     for bindings in rule_return_bindings:
#                         resolve_bindings_out.append(bindings)
#         print('---------- resolve_clause-4 ---------')  # debug
#         logging.debug('---------- resolve_clause-4 ---------')  # debug
#         for bindings in resolve_bindings_out:
#             try:
#                 # xxx = bindings['?v1007']  # debug
#                 pass
#             except KeyError:
#                 pass
#         return succeeded, resolve_bindings_out
#     # end of resolve_clause


def main():
    """Main function for RdfProlog (This is for test).

    Args:

    Returns:

    """
    rdf_prolog = RdfProlog()

    # next(1, ?ans)
    my_question = f"""
        SELECT ?ans WHERE {{ 
        ?s <http://value.org/operation> <http://value.org/next_number> . 
        ?s <http://value.org/variable_x> <http://value.org/one> . 
        ?s <http://value.org/variable_y> ?ans . 
        }}"""
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # # next(?ans, 3)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/next_number> .
    #     ?s <http://value.org/variable_x> ?ans .
    #     ?s <http://value.org/variable_y> <http://value.org/three> .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    # pass
    #
    # # next(1, 2)
    # my_question = f"""
    #     SELECT ?s WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/next_number> .
    #     ?s <http://value.org/variable_x> <http://value.org/one> .
    #     ?s <http://value.org/variable_y> <http://value.org/two> .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    # pass
    #
    # # next(1, 3)
    # my_question = f"""
    #     SELECT ?s WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/next_number> .
    #     ?s <http://value.org/variable_x> <http://value.org/one> .
    #     ?s <http://value.org/variable_y> <http://value.org/three> .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    # pass
    #
    # # next(1, ?z),next(?z, ?ans)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s1 <http://value.org/operation> <http://value.org/next_number> .
    #     ?s1 <http://value.org/variable_x> <http://value.org/one> .
    #     ?s1 <http://value.org/variable_y> ?z .
    #     ?s2 <http://value.org/operation> <http://value.org/next_number> .
    #     ?s2 <http://value.org/variable_x> ?z .
    #     ?s2 <http://value.org/variable_y> ?ans .
    #     }}"""
    #
    # # next(1, ?z),next(?z, ?x)
    # my_question = f"""
    #     SELECT ?x WHERE {{
    #     ?s1 <http://value.org/operation> <http://value.org/next_number> .
    #     ?s1 <http://value.org/variable_x> <http://value.org/one> .
    #     ?s1 <http://value.org/variable_y> ?z .
    #     ?s2 <http://value.org/operation> <http://value.org/next_number> .
    #     ?s2 <http://value.org/variable_x> ?z .
    #     ?s2 <http://value.org/variable_y> ?x .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    # pass
    #
    # # next(?x, ?y)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/next_number> .
    #     ?s <http://value.org/variable_x> ?x .
    #     ?s <http://value.org/variable_y> ?y .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    # pass
    #
    # # add(3, 1, ?ans)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/add_number> .
    #     ?s <http://value.org/variable_x> <http://value.org/three> .
    #     ?s <http://value.org/variable_y> <http://value.org/one> .
    #     ?s <http://value.org/variable_z> ?ans .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query, find_all=False)
    #
    # # add(3, 1, ?z)
    # my_question = f"""
    #     SELECT ?z WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/add_number> .
    #     ?s <http://value.org/variable_x> <http://value.org/three> .
    #     ?s <http://value.org/variable_y> <http://value.org/one> .
    #     ?s <http://value.org/variable_z> ?z .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    # pass
    #
    # # add(2, 2, ?ans)
    # my_question = f"""
    #     SELECT ?ans WHERE {{ ?s <http://value.org/operation> <http://value.org/add_number> .
    #     ?s <http://value.org/variable_x> <http://value.org/two> .
    #     ?s <http://value.org/variable_y> <http://value.org/two> .
    #     ?s <http://value.org/variable_z> ?z .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    # # pass
    #
    # # add(3, 2, ?ans)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/add_number> .
    #     ?s <http://value.org/variable_x> <http://value.org/three> .
    #     ?s <http://value.org/variable_y> <http://value.org/two> .
    #     ?s <http://value.org/variable_z> ?ans .
    #     }}"""
    #
    # # add(3, 2, ?z)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/add_number> .
    #     ?s <http://value.org/variable_x> <http://value.org/three> .
    #     ?s <http://value.org/variable_y> <http://value.org/two> .
    #     ?s <http://value.org/variable_z> ?z .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    # pass
    #
    # # add(3, 2, ?z), next(?z, ?ans)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s1 <http://value.org/operation> <http://value.org/add_number> .
    #     ?s1 <http://value.org/variable_x> <http://value.org/three> .
    #     ?s1 <http://value.org/variable_y> <http://value.org/two> .
    #     ?s1 <http://value.org/variable_z> ?z .
    #     ?s2 <http://value.org/operation> <http://value.org/next_number> .
    #     ?s2 <http://value.org/variable_x> ?z .
    #     ?s2 <http://value.org/variable_y> ?ans .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    # pass
    #
    # # add(3, 2, ?z), add(?z, 2, ?ans) -> 3+2+2 = 7
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s1 <http://value.org/operation> <http://value.org/add_number> .
    #     ?s1 <http://value.org/variable_x> <http://value.org/three> .
    #     ?s1 <http://value.org/variable_y> <http://value.org/two> .
    #     ?s1 <http://value.org/variable_z> ?z .
    #     ?s2 <http://value.org/operation> <http://value.org/add_number> .
    #     ?s2 <http://value.org/variable_x> ?z .
    #     ?s2 <http://value.org/variable_y> <http://value.org/two> .
    #     ?s2 <http://value.org/variable_z> ?ans .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    # pass
    #
    # # add(2, ?ans, 3)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/add_number> .
    #     ?s <http://value.org/variable_x> <http://value.org/two> .
    #     ?s <http://value.org/variable_y> ?ans .
    #     ?s <http://value.org/variable_z> <http://value.org/three> .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # rdf_prolog.answer_complex_question(my_sparql_query)
    #
    # # add(3, ?ans, 5)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/add_number> .
    #     ?s <http://value.org/variable_x> <http://value.org/three> .
    #     ?s <http://value.org/variable_y> ?ans .
    #     ?s <http://value.org/variable_z> <http://value.org/five> .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # rdf_prolog.answer_complex_question(my_sparql_query)
    #
    # # add(1, ?y, ?z)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/add_number> .
    #     ?s <http://value.org/variable_x> <http://value.org/one> .
    #     ?s <http://value.org/variable_y> ?y .
    #     ?s <http://value.org/variable_z> ?z .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query, find_all=True)
    # pass
    #
    # # add(9, ?y, ?z)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/add_number> .
    #     ?s <http://value.org/variable_x> <http://value.org/nine> .
    #     ?s <http://value.org/variable_y> ?y .
    #     ?s <http://value.org/variable_z> ?z .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query, find_all=True)
    # pass
    #
    # # grandfather(taro, ?ans)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/grandfather> .
    #     ?s <http://value.org/variable_x> <http://value.org/taro> .
    #     ?s <http://value.org/variable_y> ?ans .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # rdf_prolog.answer_complex_question(my_sparql_query)
    #
    # # mortal(?ans)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/mortal> .
    #     ?s <http://value.org/variable_x> ?ans .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # rdf_prolog.answer_complex_question(my_sparql_query)
    #
    # # knows(andy, bob)
    # my_question = f"""
    #     SELECT ?s WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/knows_direct> .
    #     ?s <http://value.org/variable_x> <http://value.org/andy> .
    #     ?s <http://value.org/variable_y> <http://value.org/bob> .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # rdf_prolog.answer_complex_question(my_sparql_query)
    #
    # # knows_direct(andy, chris)
    # my_question = f"""
    #     SELECT ?s WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/knows_direct> .
    #     ?s <http://value.org/variable_x> <http://value.org/andy> .
    #     ?s <http://value.org/variable_y> <http://value.org/chris> .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # rdf_prolog.answer_complex_question(my_sparql_query)
    #
    # # knows_direct(andy, ?ans)
    # my_question = f"""
    #     SELECT ?s ?ans WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/knows_direct> .
    #     ?s <http://value.org/variable_x> <http://value.org/andy> .
    #     ?s <http://value.org/variable_y> ?ans .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # rdf_prolog.answer_complex_question(my_sparql_query)
    #
    # # knows_indirect(andy, chris)
    # my_question = f"""
    #     SELECT ?s WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/knows_indirect> .
    #     ?s <http://value.org/variable_x> <http://value.org/andy> .
    #     ?s <http://value.org/variable_y> <http://value.org/chris> .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # rdf_prolog.answer_complex_question(my_sparql_query)
    #
    # # knows_indirect(andy, edgar)
    # my_question = f"""
    #     SELECT ?s WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/knows_indirect> .
    #     ?s <http://value.org/variable_x> <http://value.org/andy> .
    #     ?s <http://value.org/variable_y> <http://value.org/edgar> .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # rdf_prolog.answer_complex_question(my_sparql_query)
    #
    # # knows_indirect(andy, ?ans)
    # my_question = f"""
    #     SELECT ?s WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/knows_indirect> .
    #     ?s <http://value.org/variable_x> <http://value.org/andy> .
    #     ?s <http://value.org/variable_y> ?ans .
    #     }}"""
    # my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # # rdf_prolog.answer_complex_question(my_sparql_query)
    #
    # # knows(andy, ?ans)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/knows> . ' \
    #     ?s <http://value.org/variable_x> <http://value.org/andy> . ' \
    #     ?s <http://value.org/variable_y> ?ans . ' \
    #     }}"""
    # my_sparql_query = ClassSparqlQuery(rdf_prolog.g_rules).set(my_question).build_rule()
    # # rdf_prolog.answer_complex_question(my_sparql_query)
    #
    # # subtract(5, 3, ?ans)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/subtract_number> . ' \
    #     ?s <http://value.org/variable_x> <http://value.org/five> . ' \
    #     ?s <http://value.org/variable_y> <http://value.org/three> . ' \
    #     ?s <http://value.org/variable_z> ?ans . ' \
    #     }}"""
    # my_sparql_query = ClassSparqlQuery(rdf_prolog.g_rules).set(my_question).build_rule()
    # # rdf_prolog.answer_complex_question(my_sparql_query)
    #
    # # subtract(3, 2, ?ans)
    # my_question = f"""
    #     SELECT ?ans WHERE {{
    #     ?s <http://value.org/operation> <http://value.org/subtract_number> . ' \
    #     ?s <http://value.org/variable_x> <http://value.org/three> . ' \
    #     ?s <http://value.org/variable_y> <http://value.org/two> . ' \
    #     ?s <http://value.org/variable_z> ?ans . ' \
    #     }}"""
    # my_sparql_query = ClassSparqlQuery(rdf_prolog.g_rules).set(my_question).build_rule()
    # # rdf_prolog.answer_complex_question(my_sparql_query)


if __name__ == '__main__':
    main()  # execute the main function
