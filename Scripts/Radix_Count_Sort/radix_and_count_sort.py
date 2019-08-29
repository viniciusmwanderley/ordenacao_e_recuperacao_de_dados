import time


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

# CountSort


def countSort(a, tam_array):
    a = a.copy()
    maximum = max(a)
    minimum = min(a)
    # print(maximum, minimum)

    if minimum < 0:
        for i in range(len(a)):
            # print(i)
            a[i] -= minimum
            if maximum < a[i]:
                maximum = a[i]

    c = [0] * (maximum + 1)
    b = [0] * tam_array

    for i in range(len(a)):
        c[a[i]] = c[a[i]] + 1

    for i in range(len(c) - 1):
        c[i + 1] += c[i]

    for i in range((len(a) - 1), -1, -1):
        # print(i)

        b[c[a[i]] - 1] = a[i]
        c[a[i]] -= 1

    if minimum < 0:
        for i in range(len(b)):
            b[i] += minimum

    return b


file = '../Sort_Tests/num.1000.1.in'

values = get_values_from_matrix(file)
tam_array = values.pop()
start = time.time()
countSort(values, tam_array)
print('Count Sort Time(s):', time.time() - start)

file = '../Sort_Tests/num.1000.1.in'

values = get_values_from_matrix(file)
num_array = values.pop()
start = time.time()
radix_sort2(values)
print('Radix Sort Time(s):', time.time() - start)
