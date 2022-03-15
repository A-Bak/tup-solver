import os
import sys
import argparse

import instance_to_asp as i2a

# Dictionary specifying configurations of individual problem instances
# together with set parameters. Used to generate specific ASP source
# code.
# - Key - name of the '.lp' source file
# - Value - list consisting of [d1, d2, instance_name, heuristic]
# - Numeric values of d1,d2 should be in range:  d2 <= d1 <= R/2
# - Heuristics can be: 'paper', 'nearest', 'nearest_not_visited', None

experiments = {
	'14-5-3': [ 5, 3, 'umps14.txt', 'nearest_not_visited'],
	'14-6-3': [ 6, 3, 'umps14.txt', 'nearest_not_visited'],
	'14-7-3': [ 7, 3, 'umps14.txt', 'nearest_not_visited'],
	'14A-5-3': [ 5, 3, 'umps14A.txt', 'nearest_not_visited'],
	'14A-6-3': [ 6, 3, 'umps14A.txt', 'nearest_not_visited'],
	'14A-7-3': [ 7, 3, 'umps14A.txt', 'nearest_not_visited'],
	'14B-5-3': [ 5, 3, 'umps14B.txt', 'nearest_not_visited'],
	'14B-6-3': [ 6, 3, 'umps14B.txt', 'nearest_not_visited'],
	'14B-7-3': [ 7, 3, 'umps14B.txt', 'nearest_not_visited'],
	'14C-5-3': [ 5, 3, 'umps14C.txt', 'nearest_not_visited'],
	'14C-6-3': [ 6, 3, 'umps14C.txt', 'nearest_not_visited'],
	'14C-7-3': [ 7, 3, 'umps14C.txt', 'nearest_not_visited'],
}

# Function generates a '.lp' source code file for each TUP problem setting in the experiments dictionary.
def run_experiments(path_to_source, time_out, num_proc):
	
	if not os.path.exists('out'):
		os.makedirs('out')

	for instance_name, params in experiments.items():

		if params[3] is not None:
			heuristic = '--heuristic=Domain'
		else:
			heuristic = ''

		source_file_path = path_to_source+'/'+instance_name+'.lp' 
		
		parameters = '--opt-mode=optN --time-limit={} -q --parallel-mode {},{} {}'.format(time_out, num_proc, 'compete', heuristic)
		output_file_path = 'out/{}_comp_out.txt'.format(instance_name) 
		solve(source_file_path, parameters, output_file_path)

		parameters = '--opt-mode=optN --time-limit={} -q --parallel-mode {},{} {}'.format(time_out, num_proc, 'split', heuristic)
		output_file_path = 'out/{}_split_out.txt'.format(instance_name) 
		solve(source_file_path, parameters, output_file_path)


def solve(source_file_path, parameters, output_file_path):

	print('Solving {}.'.format(os.path.basename(source_file_path)))
	os.system('clingo {} {} > {}'.format(source_file_path, parameters, output_file_path))
	print('Finished.')


# Function generates a '.lp' source code file for each TUP problem setting in the experiments dictionary.
def generate_source_files(problem_instance_dir, asp_sources_dir):

	if not os.path.exists(problem_instance_dir):
		raise NotADirectoryError

	if not os.path.exists(asp_sources_dir):
		os.makedirs(asp_sources_dir) 

	for experiment_id, params in experiments.items():

		d1 = params[0]
		d2 = params[1]
		instance_file_path = problem_instance_dir+'/'+params[2]


		if not os.path.exists(instance_file_path):
			print('Err: Instance problem file \"{}\" not found.'.format(instance_file_path))
			print('Skipping file.')
		else:
			source_file_path = asp_sources_dir+'/'+experiment_id+'.lp' 		
			i2a.create_asp_source_file(d1, d2, instance_file_path, source_file_path, domain_heuristic=params[3])



if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Traveling umpire problem (TUP) solver.')

	#TODO Changed default

	parser.add_argument('-t','--time-out', nargs='?', default=300, help='Time out for the Clingo solver specified in seconds')
	parser.add_argument('-n','--num-proc', nargs='?', default=1, help='Number of parallel processes of the Clingo solver in range <1..N>.')
	parser.add_argument('--src', nargs='?', default='src_asp', help='Path to the directory that will contain generated \'.lp\' source files in Clingo language.')
	parser.add_argument('--inst', nargs='?', default='instances', help='Path to the directory containing TUP instances.')

	args = parser.parse_args()

	generate_source_files(args.inst, args.src)
	run_experiments(args.src, args.time_out, args.num_proc)