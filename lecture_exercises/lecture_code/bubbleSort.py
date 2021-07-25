# On each pass, successive pairs of elements are compared.
# If a pair is in increasing order, bubble sort leaves the
# values as they are. If a pair is in decreasing order, their
# values are swapped in the list. After the first pass, the
# largest value is guaranteed to sink to the highest index of
# a list. After the second pass, the second largest value is
# guaranteed to sink to the second highest index of a list, and so on.


def bubbleSort(lst: list) -> list:
    """Return a new list in acsending order."""
    over = False

    while not over:
        over = True

        for i in range(len(lst) - 1):
            if lst[i] > lst[i + 1]:
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                over = False

    return lst


a = [1, 2, 4, 5, 2, 12, 3]
print(bubbleSort(a))
