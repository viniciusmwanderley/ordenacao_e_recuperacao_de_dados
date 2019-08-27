# Insertion sort in Python
def insertionSort(array):
    for step in range(1, len(array)):
        key = array[step]
        j = step - 1
        while j >= 0 and key < array[j]:
            # For descending order, change key<array[j] to key>array[j].
            array[j + 1] = array[j]
            j = j - 1
        array[j + 1] = key


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


file = '../Sort_Tests/num.1000.1.in'

values = get_values_from_matrix(file)
num_array = values.pop()

insertionSort(values)

print('Sorted Array in Ascending Order:')
print(values)
