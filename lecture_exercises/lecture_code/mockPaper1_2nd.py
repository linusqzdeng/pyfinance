# -----------------------------------
# Mock 1 2nd practice
# -------------------------------------
import math as m
import time as t


def pmt(r, nper, pv, fv, itype):
    pmt_ = ((pv * r * (1 + r) ** nper) - fv) / ((1 + r * itype) * ((1 + r) ** nper - 1))
    return pmt_


def nfv(r, nper, cost, cf=None):
    # again, as cf is defined, so need to be put at the end of string
    value = []
    # i as index for list, need to be a int not a float, so just 0, not 0.0
    for i in range(nper):
        nfv_ = cf[i] * (1 + r) ** (nper - i + 1)
        value.append(nfv_)
    value_ = sum(value) - cost * (1 + r) ** nper
    return value_


def main():
    # --------------------------------
    # Here start with input variable
    """
    while True:
        try:
            r = float(input("Enter r =:"))
            if r < 0.0 or r > 1.0:
                print("Out of range, re-enter:")
                continue
            break
        except:
            print("You should enter a float number!")
    while True:
        try:
            nper = int(input("Enter n =:"))
            if nper<0:
                print("Out of range, re-enter:")
                continue
            break
        except:
            print("You should enter a int number!")
    while True:
        try:
            pv = float(input("Enter pv =:"))
            if pv < 0.0:
                print("Out of range, re-enter:")
                continue
            break
        except:
            print("You should enter a float number!")
    while True:
        try:
            fv = float(input("Enter fv =:"))
            if fv < 0.0 :
                print("Out of range, re-enter:")
                continue
            break
        except:
            print("You should enter a float number!")
    while True:
        try:
            cost = float(input("Enter cost =:"))
            if cost<0.0:
                print("Out of range, re-enter:")
                continue
            break
        except:
            print("You should enter a float number!")
    """
    r = 0.03
    nper = 2
    pv = 90
    fv = 0
    cost = 10
    # input list variable
    cf = []
    while True:
        try:
            for i in range(1, nper + 1):
                temp = float(input("Pleace enter you " + str(i) + " cash flow :"))
                cf.insert(i, temp)
            break
        except:
            print("Should enter a float number")

    # --------------------------------
    # Here start calling the functions
    print(cf)
    print("payment for annuity due :{0:.2f}".format(pmt(r, nper, pv, fv, 1)))
    print("payment ordinary annuity for:{0:.2f}".format(pmt(r, nper, pv, fv, 0)))
    print("The future value is calculated as {0:.2f}".format(nfv(r, nper, cost, cf)))


main()
