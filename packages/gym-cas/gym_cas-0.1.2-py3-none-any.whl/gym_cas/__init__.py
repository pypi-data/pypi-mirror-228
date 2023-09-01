# SPDX-FileCopyrightText: 2023-present JACS <jacs@zbc.dk>
#
# SPDX-License-Identifier: MIT

from sympy import *
from sympy.abc import *
from spb import *
from numpy import mean, median, var, std
from .trigonometry import *
from .vector import plot_vector, plot_vector_field, plot3d_line, plot3d_plane
from .stats import group, degroup, frequency, kvartiler, percentile, group_std, group_mean, group_percentile, group_var
from .stat_plot import boxplot, plot_bars, plot_sum, plot_hist
from .regression import regression_poly, regression_power, regression_exp
from .ode import plot_ode
