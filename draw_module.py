# coding: utf-8

from equations_module import ellips

import os
import numpy as np
from scipy.signal import argrelextrema

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def	draw_poincare(e, h_arr, time_arr, dict_sol, save_dir_pic, step, clr_par):
	"""
	Drawing and saving Poincare sections.

	Parameters
	----------
	e : float
		Eccentricity.
	h_arr : list
		Array of initial heights.
	time_arr : list
		Array of times for which values are calculated.
	dict_sol : dictionary
		Dictionary with the solution of the problem (coordinates and velocity for each initial height).
	save_dir_pic : string
		Directory for saving graphs.
	step : integer
		The step through which the images should be rendered.
	clr_par : string
		The color palette of the Poincare section graph.
	"""

	plt.close()
	fig = plt.figure(figsize=(16,9))
	fig.suptitle(f"The Poincare section through each revolution. e = {e}")

	ax = fig.add_subplot(111)

	if clr_par == "gradient":
		clr1 = np.linspace(0.01, 0.99, len(h_arr))
		clr2 = np.linspace(0.01, 0.6, len(h_arr))
		clr3 = np.linspace(0.01, 0.1, len(h_arr))
		c = 0
		for h in h_arr:
			for i in range(0, len(time_arr), step):
				ax.plot(dict_sol[h][0][i], dict_sol[h][1][i], ".", color=[clr1[c], clr2[c], clr3[c]])
			ax.plot(dict_sol[h][0][-1], dict_sol[h][1][-1], ".", color=[clr1[c], clr2[c], clr3[c]], label=f"$h_0$ = {h}")
			c += 1

	elif clr_par == "multicoloured":
		c = 0
		for h in h_arr:
			for i in range(0, len(time_arr), step):
				ax.plot(dict_sol[h][0][i], dict_sol[h][1][i], ".", color=f"C{c}")
			ax.plot(dict_sol[h][0][-1], dict_sol[h][1][-1], ".", color=f"C{c}", label=f"$h_0$ = {h}")
			c += 1
	
	elif clr_par == "black":
		c = 0
		for h in h_arr:
			for i in range(0, len(time_arr), step):
				ax.plot(dict_sol[h][0][i], dict_sol[h][1][i], ".", color="black")
			ax.plot(dict_sol[h][0][-1], dict_sol[h][1][-1], ".", color="black", label=f"$h_0$ = {h}")
			c += 1
	else:
		print("# The wrong color palette is specified.")

	ax.legend()
	ax.set_xlabel("z")
	ax.set_ylabel("v")
	ax.set_ylim(-2.5, 2.5)
	ax.set_xlim(-3, 3)
	ax.set_aspect('equal')
	ax.grid()
	fig.tight_layout()
	fig.savefig(os.path.join(save_dir_pic, f"poincare_e={e}_h0={h_arr[0]}-{h_arr[-1]}.png"))
	plt.show()




