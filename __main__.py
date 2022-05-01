import argparse
import functools
import json
import os
import sys

FILENAME = 'projects_saved.json'

def move_to_project_path(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		project_path = os.path.dirname(os.path.realpath(__file__))
		os.chdir(project_path)
		return func(*args, **kwargs)
	return wrapper
	
class ProjectFile:
	def __init__(self, filename=None):
		if filename is None:
			self.filename = FILENAME

		self.projects = {}
		project_path = os.path.dirname(os.path.realpath(__file__))
		file_path = os.path.join(project_path, self.filename)

		# check if file exists
		if os.path.exists(file_path):
			self.projects = self.read_file() or {}
		else:			
			self.create_file()
		
	def add_project(self, project):
		# project_name = project.get('name')
		project_name = project['name']		
		if not project_name in self.projects:
			self.projects[project_name] = project['metadata']
			self.update_file()

	def remove_project(self, project):
		is_removed = False
		if self.projects:
			if project_name in self.projects:
				del self.projects[project_name]
				is_removed = True
		if is_removed:
			self.update_file

	def list_projects(self):
		return self.projects

	@move_to_project_path
	def update_file(self):
		with open(self.filename, 'w') as f:
			json.dump(self.projects, f)

	@move_to_project_path
	def create_file(self):
		with open(self.filename, 'w') as f:
			pass
			
		msg = f'File "{self.filename}" created!'
		print('-' * len(msg))
		print('{0}'.format(msg))
		print('-' * len(msg))

	@move_to_project_path
	def read_file(self):	
		content = None
		with open(self.filename, 'r') as f:
			data = f.read()
			if data:
				content = json.loads(data)
		return content

	def __repr__(self):
		return '{}: {}'.format(
			self.filename,
			self.projects[:30]
		)

def create_config_file():
	pass

def is_valid_project():
	pass



filepath = os.getcwd()

project_file = ProjectFile()

parser = argparse.ArgumentParser(description="Help ya save/get your project")

parser.add_argument(
	'-l',
	'--list-all',
	action='store_true'
)

parser.add_argument(
	'-s',
	'--save-project',
	action='store_true'
)

parser.add_argument(
	'-a',
	'--access-project',
	action='store_true'
)

VIEW = 1
SAVE = 2
ACCESS = 3

action_options = {
	VIEW: 'view all projects',
	SAVE: 'Save project',
	ACCESS: 'access project',
}

user_action = None

args = parser.parse_args()

if not any(args.__dict__.values()):
	print('Choose one of the following')
	for action_option in action_options:
		action_desc = action_options[action_option]
		print(f'{action_option}: {action_desc}')
	user_action = int(input('What would you like to do today? '))

if args.list_all or user_action == VIEW:
	print(project_file.list_projects())

if args.save_project or user_action == SAVE:
	name = input('What is the name of this project (the current directory name will be used if left blank)? ')\
		or filepath.split('/')[-1]

	path = input('What is the path (the current file path will be used if left blank)? ')\
		or filepath

	project = {
		'name': name,
		'metadata': {
			'path': path
		}
	}

	if name:
		project['name'] = name

	if path:
		project['metadata']['path'] = path

	project_file.add_project(project)

if args.access_project or user_action == ACCESS:
	all_projects = project_file.list_projects()
	print(list(all_projects.keys()))
	num_tries = 3
	for i in range(num_tries):
		name = input('Which one? ').strip()
		if name in all_projects:
			project_path = all_projects[name]['path']
			try:
				os.chdir(project_path)
				os.system('pwd')
				os.system('/bin/zsh')
				break
			except FileNotFoundError as e:
				print(e)

