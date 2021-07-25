# When a list is sorted, a high-speed binary search technique can find
# items in the list quickly. The binary search algorithm eliminates from
# consideration one-half of the elements in the list being searched after
# each comparison. The algorithm locates the middle element of the list and
# compares it with the search key. If they are equal, the search key is found,
# and the subscript of that element is returned. Otherwise, the problem is reduced
# to searching one half of the list. If the search key is less than the middle
# element of the list, the first half of the list is searched. If the search key
# is not the middle element in the specified piece of the original list, the
# algorithm is repeated on one-quarter of the original list. The search continues
# until the search key is equal to the middle element of the smaller list or until
# the smaller list consists of one element that is not equal to the search key
# (i.e. the search key is not found.)

def binarySearch(lst, key, start, end):
    """
    Return the index of the search key, return
    -1 if the key is not found.
    """
    # while True:
    #     index = len(lst) // 2

    #     if key == lst[index]:
    #         break

    #     elif key < lst[index]:
    #         lst = lst[:index]

    #     else:
    #         lst = lst[index:]

    # return index

    if end >= start:

        mid = (start + end) // 2

        if lst[mid] == key:
            return mid
        elif lst[mid] > key:
            print(1)
            return binarySearch(lst, key, start, mid - 1)
        else:
            print(2)
            return binarySearch(lst, key, mid + 1, end)

    else:
        return -1


a = [i for i in range(1, 12)]
key = 10

print(binarySearch(a, key, 0, len(a) - 1))
