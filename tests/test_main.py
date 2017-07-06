import numpy as np

from vicsek.model import vicsek_model_factory


def test_main():
    model = vicsek_model_factory(model='angular',
                                 n=200, L=50.0, eta=0.05, v_0=0.5)
    for _ in range(n):
        model.iterate()
