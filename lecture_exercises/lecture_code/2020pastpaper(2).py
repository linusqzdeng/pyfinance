# ----------------------------------
# 2020 past paper
# -------------------------------------
# s =100
# x = 95
# r = 0.08
# q = 0.03
# t0 = 0
# tT = 0.5
# oT = 0.5
# sigma = 0.2
import math
import time as t

s1 = []
po = []


def nStepBTreeSharePrices(s, u, d, n):
    i = 0
    while i < n + 1:
        s_ = s * (u ** i) * (d ** (n - i))
        i += 1
        s1.insert(i, s_)
    return s1


def calcBTreeEuropeanOpValue(po, p, pstar, stepdiscount):
    # po = [(pstar * po[i] + p * po[i + 1]) * stepdiscount for i in range(len(po) - 1)]
    temp = []
    i = 0
    while i < (len(po) - 1):
        temp.append((pstar * po[i] + p * po[i + 1]) * stepdiscount)
        i += 1
    print(temp)
    if len(temp) > 1:
        po = temp
        return calcBTreeEuropeanOpValue(po, p, pstar, stepdiscount)
    elif len(temp) == 1:
        return temp[0]


def main():
    start = t.time()
    while True:
        try:
            print("\t\t1:enter from the key board")
            print("\t\t2:use the trial input data")
            chose = int(input("Please enter 1 or 2 to choose"))
            if chose == 1:
                while True:
                    try:
                        s = float(input("S = :"))
                        if s < 0:
                            print("invaild")
                            continue
                        break
                    except:
                        print("enter a float number")
                while True:
                    try:
                        x = float(input("X = :"))
                        if x < 0:
                            print("invaild")
                            continue
                        break
                    except:
                        print("enter a float number")
                while True:
                    try:
                        r = float(input("r = :"))
                        if r < 0 or r > 1:
                            print("invaild")
                            continue
                        break
                    except:
                        print("enter a float number")
                while True:
                    try:
                        q = float(input("q = :"))
                        if q < 0 or q > 1:
                            print("invaild")
                            continue
                        break
                    except:
                        print("enter a float number")
                while True:
                    try:
                        t0 = float(input("time now = :"))
                        if t0 < 0:
                            print("invaild")
                            continue
                        break
                    except:
                        print("enter a float number")
                while True:
                    try:
                        tT = float(input("Time maturity = :"))
                        if tT < 0:
                            print("invaild")
                            continue
                        break
                    except:
                        print("enter a float number")
                while True:
                    try:
                        oT = float(input("option life = :"))
                        if oT < 0:
                            print("invaild")
                            continue
                        break
                    except:
                        print("enter a float number")
                while True:
                    try:
                        sigma = float(input("volatility = :"))
                        if sigma < 0:
                            print("invaild")
                            continue
                        break
                    except:
                        print("enter a float number")
                break
            elif chose == 2:
                s = 100
                x = 95
                r = 0.08
                q = 0.03
                t0 = 0
                tT = 0.5
                oT = 0.5
                sigma = 0.2
                n = 9
                break
        except:
            print("\t\tYou should enter a int number 1 or 2")
    # -----------------------
    timeDuration = oT / n
    sqrtTime = math.sqrt(timeDuration)
    u = math.exp(sigma * sqrtTime)
    d = 1 / u
    # p = (((math.exp(r - q)) * timeDuration) - d) / (u - d)
    p = (math.exp((r - q) * timeDuration) - d) / (u - d)
    pstar = 1 - p
    stepdiscount = math.exp(-r * timeDuration)
    # ----------------------------------
    s1 = nStepBTreeSharePrices(s, u, d, n)
    po = [max((si - x), 0) for si in s1]
    optValue = calcBTreeEuropeanOpValue(po, p, pstar, stepdiscount)
    print(s1)
    print(po)
    print(optValue)
    end = t.time()
    print((end - start))


main()
