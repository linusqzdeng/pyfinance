import random


def task1_a1():
    """
    Write a program that prompts the user to
    enter a real number, computers the square root
    of the number and prints it out in two decimal places.
    """
    x1 = float(input('Enter a real number: '))
    print(f'{x1**0.5:.2f}')


def task1_a2():
    """
    Write a program that prompts the user to enter
    a real number and an integer number n, computers the number
    in power n and prints it out in two decimal places.
    """
    x2 = float(input('Enter a real number: '))
    n = int(input('Enter an integer: '))
    print(f'{x2**n:.2f}')


def task1_a3():
    """
    Write a program that generates a random number between
    0.0 and 1.0 and prints it out in two decimal spaces.
    """
    x3 = random.random()
    print(f'{x3:.2f}')


def task1_b1():
    """
    Write a program that prompts the user for his/her initials,
    validates the case of the characters (upper or lower) and prints
    hem out in upper case.
    """
    initials = input('Please enter you name initials: ')
    print(initials.upper())


def task1_b2():
    """
    Write a program that prompts the user for his/her
    name and prints it out in lower case.
    """
    name = input('Please enter your name: ')
    print(name.lower())


def task1_b3():
    """
    Write a program that it prompts the user for the time t validated
    to be positive only, an amount to be received at time t validated
    to a positive real number, the discounting rate validated to be between
    0.0 and 1.0 and computes the discounted value. Make use of arithmetical,
    short cut assignment, and logical operators where appropriate.
    """

    # Asking user for entering term time
    while True:

        try:
            nper = int(input('Enter the term time for discounting: '))

            if nper > 0:
                break
            else:
                print('Term time should only be a positive integer. Please enter again.\n' + '==' * 30)

        except ValueError:
            print('Please enter a positive integer!\n' + '==' * 30)

    # Asking user for entering future value
    while True:

        try:
            fv = float(input('Enter the amount your would receive at term time: '))

            if fv > 0:
                break
            else:
                print('Future value must be a positive real number. Please enter again.\n' + '==' * 30)

        except ValueError:
            print('Please enter a valid number!\n' + '==' * 30)

    # Asking user for entering discount rate
    while True:
        try:
            rate = float(input('Enter the discount rate ranging from 0 to 1: '))

            if 0.0 < rate < 1.0:
                break
            else:
                print('Discount rate must between 0 and 1. Please enter again.\n' + '==' * 30)

        except ValueError:
            print('Please enter a valid number!\n' + '==' * 30)

    print('==' * 10 + 'Inputs' + '==' * 15)
    print(f"""
        Number of year: {nper}
        Future value: {fv}
        Discount rate: {rate}
        """)

    pv = fv / (1 + rate) ** nper

    print(f'The present value of your money is: {pv:.2f}')


def task1_b4():
    """
    Write a program that prompts the user for a character, checks to see whether it
    is a white space character. White space characters are ‘ ‘, ‘\n’, ‘\t’. If the
    non-white character is entered in upper case it converts it to lower case.
    """
    while True:
        prompts = input('Enter a character: ')

        if prompts.isspace():
            print('Your input contains white space characters. Please re-enter.')
            continue
        else:
            break

    print(prompts.lower())


def task2_a(k=100):
    """
    Consider an equity based call option with an exercise price of K= 100. Write a program
    that prompts the user the for market stock price at time t, it validates the stock price
    against the exercise and computes the option payoff and a comment on whether the “right
    to buy” is exercised or not. Use the time t option payoff formula C=MAX[St-K,0].
    Create various versions of the program using different conditional statements.
    """
    stock_price = float(input('Enter the current stock price: '))
    payoff = max(stock_price - k, 0)

    if payoff == 0:
        print('The current stock price is lower than the strike price, option would not be exercised.')
    elif payoff == k:
        print('Stock price and exercise price are the same, you could either exercise or not.')
    else:
        print(f'The payoff of your option is: {payoff}')


def task2_b(r_x=0.15, r_y=0.21):
    """
    Assume a simple case of a two-fund separation problem with stock x with return of 15%
    and stock y with a rate of return on 21% combined in a portfolio. Write a program that
    prompts the user for the capital weights and computes the portfolio’s rate of return.
    Add validation safeguards where appropriate.
    """
    while True:

        try:
            w_x = float(input('Enter the weight of stock x, ranging from 0 to 1: '))

            if 0 < w_x < 1:
                break
            else:
                print('Stock weight must between 0 and 1.')

        except ValueError:
            print('Please enter a valid number between 0 and 1.')

    w_y = 1 - w_x
    portfolio_return = w_x * r_x + w_y * r_y

    print(f'The return of the portfolio is: {portfolio_return:.2%}')


def task3_a(rate=0.1, nper=15, pmt=30000):
    """
    Assume you plan to retire in t years and want to accumulate enough by then to provide yourself
    with $30,000 a year for 15 years. The interest rate is 10 percent. Write a program that prompts
    the user for the time t to retirement and computes the amount accumulated by the time you retire.
    The time entered should be positive
    """
    pv = pmt * (1 / rate - 1 / (rate * (1 + rate)**nper))

    time_to_retirement = int(input('How many years left until you retire? '))

    acc_amount = pv / (1 + rate)**time_to_retirement

    print(f'The amount you need to accumulate now is: ${acc_amount:.2f}')


def task3_b(rate=0.1, nper=15, pmt=30000):

    time_to_retirement = int(input('How many years left until you retire? '))

    # calculate the present value of pension in retirement
    pv = 0
    for i in range(1, nper + 1):
        pv += pmt / (1 + rate)**i

    acc_amount = pv / (1 + rate)**time_to_retirement

    print(f'The amount you need to accumulate now is: ${acc_amount:.2f}')


