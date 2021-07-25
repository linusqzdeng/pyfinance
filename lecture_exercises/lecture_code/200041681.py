# ============================= Basic Info ============================
# Program: Two-fund Separation
# Tested by: Python 3.8.8
# Course: SMM283 Introduction to Python
# Date: 15th July 2021
# Author: Qizhong Deng
# Student ID: 200041681

# ============================ Discription ============================
# This program is designed for helping user to find the all possible
# combination of their two-fund portfolio. By entering assets expected
# return, volatility, correlation coefficient, risk aversion coefficient
# and the risk free rate, users are able to see all portfolios' return,
# volatility, utility and sharpe ratio. In addition, the outputs are
# sorted acsendingly by expected return and would be stored in a .xls file.

# ============================ Structure ==============================
# Main logic of this program can be divided into 3 sections:
# 1. User inputs
#     - Asking user to decided data-entering method, either by
#       key board or read inputs from .xls file
#     - Validate if the input values are within the limits
#     - Store user inputs into a dictionary
#     - Print out user inputs and ask user whether they enter correctly
#       - if not, rerun the program and enter again
#       - if yes, write user inputs to a file "inputs.xls" and go on
# 2. Capital weights generation
#     - Prompt user to choose which method do they prefer to
#       generate capital weights, either
#       - Self incremental
#       - Huang and Litzenberger method
# 3. User outputs
#     - Calculate portfolio's return, volatility, utility and sharpe
#     - Return them as a two-dimensional array
#     - Sort the outputs by portfolio's expected return (ascending)
#     - Ask user for whether display outputs on screen
#     - Find out the market portfolio and highest utility portfolio
#       and print out their corresponding attributes on screen
#     - Ask if the user would like to rerun the program
#       - if not, end the program
#
# PS: 1. Use the "input.xls" as a template to enter asset data.
#     Otherwise, it will cause encoding error when reading from excel.
#     2. The outputs in the attached excel file are derived from the
#     following inputs (via self-incremented weights, interval=0.001):
#
#     Attrs                Asset_1  Asset_2
#     Expected_return        0.25    0.18
#     Volatility             0.15    0.10
#     Coefficient           -0.70
#     Risk_aversion          2.00
#     Risk_free              0.05
# ======================================================================

import sys
from textwrap import dedent, indent
from collections import defaultdict
from typing import DefaultDict

SLICES = 100
input_file = "inputs.xls"
output_file = "outputs.xls"

output_columns = ["#", "w1", "w2", "Return", "Risk", "Utility", "Sharpe"]
assets = ["Asset_1", "Asset_2"]
attrs = ["Expected_return", "Volatility", "Coefficient", "Risk_aversion", "Risk_free"]
bounds = [(0, 1), (0, 1), (-1, 1), (1, 3), (0, 1)]  # boundaries for each attribute

data_menu = """
        DATA ENTER MENU
        1. Read from keyboard
        2. Read from Excel file
        """
weight_menu = """
            WEIGHTS GENERATING OPTIONS
            1. Self-incremental
            2. HL method
            """


def main():
    """
    Welcome to the two-fund separation program!

    This program is designed for helping user to find the all possible
    combination of their two-fund portfolio. By entering assets expected
    return, volatility, correlation coefficient, risk aversion coefficient
    and the risk free rate, users are able to see all portfolios' return,
    volatility, utility and sharpe ratio. In addition, the outputs are
    sorted ascendingly by expected return and are stored in "outputs.xls".
    """

    ## ============================= Get user inputs ============================= ##

    print(dedent(main.__doc__))  # intro

    # main loop
    over = False
    while not over:

        print(indent(dedent(data_menu), prefix="\t"))  # indention for highlighting

        choice = input("How would you like to enter the data: ")

        if choice == "1":
            usr_inputs = read_keyboard(assets, attrs)  # store inputs in a dict
            write_inputs(input_file, usr_inputs, assets)  # write inputs to .xls file
            print_excel(input_file, header="Inputs")

            print("\nYou have successfully input the data!")
            if not confirm():  # ask for user confirm
                continue

        elif choice == "2":
            print(dedent(read_excel.__doc__))  # input instruction
            if not confirm():
                continue

            usr_inputs = read_excel(input_file)
            print_excel(input_file, header="Inputs")

            print("\nYou have successfully imported the data!")
            if not confirm():
                continue

        else:
            print("\nError: Please select the choice from menu")
            continue

        ## ======================== Generate capital weights ======================== ##

        # prompt user to choose weight-gernating method
        while True:

            print(indent(dedent(weight_menu), prefix="\t"))

            choice = input("How would you like to generate capital weights: ")

            if choice == "1":
                w_1, w_2 = increment_weights(SLICES)  # weight interval = 0.01
                break

            elif choice == "2":
                w_1, w_2 = hl_weights(SLICES, usr_inputs["Expected_return"])
                break

            else:
                print("\nError: Please select the choice from menu")
                continue

        ## ========================= Process user outputs ========================= ##

        # 2-D array that contains all possible portfolios
        usr_outputs = [
            portfolio_stats(
                w,
                usr_inputs["Expected_return"],
                usr_inputs["Volatility"],
                usr_inputs["Coefficient"][0],
                usr_inputs["Risk_aversion"][0],
                usr_inputs["Risk_free"][0],
            )
            for w in zip(w_1, w_2)
        ]

        usr_outputs.sort(key=lambda x: x[2])  # usr_outputs = [w1, w2, rp, ...]
        write_outputs(output_file, usr_outputs, output_columns)

        # ask user whether to print outputs on screen
        on_screen = input("Would you like to see the outputs on screen [y/n]? ")
        if on_screen.lower() == "y":
            print_excel(output_file, header="Outputs")

        s_p = [port[5] for port in usr_outputs]  # portfolios' sharpe ratio
        u_p = [port[4] for port in usr_outputs]  # portfolios' utility

        best_sp = usr_outputs[s_p.index(max(s_p))]  # index is corresponded
        best_up = usr_outputs[u_p.index(max(u_p))]

        print("\nThe followings are some outstanding portfolios")
        print_stats(best_sp, "Sharpe ratio", align=20, decimal_place=4)
        print_stats(best_up, "Utility", align=20, decimal_place=4)

        # end of the loop
        again = input("Would you like to run the program again [y/n]? ")
        if again.lower() == "n":
            over = True
            sys.exit()


