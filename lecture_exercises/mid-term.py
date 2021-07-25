# Define the functions

## Return the Efective Annual Interest Rate
def ear(ir, nper):
    return ((1 + ir / nper) ** nper) - 1

## Return the stated interest rate
def ir(ear, nper):
    return (1 + ear) ** (1 / nper) - 1

## Return the nominal interest rate
def nominal(inflation, real_ir):
    return (real_ir + 1) * (inflation + 1) - 1

ir = 0.079
print(ear(ir, 99999))