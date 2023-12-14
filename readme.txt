RdfProlog
RDFのクエリ機能を利用してPrologの推論を実行するシステム。

質問はsparql queryで与える。
grandfather(jiro, Y).の場合。
SELECT ?ans WHERE {
    ?s VAL:operation　VAL:grandfather .
    ?s VAL:variable_x　VAL:jiro .
    ?s VAL:variable_y ?ans . }

事実はRDFで与える。
father(jiro, taro).は以下のようになる。
VAL:rule_father_jiro_taro
    VAL:operation VAL:father ;
    VAL:variable_x VAL:jiro ;
    VAL:variable_y VAL:taro .

ルールもRDFで与える。
grandfather(X, Y) :- father(X, U), father(U, Y).は次のようになる。
VAL:grandfather_father_father
    VAL:left_side [
        VAL:operation VAL:grandfather ;
        VAL:variable_x VAR:x ;
        VAL:variable_y VAR:y ] ;
    VAL:right_side [
        VAL:priority "1" ;
        VAL:child [
            VAL:operation VAL:father ;
            VAL:variable_x VAR:x ;
            VAL:variable_y VAR:u ] ] ;
    VAL:right_side [
        VAL:priority "2" ;
        VAL:child [
             VAL:operation VAL:father ;
             VAL:variable_x VAR:u ;
             VAL:variable_y VAR:y ] ] .

＜実行手順＞
[answer_question]
answer_questionにquestionを与える。この関数がresolveを呼び出して、結果を出力する。
    rdf_prolog.answer_question(my_question)

[resolve]
answer_questionはresolveを呼び出す。resolveが実質的な処理関数。
    resolve_succeeded, resolve_results, resolve_bindings = self.resolve(question, resolve_bindings)
questionは上記の質問。
resolve_bindingsは変数の対応関係を示す、dictのlist。初期値として[]を与える。
推論が成功すると、resolve_succeededがTrueになる。失敗するとFalseになる。
推論が成功すると、resolve_resultsに回答が格納される。
resolve_bindingsには変数の対応関係が格納される。

＜resolve内の処理＞
処理の核心であるresolveは再起的に呼び出される。

＜resolve前半、直接探索＞
resolveの前半ではquestionに対する直接の回答が無いかを検索する。
このとき、direct_search()を呼び出す。
    direct_search_succeeded, results_of_direct_search, returned_direct_search_bindings \
            = direct_search(resolve_question)
resolve_questionは回答すべき質問。
データベースに適合する事実が存在するとdirect_search_resultsはTrueになる。存在しなければFalseになる。
grandfather(jiro, Y).は失敗する。
father(jiro, U).は成功する。
事実が存在すると、検索結果がresult_of_direct_searchに格納される。

変数の対応関係はreturned_direct_search_bindingsに格納される。
father(jiro, U).に対する変数の対応は次のようになる。
[{'?s': '<http://value.org/rule_father_jiro_taro>', '?u': '<http://value.org/taro>'}]

＜resolve後半、ルール探索＞
後半では適用可能なルールを検索して順番に試す。
直接の回答が見つからなかった時にはこちらに進む。
直接の回答が見つかった時には実行されない。

[find_rules]
与えられた質問に対応するルールの左辺値はあらかじめリストしておく。create_list_of_left_rules()
質問に適合するルールを検索する関数がfind_rulesである。
    parents_found, bindings_found = find_rules(resolve_question)
質問を与えて、適合するルールのリストを得る。
parents_foundにはルールの親のラベルが格納される。
bindings_foundにはルールと質問の間の変数の対応関係が格納される。
戻り値のリストが空の時には、適合するルールが見つからなかったので、resolveを失敗で呼び出し先に戻る。

grandfather(jiro, Y).の場合には、２つのルールが適合する。
parents_foundは２要素のリストになる。
['<http://value.org/grandfather_father_father>',
 '<http://value.org/grandfather_mother_father>']

bindings_foundはdictのlistのlistになる。keyがルール側、valueが質問側になる。
[[{rdflib.term.Variable('s'): rdflib.term.URIRef('http://value.org/subj'),
  rdflib.term.Variable('x'): rdflib.term.URIRef('http://value.org/jiro'),
  rdflib.term.Variable('y'): rdflib.term.URIRef('http://variable.org/ans')}],
 [{rdflib.term.Variable('s'): rdflib.term.URIRef('http://value.org/subj'),
 rdflib.term.Variable('x'): rdflib.term.URIRef('http://value.org/jiro'),
 rdflib.term.Variable('y'): rdflib.term.URIRef('http://variable.org/ans')}]]

適合したルールを順番に試す。
１つでも成功すれば、その段階で打ち切って、成功を返す。
全てのルールで失敗したら、失敗を返す。

[resolve_right_side]
個々のルールを試すのがresolve_right_side()である。
    right_side_succeeded, resolve_result, resolve_bindings = resolve_right_side(parent_found, binding_found, resolve_bindings)

