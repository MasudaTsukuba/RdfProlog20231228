"""
RdfProlog
Executing Prolog on RDF query system
2022/12/20, 2023/3/16, 2023/10/30
T. Masuda
"""
import os

# import rdflib
from rdflib import Graph, URIRef, BNode, Variable
# from src.PR import PR
from src.RdfClass import ClassRule, ClassRules, ClassRuleRight, ClassSparqlQuery, ClassTerm

find_all = False  # stop the search if the first result is obtained.
# find_all = True  # find all the results using inferences.


class RdfProlog:  # Prolog Class, prepare a graph and available rules
    """
    Prolog Class, prepare a graph and available rules
    """
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
        files = os.listdir('rules')
        for file in files:
            g_temp.parse(f'rules/{file}')
        # g_temp.parse('rules/rules_human.ttl')
        # g_temp.parse('rules/rules_grandfather.ttl')
        # g_temp.parse('rules/rules_next_number.ttl')
        # g_temp.parse('rules/rules_add_number.ttl')
        # g_temp.parse('rules/rules_knows.ttl')
        results = g_temp.query('SELECT ?s ?p ?o WHERE { ?s ?p ?o . }')
        for result in results:
            ss = result['s']
            pp = result['p']
            oo = result['o']
            if isinstance(ss, BNode):  # convert blank node to URI
                ss = f'http://example.org/{str(ss)}'
            if isinstance(oo, BNode):
                oo = f'http://example.org/{str(oo)}'
            self.g_rules.add((URIRef(ss), URIRef(pp), URIRef(oo)))
        self.rules = ClassRules(self.g_rules)
        # print('$$$$$$$$$$ PREPARATION COMPLETED $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')  # debug
        print()  # line feed

    def answer_question(self, sparql_query):  # answer to sparql query by invoking resolve
        """answer to sparql query by invoking resolve
            Args:
                sparql_query
            Returns:
                None
        """
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
        """answer a sparql query with multiple clauses
            Args:
                sparql_query
            Returns:
                None
        """
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
                except Exception as e:
                    print(e)
                    pass
            print('===================================================================================================')
            return resolve_bindings
        else:
            print('answer_complex_question: RESOLVE FAILED xxxxxxxxxxxxx')
            print('resolve_bindings: ', resolve_bindings)
            print('===================================================================================================')
            return []


