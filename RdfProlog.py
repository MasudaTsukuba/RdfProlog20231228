"""
RdfProlog
Executing Prolog on RDF query system
2022/12/20, 2023/3/16, 2023/10/30
T. Masuda
"""
import rdflib
from rdflib import Graph, URIRef, BNode, Variable

# import ConvertQuery
from ConvertQuery import convert_question
from PR import PR
from VAR import VAR

# find_all = False
find_all = True


class RdfProlog:  # Prolog Class, prepare a graph and available rules
    def __init__(self):
        """initialize the RdfProlog class

            create a Graph g_rules for storing facts and rules

            prepare applicable rules from the left sides of the rules

            Args:

            Returns:
                None
            """
        # print('$$$$$$$$$$ PREPARING $$$$$$$$$$')  # debug
        self.g_rules = Graph()  # graph for facts and rules
        g_temp = Graph()  # temporary graph for reading RDF files
        g_temp.parse('rules/rules_human.ttl')
        g_temp.parse('rules/rules_grandfather.ttl')
        g_temp.parse('rules/rules_next_number.ttl')
        g_temp.parse('rules/rules_add_number.ttl')
        g_temp.parse('rules/rules_knows.ttl')
        results = g_temp.query('SELECT ?s ?p ?o WHERE { ?s ?p ?o . }')
        for result in results:
            ss = result['s']
            pp = result['p']
            oo = result['o']
            if type(ss) == BNode:  # convert blank node to URI
                ss = f'{PR.url}{str(ss)}'
            if type(oo) == BNode:
                oo = f'{PR.url}{str(oo)}'
            self.g_rules.add((URIRef(ss), URIRef(pp), URIRef(oo)))
        self.rules = ClassRules(self.g_rules)
        # print('$$$$$$$$$$ PREPARATION COMPLETED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')  # debug
        print()  # line feed

    def answer_question(self, sparql_query):  # answer to sparql query by invoking resolve
        print('QUERY: ', sparql_query.query)  # debug
        resolution = Resolution(self.g_rules, self.rules)  # create an instance.  # left_rules: ClassLeftRules
        resolve_succeeded, resolve_results, resolve_bindings = resolution.resolve_clause(sparql_query)  # resolve a single clause
        print('RESULTS FOR:', sparql_query.query)  # print the query results
        if resolve_succeeded:
            for result in resolve_results:
                print('ANSWER: ' + str(result))
            print('BINDINGS: ' + str(resolve_bindings))
            print('===================================================================================================')
            return resolve_results, resolve_bindings
        else:
            print('resolution failed')
            print('===================================================================================================')
            return [], []

    def answer_complex_question(self, sparql_query):  # answer a sparql query with multiple clauses
        resolution = Resolution(self.g_rules, self.rules)  # left_rules: ClassLeftRules
        resolve_succeeded, resolve_bindings \
            = resolution.resolve_rule(sparql_query.rule)  # execute the resolution
        if resolve_succeeded:
            print('answer_complex_question: RESOLVE SUCCEEDED')
            print('sparql_query: ', sparql_query.query)
            print('resolve_bindings: ', resolve_bindings)
            for binding in resolve_bindings:
                try:
                    print('?ans: ', binding['?ans'])
                except KeyError:
                    pass
                except:
                    pass
            print('===================================================================================================')
            return resolve_bindings
        else:
            print('answer_complex_question: RESOLVE FAILED xxxxxxxxxxxxx')
            print('resolve_bindings: ', resolve_bindings)
            print('===================================================================================================')
            return []


