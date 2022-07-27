import numpy as np

def define_bounds(NoofPeaks, Emin, Emax, back):

    #defines bounds and puts it in an array for curve_fit
    bound_min = []
    bound_max = []
    for i in range(NoofPeaks):
        bound_min.append(Emin)
        bound_min.append(0.0)
        bound_min.append(0.01)
        bound_max.append(Emax)
        bound_max.append(np.inf)
        bound_max.append(2.0)
        #print('bm', bound_min, bound_max)

    for j in range(len(back)):
        bound_min.append(-np.inf)
        bound_max.append(np.inf)

    bound_all = []
    bound_all.append(tuple(bound_min))
    bound_all.append(tuple(bound_max))
    print(bound_all)

    return bound_all