class Resolution:  # main class for resolution
    """
    main class for resolution
    """
    resolve_right_recursive_count = 0  # indicate the depth of recursive call.  # for debug

    def __init__(self, graph, rules):
        """
        initialize Resolution class
        :param graph:
        :param rules:
        """
        self.graph = graph  # set the knowledge graph
        self.rules = rules  # ClassRules(graph)
        pass

    def resolve_recursive(self, right_clauses):  # resolve_bindings_in 辞書の配列
        """
        resolve_right_recursiveはルールの右側のclauseを順番に再帰呼び出しで処理する。

        １つのclauseが複数の結果を返す場合があるので、処理がツリー状に分岐する。

        第２戻り値は辞書の配列

        入力：
            right_clauses: 処理するルールの右側

            resolve_bindings_in: 変数と値を結びつける辞書の配列
        出力：
            succeeded: 結果が得られた時True

            bindings: 変数と値を結びつける辞書の配列

        resolve recursively
        :param right_clauses:
        :return:
        """
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
                            for bindings1 in resolve_bindings_array:
                                print(r_bindings, bindings1)  # debug
                                if bindings1:
                                    r_bindings.update(bindings1)  # append to the dict
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

    def resolve_rule(self, rule):  # resolve multiple clauses
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

        resolve multiple clauses
        :param rule:

        :return:
        """
        # ルールの左辺と一致するようの変数をbindingする。戻り値は辞書型。
        print('++++++++++ resolve_rule ++++++++++')  # debug

        def build_argument_bindings_for_left(bindings_for_left):  # 左辺の変数をチェック
            """
            左辺の変数をチェック
            :param bindings_for_left:
            :return:
            """
            print('BINDINGS FOR LEFT: ' + str(bindings_for_left))  # debug
            argument_bindings_built = {}
            # print('(DEBUG) TYPE OF BINDING[0]: '+str(type(binding)))
            # print('(DEBUG) LENGTH OF BINDING: ', len(binding))
            for item in bindings_for_left:
                my_key = str(item)
                if isinstance(item, Variable):
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
        # resolve_right_bindings_in = []  # [argument_binding]  右辺の項を修正したのでbindingsは不要。
        right_side_succeeded, resolve_bindings_array \
            = self.resolve_recursive(right_clauses_sub_revised)  # ルールの右辺を評価
        return right_side_succeeded, resolve_bindings_array

    def resolve_clause(self, resolve_query):  # resolve a single clause
        """
        resolve_clauseは１つのclauseを対象にする。

        戻り値のbindings[]は２つ以上の辞書を含む場合がある。

        knows_direct(andy, ?ans)に対する、bob, davidのような場合。

        入力：
            resolve_query: 処理するクエリ＝節

            resolve_bindings_in: 変数と値を結びつける辞書の配列
        出力：
            succeeded: 結果が得られた時True

            bindings: 変数と値を結びつける辞書の配列
        resolve a single clause
        :param resolve_query:
        :return:
        """
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
            print('DIRECT ANSWERS WERE NOT FOUND. TRYING TO FIND APPLICABLE RULES. ')  # debug
        if not find_all:
            if direct_search_succeeded:
                print('======= LEAVING RESOLVE, AFTER FINDING DIRECT ANSWER =======')  # debug
                print('---------- resolve_clause-1 ---------')  # debug
                return True, resolve_bindings_out  # 辞書の配列
        rules = resolve_query.find_applicable_rules(self.rules)  # set left side bindings
        if len(rules) == 0:
            print('NO APPLICABLE RULES FOUND.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')  # debug
            print('---------- resolve_clause-2 ---------')  # debug
            return succeeded, resolve_bindings_out
        print('APPLICABLE RULES WERE FOUND. NUMBER WAS ' + str(len(rules)))  # debug
        for rule_template in rules:
            rule = ClassRule().build(self.graph, rule_template.label, rule_template.rule_left.label)
            rule.modify_variables()  # x -> x1000, etc.
            rule.rule_left.bindings = rule_template.rule_left.bindings
            right_side_succeeded, resolve_bindings_array = self.resolve_rule(rule)
            if right_side_succeeded:
                succeeded = True  # at least one rule is succeeded.
                print('==RESOLVE BINDINGS: ', resolve_bindings_array)  # debug
                print('=======RESOLVE SUCCEEDED=======')  # debug
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
                    print('---------- resolve_clause-3 ---------')  # debug
                    return succeeded, rule_return_bindings
                else:
                    for bindings in rule_return_bindings:
                        resolve_bindings_out.append(bindings)
        print('---------- resolve_clause-4 ---------')  # debug
        return succeeded, resolve_bindings_out


def main():
    """
    main function for RdfProlog
    :return:
    """
    rdf_prolog = RdfProlog()

    # next(1, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/one> . ' \
        f'?s <http://example.org/variable_y> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # next(?ans, 3)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s <http://example.org/variable_x> ?ans . ' \
        f'?s <http://example.org/variable_y> <http://example.org/three> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # next(1, 2)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/one> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/two> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # next(1, 3)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/one> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/three> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # next(1, ?z),next(?z, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s1 <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s1 <http://example.org/variable_x> <http://example.org/one> . ' \
        f'?s1 <http://example.org/variable_y> ?z . ' \
        f'?s2 <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s2 <http://example.org/variable_x> ?z . ' \
        f'?s2 <http://example.org/variable_y> ?ans . ' \
        f'}}'
    # next(1, ?z),next(?z, ?x)
    my_question = \
        f'SELECT ?x WHERE {{' \
        f'?s1 <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s1 <http://example.org/variable_x> <http://example.org/one> . ' \
        f'?s1 <http://example.org/variable_y> ?z . ' \
        f'?s2 <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s2 <http://example.org/variable_x> ?z . ' \
        f'?s2 <http://example.org/variable_y> ?x . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # add(3, 1, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/three> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/one> . ' \
        f'?s <http://example.org/variable_z> ?ans . ' \
        f'}}'
    # add(3, 1, ?z)
    my_question = \
        f'SELECT ?z WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/three> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/one> . ' \
        f'?s <http://example.org/variable_z> ?z . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # add(2, 2, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{ ?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/two> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/two> . ' \
        f'?s <http://example.org/variable_z> ?z . ' \
        f'}} '
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # add(3, 2, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/three> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/two> . ' \
        f'?s <http://example.org/variable_z> ?ans . ' \
        f'}}'
    # add(3, 2, ?z)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/three> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/two> . ' \
        f'?s <http://example.org/variable_z> ?z . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # add(3, 2, ?z), next(?z, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s1 <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s1 <http://example.org/variable_x> <http://example.org/three> . ' \
        f'?s1 <http://example.org/variable_y> <http://example.org/two> . ' \
        f'?s1 <http://example.org/variable_z> ?z . ' \
        f'?s2 <http://example.org/operation> <http://example.org/next_number> . ' \
        f'?s2 <http://example.org/variable_x> ?z . ' \
        f'?s2 <http://example.org/variable_y> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # add(3, 2, ?z), add(?z, 2, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s1 <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s1 <http://example.org/variable_x> <http://example.org/three> . ' \
        f'?s1 <http://example.org/variable_y> <http://example.org/two> . ' \
        f'?s1 <http://example.org/variable_z> ?z . ' \
        f'?s2 <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s2 <http://example.org/variable_x> ?z . ' \
        f'?s2 <http://example.org/variable_y> <http://example.org/two> . ' \
        f'?s2 <http://example.org/variable_z> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # resolve_bindings = rdf_prolog.answer_complex_question(my_sparql_query)
    pass

    # add(3, ?ans, 5)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/add_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/three> . ' \
        f'?s <http://example.org/variable_y> ?ans . ' \
        f'?s <http://example.org/variable_z> <http://example.org/five> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # grandfather(taro, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/grandfather> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/taro> . ' \
        f'?s <http://example.org/variable_y> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # mortal(?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/mortal> . ' \
        f'?s <http://example.org/variable_x> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # knows(andy, bob)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/knows_direct> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/andy> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/bob> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # knows_direct(andy, chris)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/knows_direct> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/andy> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/chris> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # knows_direct(andy, ?ans)
    my_question = \
        f'SELECT ?s ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/knows_direct> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/andy> . ' \
        f'?s <http://example.org/variable_y> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # knows_indirect(andy, chris)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/knows_indirect> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/andy> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/chris> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # knows_indirect(andy, edgar)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/knows_indirect> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/andy> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/edgar> . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # knows_indirect(andy, ?ans)
    my_question = \
        f'SELECT ?s WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/knows_indirect> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/andy> . ' \
        f'?s <http://example.org/variable_y> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # knows(andy, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/knows> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/andy> . ' \
        f'?s <http://example.org/variable_y> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    # rdf_prolog.answer_complex_question(my_sparql_query)

    # subtract(5, 3, ?ans)
    my_question = \
        f'SELECT ?ans WHERE {{' \
        f'?s <http://example.org/operation> <http://example.org/subtract_number> . ' \
        f'?s <http://example.org/variable_x> <http://example.org/five> . ' \
        f'?s <http://example.org/variable_y> <http://example.org/three> . ' \
        f'?s <http://example.org/variable_z> ?ans . ' \
        f'}}'
    my_sparql_query = ClassSparqlQuery().set(my_question).build_rule()
    rdf_prolog.answer_complex_question(my_sparql_query)

if __name__ == '__main__':
    main()  # execute the main function
