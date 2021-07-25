# SMM283 Introduction to Python Final Exam
# Student ID: 200041681
# Tested by: Python 3.8.8

import time


## Question a ##
def maximum(x, y):
    """Returns the larger one between real number x and y."""
    return x if x > y else y


## Question b ##
def option_payoff(o_type: str, s: float, k: float) -> float:
    """
    Returns the payoff of a put or call option.
    
    Parameters:
    - o_type: option type. 'c' denotes call opiton while 'p' denotes put option
    - s: current market price of the underlying asset
    - k: strike price of the option
    """
    if s < 0 or k < 0:
        print("Invalid input of share price or strike price. Please only enter positive values.")

    if o_type == "c":
        return maximum(0, (k - s))
    elif o_type == "p":
        return maximum((s - k), 0)
    else:
        print(f"Error: unrecoginisable option type '{o_type}'")


## Question c ##
def print_payoff(msg: str, s: list=None, payoff: list=None, ip=1) -> None:
    """
    Prints out option payoff to monitor or to a .xls file. Default to monitor.

    Parameter:
    - msg: name of the output file
    - s: share price of the underlying asset
    - payoff: option payoff
    - ip: mode of print out. 1 denotes print out on screen,
      2 denotes print out to .xls file.
    """
    if s is None:
        s = []
    if payoff is None:
        payoff = []

    # print out on screen
    if ip == 1:
        print("Stock Prices" + "\t" + "Option Payoffs")
        for i in range(len(s)):
            print(f"£ {s[i]:>10.2f}" + "\t" + f"£ {payoff[i]:>12.2f}")
    # print out to .xls file
    elif ip == 2:
        with open(msg, "w") as f:
            # text message and column titles
            f.write("Stock Prices" + "\t" + "Option payoffs" + "\n")

            # data field
            for i in range(len(s)):
                f.write(str(s[i]) + "\t" + str(payoff[i]))
                f.write("\n")  # go to the next line
    else:
        print(f"Error: unrecognisable print out mode '{ip}'")


def main():
    """Receives user input and print out butterfly option payoffs."""
    tic = time.time()  # program started time

    # input for option type
    while True:
        stype = input("\nEnter option type 'c' for call 'p' for put: ").lower()

        if stype not in ["c", "p"]:
            print("  Invalid option type, please try again")
        else:
            print("Successfully enter the option type!")
            break

    # input for size of the list
    while True:
        try:
            size = int(input("\nEnter size of array (>=40 or <= 140): "))

            if size < 40 or size > 140:
                print("  Input value out of range [40, 140], please try again")
            else:
                print("Successfully enter the array size!")
                break
        except ValueError as error:
            print("  ValueError:", error)

    # input for print out mode
    while True:
        try:
            ip = int(input("\nEnter print out mode, 1 for monitor; 2 for .xls file: "))

            if ip not in [1, 2]:
                print("  Invalid mode. Please enter 1 for monitor; 2 for .xls file")
            else:
                print("Successfully print out the payoffs!")
                break
        except ValueError as error:
            print("  ValueError", error)

    # pre-defined variables
    x = 0.0
    dx = 10.0
    s = [i * 10 for i in range(size)]
    k1 = size * dx * 0.3
    k2 = size * dx * 0.5
    k3 = size * dx * 0.7
    long_option_k1 = [option_payoff(stype, si, k1) for si in s]
    long_option_k3 = [option_payoff(stype, si, k3) for si in s]
    short_option_k2 = [option_payoff(stype, si, k2) for si in s]

    # output butterfly spreads
    butterfly = [
        long_opt1 - 2 * short_opt2 + long_opt3
        for long_opt1, short_opt2, long_opt3 in zip(long_option_k1, short_option_k2, long_option_k3)
    ]

    print_payoff("butterfly.xls", s, butterfly, ip)

    toc = time.time()  # end of the program
    run_time = toc - tic
    print(f"It takes {run_time:.2f}s to run this program")


if __name__ == "__main__":
    main()
