# Write a Python program that computes the future value of $100,000 received
# today and values it a year from now. Assume an annual interest rate of
# 0.0245. The computed value should be output right adjusted, with two decimal
# places and with the £ symbol appended.

import numpy_financial as npf

pv = 100000
ir = 0.0245
nper = 1

fv = npf.fv(rate=ir, nper=nper, pv=-pv, pmt=0)

print("£" + "{:.2f}".format(fv).rjust(10))
