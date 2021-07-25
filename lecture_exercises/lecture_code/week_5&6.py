# Use a list of lists to solve the following problem.
# A company has four salespeople (1 to 4) who sell five
# different products (1 to 5). Once a day, each salesperson
# passes in a slip for each different type of product sold.
# Each slip contains:
#   a) The salesperson number.
#   b) The product number.
#   c) The number of that product sold that day.
# Thus, each salesperson passes in between 0 and 5 sales slips
# per day. Assume that the information from all of the slips for
# last month is available.

def zeros(shape: tuple) -> list:
    """
    Return a metrics that all elements are
    zero with the specified shape.
    """
    return [shape[1] * [0] for _ in range(shape[0])]


def sales_record(record: list, which: tuple) -> list:
    """
    Add one sale to the sepcified salesperson and
    the product number. Return a list with the
    updated sale record.
    -----------------------
    Parameters:
    - record: list
        Two-dimensional array that contains the record
        of each salesperson's sale.
    - which: tuple
        The first argument specifies which product (row),
        the second argument specifies which salesperon (col).
    """
    row = which[0] - 1
    col = which[1] - 1

    record[row][col] += 1

    return record


def transpose(array: list) -> list:
    """Return the transposed array."""
    return [[array[i][j] for i in range(len(array))] for j in range(len(array[0]))]


def salesperson_sum(record: list) -> list:
    """ Return the number of product sold by each salesperson."""
    return [sum(i) for i in transpose(record)]


def product_sum(record: list) -> list:
    """Return a list that contains the sum of each prodcut sales."""
    return [sum(i) for i in record]


def main():

    print('This program calculates sales totals.')

    # initialise the sales record to zero
    HM_SALESPERSON = 4
    HM_PRODUCT = 5
    record = zeros((HM_PRODUCT, HM_SALESPERSON))

    # while loop for user input
    # over = False
    # while not over:

    #     print('\n')
    #     salesperson = int(input('Enter salesperson (-1 to quit): '))

    #     if salesperson != -1:
    #         product_num = int(input('Enter product number: '))
    #         recotd = sales_record(record, (product_num, salesperson))
    #     else:
    #         over = True

    # test
    record = [[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 0, 0],
              [0, 0, 1, 0], [1, 1, 2, 0]]

    # calculate the sales summary
    total_product = product_sum(record)
    total_salesperson = salesperson_sum(record)

    # print out the sales record output
    print('\n' + 'Product' + '\t' * 4 + 'Salesperson' + '\t' * 4 + 'Total Product Sold')
    print('\t' * 3, end=' ')

    for j in range(1, HM_SALESPERSON + 1):
        print(f'[{j}]', end=' ' * 4)

    print('\n', end='')

    for x, y in enumerate(record):
        print(f'[{x+1}]' + '\t  ' * 3 + '      '.join(map(str, y)) + '\t' * 4 + str(total_product[x]))

    print('\n' + 'Total:' + '\t  ' * 2 + '      '.join(map(str, total_salesperson)))


if __name__ == '__main__':
    main()