def valid_input(msg: str, bound: tuple) -> float:
    """
    Validate if user inputs are within the boundary and
    whether they are float type.
    ======================
    Parameters:
    - msg: Message prompts to users
    - bound: The upper and the lower limits

    Returns:
    - data: float
    """
    valid = False
    while not valid:
        # check input data type
        try:
            data = float(input(msg))
        except ValueError as e:
            print(
                f"\nValueError: {e}",
                "  Please enter a real number\n",
                sep="\n"
            )
            continue

        # check if the input is within the range
        if data >= bound[0] and data <= bound[1]:
            valid = True
        else:
            print(
                "\nInputError: input value out of range",
                f"  Please enter value between {bound[0]} and {bound[1]}\n",
                sep="\n"
            )

    return data


def confirm() -> bool:
    """Ask for user comfirmation. Return True if confirmed."""
    is_correct = input("Press <Enter> if you want to go on, <n> for rerunning the program: ")

    return True if is_correct == "" else False


def increment_weights(sep: int) -> list:
    """
    Return w1, w2 start from 0.0000 to 1.0000,
    Note that w1 + w2 = 1
    ==========================================
    Parameters:
    - sep: Steps for increment
    """
    w1 = [i / sep for i in range(sep + 1)]
    w2 = [1.0 - w for w in w1]

    return w1, w2


def hl_weights(sep: int, rt: list) -> list:
    """
    Return w1, w2 based on the Huang and Lizenberger methods.
    ========================================================
    Parameters:
    - sep: Steps for increment
    - rt: asset returns
    """
    r_p = [i / sep for i in range(sep + 1)]  # target returns from 0.0 to 1.0
    r1, r2 = rt[0], rt[1]
    g1 = r2 / (r2 - r1)
    h1 = 1.0 / (r1 - r2)

    w1 = [(g1 + rp * h1) for rp in r_p]
    w2 = [(1.0 - w) for w in w1]

    return w1, w2


def portfolio_stats(w: list, rt: list, std: list, coef: float, ra: float, rf: float) -> list:
    """
    Store key portfolio statistics into a list.
    ===========================================================
    Parameters:
    - w: 1-D array contains weight of each asset
    - rt: 1-D array of each asset's expected return
    - std: 1-D array of each asset's volatility/risk
    - coef: Correlation coefficient between assets
    - ra: Risk aversion coefficient varies from different users
    - rf: Risk free rate at current time

    Returns:
    - w:  float  Asset weights
    - rp: float  Portfolio's expected return
    - vp: float  Portfolio's standard deviation
    - up: float  Portfolio's utility
    - sp: float  Portfolio's sharpe ratio
    """
    rp = sum([w * rt for w, rt in zip(w, rt)])  # sum product of w and rt
    vp = (
        (w[0] * std[0]) ** 2 + (w[1] * std[1]) ** 2
        + 2 * w[0] * w[1] * std[0] * std[1] * coef
    ) ** 0.5
    up = rp - 0.5 * ra * vp ** 2
    sp = ((rp - rf) / vp) if round(vp, 5) != 0 else 0  # avoid zero division

    return [w[0], w[1], rp, vp, up, sp]


def write_inputs(filename: str, usr_inputs: dict, assets: list) -> None:
    """
    Receive user inputs and write them into .xls file.
    The column contain each asset's name and the row
    are asset attrs.
    =================================================
    Sample output:
    Attrs                Asset_1  Asset_2
    Expected_return        .        .
    Volatility             .        .
    Coefficient            .
    Risk_aversion          .
    Risk_free              .
    """
    with open(filename, "w") as file:
        file.write("Attrs")

        # write asset titles for column names
        for asset in assets:
            file.write(f"\t{asset}")

        # write attrs and data
        for attrs, data in usr_inputs.items():
            file.write(f"\n{attrs}")

            for d in data:
                file.write(f"\t{d:.4f}")

    return


