from abc import ABCMeta, abstractmethod

import numpy as np

from .particle_numerics import vicsek_angular, vicsek_vectorial


class BaseVicsekModel(object):
    __metaclass__ = ABCMeta

    def __init__(self, n, L, eta, v_0):
        self.L = L
        self.eta = eta
        self.v_0 = v_0

        self.r = np.random.uniform(-self.L_half, self.L_half, size=(n, 2))
        self.th = np.random.uniform(-np.pi, np.pi, size=self.n)

    @property
    def eta_half(self):
        return self.eta / 2.0

    @property
    def n(self):
        return self.r.shape[0]

    @property
    def d(self):
        return self.r.shape[1]

    @property
    def L_half(self):
        return self.L / 2.0

    @property
    def r_v(self):
        return 1.0

    @property
    def u(self):
        return np.array([np.cos(self.th), np.sin(self.th)]).T

    @property
    def v(self):
        return self.v_0 * self.u

    @property
    def macro_u(self):
        return np.mean(self.u, axis=0)

    @property
    def macro_u_mag(self):
        return np.sqrt(np.sum(np.square(self.macro_u)))

    def _move_wrap(self):
        self.r += self.v
        self.r[self.r > self.L_half] -= self.L
        self.r[self.r < -self.L_half] += self.L

    @abstractmethod
    def iterate(self):
        self._move_wrap()


class AngularVicsekModel(BaseVicsekModel):

    def iterate(self):
        self.th[...] = vicsek_angular(self.r, self.th, self.L, self.r_v,
                                      self.eta)
        super(AngularVicsekModel, self).iterate()


class VectorialVicsekModel(BaseVicsekModel):

    def iterate(self):
        self.th[...] = vicsek_vectorial(self.r, self.th, self.L, self.r_v,
                                        self.eta)
        super(VectorialVicsekModel, self).iterate()


def vicsek_model_factory(model, **model_args):
    '''Make a VicsekModel object

    model: one of ('angular', 'vectorial')
    '''
    if model == 'angular':
        return AngularVicsekModel(**model_args)
    elif model == 'vectorial':
        return VectorialVicsekModel(**model_args)
    else:
        raise ValueError('Invalid model string')
