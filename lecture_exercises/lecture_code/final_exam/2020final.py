import math
import time


def is_in_bound(x, bound=None):
    """Check if the value is within the limits."""
    if bound == None:
        bound = math.inf  # default to greater than zero

    if x > 0 and x < bound:
        return 1
    else:
        return 0


def is_valid(msg: str, bound: tuple) -> float:
    """
    Validate user inputs.
    ======================
    Parameters:
    - msg: Message prompts to users
    - bound: The upper and the lower limits

    Returns:
    - data: float
    """
    valid = False
    while not valid:
        try:
            data = float(input(msg))
        # if entered a wrong data type
        except ValueError as e:
            print(f"\nValueError: {e}", "Please enter a real number\n", sep="\n")

        # if entered value is not within the range
        if bound[0] <= data <= bound[1]:
            valid = True
        else:
            print(
                "\nInputError: input value out of range",
                f"Enter value between {bound[0]} and {bound[1]}",
                "Please try again\n",
                sep="\n",
            )

    return data


def nStepBTreeSharePrices(s, u, d, n):
    """
    Return a list of computed evolved share
    price at the n step in binomial tree.
    """
    return [s * (u ** i) * (d ** (n - i)) for i in range(n + 1)]


def calcBTreeEuropeanOpValue(po, p, pstar, step_discount):
    """Computes and returns the options value at time 0."""
    if po is None:
        po = []

    po = [(p * po[i + 1] + pstar * po[i]) * step_discount for i in range(len(po) - 1)]

    if len(po) == 1:
        return po[0]
    else:
        return calcBTreeEuropeanOpValue(po, p, pstar, step_discount)
    # temp = []
    # i = 0
    # while i < (len(po) - 1):
    #     temp.append(pstar * po[i] + p * po[i + 1] * step_discount)
    #     i += 1
    # print(temp)
    # if len(temp) > 1:
    #     po = temp
    #     return calcBTreeEuropeanOpValue(po, p, pstar, step_discount)
    # if len(temp) == 1:
    #     return temp[0]


def main():

    n = 9  # steps in binomial tress

    # input data
    # S = is_valid("Enter initial share price (greater than 0): ", (0, math.inf))
    # X = is_valid("Enter exercise price (greater than 0):", (0, math.inf))
    # r = is_valid("Enter interest rate (0 to 1): ", (0, 1))
    # q = is_valid("Enter dividend yield (0 to 1): ", (0, 1))
    # T = is_valid("Enter time to maturity (greater than 0): ", (0, math.inf))
    # s = is_valid("Enter volatility (0 to 1): ", (0, 1))

    S = 100
    X = 95
    r = 0.08
    q = 0.03
    T = 0.5
    s = 0.2

    # calculations of essential parameters
    delta_t = T / n
    u = math.exp(s * (delta_t ** 0.5))
    d = 1 / u
    p = (math.exp((r - q) * delta_t) - d) / (u - d)
    pstar = 1 - p
    step_discount = math.exp(-r * delta_t)

    # call the defined functions
    n_step_share_values = nStepBTreeSharePrices(S, u, d, n)
    po = [max((s_i - X), 0) for s_i in n_step_share_values]
    t0_opt_value = calcBTreeEuropeanOpValue(po, p, pstar, step_discount)

    rev_shares = [round(i, 2) for i in n_step_share_values[::-1]]
    
    print(f"The evolved share prices at the {n}th step binomial tree are: {' '.join(list(map(str, rev_shares)))}")
    print(f"the option value at time 0 is {t0_opt_value:.2f}")


if __name__ == "__main__":
    start = time.time()
    main()
    print(time.time() - start)
