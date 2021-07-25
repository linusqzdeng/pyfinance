# ============================= Basic Info ============================
# Program: Two-fund Separation
# Tested by: Python 3.8.8
# Course: SMM283 Introduction to Python
# Date: 25th June 2021
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
# PS: 1. Use the "input.xls" as a template to enter asset data. Otherwise,
#     it will cause encoding error when reading from excel.
#     2. The outputs in the attached excel file are derived from the
#     following inputs (via self-incremented weights, interval=0.001):
#
#     Attrs                Asset 1  Asset 2
#     Expected return        0.25    0.18
#     Volatility             0.15    0.10
#     Coefficient           -0.70
#     Risk aversion          2.00
#     Risk free              0.05


from textwrap import dedent, indent
from collections import defaultdict

def main():

    input_file = 'inputs.xls'
    output_file = 'outputs.xls'
    output_columns = ['#', 'w1', 'w2', 'Return', 'Risk', 'Utility', 'Sharpe']
    assets = ['Asset_1', 'Asset_2']
    attrs = ['Expected_return',
             'Volatility',
             'Coefficient',
             'Risk_aversion',
             'Risk_free']

    ## ============================= Get user inputs ============================= ##

    print(dedent("""
            Welcome to the two-fund separation program!
            This program is designed for helping user to find the all possible
            combination of their two-fund portfolio. By entering assets expected
            return, volatility, correlation coefficient, risk aversion coefficient
            and the risk free rate, users are able to see all portfolios' return,
            volatility, utility and sharpe ratio. In addition, the outputs are
            sorted ascendingly by expected return and are stored in "outputs.xls".
            """))

    # main loop
    over = False
    while not over:

        print(indent(dedent("""
            DATA ENTER MENU
            1. Read from keyboard
            2. Read from Excel file
            """), prefix='\t'))                                 # indention for highlighting

        choice = input('How would you like to enter the data: ')

        if choice == '1':
            usr_inputs = read_keyboard(assets, attrs)           # store inputs in a dict
            write_inputs(input_file, usr_inputs, assets)        # write inputs to .xls file
            print_excel(input_file, 'Inputs')

            # ask for user confirm
            print('\nYou have successfully input the data!')
            if not confirm():
                continue

        elif choice == '2':
            print(dedent(read_excel.__doc__))                   # input instruction
            if not confirm():
                continue

            usr_inputs = read_excel(input_file)
            print_excel(input_file, 'Inputs')

            # ask for user confirm
            print('\nYou have successfully imported the data!')
            if not confirm():
                continue

        else:
            print('Select the choice from menu')
            continue

    ## ======================== Generate capital weights ======================== ##

        # prompt user to choose weight-gernating method
        while True:

            print(indent(dedent("""
                WEIGHTS GENERATING OPTIONS
                1. Self incremental
                2. HL method
                """), prefix='\t'))

            choice = input('How would you like to generate capital weights: ')

            sep = 100                                          # interval = 0.01
            if choice == '1':
                w_1, w_2 = generate_weights(sep)
                break

            elif choice == '2':
                w_1, w_2 = generate_weights(sep, usr_inputs['Expected_return'], h_l=True)
                break

            else:
                print('Please select the choice from menu')
                continue

    ## ========================= Process user outputs ========================= ##

        # 2-D array that contains all possible portfolios
        usr_outputs = [portfolio_stats(w, usr_inputs['Expected_return'], usr_inputs['Volatility'],
                                       usr_inputs['Coefficient'][0], usr_inputs['Risk_aversion'][0],
                                       usr_inputs['Risk_free'][0]) for w in zip(w_1, w_2)]

        usr_outputs.sort(key=lambda x: x[2])                      # sorted by rp
        write_outputs(output_file, usr_outputs, output_columns)   # write outputs to .xls file

        # ask user whether to print outputs on screen
        on_screen = input('Would you like to see outputs on screen [y/n]? ')
        if on_screen.lower() == 'y':
            print_excel(output_file, 'Outputs')

        s_p = [port[5] for port in usr_outputs]                   # portfolios' sharpe ratio
        u_p = [port[4] for port in usr_outputs]                   # portfolios' utility

        best_sp = usr_outputs[s_p.index(max(s_p))]                # index is corresponded
        best_up = usr_outputs[u_p.index(max(u_p))]

        print_stats(best_sp, 'Sharpe ratio')
        print_stats(best_up, 'Utility')

        # ask if the user want to run again
        again = input('Would you like to run the program again [y/n]? ')

        # end of the loop
        if again.lower() == 'n':
            over = True


