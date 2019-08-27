# Radix sort in Python
def countingSort(array, place):
    size = len(array)
    output = [0] * size
    count = [0] * 10
    for i in range(0, size):
        index = array[i] // place
        count[index % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    i = size - 1
    while i >= 0:
        index = array[i] // place
        output[count[index % 10] - 1] = array[i]
        count[index % 10] -= 1
        i -= 1
    for i in range(0, size):
        array[i] = output[i]


def radixSort(array):
    max_element = max(array)
    place = 1
    while max_element // place > 0:
        countingSort(array, place)
        place *= 10

    return array


def radix_sort2(lst):
    positive_ints = radixSort(list((x for x in lst if x >= 0)))
    negative_ints = radixSort(list(-x for x in lst if x < 0))
    return [-x for x in reversed(negative_ints)] + positive_ints


def get_values_from_matrix(filename):

    values = []

    with open(filename, 'r') as r:
        for line in r:
            line = line.replace('\t', ' ')
            line = line.replace('\n', ' ')
            for i in line.split(' '):
                if i != '':
                    values.append(int(i))

    return values


file = '../Sort_Tests/num.100000.4.in'

values = get_values_from_matrix(file)
num_array = values.pop()
print(len(values))

print(radix_sort2(values))
