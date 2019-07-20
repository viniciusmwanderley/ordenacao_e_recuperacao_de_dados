from collections import Counter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', default=None)
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
        with open(args.file, encoding='latin1', newline='\n') as in_file:
            text = in_file.read()

            tree = HuffmanTree()
            tree.add_text(text)
            tree.mount()

            # árvore codificada
            tree_cod = tree.encode(text)
            print('tree_cod:', tree_cod)

            # árvore decodificada
            tree_decod = tree.decode(tree_cod)
            print('tree_decod:', tree_decod)

    except EOFError:
        pass
