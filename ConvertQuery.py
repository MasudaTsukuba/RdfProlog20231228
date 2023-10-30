from lark import Lark
# Tree, Token, \
from lark import Transformer

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


class MyTransformer(Transformer):
    var_name = '?my_var'
    var_num = 100
    variable_dictionary = {}
    predicate_object_pair = {}
    # predicate_is_operation = False

    @staticmethod
    def sparql(tree):
        # print('>>> ', tree)
        return_str = 'SELECT '
        # for element in tree:
        #     return_str += element
        return_str += ''.join(tree)
        return return_str

    @staticmethod
    def where(tree):
        # return_str = ''
        # for element in tree:
        #     return_str += element
        return_str = ''.join(tree)
        return 'WHERE { ' + return_str + '}'

    @staticmethod
    def var(tree):
        # print('### ', tree[0].type, tree[0].value)
        return f'{tree[0]}'

    @staticmethod
    def triple(tree):
        # print('&&& ' + tree[0] + tree[1])
        # return_str = ''
        # for element in tree:
        #     return_str += element
        return_str = ''.join(tree)
        MyTransformer.predicate_object_pair[tree[1]] = tree[2]
        return return_str + '. '

    @staticmethod
    def subject(tree):
        # print('¥¥¥ ', tree)
        if tree[0].type == 'VAR':
            ret = tree[0].value
        else:
            ret = tree[0].value
        return ret

    @staticmethod
    def predicate(tree):
        # print('@@@ ', tree)
        if tree[0].type == 'VAR':
            ret = tree[0].value
        else:
            ret = tree[0].value
        # if tree[0].value == '<http://example.org/operation> ':
        #     MyTransformer.predicate_is_operation = True
        # else:
        #     MyTransformer.predicate_is_operation = False
        return ret

    @staticmethod
    def object(tree):
        # global var_name, var_num
        # print('$$$ ', tree)
        ret = tree[0].value
        if tree[0].type != 'VAR':
            if not MyTransformer.predicate_is_operation:
                ret = MyTransformer.var_name + str(MyTransformer.var_num) + ' '
                MyTransformer.variable_dictionary[ret] = tree[0].value
                MyTransformer.var_num += 1
        return ret

    # def HTTP(self, tree):
    #     print('!!! ', tree)
    #     return tree


class MyTransformer2(Transformer):
    list_of_rdfs = []
    element = []

    @staticmethod
    def sparql(tree):
        return_str = 'SELECT '
        return_str += ''.join(tree)
        return return_str

    @staticmethod
    def where(tree):
        return_str = ''.join(tree)
        return 'WHERE { ' + return_str + '}'

    def var(self, tree):
        # print('### ', tree[0].type, tree[0].value)
        return f'{tree[0]}'

    def triple(self, tree):
        self.element = []
        return_str = ''.join(tree)
        MyTransformer.predicate_object_pair[tree[1]] = tree[2]
        return return_str + '. '

    def subject(self, tree):
        # print('¥¥¥ ', tree)
        if tree[0].type == 'VAR':
            ret = f'<http://variable.org/{tree[0].value.replace("?", "").replace(" ", "")}>'
            # ret = tree[0].value  # '<http://example.org/subj> '
        else:
            ret = tree[0].value  # '<http://example.org/subj> '  # tree[0].value
        self.element = []
        self.element.append(ret.replace(' ', ''))
        return ret + ','

    def predicate(self, tree):
        if tree[0].type == 'VAR':
            ret = tree[0].value
        else:
            ret = tree[0].value
        # if tree[0].value == '<http://example.org/operation> ':
        #     MyTransformer.predicate_is_operation = True
        # else:
        #     MyTransformer.predicate_is_operation = False
        self.element.append(ret.replace(' ', ''))
        return ret+','

    def object(self, tree):
        my_value = tree[0].value
        ret = my_value
        if tree[0].type == 'VAR':
            ret = f'<http://variable.org/{my_value.replace("?", "").replace(" ", "")}>'
        self.element.append(ret.replace(' ', ''))
        self.list_of_rdfs.append(self.element)
        return ret


def convert_query(query):
    parser = Lark(grammar, start='sparql')
    MyTransformer.variable_dictionary = {}
    MyTransformer.predicate_object_pair = {}
    MyTransformer.var_num = 100
    # print(query)
    my_tree = parser.parse(query)
    # print(my_tree)
    my_transformer = MyTransformer()
    trans = my_transformer.transform(my_tree)
    # print('??? ', trans)
    # print('*** ', MyTransformer.variable_dictionary)
    for item in MyTransformer.variable_dictionary:
        trans = trans.replace('WHERE', item + ' WHERE')
    return trans, MyTransformer.variable_dictionary, MyTransformer.predicate_object_pair


def convert_question(question):
    parser = Lark(grammar, start='sparql')
    my_tree = parser.parse(question)
    # print(my_tree)
    my_transformer2 = MyTransformer2()
    my_transformer2.list_of_rdfs = []
    trans = my_transformer2.transform(my_tree)
    # print(trans)
    # print(my_transformer2.list_of_rdfs)
    return my_transformer2.list_of_rdfs


if __name__ == '__main__':
    # my_query = 'SELECT ?ss WHERE { ?ss <http://example.org/operation> <http://example.org/add_number> . ' + \
    #            '?s <http://example.org/PP> ?o . }'
    # conv_query, var_dict, predicate_object_pair = convert_query(my_query)

    my_question = f'SELECT ?ans WHERE {{ ?s <http://example.org/operation> <http://example.org/add_number> . ' \
                  f'?s <http://example.org/variable_x> <http://example.org/three> . ' \
                  f'?s <http://example.org/variable_y> <http://example.org/two> . ' \
                  f'?s <http://example.org/variable_z> ?ans . ' \
                  f'}}'
    list_of_rdfs = convert_question(my_question)
    print(list_of_rdfs)