def draw_orbit(e, h, time_arr, sol, N, P, save_dir_pic):
	"""
	Drawing animation of the movement of bodies.

	Parameters
	----------
	e : float
		Eccentricity.
	h : float
		Initial heights.
	time_arr : list
		Array of times for which values are calculated.
	sol : numpy.ndarray
		The solution of the problem (coordinates and velocity).
	N : integer
		Number of revolutions.
	P : integer
		The rotation period of large bodies.
	save_dir_pic : string
		Directory for saving graphs.
	"""

	dx = 1 - (1 - e) / 2 

	sol_z, sol_v = sol


	plt.close()
	fig = plt.figure(figsize=(16,9))
	# fig = plt.figure()
	fig.suptitle(f"$e = {e}, h_0 = {h}$")

	ax1 = fig.add_subplot(221)
	ax1.plot(time_arr, sol_z, ls="--", color="grey")
	ax1.set_ylabel("z")
	# ax1.set_xlabel("time t")
	ax1.set_xlim(0-N*P/10, N*P+N*P/10)
	ax1.grid()
	ax12 = ax1.twiny()
	ax12.set_xlim(0-N/10, N+N/10)
	ax12.set_xlabel("number of revolutions n")
	point1, = ax1.plot([], [], "bo")

	ax3 = fig.add_subplot(223)
	ax3.plot(time_arr, sol_v, ls="--", color="grey")
	ax3.set_ylabel("v")
	ax3.set_xlabel("time t")
	ax3.set_xlim(0-N*P/10, N*P+N*P/10)
	ax3.grid()
	ax32 = ax3.twiny()
	ax32.set_xlim(0-N/10, N+N/10)
	# ax32.set_xlabel("number of revolutions n")
	point3, = ax3.plot([], [], "bo")

	# ax2 = fig.add_subplot(422)
	# ax2.axes.get_xaxis().set_visible(False)
	# ax2.axes.get_yaxis().set_visible(False)
	# time_text = ax2.text(0, 0.1, s='',
	# 						#    horizontalalignment='center',
	#     #  verticalalignment='center',
	# 	#    transform=ax[0][1].transAxes,
	# 	 fontsize=15)


	ax4 = fig.add_subplot(122, projection='3d')
	tt = np.linspace(0, 360, 360)
	sol_ell = ellips(np.radians(tt), e)

	rr = dx + sol_ell[0][0]
	try: 
		z_max = max(sol_z[argrelextrema(sol_z, np.greater)[0]])
		z_max += z_max / 10
		z_min = min(sol_z[argrelextrema(sol_z, np.less)[0]])
		z_min += z_min / 10
	except:
		z_min = -2
		z_max = 2

	ax4.plot(dx+sol_ell[0], sol_ell[1], 0, ls="-", color="grey")
	ax4.plot(-dx-sol_ell[0], sol_ell[1], 0, ls="-", color="grey")
	ax4.set_xlabel("x")
	ax4.set_ylabel("y")
	ax4.set_zlabel("z")
	ax4.grid()
	ax4.set_xlim3d([-rr, rr])
	ax4.set_ylim3d([-rr, rr])
	ax4.set_zlim3d([z_min, z_max])
	ax4.set_aspect('equal')
	ax4.set_title('Animation of body movement')
	point4red, = ax4.plot([], [], [], "o", color="red")
	point4proj, = ax4.plot(0, 0, "b.")
	point4, = ax4.plot([], [], [], "bd")

	time_text = ax4.text(0, 0, 0, s='', fontsize=15)


	def init():
		point1.set_data([], [])
		point3.set_data([], [])
		point4red.set_data([], [])
		point4red.set_3d_properties(0)
		point4proj.set_marker(".")
		point4.set_data([], [])
		time_text.set_text('')

		return [point1, point3, point4red, point4proj, point4, time_text]


	def animate(i, e, z_arr, v_arr, t_arr, point1, point3, point4red, point4proj, point4, time_text):
		i -= 1
		t = t_arr[i]
		z = z_arr[i]
		v = v_arr[i]

		x, y = ellips(t, e)

		point1.set_data(t, z)
		point3.set_data(t, v)

		point4red.set_data([-dx-x, dx+x], [-y, y])
		point4red.set_3d_properties(0)

		if (v >= 0):
			point4proj.set_marker(".")
		else:
			point4proj.set_marker("x")

		point4.set_data(0, 0)
		point4.set_3d_properties(z)

		time_text.set_text(f" t = {t:.3f} \n n = {t/P:.3f} \n z = {z:.3f} \n v = {v:.3f}")

		return [point1, point3, point4red, point4proj, point4, time_text]




	anim = FuncAnimation(fig, animate, 
					  	fargs=(e, sol_z, sol_v, time_arr, point1, point3, point4red, point4proj, point4, time_text), 
						init_func=init, blit=True, 
						interval=5,
						frames=len(time_arr))

	fig.tight_layout()

	# path = os.path.join(save_dir_pic, "orbit.gif")

	# writergif = animation.PillowWriter(fps=len(time_arr)/10)

	plt.show()

	# anim.save(path, writer=writergif)
	# anim.save(path, writer='imagemagick')
	# anim.save(os.path.join(save_dir_pic, "orbit.gif"))
	# print(os.path.join(save_dir_pic, "orbit.gif"))

	  
	# saving to m4 using ffmpeg writer 
	# writervideo = animation.FFMpegWriter(fps=60) 
	# path = os.path.join(save_dir_pic, "orbit.mp4")
	# anim.save(path, writer=writervideo) 
