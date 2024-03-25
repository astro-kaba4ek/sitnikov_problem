# Computer solution for the Sitnikov's problem

The program implements a numerical solution to the [Sitnikov's problem](https://en.wikipedia.org/wiki/Sitnikov_problem), builds Poincare sections and creates visualization of the motion of bodies.


## Files
- **main.py** — main program
- **draw_module.py** — module with drawing functions
- **equations_module.py** — module with calculation functions
- **utils.py** — module with auxiliary functions
- **input.json** — example of a file with input data

## The content of the input.json
- **input_parameters.e** — the general eccentricity of massive bodies ($0 \leqslant e < 1$)
- **input_parameters.h0_array** — an array of initial heights from which a small body falls
- **input_parameters.n_rot** — the number of revolutions of massive bodies
- **integrator.method** — the integration method used to solve a system of differential equations (RK45, RK23, DOP853, Radau, BDF or LSODA)
- **graphs.poincare** — if this parameter is True, Poincare sections will be constructed
- **graphs.orbit** — if this parameter is True, a visual animation of the movement of bodies will be created
- **output_files.poincare_color** — the color palette of the Poincare section graph
- **output_files.save_dir_pic** — the path to save the graphs
- **output_files.save_dir_txt** — the path to save the calculated data

## Usage
To run the program, you can use the command 
```bash
python3 ./main.py --input input.json
``` 
You can use additional flags instead of the `input.json`. To learn more, use the 
```bash
python3 ./main.py --help
```
## Additional information
- The following packages are required for the program to work:
	- **time**
	- **scipy**
	- **os**
	- **numpy**
	- **matplotlib**
	- **json**
	- **argparse**
	- **pandas**
- This version of the program cannot save the visualization of the movement of bodies due to too long a save time. This may be fixed in the future.
- If you find an error, be sure to report it.

### You may copy, modify and distribute this code, but must provide attribution

