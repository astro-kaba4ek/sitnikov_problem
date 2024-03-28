# coding: utf-8

import json
import argparse
import pandas as pd
import os


def create_parser():
	"""
	Creating an argument parser.

	Returns
	-------
	parser : argparse.ArgumentParser
		Argument Parser.
	"""

	parser = argparse.ArgumentParser(
		description="""The program implements a numerical solution to the Sitnikov's problem, \n
		builds Poincare sections and creates visualization of the motion of bodies.""",
    	epilog="""Program written as part of the course "Computer Simulation" under the guidance of Assistant professor V.S. Shaidulin. Author S.I. Laznevoi.""")
	
	parser.add_argument("-in_f", "--input", help="the full name of the input-file")
	parser.add_argument("-e", "--eccentricity", default=0.1, type=float, help="the general eccentricity of massive bodies")
	parser.add_argument("-h0", "--h0_array", nargs="+", default=[1.0], type=float, help="an array of initial heights from which a small body falls")
	parser.add_argument("-n", "--number_of_revolutions", default=500, type=int, help="the number of revolutions of massive bodies")
	parser.add_argument("-method", "--integration_method", choices=["RK45", "RK23", "DOP853", "Radau", "BDF", "LSODA"], 
					 	default=["DOP853"],	help="the integration method used to solve a system of differential equations")
	parser.add_argument("-zv", "--poincare_sections", action="store_const", const=True, 
					 	help="if this flag is enabled, Poincare sections will be constructed")
	parser.add_argument("-gif", "--orbit_gif", action="store_const", const=True, 
					 	help="if this flag is enabled, a visual animation of the movement of bodies will be created")
	parser.add_argument("-clr", "--poincare_color", choices=["gradient", "multicoloured", "black"], 
					 	default=["gradient"],	help="the color palette of the Poincare section graph")
	parser.add_argument("-dir_pic", "--save_dir_pic", default="graphics", help="the path to save the graphs")
	parser.add_argument("-dir_txt", "--save_dir_txt", default="output", help="the path to save the calculated data")
	
	return parser


def initializ_params(args):
	"""
	Reading the input-file, setting parameters from the console, or using default parameters.

	Parameters
	----------
	args : argparse.Namespace
		Command line arguments at program startup.

	Returns
	-------
	e : float
		Eccentricity.
	h : list
		Array of initial heights.
	n : integer
		Number of revolutions.
	method : string
		Method for integration.
	poincare : bool
		Is it necessary to build a Poincare section?
	orbit : bool
		Is it necessary to build an animation of the movement of bodies?
	poincare_color : string
		The color palette of the Poincare section graph.
	save_dir_pic : string
		Directory for saving graphs.
	save_dir_txt : string
		Directory for saving calculated data.
	"""

	try:
		with open(args.input, 'r') as in_file:
			s = json.load(in_file)
				
			e = s["input_parameters"]["e"]
			h = s["input_parameters"]["h0_array"]
			n = s["input_parameters"]["n_rot"]
			
			method = s["integrator"]["method"]

			poincare = s["graphs"]["poincare"]
			orbit = s["graphs"]["orbit"]

			poincare_color = s["output_files"]["poincare_color"]
			save_dir_pic = s["output_files"]["save_dir_pic"]
			save_dir_txt = s["output_files"]["save_dir_txt"]

		print("# The input-file has been read successfully:\n")
	except:
		print("# The input file was not found, specified, or has errors.",
				"The values entered in the console or the default values are used:\n")

		e = args.eccentricity
		h = args.h0_array
		n = args.number_of_revolutions

		method = args.integration_method

		if (args.poincare_sections == None):
			poincare = False
		else:
			poincare = args.poincare_sections
		if (args.orbit_gif == None):
			orbit = False
		else:
			orbit = args.orbit_gif

		poincare_color = args.poincare_color
		save_dir_pic = args.save_dir_pic
		save_dir_txt = args.save_dir_txt

	if not os.path.isdir(save_dir_pic): os.mkdir(save_dir_pic)
	if not os.path.isdir(save_dir_txt): os.mkdir(save_dir_txt)

	return e, h, n, method, poincare, orbit, poincare_color, save_dir_pic, save_dir_txt


def save_data(e, h_arr, time_arr, dict_sol, save_dir_txt):
	"""
	Saving calculated data.

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
	save_dir_txt : string
		Directory for saving calculated data.

	"""

	for h in h_arr:
		df = pd.DataFrame() 

		df["time"] = time_arr
		df["z"] = dict_sol[h][0]
		df["v"] = dict_sol[h][1]

		path = os.path.join(save_dir_txt, f"output_e={e}_h0={h}.csv")

		df.to_csv(path, index=False)