def is_valid(msg: str, edge: tuple) -> float:
    """
    Validate user inputs.
    =========================================
    Parameters:
    - msg: str
        Message prompts to users
    - edge: tuple
        The upper and the lower limits for
        validation

    Returns:
    - data: float
    """
    valid = False

    while not valid:
        try:
            data = float(input(msg))
            if edge[0] <= data <= edge[1]:
                valid = True
            # if entered value is not within the range
            else:
                print('\nInputError: input value out of range',
                      f'Enter value between {edge[0]} and {edge[1]}',
                      'Please try again\n',
                      sep='\n')
        # if entered a wrong data type
        except ValueError as e:
            print(f'\nValueError: {e}',
                  'Please enter a float type\n',
                  sep='\n')

    return data


def confirm() -> bool:
    """
    Prompt the user to confirm if the user
    inputs are correct, return True if correct.
    """
    correct = input("Press <Enter> if you want to go on, "
                    "<n> for rerunning the program: ")

    return True if correct == '' else False


def generate_weights(sep: int, rt=None, h_l=False) -> list:
    """
    Return w1, w2 start from 0.0000 to 1.0000,
    Note that w1 + w2 = 1
    ==========================================
    Parameters:
    - sep: int
        Steps of increment
    - rt: list
        List of asset returns when applying
        HL method, default to None.
    """
    if h_l and rt:
        r1, r2 = rt[0], rt[1]

        g1 = r2 / (r2 - r1)
        g2 = 1.0 - g1
        h1 = 1.0 / (r1 - r2)
        h2 = -h1

        r_p = [i / sep for i in range(sep + 1)]     # target return from 0.0 to 1.0

        w1 = [g1 + rp * h1 for rp in r_p]
        w2 = [g2 + rp * h2 for rp in r_p]

        return w1, w2

    w1 = [i / sep for i in range(sep + 1)]
    w2 = [1.0 - w for w in w1]

    return w1, w2


def portfolio_stats(w: list, rt: list, std: list,
                    coef: float, ra: float, rf: float) -> list:
    """
    Parameters:
    - w: 1-D array contains weight of each asset
    - rt: 1-D array of each asset's expected return
    - std: 1-D array of each asset's volatility/risk
    - coef: Correlation coefficient between assets
    - ra: Risk aversion coefficient varies from different users
    - rf: Risk free rate at current time
    ========================================
    Returns:
    - w:  float  Asset weights
    - rp: float  Portfolio's expected return
    - vp: float  Portfolio's standard deviation
    - up: float  Portfolio's utility
    - sp: float  Portfolio's sharpe ratio
    """
    rp = sum([w * rt for w, rt in zip(w, rt)])                     # sum product of w and rt
    vp = ((w[0] * std[0]) ** 2 + (w[1] * std[1]) ** 2
          + 2 * w[0] * w[1] * std[0] * std[1] * coef) ** 0.5
    up = rp - 0.5 * ra * vp ** 2
    sp = ((rp - rf) / vp) if vp != 0 else 0                        # avoid zero division

    return [w[0], w[1], rp, vp, up, sp]


def max_len(filename: str) -> int:
    """
    Extract all elemets within the file,
    find out which component with the
    longest length. Return the length of
    that component and the number of columns
    """
    with open(filename, 'r') as file:
        table = [line.split() for line in file.readlines()]        # 2-D array
        length = max([len(x) for row in table for x in row])       # adjust padding
        col = len(table[0])

    return length, col


def write_inputs(filename: str, usr_inputs: dict,
                 assets: list):
    """
    Receive user inputs and write them into .xls file.
    The column contain each asset's name and the row
    are asset attrs.
    =================================================
    Sample output:
    Attrs                Asset 1  Asset 2
    Expected return        .        .
    Volatility             .        .
    Coefficient            .
    Risk aversion          .
    Risk free              .
    """
    with open(filename, 'w') as file:
        file.write('Attrs')

        for asset in assets:                        # write asset titles for column names
            file.write(f'\t{asset}')

        for attrs, data in usr_inputs.items():      # write attrs and data
            file.write(f'\n{attrs}')

            for d in data:
                file.write(f'\t{d:.4f}')


