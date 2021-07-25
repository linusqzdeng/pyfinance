def mean(x=None):
    if x is None:
        x = []
        return 0

    return sum(x) / len(x)


def pmean(p=None, x=None):
    """Return the probabilistic average of two array."""
    if (p and x) is None:
        p, x = [], []
        return 0

    product = [i * j for i, j in zip(p, x)]
    return sum(product)


def var(x=None):
    """Return the variance of an array of real numbers."""
    if x is None:
        x = []
        return 0

    avg = mean(x)
    resid_square = [(i - avg) ** 2 for i in x]
    variance = sum(resid_square) / len(x)
    return variance


def pvar(x=None, p=None):
    """Return the probabilistic variance of two array."""
    if (x and p) is None:
        x, p = [], []
        return 0

    resid_square = [(i - mean(x)) ** 2 for i in x]
    variance_list = [(i * j) for i, j in zip(p, resid_square)]
    return sum(variance_list)


def trainspose(m=None):
    if m is None:
        m = [[]]
        return None

    # return [[a[i] for a in m] for i in range(len(m[0]))]
    return [[m[i][j] for i in range(len(m))] for j in range(len(m[0]))]


def main():
    x = list(map(float, input('Please enter values for x, split data by spaces: ').strip().split()))
    p = list(map(float, input('Please enter values for p, split data by spaces: ').strip().split()))

    m = []
    count = 1
    while True:
        try:
            line = list(map(int, input(f'Enter line {count} of the metrix (<q> for quit): ').strip().split()))
            m.append(line)
            count += 1
        except ValueError:
            break

    print(m)
    print(trainspose(m))


main()