def write_outputs(filename: str, usr_outputs: list, column_names: list) -> None:
    """
    Write user outputs into a .xls file.
    ====================================
    Parameters:
    - filename
    - usr_outputs: Two-dimensional array
    - column_names
    """
    with open(filename, "w") as file:
        for name in column_names:  # write column titles
            file.write(f"{name}\t")

        file.write("\n")  # go to the next line

        for index, outputs in enumerate(usr_outputs):
            file.write(f"{index + 1}\t")  # index column
            for output in outputs:
                file.write(f"{output:.4f}\t")

            file.write("\n")

    return


def read_keyboard(assets: list, attrs: list) -> DefaultDict:
    """
    Read asset attrs and data from keyboard inputs
    and store the inputs in a dictionary.
    ==============================================
    Parameters:
    - attrs: List of asset attributes
    - assets: List of asset names
    """
    usr_inputs = defaultdict(list)

    # input expected return and volatility
    for asset in assets:
        print(f"\n**** {asset}'s Info ****")
        for attr in attrs[:2]:
            data = valid_input(f"Enter {asset} {attr} (0 to 1): ", bounds[0])
            usr_inputs[attr].append(data)

    # input coefficient, risk aversion and risk free
    print("\n**** Other Info ****")
    for attr, bound in zip(attrs[2:], bounds[2:5]):
        data = valid_input(f"Enter {attr} ({bound[0]} to {bound[1]}): ", bound)
        usr_inputs[attr].append(data)

    return usr_inputs


def read_excel(filename: str) -> DefaultDict:
    """
    Import user inputs from excel. Please open/create a
    "inputs.xls" under the same directory and enter
    the data using the following layout:

    Attrs                Asset_1  Asset_2
    Expected_return        .        .
    Volatility             .        .
    Coefficient            .
    Risk_aversion          .
    Risk_free              .

    This will return a dictionary that uses attributes as
    keys and input data as values. Please make sure you have
    followed the instruction and saved the input file before
    you go to the next step.

    Note: Please follow the exact format specified above and
          avoid spaces between words. Otherwise if might cause
          failures to reading data properly.
    """
    usr_inputs = defaultdict(list)
    try:
        with open(filename, "r") as file:
            for line in file.readlines()[1:]:  # ignore the cloumn titles
                info = line.split()
                attr, *data = info  # unpack each line
                data = list(map(float, data))  # convert str to float
                usr_inputs[attr] = data
    except FileNotFoundError as e:
        print("\nFileNotFoundError:", e)
        print(f"Please create '{filename}' under the current directory")
        sys.exit()

    return usr_inputs


def split_table(table: list) -> list:
    """Extract the first column from the table. Return it and the remaining columns."""
    index_col = [row[0] for row in table]
    data_col = [row[1:] for row in table]  # remaining columns as 2-D array

    return index_col, data_col


def max_length(table: list) -> int:
    """Return the length of the longest element in the table"""
    return max([len(x) for row in table for x in row])


def print_excel(filename: str, header: str) -> None:
    """
    Print out all the content within the parsing .xls
    file with formatted alignment and table header.
    Numerical figures are formatted in 4 decimal places.
    ==================================================
    Parameters
    - filename
    - header: Title of the printed out dataframe
    """
    # read the whole table are store as a 2-D array
    with open(filename, "r") as file:
        table = [line.split() for line in file.readlines()]

    # variables for table formatting
    index_col, data_col = split_table(table)
    align = max_length(table) + 1  # adjust for 1 additional space
    n_col = len(table[0])  # number of column
    width = align * n_col // 2  # length of half section line

    # format the table and print out each line
    print("\n" + "=" * width + f"{header}" + "=" * width)

    for i in range(len(data_col)):
        index = index_col[i].ljust(align)  # left justify the first column
        data = [j.center(align) for j in data_col[i]]  # center justify data columns

        if i == 0:  # no need to reformat the column titles
            print(index + " ".join(data))
        else:
            data = list(map(float, data))
            data = [f"{data_col:^{align}.4f}" for data_col in data]
            print(index + " ".join(data))

    print("=" * width + f"{header}" + "=" * width)

    return


def print_stats(stats: list, highlight: str, align: int, decimal_place: int) -> None:
    """Print out portfolio's details"""
    info = f"""
        Portfolio with the highest {highlight}:
        ========================================
        Weight of asset 1: {stats[0]:>{align}.{decimal_place}f}
        Weight of asset 2: {stats[1]:>{align}.{decimal_place}f}
        Expected return:   {stats[2]:>{align}.{decimal_place}f}
        Volatility:        {stats[3]:>{align}.{decimal_place}f}
        Utility:           {stats[4]:>{align}.{decimal_place}f}
        Sharpe ratio:      {stats[5]:>{align}.{decimal_place}f}
        ========================================
        """
    print(dedent(info))

    return


if __name__ == "__main__":
    main()
