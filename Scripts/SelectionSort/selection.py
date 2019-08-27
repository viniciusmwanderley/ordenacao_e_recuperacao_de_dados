def selectionSort(array, size):
    for step in range(size):
        min_idx = step
        for i in range(step + 1, size):
            # To sort in descending order, change > to < in this line.
            if array[i] < array[min_idx]:
                min_idx = i
        (array[step], array[min_idx]) = (array[min_idx], array[step])


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
print(len(values))

size = len(values)
selectionSort(values, size)
print('Sorted Array in Ascending Order:\n')
print(values)
