import globals

def Energy_Corrections():

    print(globals.E_Corr_GE1_apply)

    if globals.E_Corr_GE1_apply:
        globals.x_GE1 = lincorr(globals.x_GE1, globals.E_Corr_GE1_gradient, globals.E_Corr_GE1_offset)

    if globals.E_Corr_GE2_apply:
        globals.x_GE2 = lincorr(globals.x_GE2, globals.E_Corr_GE2_gradient, globals.E_Corr_GE2_offset)

    if globals.E_Corr_GE3_apply:
        globals.x_GE3 = lincorr(globals.x_GE3, globals.E_Corr_GE3_gradient, globals.E_Corr_GE3_offset)

    if globals.E_Corr_GE4_apply:
        globals.x_GE4 = lincorr(globals.x_GE4, globals.E_Corr_GE4_gradient, globals.E_Corr_GE4_offset)


def lincorr(x, m, c):
    new_x = x*float(m)+float(c)

    return new_x
