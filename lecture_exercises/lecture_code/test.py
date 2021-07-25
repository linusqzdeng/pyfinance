
import numpy as np
from collections import defaultdict

np.random.seed(1)
a = np.random.randint(10, size=(3, 6))

# print(a)


# def draw_grid(arr: list):
#     row = ' ---'
#     column = '| '

#     row_num = len(arr)
#     col_num = len(arr[0])

#     for r in range(row_num):
#         print(row * col_num)

#         for c in range(col_num):
#             print(column + f'{arr[r][c]}', end=' ')

#         print(column)
#     print(row * col_num)


# draw_grid(a)

def is_valid(msg: str, edge: tuple) -> bool:
    """
    Validate user inputs.
    =========================================
    Parameters:
    - msg: str
        message prompts to users
    - edge: tuple
        the upper and the lower limit for
        keeping user inputs within the bound

    Returns:
    - data: float
    """
    valid = False

    while not valid:
        try:
            data = float(input(msg))
            if edge[0] <= data <= edge[1]:                    # check if input is within the limits
                valid = True
            else:
                print('**' * 25,
                      f'Enter value between {edge[0]} and {edge[1]}.',
                      'Please enter again.',
                      '**' * 25,
                      sep='\n')

        except ValueError as e:
            print('**' * 25,
                  f'ValueError: {e}',
                  'Please enter a float type.',
                  '**' * 25,
                  sep='\n')

    return data


def read_keyboard(assets: list,
                  attrs=['ER', 'std', 'coef', 'ra', 'rf']) -> dict:
    """

    """
    usr_inputs = defaultdict(list)

    for asset in assets:
        # inputs for ER and std
        for attr in attrs[:2]:
            data = is_valid(f"Enter {asset}'s {attr}: ", edge=(0, 1))
            usr_inputs[attr].append(data)

    # inputs for coef, ra and rf
    edges = [(-1, 1), (1, 3), (0, 1)]
    for attr, edge in zip(attrs[2:], edges):
        prompts = f"Enter the {attr}: "
        data = is_valid(f"Enter {attr}: ", edge=edge)
        usr_inputs[attr].append(data)

    return usr_inputs


print(read_keyboard(['asset 1', 'asset 2']))
