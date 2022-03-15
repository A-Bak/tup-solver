import os
import sys

import instance_parse




def generate_main_rules(q1, q2, num_teams, r=None):

	file_lines = []

	file_lines.append('limit_big({}).  limit_small({}).'.format(q1, q2))
	file_lines.append('team(1..{}).  umpire(1..{}).'.format(num_teams, num_teams // 2))
	# Note changed numbering of rounds from 0..r-1 to 1..r where r = 2(2n-1)
	r = 2*(num_teams - 1)
	file_lines.append('round(1..{}).  last({}).'.format(r, r))

	return '\n'.join(file_lines)


def generate_distance_rules(distance_matrix):

	file_lines = []

	for i in range(len(distance_matrix)):
		row = []
		for j in range(len(distance_matrix[i])):
			row.append('distance({}, {}, {}).'.format(i+1, j+1, distance_matrix[i][j]))
		file_lines.append(' '.join(row))

	file_lines.append('distance(X,Y,D) :- distance(Y,X,D).')

	max_distance =  max(map(max, distance_matrix))
	file_lines.append('max_distance({}).'.format(max_distance))

	return '\n'.join(file_lines)


def generate_opponent_rules(opponent_matrix):
	file_lines = []

	for i in range(len(opponent_matrix)):
		row = []
		for j in range(len(opponent_matrix[i])):

			if opponent_matrix[i][j] > 0:
				row.append('plays({}, {}, {}).'.format(j+1, opponent_matrix[i][j], i+1))

		file_lines.append(' '.join(row))
	
	return '\n'.join(file_lines)


def generate_constraint_rules():

	file_lines = []

	file_lines.append('% Defines home team as the first of the two teams.')
	file_lines.append('home_team(Home,R) :- plays(Home,Away,R).')
	file_lines.append('')
	file_lines.append('% Generating search space, Umpire X moves to the home venue of team Y in round T')
	file_lines.append('% Constrains the umpires movement to 1 move per round')
	file_lines.append('1 { move(X,Y,T) : home_team(Y,T) } 1 :- umpire(X), round(T).')
	file_lines.append('')
	file_lines.append('% Constrains the maximum number of umpires at a game to 1')
	file_lines.append(':- move(U1,T,R), move(U2,T,R), U1 != U2.')
	file_lines.append('')
	file_lines.append('% Constrains the minimum number of umpires at a game to 1')
	file_lines.append(':- home_team(T,R), round(R), { move(U,T,R) : umpire(U) } 0.')
	file_lines.append('')
	file_lines.append('% Express constrain that every umpire must visit each venue at least once')
	file_lines.append('been_to(U,T) :- round(R), move(U,T,R).')
	file_lines.append(':- umpire(U), team(T), not been_to(U,T).')
	file_lines.append('')
	file_lines.append('% Express the constraint d1')
	file_lines.append(':- move(U,T,R1), move(U,T,R2), R1 < R2, limit_big(B), R2 - R1 + 1 <= B.')
	file_lines.append('')
	file_lines.append('% Express the constraint d2')
	file_lines.append('officiates(U,Home,R) :- move(U,Home,R).')
	file_lines.append('officiates(U,Away,R) :- move(U,Home,R), plays(Home,Away,R).')
	file_lines.append(':- officiates(U,T,R1), officiates(U,T,R2), R1 < R2, limit_small(S), R2 - R1 + 1 <= S.')
	file_lines.append('')
	file_lines.append('moved(U,R,D) :- umpire(U), team(T), round(R), R > 1, move(U,T,R), move(U,Tp,R-1), distance(T,Tp,D).')
	file_lines.append('')
	file_lines.append('% Optimization objective - Minimize distance D traveled')
	file_lines.append('#minimize { D,U,R : moved(U,R,D) }.')

	return '\n'.join(file_lines)


def generate_domain_heuristic(heuristic):

	if heuristic == 'paper':
		return '#heuristic move(U,T,R) : last(L), round(R), team(T), umpire(U), move(U,T1,R-1), distance(T,T1,D), max_distance(M). [(L-R+1) * M + (M-D), level]\n'
	elif heuristic == 'nearest':
		return '#heuristic move(U,T,R) : round(R), team(T), umpire(U), move(U,T1,R-1), distance(T,T1,D). [-D, level]\n'
	elif heuristic == 'nearest_not_visited':
		 
		return ('#heuristic move(U,T,R) : round(R), team(T), umpire(U), not been_to(U,T), move(U,T1,R-1), distance(T,T1,D). [-R*D@2, level]\n'+
			   '#heuristic move(U,T,R) : round(R), team(T), umpire(U), move(U,T1,R-1), distance(T,T1,D). [-D@1, level]\n')
	else:
		return ''



def create_asp_source_file(q1, q2, path_to_src, path_to_target, domain_heuristic=None):

	if not os.path.exists(path_to_src):
		raise FileNotFoundError

	if not os.path.exists(os.path.dirname(path_to_target)):
		os.makedirs(os.path.dirname(path_to_target)) 

	n, d, o = instance_parse.parse_problem_instance_file(path_to_src)

	f = open(path_to_target, 'w')

	f.write(generate_main_rules(q1, q2, n))
	f.write('\n\n')
	f.write(generate_distance_rules(d))
	f.write('\n\n')
	f.write(generate_opponent_rules(o))
	f.write('\n\n')
	f.write(generate_constraint_rules())
	f.write('\n\n')

	if domain_heuristic:
		f.write(generate_domain_heuristic(domain_heuristic))
		f.write('\n\n')	

	f.close()


if __name__ == '__main__':
	
	instance_name = sys.argv[1]
	q1 = int(sys.argv[2])
	q2 = int(sys.argv[3])

	path_to_instance = 'instances/{}.txt'.format(instance_name)
	path_to_asp = 'asp/{}.lp'.format(instance_name)
	
	create_asp_source_file(q1, q2, path_to_instance, path_to_asp)

	