def write_outputs(filename: str, usr_outputs: list, column_names: list):
    """
    Print out all possible weights, portoflio expected
    return, volatility, utility and sharpe ratio in a
    .xls file. Sorted by the portfolio return from the
    lowest to the highest.
    ==================================================
    Parameters:
    - filename: str
    - usr_outputs: list
        Two-dimensional array
    - column_names: list
    """
    with open(filename, 'w') as file:
        for name in column_names:                   # write column titles
            file.write(f'{name}\t')

        file.write('\n')                            # go to the next line

        for index, outputs in enumerate(usr_outputs):
            file.write(f'{index + 1}\t')            # index column
            for output in outputs:
                file.write(f'{output:.4f}\t')

            file.write('\n')


def read_keyboard(assets: list, attrs: list) -> dict:
    """
    Read asset attrs and data from keyboard inputs
    and store the inputs in a dictionary.
    ==============================
    Parameters:
    - attrs: list
        List of asset attrs
    - assets: list
        List of assets
    """
    usr_inputs = defaultdict(list)

    for asset in assets:
        print(f"\n**{asset}'s Info**")
        # input ER and std
        for attr in attrs[:2]:
            data = is_valid(f"Enter {attr} (0 to 1): ", edge=(0, 1))
            usr_inputs[attr].append(data)

    # input coef, ra and rf
    print('\n**Other Info**')
    edges = [(-1, 1), (1, 3), (0, 1)]               # boundary for each attribute
    for attr, edge in zip(attrs[2:], edges):
        data = is_valid(f"Enter {attr} ({edge[0]} to {edge[1]}): ", edge)
        usr_inputs[attr].append(data)

    return usr_inputs


def read_excel(filename: str) -> dict:
    """
    Import user inputs from excel. Please open/create a
    "inputs.xls" under the same directory and enter
    the data using the following layout:

    Attrs                Asset 1  Asset 2
    Expected return        .        .
    Volatility             .        .
    Coefficient            .
    Risk aversion          .
    Risk free              .

    This will return a dictionary that uses attributes as
    keys and input data as values. Please make sure to
    follow the instruction and the input file has been saved.
    """
    with open(filename, 'r') as file:
        usr_inputs = {}

        for line in file.readlines()[1:]:                   # ignore the cloumn titles
            info = line.split()

            attr, *data = info                              # unpack each line
            data = list(map(float, data))                   # convert str to float
            usr_inputs[attr] = data

    return usr_inputs


def print_excel(filename: str, header: str):
    """
    Read all contents within the parsing .xls
    file and print them out.
    =========================================
    Parameters
    - filename: str
    - header: str
        Title of the print out message
    """
    align, col_num = max_len(filename)                      # padding and no. of column
    n = (col_num * 3 + 29) // 2                             # length of section line

    with open(filename, 'r') as file:
        print('\n' + '=' * n + f' {header} ' + '=' * n)     # section line

        for line in file.readlines():
            print(line.split()[0].ljust(align), end='')     # left justify the first column

            # center justify the remaining columns
            data_col = []
            for cell in line.split()[1:]:
                # format user inputs to 4 decimal places
                try:
                    data_col.append(f'{float(cell):^{align + 1}.4f}')
                except ValueError:
                    data_col.append(cell.center(align + 1))  # except for the column titles

            print(' '.join(data_col))

        print('=' * n + f' {header} ' + '=' * n)


def print_stats(stats: list, highlight: str) -> str:
    """Print out portfolio's details"""
    info = f"""
        Portfolio with the highest {highlight}:
        ========================================
        Weight of asset 1:        {stats[0]:>13.4f}
        Weight of asset 2:        {stats[1]:>13.4f}
        Expected return:          {stats[2]:>13.4f}
        Volatility:               {stats[3]:>13.4f}
        Utility:                  {stats[4]:>13.4f}
        Sharpe ratio:             {stats[5]:>13.4f}
        ========================================
        """

    print(indent(dedent(info), prefix='\t'))


if __name__ == '__main__':
    main()
