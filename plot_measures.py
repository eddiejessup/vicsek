import numpy as np
import matplotlib.pyplot as plt
from ciabatta import ejm_rcparams
import numpy as np

save_flag = True

use_latex = save_flag
use_pgf = True

ejm_rcparams.set_pretty_plots(use_latex, use_pgf)

fig = plt.figure(figsize=(12, 12 * ejm_rcparams.golden_ratio))
ax = fig.add_subplot(111)
ejm_rcparams.prettify_axes(ax)

eta_vec, v_mean_vec, v_mean_vec_err, v_std_vec, v_std_vec_err = np.loadtxt('res_vec_big.txt', unpack=True)
eta_ang, v_mean_ang, v_mean_ang_err, v_std_ang, v_std_ang_err = np.loadtxt('res_ang_big.txt', unpack=True)

ax.plot(eta_ang, v_mean_ang, label='Angular noise')
ax.plot(eta_vec, v_mean_vec, label='Vectorial noise')

ax.legend(loc='lower left', fontsize=26)
ax.set_xlabel(r'$\eta$', fontsize=35)
ax.set_ylabel(r'$\bar{\mathrm{v}}$', fontsize=35)
ax.tick_params(axis='both', labelsize=26, pad=10.0)
ax.set_ylim(0.0, 1.05)
ax.set_xlim(0.1, 0.8)

if save_flag:
    plt.savefig('vicsek_mean.pdf', bbox_inches='tight', transparent=True)
else:
    plt.show()

ax.cla()

ax.plot(eta_ang, v_std_ang ** 2, label='Angular noise')
ax.plot(eta_vec, v_std_vec ** 2, label='Vectorial noise')

ax.legend(loc='lower right', fontsize=26)
ax.set_xlabel(r'$\eta$', fontsize=35)
ax.set_ylabel(r'$\mathrm{Var} \left( \bar{\mathrm{v}} \right)$', fontsize=35)
ax.tick_params(axis='both', labelsize=26, pad=10.0)
ax.set_ylim(1e-12, 1e-1)
ax.set_yscale('log')
ax.set_xlim(0.1, 0.8)

if save_flag:
    plt.savefig('vicsek_std.pdf', bbox_inches='tight', transparent=True)
else:
    plt.show()
