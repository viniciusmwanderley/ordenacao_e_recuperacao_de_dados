from collections import Counter
import heapq

''' EQUAL: READ AND COUNT FREQUENCY -> WORKING '''

LEFT = 2
RIGHT = 3


def frequency(text):
    return Counter(text)


def join_nodes(a, b):
    frequency = a[0] + b[0]
    parent_node = (frequency, None, a, b)
    return parent_node


def prefixes(frequencies):
    tree = []
    for char, freq in frequencies.items():
        heapq.heappush(tree, (freq, char))

    while len(tree) > 1:
        left = heapq.heappop(tree)
        right = heapq.heappop(tree)
        parent = join_nodes(left, right)
        heapq.heappush(tree, parent)
    root = tree[0]
    return root


def dictionary(tree, symbol=''):
    node = tree[1]

    if node is not None:
        return {node: symbol or '0'}
    else:
        a = dictionary(tree[LEFT], symbol + '0')
        b = dictionary(tree[RIGHT], symbol + '1')
        a.update(b)
        return a


def code(text, dictionary):
    return "".join([dictionary[letter] for letter in text])


def decode(codes, tree):
    text = []
    node = tree
    for code in codes:
        if node[1] is None:
            if code == '0':
                node = node[LEFT]
            elif code == '1':
                node = node[RIGHT]
        if node[1] is not None:
            text.append(node[1])
            node = tree

    return "".join(text)


def pack(codes):
    bytes = [chr(int(codes[i:i + 8], 2)) for i in range(0, len(codes), 8)]
    return "".join(bytes)


def unpack(text_pack, prefixes):
    bytes = [bin(ord(byte))[2:] for byte in text_pack]
    for i in range(0, len(bytes) - 1):
        bytes[i] = bytes[i].zfill(8)
    text_code = "".join(bytes)
    text_unpack = decode(text_code, prefixes)
    return text_unpack


def main():

    # Read text
    # equal = open("generated.equal", encoding='latin1', newline='\n').read()
    equal = 'abacaxi'
    fib25 = open("generated.fib25", encoding='latin1', newline='\n').read()

    # Compute frequency
    frequency_equal = frequency(equal)
    print('FREQUENCY:', frequency_equal)
    # frequency_fib25 = frequency(fib25)

    # Compute prefixe
    prefix_equal = prefixes(frequency_equal)
    print('PREFIX:', prefix_equal)

    # Compute dictionary
    dictionary_equal = dictionary(prefix_equal)
    print('DICTIONARY:', dictionary_equal)

    # Compute code
    code_equal = code(equal, dictionary_equal)
    print('CODE:', code_equal)

    # Compute decode
    # decode_equal = decode(code_equal, prefixes)
    # print('DECODE:', decode_equal)

    # Compute pack
    pack_equal = pack(code_equal)
    print('PACK:', pack_equal)

    # Compute unpack
    unpack_equal = unpack(pack_equal, prefix_equal)
    print('UNPACK:', unpack_equal)


if __name__ == '__main__':
    main()


''' TEST: WRITE BYTE '''
# f = open("teste.bin", "wb")
# f.write(bytearray((0, 0, 255, 255, 128, 128)))
# f.close()
# print(open("teste.bin", encoding="latin1").read())