parent_foundには上記find_rules()で得たparents_foundの要素が入る。
binding_foundには上記find_rules()で得たbindings_foundの要素が入る。
resolve_bindingsには、それまでの変数対応のリストが入る。
この関数の中でresolveを再起的に呼び出す。
ルールの右辺が成功すればright_side_succeededはTrueになる。
失敗すればright_side_succeededはFalseになる。
クエリの結果はresolve_resultに格納される。
変数の対応はresolve_bindingsに格納される。

grandfather(jiro, Y).の場合、最初にfather(jiro, U), father(U, Y).を試す。
最初はresolve_bindings=[]である。
左辺の変数の対応関係を解決するためにbuild_argument_bindings()を呼び出す。
    argument_binding = build_argument_bindings(binding[0])
binding[0]で変数対応の辞書を取り出す。
戻り値のargument_bindingには左辺値の対応が入っている。
{'?s': '<http://value.org/subj>', '?x': '<http://value.org/jiro>', '?y': '?ans'}

次に右辺の各項を順番に試す。
右辺の各項は親のラベルparent_for_rightを基にして、find_right_sides()で取り出す。
    results_for_right = find_right_sides(parent_for_right)  # find right hand of the rule
results_for_rightの各項rightのright_side[0]で右辺の各項のラベルが取得できる。

各項のラベルからfind_child_right()でこの子要素を取り出す。
    results_of_right_side_search = find_child_right(right_side[0])

その結果からさらに孫要素を取り出すと、get_grand_child_rules()で右辺各項の実体が得られる。
    results_for_grandchild_rules = get_grand_child_rules(result[0])
results_for_grandchild_rulesのbindingsは次のようになる。　これはfather(X, U).を表す。
[{rdflib.term.Variable('p'): rdflib.term.URIRef('http://value.org/operation'),
  rdflib.term.Variable('o'): rdflib.term.URIRef('http://value.org/father')},
 {rdflib.term.Variable('p'): rdflib.term.URIRef('http://value.org/variable_y'),
  rdflib.term.Variable('o'): rdflib.term.URIRef('http://variable.org/variable_u')},
 {rdflib.term.Variable('p'): rdflib.term.URIRef('http://value.org/variable_x'),
  rdflib.term.Variable('o'): rdflib.term.URIRef('http://variable.org/variable_x')}]

右辺各項をresolveに対する質問に変換するためには、変数を置き換える必要がある。
これをbuild_query()で処理する。
    built_query = build_query(results_for_grandchild_rules, resolve_bindings, argument_binding)
戻り値はクエリになる。

father(jiro, U).の場合には、以下のように置き換えられる。
SELECT ?s ?u  WHERE {
    ?s <http://value.org/operation> <http://value.org/father> .
    ?s <http://value.org/variable_x> <http://value.org/jiro> .
    ?s <http://value.org/variable_y> ?u . }'
build_query()内でこの変換を行うために、tripleのpredicateとobjectを抽出する。predicateはそのままクエリに使う。
objectについては変数でなければ、そのままクエリに使う。
変数の場合、まず<http://variable.org/variable_x>などを?xに置き換える。
次に、左辺値での対応argument_bindingを使って、?xを<http://value.org/jiro>に置き換える。?uは対応がないのでそのままになる。
最後に、前段階までのresolve_bindingsを使って確定した変数を置き換える。
その結果、右辺の最初の項は上記のようなクエリに置き換えられる。

このクエリに対してresolve()を実行すると直接の適合が見つかる。
resolve_bindingsの戻り値は次にようになる。
[{'?s': '<http://value.org/rule_father_jiro_taro>', '?u': '<http://value.org/taro>'}]

右辺第２項father(U, Y).に対してbuild_query()する際にはargument_bindingは同じだが、resolve_bindingsが
[{'?s': '<http://value.org/rule_father_jiro_taro>', '?u': '<http://value.org/taro>'}]
になっているので、クエリはのようになる。
SELECT ?s ?ans  WHERE {
    ?s <http://value.org/operation> <http://value.org/father> .
    ?s <http://value.org/variable_x> <http://value.org/taro> .
    ?s <http://value.org/variable_y> ?ans . }'

これは失敗して、第２ルールgrandfather_mother_fatherを調べる。
第２ルールの右辺第１項は
SELECT ?s ?u  WHERE {
    ?s <http://value.org/operation> <http://value.org/mother> .
    ?s <http://value.org/variable_x> <http://value.org/jiro> .
    ?s <http://value.org/variable_y> ?u . }'
これは成功して、?uがhanaになる。
第２ルールの右辺第２項は
SELECT ?s ?ans  WHERE {
    ?s <http://value.org/operation> <http://value.org/father> .
    ?s <http://value.org/variable_x> <http://value.org/hana> .
    ?s <http://value.org/variable_y> ?ans . }'
これも成功して、?ansにichiroが入る。
最終的なresolve_bindingsは次にようになる。
[{'?s': '<http://value.org/rule_father_hana_ichiro>', '?ans': '<http://value.org/ichiro>'}]
