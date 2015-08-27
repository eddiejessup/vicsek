from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem
from ciabatta import ejm_rcparams
from model import vicsek_model_factory


def plot_vicsek(model, n):
    fig = plt.figure()
    ax = fig.gca()
    q = ax.quiver(model.r, model.L * model.u)
    ax.set_xlim(-model.L_half, model.L_half)
    ax.set_ylim(-model.L_half, model.L_half)
    ax.set_aspect('equal')
    plt.ion()
    plt.show()
    for _ in range(n):
        model.iterate()
        q.set_offsets(model.r)
        q.set_UVC(*(model.L * model.u.T))
        fig.canvas.draw()
    return model.macro_u_mag()


def make_illustration_snapshot():
    fig = plt.figure()
    ax = fig.gca()
    model = vicsek_model_factory(model='angular',
                                 n=200, L=100.0, eta=0.2, v_0=0.5)
    for _ in range(100):
        model.iterate()
    ejm_rcparams.set_pretty_plots(use_latex=True, use_pgf=True)
    ejm_rcparams.prettify_axes(ax)

    ax.set_xlim(-model.L_half, model.L_half)
    ax.set_ylim(-model.L_half, model.L_half)
    ax.set_aspect('equal')

    i_source = np.argmin(np.sum(np.square(model.r), axis=1))
    r_i = model.r[i_source]
    c = plt.Circle(r_i, radius=model.r_v, fill=False, edgecolor='red')
    ax.add_patch(c)
    colors = np.zeros([model.n])
    colors[i_source] = 1.0
    i_neighbs = model._neighbs(i_source)
    for i_neighb in i_neighbs:
        colors[i_neighb] = 0.5

    s = 2.0
    ax.quiver(model.r[:, 0], model.r[:, 1],
              s * model.L * model.u[:, 0], s * model.L * model.u[:, 1],
              colors, pivot='mid', edgecolor='none')
    ax.axis('off')

    plt.savefig('vicsek_snapshot_demo.pdf', bbox_inches='tight',
                transparent=True)


def make_ordered_snapshot():
    model = vicsek_model_factory(model='angular',
                                 n=100, L=100.0, eta=0.05, v_0=0.5)
    for _ in range(100):
        model.iterate()

    fig = plt.figure()
    ax = fig.gca()
    ejm_rcparams.set_pretty_plots(use_latex=True, use_pgf=True)
    ejm_rcparams.prettify_axes(ax)

    ax.set_xlim(-model.L_half, model.L_half)
    ax.set_ylim(-model.L_half, model.L_half)
    ax.set_aspect('equal')
    s = 2.0
    ax.quiver(model.r[:, 0], model.r[:, 1],
              s * model.L * model.u[:, 0], s * model.L * model.u[:, 1],
              pivot='mid', edgecolor='none')
    ax.axis('off')

    plt.savefig('vicsek_snapshot_ordered.pdf', bbox_inches='tight',
                transparent=True)


def make_disordered_snapshot():
    model = vicsek_model_factory(model='angular',
                                 n=100, L=100.0, eta=0.8, v_0=0.5)
    for _ in range(100):
        model.iterate()

    fig = plt.figure()
    ax = fig.gca()
    ejm_rcparams.set_pretty_plots(use_latex=True, use_pgf=True)
    ejm_rcparams.prettify_axes(ax)
    ax.set_xlim(-model.L_half, model.L_half)
    ax.set_ylim(-model.L_half, model.L_half)
    ax.set_aspect('equal')
    s = 2.0
    ax.quiver(model.r[:, 0], model.r[:, 1],
              s * model.L * model.u[:, 0], s * model.L * model.u[:, 1],
              pivot='mid', edgecolor='none')
    ax.axis('off')

    plt.savefig('vicsek_snapshot_disordered.pdf', bbox_inches='tight',
                transparent=True)


def get_vicsek_stats():
    for eta in np.linspace(0.0, 0.8, 40):
        model = vicsek_model_factory(model='angular', n=2048, L=32.0, eta=eta, v_0=0.5)

        # Equilibrate
        for _ in range(100):
            model.iterate()

        # Take measurements
        mags = []
        for _ in range(1000):
            model.iterate()
            mags.append(model.macro_u_mag)
        print(eta, np.mean(mags), sem(mags), np.var(mags),
              np.var(mags) / np.sqrt(len(mags)))


if __name__ == '__main__':
    plot_vicsek(vicsek_model_factory(model='angular',
                                     n=200, L=50.0, eta=0.05, v_0=0.5), 100)
