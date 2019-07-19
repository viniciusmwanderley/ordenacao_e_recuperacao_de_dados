from collections import Counter
from os import path
import argparse
import pickle as pkl

parser = argparse.ArgumentParser()
parser.add_argument('file', help='Arquivo de entrada', nargs='?', default=None)
parser.add_argument(
    'pickle_file', help='Arquivo com o objeto', nargs='?', default=None)
parser.add_argument(
    '-d', '--decode', help='Usado para realizar o decode', action='store_true')
args = parser.parse_args()


class Node():

    def __init__(self, label, value):
        self.label = label
        self.value = value
        self.right = None
        self.left = None

    def __repr__(self):
        return str((self.label, self.value, self.left, self.right))


class HuffmanTree():

    def __init__(self):
        self.nodes = []
        self.head = None
        self.dict = {}
        self.reversed_dict = {}

    def add_text(self, text):
        count = Counter(list(text))
        for key in count:
            self.add_node(Node(key, count[key]))

    def add_node(self, node):
        self.nodes.append(node)
        self.nodes.sort(key=lambda x: x.value, reverse=True)

    def mount(self):
        while len(self.nodes) > 1:

            node_left = self.nodes[-2]
            node_right = self.nodes[-1]

            node = Node(node_left.label + node_right.label,
                        node_left.value + node_right.value)

            node.left = node_left
            node.right = node_right

            self.nodes = self.nodes[:-2]

            self.add_node(node)

        self.head = self.nodes[0]

        self.__mount_dict()

        self.__reverse_dict()

    def __mount_dict(self):
        self.__nav_tree(self.head, '')

    def __nav_tree(self, node, code):

        if node.left == node.right:
            self.dict[node.label] = code
        else:

            if node.left:
                self.__nav_tree(node.left, code + '0')

            if node.right:
                self.__nav_tree(node.right, code + '1')

    def __reverse_dict(self):

        self.reversed_dict = {self.dict[key]: key for key in self.dict}

    def encode(self, text):

        result = ''

        for letter in list(text):

            if self.dict.get(letter):
                result += self.dict[letter]
            else:
                result += '?'

        return result

    def decode(self, code):

        result = ''
        acc = ''

        code = [c for c in code if c.isdigit()]

        for number in code:
            acc += number

            if self.reversed_dict.get(acc):
                result += self.reversed_dict[acc]
                acc = ''

        return result


if __name__ == '__main__':
    try:
        # verifica se é uma arquivo
        if args.file:
            with open(args.file, encoding='latin1', newline='\n') as in_file:
                text = in_file.read()

                # verifica se é para realizar o decode
                if args.decode:
                    tree = pkl.load(open(args.pickle_file, 'rb'))
                    print(tree.decode(text))

                else:
                    # realiza o encode do texto e salva o objeto
                    tree = HuffmanTree()
                    tree.add_text(text)
                    tree.mount()

                    print(tree.encode(text))

                    # salva o objeto
                    pkl.dump(tree, open(
                        path.splitext(args.file)[-2] + '.code', 'wb'))
        else:
            # modo interativo
            while True:
                text = input()

                if len(text) > 0:
                    characters = list(text)
                    tree = HuffmanTree()
                    tree.add_text(text)
                    tree.mount()
                    # print(tree.dict)
                    code = tree.encode(text)
                    print(code)
                    # print(tree.decode(code))

                else:
                    raise EOFError
    except EOFError:
        pass
