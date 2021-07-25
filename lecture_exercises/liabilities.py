import numpy_financial as npf

ir = 0.08
coupon_rate = 0.1
par = 500000
nper = 10

pv = npf.pv(ir, nper, coupon_rate * par, par)
print('the present value is:', round(pv * -1, 2))
