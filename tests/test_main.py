import numpy as np

from vicsek.model import vicsek_model_factory


def test_angular():
    model = vicsek_model_factory(model='angular',
                                 n=2000, L=50.0, eta=0.05, v_0=0.5)
    for _ in range(100):
        model.iterate()


def test_vectorial():
    model = vicsek_model_factory(model='vectorial',
                                 n=2000, L=50.0, eta=0.05, v_0=0.5)
    for _ in range(100):
        model.iterate()
