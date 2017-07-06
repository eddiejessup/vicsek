import numpy as np
import matplotlib.pyplot as plt
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
        print(model.r)
        q.set_offsets(model.r)
        q.set_UVC(*(model.L * model.u.T))
        fig.canvas.draw()


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


def eta_scan(model, n, L, v_0, num_equil, num_measure, etas):
    for eta in etas:
        m = vicsek_model_factory(model=model, n=n, L=L, eta=eta, v_0=v_0)
        # Equilibrate
        for _ in range(num_equil):
            m.iterate()
        # Take measurements
        mags = []
        for _ in range(num_measure):
            m.iterate()
            mags.append(m.macro_u_mag)
        yield eta, np.mean(mags), np.std(mags), len(mags)


def make_vicsek_stats():
    n = 2048
    L = 32.0
    v_0 = 0.5
    num_equil = 100
    num_measure = 500

    for model in ('angular', 'vectorial'):
        if model == 'angular':
            etas = np.linspace(0.6, 0.8, 20)
        else:
            etas = np.linspace(0.55, 0.65, 20)
        stats = eta_scan(model, n, L, v_0, num_equil, num_measure, etas)
        np.savetxt('{}_stats.txt'.format(model), list(stats))


def plot_vicsek_stats_mean():
    fig = plt.figure()
    ax = fig.gca()

    eta_ang, v_mean_ang, v_std_ang, n_ang = np.loadtxt('angular_stats.txt', unpack=True)
    eta_vec, v_mean_vec, v_std_vec, n_vec = np.loadtxt('vectorial_stats.txt', unpack=True)

    ax.errorbar(eta_ang, v_mean_ang, yerr=v_std_ang, label='Angular noise')
    ax.errorbar(eta_vec, v_mean_vec, yerr=v_std_vec, label='Vectorial noise')

    ax.legend(loc='lower left', fontsize=26)
    ax.set_xlabel(r'$\eta$', fontsize=35)
    ax.set_ylabel(r'$\bar{\mathrm{v}}$', fontsize=35)
    ax.tick_params(axis='both', labelsize=26, pad=10.0)
    ax.set_ylim(0.0, 1.05)
    ax.set_xlim(0.0, 1.0)

    plt.savefig('vicsek_mean.pdf', bbox_inches='tight', transparent=True)


def plot_vicsek_stats_mean():
    fig = plt.figure()
    ax = fig.gca()

    eta_ang, v_mean_ang, v_std_ang, n_ang = np.loadtxt('angular_stats.txt',
                                                       unpack=True)
    eta_vec, v_mean_vec, v_std_vec, n_vec = np.loadtxt('vectorial_stats.txt',
                                                       unpack=True)

    v_std_err_ang = v_std_ang / np.sqrt(n_ang)
    v_std_err_vec = v_std_vec / np.sqrt(n_vec)

    ax.errorbar(eta_ang, v_std_ang ** 2, yerr=v_std_err_ang ** 2,
                label='Angular noise')
    ax.errorbar(eta_vec, v_std_vec ** 2, yerr=v_std_err_vec ** 2,
                label='Vectorial noise')

    ax.legend(loc='lower right', fontsize=26)
    ax.set_xlabel(r'$\eta$', fontsize=35)
    ax.set_ylabel(r'$\mathrm{Var} \left( \bar{\mathrm{v}} \right)$', fontsize=35)
    ax.tick_params(axis='both', labelsize=26, pad=10.0)
    ax.set_ylim(1e-10, 1e0)
    ax.set_yscale('log')
    ax.set_xlim(0.0, 1.0)

    plt.savefig('vicsek_var.pdf', bbox_inches='tight', transparent=True)

if __name__ == '__main__':
    plot_vicsek(vicsek_model_factory(model='angular',
                                     n=200, L=50.0, eta=0.05, v_0=0.5), 100)
