# Traveling Umpire Problem Solver
## Overview
***
This program is based on the paper [Solving the Travelling Umpire Problem with Answer Set Programming](https://link.springer.com/chapter/10.1007/978-3-319-67468-1_8) .
The goal is to solve instances of traveling umpire problem (TUP), the definition of TUP can be viewed [here](https://benchmark.gent.cs.kuleuven.be/tup/en/problem/) . 
This program uses a Python script to generate source code files in Clingo language which are used together
with the Clingo solver to find optimal solutions for the instances of TUP.  


## Dependencies
---
* Python version 3.8.3
* Clingo - easiest way to install is  `conda install -c potassco clingo`, otherwise see [release](https://github.com/potassco/clingo/releases/)


## Running the Project
---
1. [Download](https://benchmark.gent.cs.kuleuven.be/tup/en/results/) TUP instance files and add them to the `/instances` directory
2. (Optional) Compile your own program in Clingo language
3. Open `Anaconda Prompt` 
4. (Optional) Change configuration of experiments in `run.py` 
5. Run `python run.py [-h] [-t [TIME_OUT]] [-n [NUM_PROC]] [--src [SRC]] [--inst [INST]]` script
6. View results in the `/out` directory

Optional command line arguments for the TUP solver:
 - -h, --help  &nbsp; &nbsp; &nbsp; Show the help message and exit
 - -t [TIME_OUT], --time-out [TIME_OUT] &nbsp; &nbsp; &nbsp;  Time out for the Clingo solver specified in seconds, `default=300`
 - -n [NUM_PROC], --num-proc [NUM_PROC] &nbsp; &nbsp; &nbsp;  Number of parallel processes of the Clingo solver, `default=1`
 - --src [SRC] &nbsp; &nbsp; &nbsp;  Path to the directory that will contain generated '.lp' source files in Clingo language, `default='src_asp'`
 - --inst [INST] &nbsp; &nbsp; &nbsp; Path to the directory containing TUP instances`default='instances'`

If you want to run individual ASP programs with your own parameters you can use Clingo directly:
`clingo [SRC]  --opt-mode=optN --time-limit=[T] --parallel-mode=[NUM_PROC],[MODE] -q`

If you want to view the models that are computed, don't run Clingo with the paremeter `-q`.
Be midful that the sheer volume of output is rather confusing. If you only want to view the 
setting of specific atoms you need to modify the ASP program with `#show A/n` directive, 
where`A` is the name of the atom and  `n` is its arity.