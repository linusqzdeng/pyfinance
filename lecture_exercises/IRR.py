import numpy_financial as npf

pmt = [30000, -2000, -2000, -2000, -2000, -2000, -2000, -2000
        -2000, -2000, -2000, -2000, -2000]

EAR = 0.12
ir_mon = 0.1139 / 12
npv = npf.npv(ir_mon, pmt)

mon_irr = npf.irr(pmt)
yr_irr = mon_irr * 12


# print(npv)
print(mon_irr)
# print(yr_irr)
