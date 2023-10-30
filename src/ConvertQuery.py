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

from lark import Lark, Transformer, Token  # , Tree

grammar = """
sparql : "SELECT " (var)+ where
where : "WHERE {" (" ")* (triple)+ "}" (" ")* 
var : VAR
VAR : "?" WORD (" ")+
triple : subject predicate object "." (" ")* 
WORD : CHAR (CHAR | NUMBER)*
CHAR : "a".."z" | "A".."Z"
NUMBER : "0".."9"
subject   : (VAR | HTTP) 
predicate : (VAR | HTTP)
object    : (VAR | HTTP)
HTTP : "<http://" HTTP_WORD ">" (" ")* 
HTTP_WORD : CHAR (CHAR | NUMBER | "." | "/" | "_" | "-")*
"""


# class MyTransformer(Transformer):
#     """
#     MyTransformer
#     """
#     var_name = '?my_var'
#     var_num = 100
#     variable_dictionary = {}
#     predicate_object_pair = {}
#     # predicate_is_operation = False
#
#     @staticmethod
#     def sparql(tree):
#         """
#
#         :param tree:
#         :return:
#         """
#         # print('>>> ', tree)
#         return_str = 'SELECT '
#         # for element in tree:
#         #     return_str += element
#         return_str += ''.join(tree)
#         return return_str
#
#     @staticmethod
#     def where(tree):
#         """
#
#         :param tree:
#         :return:
#         """
#         # return_str = ''
#         # for element in tree:
#         #     return_str += element
#         return_str = ''.join(tree)
#         return 'WHERE { ' + return_str + '}'
#
#     @staticmethod
#     def var(tree):
#         """
#
#         :param tree:
#         :return:
#         """
#         # print('### ', tree[0].type, tree[0].value)
#         return f'{tree[0]}'
#
#     @staticmethod
#     def triple(tree):
#         """
#
#         :param tree:
#         :return:
#         """
#         # print('&&& ' + tree[0] + tree[1])
#         # return_str = ''
#         # for element in tree:
#         #     return_str += element
#         return_str = ''.join(tree)
#         MyTransformer.predicate_object_pair[tree[1]] = tree[2]
#         return return_str + '. '
#
#     @staticmethod
#     def subject(tree):
#         """
#
#         :param tree:
#         :return:
#         """
#         # print('¥¥¥ ', tree)
#         if tree[0].type == 'VAR':
#             ret = tree[0].value
#         else:
#             ret = tree[0].value
#         return ret
#
#     @staticmethod
#     def predicate(tree):
#         """
#
#         :param tree:
#         :return:
#         """
#         # print('@@@ ', tree)  # debug
#         if tree[0].type == 'VAR':
#             ret = tree[0].value
#         else:
#             ret = tree[0].value
#         # if tree[0].value == '<http://example.org/operation> ':
#         #     MyTransformer.predicate_is_operation = True
#         # else:
#         #     MyTransformer.predicate_is_operation = False
#         return ret
#
#     @staticmethod
#     def object(tree):
#         """
#
#         :param tree:
#         :return:
#         """
#         # global var_name, var_num
#         # print('$$$ ', tree)
#         ret = tree[0].value
#         if tree[0].type != 'VAR':
#             if not MyTransformer.predicate_is_operation:
#                 ret = MyTransformer.var_name + str(MyTransformer.var_num) + ' '
#                 MyTransformer.variable_dictionary[ret] = tree[0].value
#                 MyTransformer.var_num += 1
#         return ret
#
#     # def HTTP(self, tree):
#     #     print('!!! ', tree)
#     #     return tree
#

class MyTransformer2(Transformer):
    """
    list_of_rdf_triples (list[list[str]]): a list of triples.

    list_of_each_triple (list[str]): a list of each triple.
    """
    def __init__(self):
        """

        """
        super().__init__()
        self.list_of_rdf_triples = []
        self.list_of_each_triple = []
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
        :param tree: lark tree string
        :return where_string:
        """
        where_string = ''.join(tree)
        return 'WHERE { ' + where_string + '}'

    @staticmethod
    def var(tree: list[Token]) -> str:
        """

        :param tree: list of tokens
        :return token for a variable:
        """
        # print('### ', tree[0].type, tree[0].value)
        return f'{tree[0]}'

    def triple(self, tree: list[str]) -> str:
        """
        build a triple in a sparql query string
        :param tree:
        :return:
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
        self.list_of_each_triple.append(ret.strip())  # subject of a triple
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
        self.list_of_each_triple.append(ret.strip())  # predicate of a triple
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
        self.list_of_each_triple.append(ret.strip())  # element holds a triple as a list # remove unnecessary spaces
        self.list_of_rdf_triples.append(self.list_of_each_triple)  # append the triple to the list
        return ret


# def convert_query(query):
#     """
#     NOT USED
#     :param query:
#     :return:
#     """
#     parser = Lark(grammar, start='sparql')
#     MyTransformer.variable_dictionary = {}
#     MyTransformer.predicate_object_pair = {}
#     MyTransformer.var_num = 100
#     # print(query)
#     my_tree = parser.parse(query)
#     # print(my_tree)
#     my_transformer = MyTransformer()
#     trans = my_transformer.transform(my_tree)
#     # print('??? ', trans)
#     # print('*** ', MyTransformer.variable_dictionary)
#     for item in MyTransformer.variable_dictionary:
#         trans = trans.replace('WHERE', item + ' WHERE')
#     return trans, MyTransformer.variable_dictionary, MyTransformer.predicate_object_pair


def convert_question(question: str) -> list[str]:
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
    my_transformer2 = MyTransformer2()  # create an instance of MyTransformer2
    my_transformer2.list_of_rdfs = []  # initialize the list of rdfs
    # trans =
    my_transformer2.transform(my_tree)  # transform a lark tree to list of rdfs
    # print(trans)  # debug
    # print(my_transformer2.list_of_rdfs)  # debug
    return my_transformer2.list_of_rdf_triples


if __name__ == '__main__':
    # my_query = 'SELECT ?ss WHERE { ?ss <http://example.org/operation> <http://example.org/add_number> . ' + \
    #            '?s <http://example.org/PP> ?o . }'
    # conv_query, var_dict, predicate_object_pair = convert_query(my_query)

    my_question = f'SELECT ?ans WHERE {{ ?s <http://example.org/operation> <http://example.org/add_number> . ' \
                  f'?s <http://example.org/variable_x> <http://example.org/three> . ' \
                  f'?s <http://example.org/variable_y> <http://example.org/two> . ' \
                  f'?s <http://example.org/variable_z> ?ans . ' \
                  f'}}'
    list_of_rdf_triples = convert_question(my_question)
    print(list_of_rdf_triples)
