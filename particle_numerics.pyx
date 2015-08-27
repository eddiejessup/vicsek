import numpy as np
from ciabatta import vector
cimport numpy as np
cimport cython
import cmath
from cellulist import cell_list


@cython.cdivision(True)
@cython.boundscheck(False)
def vicsek_angular(np.ndarray[np.float_t, ndim=2] r,
                   np.ndarray[np.float_t, ndim=1] th,
                   double L, double r_v, double eta):
    cdef:
        unsigned int i_1, i_i_2
        complex comp
        np.ndarray[np.float_t, ndim=1] th_vic = th.copy()
        np.ndarray[np.float_t, ndim=1] noise = np.random.uniform(-np.pi, np.pi, size=th.shape[0])
        tuple res = cell_list.get_inters(r, L, r_v)
        np.ndarray[int, ndim=2] inters = res[0]
        np.ndarray[int, ndim=1] intersi = res[1]
    for i_1 in range(th.shape[0]):
        comp = cmath.exp(1.0j * th[i_1])
        for i_i_2 in range(intersi[i_1]):
            comp += cmath.exp(1.0j * th[inters[i_1, i_i_2] - 1])
        th_vic[i_1] = cmath.phase(comp / (intersi[i_1] + 1.0)) + eta * noise[i_1]
    return th_vic


@cython.cdivision(True)
@cython.boundscheck(False)
def vicsek_vectorial(np.ndarray[np.float_t, ndim=2] r,
                     np.ndarray[np.float_t, ndim=1] th,
                     double L, double r_v, double eta):
    cdef:
        unsigned int i_1, i_i_2
        complex comp
        np.ndarray[np.float_t, ndim=1] th_vic = th.copy()
        np.ndarray[np.float_t, ndim=1] noise = np.random.uniform(-np.pi, np.pi, size=th.shape[0])
        tuple res = cell_list.get_inters(r, L, r_v)
        np.ndarray[int, ndim=2] inters = res[0]
        np.ndarray[int, ndim=1] intersi = res[1]
    for i_1 in range(th.shape[0]):
        comp = cmath.exp(1.0j * th[i_1])
        for i_i_2 in range(intersi[i_1]):
            comp += cmath.exp(1.0j * th[inters[i_1, i_i_2] - 1])
        th_vic[i_1] = cmath.phase(comp / (intersi[i_1] + 1.0) + eta * cmath.exp(1.0j * noise[i_1]))
    return th_vic
