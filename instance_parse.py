import os
import re

def parse_teams(raw_text):

	regex = r'nTeams\s*=\s*[0-9]*\s*;'
	match = re.search(regex, raw_text)

	if match is None:
		return None
	else:
		return int(re.sub(r'\D', '', match.group(0)))


def extract_array(array_2d_string):

	# Split 2D array into a list of array on '\n'
	# Remove first and last element which are leading [ and trailing ];
	contents = array_2d_string.split('\n')[1:-1]

	# print(contents)
	array_2d = []

	for array_1d_string in contents:

		# Remove brackets and leading and trailing white spaces
		# Get the elements by splitting on whitespace
		array_1d = re.sub(r'[\[\]]', '', array_1d_string)
		array_1d = array_1d.strip().split()

		array_1d = list(map(int, array_1d))
		array_2d.append(array_1d)

	return array_2d


def parse_arrays(raw_text):

	# Match everything between [ and ];
	regex = r'\[[^a-zA-Z]*\];'
	match = re.findall(regex, raw_text)

	if match is None or len(match) < 2:
		return None

	dist = extract_array(match[0])
	opponents = extract_array(match[1])
	return dist, opponents


def parse_problem_instance_file(path_to_file):

	if not os.path.exists(path_to_file):
		raise FileNotFoundError

	f = open(path_to_file, 'r')
	contents = f.read()
	f.close()

	num_teams = parse_teams(contents)
	dist_matrix, opponents_matrix = parse_arrays(contents)

	return num_teams, dist_matrix, opponents_matrix