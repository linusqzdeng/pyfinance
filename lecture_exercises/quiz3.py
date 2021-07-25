import numpy_financial as npf
import numpy as np

## question 1
# coc = 0.1
# pmt = [14, -5, -5 ,-5]
# npv = npf.npv(coc, pmt)
# print(npv)

## question 2
cf_a = np.array([-41215, 12500, 14000, 16500, 18000, 20000, 0])
cf_b = np.array([-46775, 15000, 15000, 15000, 15000, 15000, 15000])

incremental_cf = cf_a - cf_b
print(incremental_cf)

# calculate the incremental IRR
incre_irr = npf.irr(incremental_cf)
print('the incremental IRR is:', incre_irr)