
# ============================= Basic Info ============================
# Program: Two-fund Separation (Python 3.8.8)
# Course: SMM283 Introduction to Python
# Date: 4th June 2021
# Author: Qizhong Deng
# Student ID: 200041681

# ============================ Discription ============================
# This program is designed for helping user to find the
# optimal weights of a two-fund portfolio. By entering
# assets expected return, volatility, correlation coefficient,
# risk aversion coefficient and the risk free rate, users are
# expecting to see all possible portfolios with asset weights,
# portfolio returns, volatility, utility and sharpe ratio.

# ============================ Structure ==============================
# Main function can be divided into 3 parts:
# 1. User inputs
#     - Asking user to decided data-entering method, either by
#       key board or read inputs from excel file
#     - Validate if the input values are within the limits
#     - Store user inputs into a dictionary
#     - Print out user inputs and ask user whether they enter correctly
#       - if not, rerun the program and enter again
#       - if yes, write user inputs to a file "inputs.xls"
# 2. Capital weights generation
#     - Prompt user to choose which method would they prefer to
#       generate capital weights
#       - Self-increment
#       - HL method
# 3. User outputs
#     - Calculate portfolio's attributes
#     - Convert them into a two-dimensional array
#     - Sort the outputs by portfolio's expected return (ascending)
#     - Display user outputs on screen
#     - Find out the market portfolio and highest utility portfolio
#       and print out their corresponding attributes
#     - Ask if the user would like to rerun the program
#       - if not, end the program
#
# PS: 1. Use the "input.xls" as a template to enter asset data. Otherwise,
#     it will cause encoding error when reading from excel.
#     2. The outputs in the attached excel file are derived from the
#     following inputs (via self-incremented weights, interval=0.001):
#
#     attr     asset1  asset2
#      ER       0.25    0.18
#      std      0.15    0.10
#      coef    -0.70
#      ra       2.00
#      rf       0.05


import os.path
import sys


def main():

    input_file = Excel('inputs.xls')
    output_file = Excel('outputs.xls')
    input_columns = ['asset1', 'asset2']
    output_columns = ['w1', 'w2', 'Return', 'Risk', 'Utility', 'Sharpe']

    over = False

    ## ========================= Receive user inputs ========================= ##

    while not over:

        print("""
            DATA ENTER MENU
            1. Read from keyboard
            2. Read from Excel file
            """)

        Asset.asset_num = 0                                       # reset asset number

        choice = input('How would you like to enter the data: ')

        # input data via keyboard
        if choice == '1':
            a1 = Asset()
            a2 = Asset()
            Asset.common_attrs()

            usr_inputs = {"ER": [a1.rt, a2.rt],
                          'std': [a1.std, a2.std],
                          'coef': [Asset.coef],
                          'ra': [Asset.ra],
                          'rf': [Asset.rf]}

            input_file.write_inputs(usr_inputs, input_columns)    # write inputs to .xls file
            input_file.print_excel('Inputs')                      # print inputs on screen

            # enter inputs again if there are some mistakes
            print('You have successfully input the data!')
            check = input("Press 'Enter' if the above inputs "
                          "are correct: ")
            if check != '':
                continue

        # read data from .xls file
        elif choice == '2':
            print(Excel.read_excel.__doc__)                       # input guideline

            # check if the "inputs.xls" exits under the same dir
            if not input_file.is_exist():
                print('There is no input file exists.',
                      'Please create "inputs.xls" under current'
                      'directory and rerun the program.',
                      sep='\n')
                sys.exit()

            # check if user enter the inputs properly
            if input_file.is_empty():
                print('You have not input any value or there'
                      'are some missing values.',
                      'Please enter data follow the template '
                      'and rerun the program.',
                      sep='\n')
                sys.exit()

            usr_inputs = input_file.read_excel()                  # assign excel inputs to a dict

            # assign inputs to Asset objects
            from_keyboard = False
            a1 = Asset(usr_inputs, from_keyboard)
            a2 = Asset(usr_inputs, from_keyboard)
            Asset.common_attrs(usr_inputs, from_keyboard)

            input_file.print_excel('Inputs')                      # print inputs on screen

            # loop again if user does not confirm
            print('You have successfully imported the data!')
            check = input("Press 'Enter' if the above inputs "
                          "are correct: ")
            if check != '':
                continue

        # loop again
        else:
            print('Please select the choice from menu')
            continue

    ## ========================= Generate capital weights ========================= ##

        # prompt user to choose whether to use
        # HL method to generate capital weights
        while True:

            print("""
            WEIGHTS GENERATING OPTIONS
            1. Self-increment
            2. HL method
                """)

            choice = input('How would you like to generate capital weights: ')

            slices = 100

            if choice == '1':
                w_1, w_2 = Asset.generate_weights(slices)
                break

            elif choice == '2':
                w_1, w_2 = Asset.generate_weights(slices, a1.rt, a2.rt, h_l=True)
                break

            else:
                print('Please select the choice from menu')
                continue

    ## ========================= Display user outputs ========================= ##

        # list of all portfolio objects
        portfolios = [Portfolio([w1, w2], usr_inputs['ER'], usr_inputs['std'],
                                Asset.coef, Asset.ra, Asset.rf) for w1, w2 in zip(w_1, w_2)]

        # two-dimendional array of asset weights, portfolio's
        # return, volatility utility and sharpe ratio
        usr_outputs = [[port.w[0], port.w[1], port.rp, port.vp, port.up, port.sp]
                       for port in portfolios]

        usr_outputs.sort(key=lambda x: x[2])                      # sorted by rp
        output_file.write_outputs(usr_outputs, output_columns)    # write outputs to .xls file
        output_file.print_excel('Outputs')                        # print outputs on screen

        s_p = [port.sp for port in portfolios]                    # portfolios' sharpe ratio
        u_p = [port.up for port in portfolios]                    # portfolios' utility

        mkt_p = portfolios[s_p.index(max(s_p))]                   # indices are corresponded
        best_up = portfolios[u_p.index(max(u_p))]

        print(mkt_p.__str__('Sharpe ratio'))                      # print out portfolio with the highest
        print(best_up.__str__('Utility'))                         # sharpe ratio and utility

        # ask if the user want to run again
        again = input('Would you like to run the program again [y/n]? ')

        if again == 'n':
            over = True


