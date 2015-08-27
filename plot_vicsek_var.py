from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt
from ciabatta import ejm_rcparams

save_flag = True

use_latex = save_flag
use_pgf = True

ejm_rcparams.set_pretty_plots(use_latex, use_pgf)

fig = plt.figure(figsize=(12, 12 * ejm_rcparams.golden_ratio))
ax = fig.add_subplot(111)
ejm_rcparams.prettify_axes(ax)

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

if save_flag:
    plt.savefig('vicsek_var.pdf', bbox_inches='tight', transparent=True)
else:
    plt.show()