def task4_a1():
    """
    Write a program to count blanks, tabs, and newlines
    """
    s = input('Please enter your input: ')

    # for loop for computing the white space characters
    count = 0

    for i in s:
        if i.isspace():
            count += 1

    print(f'There are {count} white space in your input.')


def task4_a2():
    """
    Write a program to copy its input to its output,
    replacing each string of one or more blanks by a single blank.
    """
    s = input('Enter your input: ')

    print(' '.join(s.split()))


def task4_a3():
    """
    Write a program to copy its input to its output, replacing each
    tab by \t, each backspace by \b, and each backslash by \\. This
    makes tabs and backspaces visible in an unambiguous way.
    """
    s = input('Enter your inpyt: ')

    s = s.replace('\t', '\\t')
    s = s.replace('\b', '\\b')

    print(s)


def task4_a4():
    """
    Write a program that prints its input one word perline.
    """
    s = input('Please enter your input: ')

    s_list = s.split(sep=' ')

    for word in s_list:
        print(word)


def task4_b1():
    """
    Write a program that prompts the user to enter his/her
    name one character at a time as part of a loop and assigns
    them to a string variable. The program should also print the
    name one character at a time using another for loop
    """
    letters = []

    while True:

        name = input("Please enter your name one character each time (finish by entering 'quit'): ")

        if name == 'quit':
            break
        elif len(name) == 1:
            letters.append(name)
        else:
            print('You must enter one character each time.')
            continue

    for letter in letters:
        print(letter)


def task4_b2():
    """
    Write a program that prompts the user to enter a sentence and
    it should use a for loop to pick up and counts the number of
    times the character ‘a’ or ‘A’ is present in the sentence.
    """
    s = input('Please enter a sentence: ')

    # define a counter
    count = 0

    for i in s:
        if i == 'a' or i == 'A':
            count += 1

    print(f"The frequency of the character 'a' or 'A' is {count}")


def task5_b_34():
    """
    Write a program to process a savings-account withdrawal. The program
    should request the current balance and the amount of the withdrawal as
    input and then display the new balance. If the withdrawal is greater than
    the original balance, the program should display “Withdrawal denied.”
    If the new balance is less than $150, the message “Balance below $150”
    should also be displayed.
    """
    current_balance = float(input('Please enter your current balance: '))
    withdrawal_amount = float(input('Please enter the amount you would like to withdrawal: '))
    new_balance = current_balance - withdrawal_amount

    if new_balance < 0:
        print('Withdrawal denied')
    elif new_balance < 150:
        print('Balamce below 150')

    print(f'The new balance is ${new_balance:.2f}')


def task5_b_35():
    """
    Write a program that asks the user to enter a single uppercase letter and
    then informs the user if they didn’t comply with the request.
    """
    prompts = input('Enter a single uppercase letter: ')

    if prompts != prompts.upper():
        print('You did not comply with the request.')
    else:
        print('Well done!')


def task5_b_39():
    """
    Write a program that compares interest rates offer by two banks, and determine
    the most favourable interst rate.
    """
    ir_1 = float(input('Enter the annual interest rate for Bank 1: '))
    nper_1 = int(input('Enter the number of compounded period for Bank 1: '))

    ir_2 = float(input('Enter the annual interest rate for Bank 2: '))
    nper_2 = int(input('Enter the number of compounded period for Bank 2: '))

    apy_1 = (1 + ir_1 / nper_1) ** nper_1 - 1
    apy_2 = (1 + ir_2 / nper_2) ** nper_2 - 1

    which_better = max(apy_1, apy_2)

    print(f'APY for Bank 1 is: {apy_1:.3%}')
    print(f'APY for Bank 2 is: {apy_2:.3%}')

    if which_better == apy_1:
        print('Bank 1 is the better bank')
    else:
        print('Bank 2 is the better bank')


def task5_b_31(initial_balance=1000):
    """
    Write a menu-driven program that allows the user to make transactions to a
    savings account. Assume that the account initially has a balance of $1,000.
    """
    print("""
        Options:
        1. Make a deposit
        2. Make a withdrawal
        3. Obtain balance
        4. Quit
        """)

    balance = initial_balance

    while True:

        # validate the selection number
        try:
            selection = int(input('Make a selection from the option menu: '))
        except ValueError:
            print('Please enter a valid number.')
            continue

        # display messages in terms of selection
        if selection == 1:

            while True:
                try:
                    deposit = float(input('Enter the amount of deposit: '))
                    balance += deposit
                    break
                except ValueError:
                    print('Please enter a valid number.')
                    continue

        elif selection == 2:

            while True:
                try:
                    withdrawal = float(input('Enter the amount of withdrawal: '))

                    # check if the withdrawal exceeds the current balance
                    if withdrawal > balance:
                        print(f'Denied. Maximum withdrawal is: ${balance:.2f}')
                        continue
                    else:
                        balance -= withdrawal
                        break
                except ValueError:
                    print('Please enter a valid number.')
                    continue

        elif selection == 3:
            print(f'Balance: ${balance:.2f}')

        elif selection == 4:
            break

        else:
            print('Please only select the number from the option menu: ')
            continue


def main():

    func = [
        task1_a1, task1_a2, task1_a3,
        task1_b1, task1_b2, task1_b3,
        task1_b4, task2_a, task2_b,
        task3_a, task3_b, task4_a1,
        task4_a2, task4_a4, task4_b1,
        task4_b2, task5_b_31, task5_b_34,
        task5_b_35, task5_b_39
    ]

    for i, func in enumerate(func, start=1):
        print('**' * 15 + f'Question {i}' + '**' * 15)
        func()


main()