def is_valid(msg: str, range: tuple) -> bool:
    """
    Validate user inputs.
    =========================================
    Parameters:
    - msg: str
        message prompts to users
    - range: tuple
        the upper and the lower limit for
        keeping user inputs within the bound

    Returns:
    - data: float
    """
    valid = False

    while not valid:
        try:
            data = float(input(msg))
            if range[0] <= data <= range[1]:                    # check if input is within the limits
                valid = True
            else:
                print(f'Input value between {range[0]} and {range[1]}.')

        except Exception as e:
            print('Error: ', e)
            print('--' * 26)
            print('Please enter a float type.')

    return data


class Asset:

    asset_num = 0

    def __init__(self, usr_inputs: dict=None, from_keyboard=True):
        """
        If user choose to input via keyboard and no user inputs
        are given, tigger the input prompts; else unpack user inputs
        """
        Asset.asset_num += 1                                      # count the number of object

        if not from_keyboard and usr_inputs:
            self.usr_inputs = usr_inputs
            self.rt = self.usr_inputs['ER'][Asset.asset_num - 1]  # start from the first element
            self.std = self.usr_inputs['std'][Asset.asset_num - 1]
        else:
            self.rt = is_valid(f"Enter asset{Asset.asset_num}'s expected return: ", (0, 1))
            self.std = is_valid(f"Enter asset{Asset.asset_num}'s standard deviation: ", (0, 1))

    @classmethod
    def common_attrs(cls, usr_inputs: dict=None, from_keyboard=True):
        """
        If from_keyboard is True, prompt user to enter data and pass it
        to class variables; else, take attributes in user inputs as
        class variables
        """
        if not from_keyboard and usr_inputs:
            cls.coef = usr_inputs['coef'][0]
            cls.ra = usr_inputs['ra'][0]
            cls.rf = usr_inputs['rf'][0]
        else:
            cls.coef = is_valid('Enter correlation coefficient: ', (-1, 1))
            cls.ra = is_valid('Enter risk aversion coefficient: ', (1, 3))
            cls.rf = is_valid('Enter risk free rate: ', (0, 1))

    @staticmethod
    def generate_weights(sep: int, r1=None,
                         r2=None, h_l=False) -> list:
        """
        Return w1, w2 start from 0.0000 to 1.0000,
        the interval equals to 1/sep.
        w1 + w2 = 1
        """
        if h_l and r1 and r2:
            g1 = r2 / (r2 - r1)
            g2 = 1.0 - g1
            h1 = 1.0 / (r1 - r2)
            h2 = -h1

            r_p = [i / sep for i in range(sep + 1)]              # target return from 0.0 to 1.0

            w1 = [g1 + rp * h1 for rp in r_p]
            w2 = [g2 + rp * h2 for rp in r_p]

            return w1, w2

        w1 = [i / sep for i in range(sep + 1)]
        w2 = [1.0 - w for w in w1]

        return w1, w2


