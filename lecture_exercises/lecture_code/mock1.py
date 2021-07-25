# Mock test 1


def pmt(rate: float, nper: int, pv: float, fv=0, type=0):
    return (pv * rate * (1 + rate) ** nper - fv) / ((1 + rate * type) * ((1 + rate) ** nper - 1))


def nfv(rate, nper, cost, cf=None):
    if cf is None:
        cf = []

    fv = [cf[i] * (1 + rate) ** (nper - i + 1) for i in range(nper)]

    return sum(fv) - cost * (1 + rate) ** nper


print(pmt(rate=0.1, nper=10, pv=1000))
print(nfv(0.03, 2, 10, [50, 50]))
