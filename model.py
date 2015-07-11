from abc import ABCMeta, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
from ciabatta.cell_list import intro
from particle_numerics import vicsek_angular, vicsek_vectorial


class BaseVicsekModel(object):
    __metaclass__ = ABCMeta

    def __init__(self, n, L, eta, v_0):
        self.d = 2
        self.n = n
        self.L = L
        self.L_half = L / 2.0
        self.eta = eta
        self.eta_half = eta / 2.0
        self.r_v = 1.0
        self.v_0 = v_0

        self.r = np.random.uniform(-self.L_half,
                                   self.L_half, size=(self.n, self.d))
        self.th = np.random.uniform(-np.pi, np.pi, size=self.n)

    def u(self):
        return np.array([np.cos(self.th), np.sin(self.th)]).T

    def v(self):
        return self.v_0 * self.u()

    def macro_u(self):
        return np.mean(self.u(), axis=0)

    def macro_u_mag(self):
        return np.sqrt(np.sum(np.square(self.macro_u())))

    def _move_wrap(self):
        self.r += self.v()
        self.r[self.r > self.L / 2.0] -= self.L
        self.r[self.r < -self.L / 2.0] += self.L

    def _neighbs(self, i):
        inters, intersi = intro.get_inters(self.r, self.L, self.r_v)
        return inters[i, :intersi[i]]

    @abstractmethod
    def iterate(self):
        self._move_wrap()

    def snapshot(self, ax=None, demo=False):
        if ax is None:
            ax = plt.gca()
        ax.set_xlim(-self.L_half, self.L_half)
        ax.set_ylim(-self.L_half, self.L_half)
        ax.set_aspect('equal')

        s = 2.0
        ax.quiver(self.r[:, 0], self.r[:, 1],
                  s * self.L * self.u()[:, 0], s * self.L * self.u()[:, 1],
                  pivot='mid', edgecolor='none')
        ax.axis('off')
        return ax


class AngularVicsekModel(BaseVicsekModel):

    def iterate(self):
        self.th[...] = vicsek_angular(self.r, self.th, self.L, self.r_v,
                                      self.eta)
        BaseVicsekModel.iterate(self)


class VectorialVicsekModel(BaseVicsekModel):

    def iterate(self):
        self.th[...] = vicsek_vectorial(self.r, self.th, self.L, self.r_v,
                                        self.eta)
        BaseVicsekModel.iterate(self)