class Portfolio:

    def __init__(self, w: list, rt: list, std: list,
                 coef: float, ra: float, rf: float):
        """
        Parameters:
        - w: list
            1-D array contains weight of each asset
        - rt: list
            1-D array of each asset's expected return
        - std: list
            1-D array of each asset's volatility/risk
        - coef: float
            correlation coefficient between assets
        - ra: float
            risk aversion coefficient varies from
            different users
        - rf: float
            risk free rate at current time

        Returned properties:
        - rp: float
            portfolio's expected return
        - vp: float
            portfolio's standard deviation
        - up: float
            portfolio's utility
        - sp: float
            portfolio's sharpe ratio combined with
            risk free asset
        """
        self.w = w
        self.rt = rt
        self.std = std

        # sum product of weights and returns
        self.rp = sum([w * rt for w, rt in zip(self.w, self.rt)])
        self.vp = ((self.w[0] * self.std[0])**2 + (self.w[1] * self.std[1])**2 +
                   2 * self.w[0] * self.w[1] * self.std[0] * self.std[1] * coef)**0.5
        self.up = self.rp - 0.5 * ra * self.vp**2
        self.sp = (self.rp - rf) / self.vp

    def __str__(self, attr: str):
        """Print out portfolio's details"""
        info = f"""
            Portfolio with the highest {attr}:

                Weight of asset 1: {self.w[0]:.4f}
                Weight of asset 2: {self.w[1]:.4f}
                Expected return: {self.rp:.4f}
                Volatility: {self.vp:.4f}
                Sharpe ratio: {self.sp:.4f}
                Utility: {self.up:.4f}
            ========================================
            """

        return info


class Excel:

    def __init__(self, filename: str):
        self.filename = filename

    def is_exist(self) -> bool:
        """Dectect if inputs file exist under the current dir"""
        return os.path.isfile(self.filename)

    def is_empty(self) -> bool:
        """
        Check if there are missing values in input file.
        Except for the first line, input component ought
        to be exactly 12.
            attr     asset1  asset2
            ER         .      .
            std        .      .
            coef       .
            ra         .
            rf         .
        Return True if inputs are not entered properly.
        """
        try:
            with open(self.filename, 'r') as file:
                component = 0                               # count the total elements

                for line in file.readlines()[1:]:           # first line does not count
                    component += len(line.split())          # no. of elements each line

                return False if component == 12 else True

        except Exception as e:
            print(e)
            return True

    def read_excel(self) -> dict:
        """
        Import user inputs from excel. Please open/create a
        "inputs.xls" under the same directory and enter
        the data using the following layout:

        attr     asset1  asset2
        ER         .      .
        std        .      .
        coef       .
        ra         .
        rf         .

        where ER ---- asset's expected return
              std ---- asset's volatility
              coef ---- correlation coefficient
              ra ---- risk aversion coefficient
              rf ---- risk free rate.

        Return a dictionary that uses attributes as keys and
        input data as values.
        """
        with open(self.filename, 'r') as file:
            usr_inputs = {}

            for line in file.readlines()[1:]:           # ignore column names
                info = line.split()                     # convert each line to a list

                attr, *data = info                      # unpack each line
                data = list(map(float, data))
                usr_inputs[attr] = data

        return usr_inputs

    def write_inputs(self, usr_inputs: dict, assets: list):
        """
        Receive user inputs and write them into .xls file.
        The column contain each asset's name and the row
        are asset attributes.
        =================================================
        Parameters:
        - usr_inputs: dict
            contains asset attributes and the
            data for each asset
        - assets: list
            assets of interest

        Sample output:
            attr     asset1  asset2
            ER         .      .
            std        .      .
            coef       .
            ra         .
            rf         .
        """
        with open(self.filename, 'w') as file:
            file.write('attr')                          # first column title

            for asset in assets:                        # asset names
                file.write(f'\t{asset}')

            for attrs, values in usr_inputs.items():    # write attribute names
                file.write(f'\n{attrs}')

                for value in values:                    # write data
                    file.write(f'\t{value:.4f}')

    def write_outputs(self, usr_outputs: list, column_names: list):
        """
        Write all elements with the user outputs to .xls file.
        =====================================================
        Parameters:
        - usr_outputs: list
            two-dimensional array
        - column_names: list
            title of each column
        """
        with open(self.filename, 'w') as file:
            for name in column_names:
                file.write(f'{name}\t')

            file.write('\n')                            # go to the next line

            for output in usr_outputs:                  # write user outputs
                for data in output:
                    file.write(f'{data:.4f}\t')

                file.write('\n')

    def print_excel(self, header: str):
        """
        Read all contents within the parsing .xls
        file and print them out.
        =========================================
        Parameters
        - header: str
            title of the print out message
        """
        print('=' * 28 + f'{header}' + '=' * 28)        # section line

        with open(self.filename, 'r') as file:
            for line in file.readlines():
                cells = line.split()                    # one cell one element in the list

                for cell in cells:
                    print(f'{cell:<10s}', end=' ')

                print('\n')                             # go to the next line


if __name__ == '__main__':
    main()