class Resolution:  # main class for resolution
    resolve_right_recursive_count = 0  # indicate the depth of recursive call.  # for debug

    def __init__(self, graph, rules):
        self.graph = graph  # set the knowledge graph
        self.rules = rules  # ClassRules(graph)
        pass

    """
    # resolve_right_recursiveはルールの右側のclauseを順番に再帰呼び出しで処理する。
    # １つのclauseが複数の結果を返す場合があるので、処理がツリー状に分岐する。
    # 第２戻り値は辞書の配列
    入力：
        right_clauses: 処理するルールの右側
        resolve_bindings_in: 変数と値を結びつける辞書の配列
    出力：
        succeeded: 結果が得られた時True
        bindings: 変数と値を結びつける辞書の配列
    """
    def resolve_recursive(self, right_clauses):  # resolve_bindings_in 辞書の配列
        print('++++++++++ resolve_right_recursive ++++++++++')  # debug
        if len(right_clauses) == 0:  # clauseが無くなったら再帰呼び出しを終了して戻る。
            return True, []  # resolution=success, 辞書の配列の配列を返す。
        else:  # 右側にまだclauseがある時。
            print('[', Resolution.resolve_right_recursive_count, '] ENTERING resolve_right_recursive')  # debug
            Resolution.resolve_right_recursive_count += 1  # 再帰呼び出しの深さを更新。debug
            grandchild_rules = right_clauses[0]  # first clauseを取り出す。
            right_clauses_sub = right_clauses[1:]  # rest clausesは後で処理する。
            built_query = ClassSparqlQuery().set('SELECT ?s ?p ?o WHERE {?s ?p ?o .}')  # dummy query
            built_query.build_query(grandchild_rules)  # resolveを呼び出すためのクエリ
            succeeded, bindings_array = self.resolve_clause(built_query)  # execute resolve
            # 戻り値のbindings_arrayは辞書の配列
            if len(bindings_array) > 1:  # debug
                pass  # debug
            if not succeeded:  # resolve failed
                Resolution.resolve_right_recursive_count -= 1  # debug 再帰呼び出しの深さを戻す
                print('---------- resolve_right_recursive-1 ---------')
                return False, []  # 失敗で戻る
            resolve_bindings_out = []  # 戻り値の初期化
            return_succeeded = False  # succeeded  # 戻り値
            print('%%% bindings_array: ', bindings_array)  # debug
            iteration = 1  # 横方向の分岐の数 debug

            for bindings in bindings_array:  # bindings は辞書、bindings_arrayは辞書の配列、resolve_clauseの戻り値
                print(iteration, '??? bindings: ', bindings, '<<< ', bindings_array)  # debug
                iteration += 1  # 横方向の分岐のレベル  debug
                return_bindings = [bindings]
                right_clauses_sub_revised = []  # 右辺の修正したもの
                for right_clause in right_clauses_sub:  # 右辺の各項を修正
                    right_clause_revised = ClassRuleRight()  # 新規にインスタンスを作る
                    right_clause_revised.revise(right_clause, bindings)  # 修正の実行
                    right_clauses_sub_revised += [right_clause_revised]  # 修正したものを追加。
                    pass
                resolve_succeeded, resolve_bindings_array \
                    = self.resolve_recursive(right_clauses_sub_revised)  # 再帰呼び出し
                if resolve_succeeded:
                    return_succeeded = True  # at least one trial was successful
                    for r_bindings in return_bindings:  # results of the first clause
                        temp = [r_bindings]
                        if resolve_bindings_array:  # results of the rest clauses
                            temp = []
                            for bdgs in resolve_bindings_array:
                                print(r_bindings, bdgs)  # debug
                                if bdgs:
                                    r_bindings.update(bdgs)  # append to the dict
                                    temp.append(r_bindings)  # append to the list
                        resolve_bindings_out += temp
                else:
                    pass
                Resolution.resolve_right_recursive_count -= 1  # depth of recursive call.  # debug
            print('[', Resolution.resolve_right_recursive_count,
                  '] ==resolve_bindings_out IN resolve_right_recursive: ',
                  resolve_bindings_out)  # debug
            print('---------- resolve_right_recursive-2 ---------')  # debug
            return return_succeeded, resolve_bindings_out

    """ 
    resolve_ruleはルールを処理する。
    ルールとして呼び出された場合には左側が評価されてargument_bindingsが生成される。
    クエリとして呼び出された場合には、左側は評価されない。ルールに左側が設定されていない。
    実際の処理はresolve_right_recursiveが行う。
    入力：
        rule: 処理するルール
        resolve_bindings_in: 変数と値を結びつける辞書の配列
    出力：
        succeeded: 結果が得られた時True
        bindings: 変数と値を結びつける辞書  ####の配列
    """
    def resolve_rule(self, rule):  # resolve multiple clauses
        # ルールの左辺と一致するようの変数をbindingする。戻り値は辞書型。
        print('++++++++++ resolve_rule ++++++++++')  # debug

        def build_argument_bindings_for_left(bindings_for_left):  # 左辺の変数をチェック
            print('BINDINGS FOR LEFT: ' + str(bindings_for_left))
            argument_bindings_built = {}
            # print('(DEBUG) TYPE OF BINDING[0]: '+str(type(binding)))
            # print('(DEBUG) LENGTH OF BINDING: ', len(binding))
            for item in bindings_for_left:
                my_key = str(item)
                if type(item) == Variable:
                    my_key = '?' + my_key
                    try:
                        my_key = rule.variables_dict[my_key]  # ?x ->?x1000, etc.
                    except KeyError:
                        pass
                my_term = ClassTerm().build(my_key)
                my_value = ClassTerm().build(str(bindings_for_left[item]))
                argument_bindings_built[my_term.to_var()] = my_value.to_var()
            print('ARGUMENT BINDINGS: ' + str(argument_bindings_built))
            return argument_bindings_built

        argument_binding = build_argument_bindings_for_left(rule.rule_left.bindings)  # argument_bindingは辞書型
        right_clauses_sub_revised = []  # argument_bindingに基づいて右辺を修正する。
        for right_clause in rule.rule_right:  # 右側には複数の節が含まれる可能性がある。
            right_clause_revised = ClassRuleRight().revise(right_clause, argument_binding)  # 新規に節を作り直す。
            right_clauses_sub_revised += [right_clause_revised]  # 修正した項を追加していく。
            pass
        resolve_right_bindings_in = []  # [argument_binding]  右辺の項を修正したのでbindingsは不要。
        right_side_succeeded, resolve_bindings_array \
            = self.resolve_recursive(right_clauses_sub_revised)  # ルールの右辺を評価
        return right_side_succeeded, resolve_bindings_array

    """ 
    resolve_clauseは１つのclauseを対象にする
    戻り値のbindings[]は２つ以上の辞書を含む場合がある。
    knows_direct(andy, ?ans)に対する、bob, davidのような場合。
    入力：
        resolve_query: 処理するクエリ＝節
        resolve_bindings_in: 変数と値を結びつける辞書の配列
    出力：
        succeeded: 結果が得られた時True
        bindings: 変数と値を結びつける辞書の配列
    """
    def resolve_clause(self, resolve_query):  # resolve a single clause
        print('++++++++++ resolve_clause ++++++++++')  # debug
        global find_all  # if True, find all the results.
        succeeded = False  # final result of success. first assumed to be failed.
        resolve_bindings_out = []  # initialize bindings to be returned
        direct_search_succeeded, returned_direct_search_bindings \
            = resolve_query.direct_search(self.graph)  # direct search
        if direct_search_succeeded:
            succeeded = True  # final result is also set succeeded.
            resolve_bindings_out += returned_direct_search_bindings
        if not direct_search_succeeded:
            print('DIRECT ANSWERS WERE NOT FOUND. TRYING TO FIND APPLICABLE RULES. ')
        if not find_all:
            if direct_search_succeeded:
                print('======= LEAVING RESOLVE, AFTER FINDING DIRECT ANSWER =======')
                print('---------- resolve_clause-1 ---------')
                return True, resolve_bindings_out  # 辞書の配列
        rules = resolve_query.find_applicable_rules(self.rules)  # set left side bindings
        if len(rules) == 0:
            print('NO APPLICABLE RULES FOUND.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            print('---------- resolve_clause-2 ---------')
            return succeeded, resolve_bindings_out
        print('APPLICABLE RULES WERE FOUND. NUMBER WAS ' + str(len(rules)))
        for rule_template in rules:
            rule = ClassRule().build(self.graph, rule_template.label, rule_template.rule_left.label)
            rule.modify_variables()  # x -> x1000, etc.
            rule.rule_left.bindings = rule_template.rule_left.bindings
            right_side_succeeded, resolve_bindings_array = self.resolve_rule(rule)
            if right_side_succeeded:
                succeeded = True  # at least one rule is succeeded.
                print('==RESOLVE BINDINGS: ', resolve_bindings_array)
                print('=======RESOLVE SUCCEEDED=======')
                rule_return_bindings = []  # 不要なbindingを削除する。左辺の変数だけを返す。
                for binding in resolve_bindings_array:
                    return_dict = {}  # 戻り値の要素
                    for var in resolve_query.list_of_variables:  # var: ClassTerm instance
                        var_temp = var  # 繰り返し置き換える。
                        try:
                            value_temp = binding[var_temp.to_var()]  # key -> value (String)
                            var_temp = ClassTerm().build(value_temp)  # string -> ClassTerm
                            return_dict[var.to_var()] = var_temp.to_var()  # stringに戻す。辞書に追加。
                        except KeyError:
                            pass
                        except TypeError:
                            pass
                    rule_return_bindings += [return_dict]  # リストに追加
                if not rule_return_bindings:
                    rule_return_bindings = [{'?dummy_key': 'dummy_value'}]
                if not find_all:
                    print('---------- resolve_clause-3 ---------')
                    return succeeded, rule_return_bindings
                else:
                    for bindings in rule_return_bindings:
                        resolve_bindings_out.append(bindings)
        print('---------- resolve_clause-4 ---------')
        return succeeded, resolve_bindings_out


class ClassRules:  # list of rules
    def __init__(self, graph):
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
    serial_number = 1000  # a variable to convert variables: x -> x1000

    def __init__(self):
        self.label = ''
        self.rule_left = ClassRuleLeft()
        self.rule_right = []
        self.variables_dict = {}

    def build(self, graph, rule_label, rule_left_label):
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
    def __init__(self):
        self.label = None
        self.content = None
        self.bindings = {}
        self.var_list = []

    def build(self, graph, rule_left_label):  # executed at the initial stage
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
    def __init__(self):
        self.child = ClassRuleRightChild()  # right side has one child, which in turn has one or more grandchild

    def build(self, graph, right_side_for_child):  # executed at the initial stage
        # print('CHILD RULE: ' + str(right_side_for_child[0]))  # debug
        query_for_child = f'SELECT ?o where {{ <{str(right_side_for_child[0])}> <{PR.child}> ?o .}} '
        results_of_right_side_child = graph.query(query_for_child)  # query by the child name
        self.child.build(graph, results_of_right_side_child.bindings[0])
        return self

    def revise(self, right_clauses, bindings):  # bindingsは辞書型
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
    def __init__(self):  # child has grandchildren
        self.grandchildren = []

    def build(self, graph, result_for_grandchild):  # build the right side of a rule
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
        for grandchild in clause.child.grandchildren:
            grandchild_revised = ClassRightGrandChild()  # create a new grandchild
            new_term = grandchild.triple.subject.revise(bindings)
            grandchild_revised.triple.subject.build(new_term)  # revise the subject
            grandchild_revised.triple.predicate.build(grandchild.triple.predicate.revise(bindings))  # predicate
            grandchild_revised.triple.object.build(grandchild.triple.object.revise(bindings))  # object
            self.grandchildren.append(grandchild_revised)  # append the revised grandchild


class ClassRightGrandChild:  # grandchild of a rule having one triple
    def __init__(self):
        self.triple = ClassTriple()

    def build(self, triple_for_grandchild):
        self.triple.build(triple_for_grandchild)
        return self


class ClassTriple:  # triple class
    def __init__(self):  # triple has subject, predicate and object
        self.subject = ClassTerm()
        self.predicate = ClassTerm()
        self.object = ClassTerm()

    def build(self, triple):  # triple is a dict
        self.subject.build(triple['s'])
        self.predicate.build(triple['p'])
        self.object.build(triple['o'])


class ClassTerm:  # term is either subject, predicate or object
    def __init__(self):  # initialize
        self.term_text = ''
        self.is_variable = False

    def build(self, term_text):  # extract text element
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

    def to_uriref(self):
        return URIRef('http://variable.org/variable_' + self.term_text)

    def to_uri(self):
        if self.is_variable:
            return '<http://variable.org/variable_' + self.term_text + '>'  # x -> <http://variable.org/variable_x>
        else:
            return '<' + self.term_text + '>'  # http://example.org/andy -> <http://example.org/andy>

    def to_var(self):
        if self.is_variable:
            return '?' + self.term_text  # http://variable.org/x -> ?x
        else:
            return self.to_uri()  # http://example.org/andy -> <http://example.org/andy>

    def force_to_var(self):
        return '?' + self.term_text.replace('http://example.org/', '')  # http://example.org/x -> ?x

    def revise(self, bindings):  # bindings: dict
        term_text = self.to_var()  # if VAR x -> ?x, else http://example.org/andy -> <http://example.org/andy>
        try:
            if len(bindings) > 0:
                try:
                    term_text2 = bindings[term_text]
                    return term_text2  # return the value in the dict
                except KeyError:
                    pass
                except:
                    pass
        except:
            pass
        return term_text  # if not in bindings, return as is


class ClassSparqlQuery:  # Sparql Query Class
    def __init__(self):  # initialize the sparql query class instance
        self.query = None
        self.list_of_rdfs = []  # rdfs is an array of clauses
        self.list_of_variables = []  # list of variables
        self.rule = ClassRule()  # empty rule

    def set(self, sparql_query):  # convert from aprql query string
        self.query = sparql_query  # sparql_query is a string
        self.list_of_rdfs = []  # rdfs is an array of clauses
        self.build_variable_list()
        list_of_rdfs_temp = convert_question(self.query)
        list_of_clauses = []  # clause is an array of triples that have the same subject
        previous_subject = None
        first = True  # switch indicating the initial processing
        for rdf in list_of_rdfs_temp:  # rdf is an array of [s, p, o]
            dummy = {'s': 'Dummy', 'p': 'Dummy', 'o': 'Dummy'}  # dummy dict
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
        variable_str = self.query.replace('SELECT ', '')  # extract a string between 'SELECT' and 'WHERE'
        variable_str = variable_str[:variable_str.find(' WHERE')]
        list_of_variables_temp = variable_str.split(' ')  # split the string and convert to a list
        self.list_of_variables = [ClassTerm().build(var) for var in list_of_variables_temp]  # create a list of variables
        pass

    def build_query(self, results_for_build_query):  # build a query string
        try:
            var_list = ''  # variables list for replacing $VAR_LIST
            query_for_resolve = f'SELECT $VAR_LIST WHERE {{ '  # start the query string
            term_subject = None  # for suppressing the warning of not defined before assignment
            for triple_for_build_query in results_for_build_query.child.grandchildren:  # extract each triple of a rule
                term_subject = ClassTerm().build(triple_for_build_query.triple.subject.force_to_var())  # subject
                term_predicate = ClassTerm().build(triple_for_build_query.triple.predicate.to_uri())  # predicate
                term_object = ClassTerm().build(triple_for_build_query.triple.object.to_var())  # object
                print('PREDICATE AND OBJECT: ' + str(term_predicate.to_uri()) + ' ' + str(term_object.to_var()))  # debug
                term_value1 = term_object
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
                my_var = term_value1

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
        except:
            print('Something has happened in ClassSparqlQuery.build_query().')
            pass

    def direct_search(self, graph):  # find a triple in the graph that directly matches the query
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
                        if type(key) == rdflib.term.Variable:  # in the case of a variable
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


def main():
    rdf_prolog = RdfProlog()

    # next(1, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.next_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.one}> . ' \
        f'?s <{PR.variable_y}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # next(?ans, 3)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.next_number}> . ' \
        f'?s <{PR.variable_x}> ?ans . ' \
        f'?s <{PR.variable_y}> <{PR.three}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # next(1, 2)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <{PR.operation}> <{PR.next_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.one}> . ' \
        f'?s <{PR.variable_y}> <{PR.two}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # next(1, 3)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <{PR.operation}> <{PR.next_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.one}> . ' \
        f'?s <{PR.variable_y}> <{PR.three}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # next(1, ?z),next(?z, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s1 <{PR.operation}> <{PR.next_number}> . ' \
        f'?s1 <{PR.variable_x}> <{PR.one}> . ' \
        f'?s1 <{PR.variable_y}> ?z . ' \
        f'?s2 <{PR.operation}> <{PR.next_number}> . ' \
        f'?s2 <{PR.variable_x}> ?z . ' \
        f'?s2 <{PR.variable_y}> ?ans . ' \
        f'}}'
    # next(1, ?z),next(?z, ?x)
    my_question = \
        f'SELECT ?x WHERE {{' \
        f'?s1 <{PR.operation}> <{PR.next_number}> . ' \
        f'?s1 <{PR.variable_x}> <{PR.one}> . ' \
        f'?s1 <{PR.variable_y}> ?z . ' \
        f'?s2 <{PR.operation}> <{PR.next_number}> . ' \
        f'?s2 <{PR.variable_x}> ?z . ' \
        f'?s2 <{PR.variable_y}> ?x . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # add(3, 1, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.add_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.three}> . ' \
        f'?s <{PR.variable_y}> <{PR.one}> . ' \
        f'?s <{PR.variable_z}> ?ans . ' \
        f'}}'
    # add(3, 1, ?z)
    my_question = \
        f'SELECT ?z WHERE {{' \
        f'?s <{PR.operation}> <{PR.add_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.three}> . ' \
        f'?s <{PR.variable_y}> <{PR.one}> . ' \
        f'?s <{PR.variable_z}> ?z . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # add(2, 2, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{ ?s <{PR.operation}> <{PR.add_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.two}> . ' \
        f'?s <{PR.variable_y}> <{PR.two}> . ' \
        f'?s <{PR.variable_z}> ?z . ' \
        f'}} '
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # add(3, 2, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.add_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.three}> . ' \
        f'?s <{PR.variable_y}> <{PR.two}> . ' \
        f'?s <{PR.variable_z}> ?ans . ' \
        f'}}'
    # add(3, 2, ?z)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.add_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.three}> . ' \
        f'?s <{PR.variable_y}> <{PR.two}> . ' \
        f'?s <{PR.variable_z}> ?z . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # add(3, 2, ?z), next(?z, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s1 <{PR.operation}> <{PR.add_number}> . ' \
        f'?s1 <{PR.variable_x}> <{PR.three}> . ' \
        f'?s1 <{PR.variable_y}> <{PR.two}> . ' \
        f'?s1 <{PR.variable_z}> ?z . ' \
        f'?s2 <{PR.operation}> <{PR.next_number}> . ' \
        f'?s2 <{PR.variable_x}> ?z . ' \
        f'?s2 <{PR.variable_y}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # add(3, 2, ?z), add(?z, 2, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s1 <{PR.operation}> <{PR.add_number}> . ' \
        f'?s1 <{PR.variable_x}> <{PR.three}> . ' \
        f'?s1 <{PR.variable_y}> <{PR.two}> . ' \
        f'?s1 <{PR.variable_z}> ?z . ' \
        f'?s2 <{PR.operation}> <{PR.add_number}> . ' \
        f'?s2 <{PR.variable_x}> ?z . ' \
        f'?s2 <{PR.variable_y}> <{PR.two}> . ' \
        f'?s2 <{PR.variable_z}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # add(3, ?ans, 5)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.add_number}> . ' \
        f'?s <{PR.variable_x}> <{PR.three}> . ' \
        f'?s <{PR.variable_y}> ?ans . ' \
        f'?s <{PR.variable_z}> <{PR.five}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # grandfather(taro, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.grandfather}> . ' \
        f'?s <{PR.variable_x}> <{PR.taro}> . ' \
        f'?s <{PR.variable_y}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # mortal(?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.mortal}> . ' \
        f'?s <{PR.variable_x}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # knows(andy, bob)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <{PR.operation}> <{PR.knows_direct}> . ' \
        f'?s <{PR.variable_x}> <{PR.andy}> . ' \
        f'?s <{PR.variable_y}> <{PR.bob}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # knows_direct(andy, chris)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <{PR.operation}> <{PR.knows_direct}> . ' \
        f'?s <{PR.variable_x}> <{PR.andy}> . ' \
        f'?s <{PR.variable_y}> <{PR.chris}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # knows_direct(andy, ?ans)
    my_question = \
        f'SELECT ?s ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.knows_direct}> . ' \
        f'?s <{PR.variable_x}> <{PR.andy}> . ' \
        f'?s <{PR.variable_y}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # knows_indirect(andy, chris)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <{PR.operation}> <{PR.knows_indirect}> . ' \
        f'?s <{PR.variable_x}> <{PR.andy}> . ' \
        f'?s <{PR.variable_y}> <{PR.chris}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # knows_indirect(andy, edgar)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <{PR.operation}> <{PR.knows_indirect}> . ' \
        f'?s <{PR.variable_x}> <{PR.andy}> . ' \
        f'?s <{PR.variable_y}> <{PR.edgar}> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # knows_indirect(andy, ?ans)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <{PR.operation}> <{PR.knows_indirect}> . ' \
        f'?s <{PR.variable_x}> <{PR.andy}> . ' \
        f'?s <{PR.variable_y}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # knows(andy, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <{PR.operation}> <{PR.knows}> . ' \
        f'?s <{PR.variable_x}> <{PR.andy}> . ' \
        f'?s <{PR.variable_y}> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    rdf_prolog.answer_complex_question(my_sparql_query)


if __name__ == '__main__':
    main()
