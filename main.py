# coding: utf-8

import time
from scipy import integrate

from draw_module import *
from equations_module import *
from utils import *


P = 2*np.pi


parser = create_parser()
args = parser.parse_args()


eccentr, h_arr, N, method, poincare, orbit, clr_par, save_dir_pic, save_dir_txt = initializ_params(args)

print("# eccentricity:", eccentr)
print("# array of initial heights:", h_arr)
print("# number of revolutions:", N)
print("# integration method:", method)
print("# construction of Poincare sections:", poincare)
print("# construction of gif-orbit:", orbit)
print("# the color palette of the Poincare section graph:", clr_par)
print("# directory for saving graphs:", save_dir_pic)
print("# directory for saving calculated data:", save_dir_txt, "\n")



step = 90

time_arr = np.arange(N*P, step=P/step)

# print(time_arr)

dict_sol = {}

print("# Calculation for h_0:")


for h in h_arr:
	print("#", h, end="\t", flush=True)

	time_start = time.monotonic()
	sol = integrate.solve_ivp(differ2, y0=[h,0], t_span=[time_arr[0], time_arr[-1]], t_eval=time_arr, args=(eccentr,), method=method)
	time_finish = time.monotonic()

	print(f"done. Time: {time_finish-time_start:.3f}")

	dict_sol[h] = sol.y

print("\n# Saving data:", end="\t", flush=True)
time_start = time.monotonic()
save_data(eccentr, h_arr, time_arr, dict_sol, save_dir_txt)
time_finish = time.monotonic()
print(f"done. Time: {time_finish-time_start:.3f}\n")


if (poincare):
	print("# Drawing and saving Poincare sections:")
	draw_poincare(eccentr, h_arr, time_arr, dict_sol, save_dir_pic, step, clr_par)
	print(f"# Done\n")

if (orbit):
	print("# Rendering animation of body movement (not saving):")

	for h in h_arr:
		print("#", h, end="\t", flush=True)
		draw_orbit(eccentr, h, time_arr, dict_sol[h], N, P, save_dir_pic)
		print(f"done")

print("\n# End of program")
