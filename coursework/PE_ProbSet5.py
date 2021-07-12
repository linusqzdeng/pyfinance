import matplotlib.pyplot as plt


def hurdle(rate, nper, init_invt):
    return rate * nper * init_invt


def carry_available(gcg, hurdle):
    carry = gcg - hurdle
    return carry if carry >= 0 else 0


def actual_carry(carried_int, gcg, carry_available):
    pro_forma = carried_int * gcg
    carry = carry_available - pro_forma
    return pro_forma if carry >= 0 else carry_available


init_invt = 2000
management_fees = [0.02, 0.01]
carried_int = [0.2, 0.3]
hurdle_rate = [0.07, 0.1]

proceeds = [p for p in range(init_invt, init_invt * 3 + 1, 200)]
gross_capital_gain = [p - init_invt for p in proceeds]
lifetime = [t for t in range(1, 21)]

hurdle_a = [hurdle(hurdle_rate[0], nper, init_invt) for nper in lifetime]
hurdle_b = [hurdle(hurdle_rate[1], nper, init_invt) for nper in lifetime]

carry_a = [carry_available(gcg, hurdle) for gcg, hurdle in zip(gross_capital_gain, hurdle_a)]
carry_b = [carry_available(gcg, hurdle) for gcg, hurdle in zip(gross_capital_gain, hurdle_b)]

actual_carry_a = [actual_carry(carried_int[0], gcg, carry_available) for gcg, carry_available in zip(gross_capital_gain, carry_a)]
actual_carry_b = [actual_carry(carried_int[1], gcg, carry_available) for gcg, carry_available in zip(gross_capital_gain, carry_b)]

print(gross_capital_gain)
print(hurdle_b)
print(carry_b)
print(actual_carry_a)
print(actual_carry_b)
