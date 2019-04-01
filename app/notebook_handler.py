import pickle
import weakref
import os

# if new installation, create a global notebook table to keep track of all notebooks

def create_notebook_global_table():
	fileObject = open("NOTEBOOKS_DATA", "wb")
	pickle.dump([], fileObject)
	fileObject.close()

	return True

# check whether the global notebook table exists

def notebook_global_table_exist():
	return os.path.exists("NOTEBOOKS_DATA")	

# Global variable to keep track of opened notebooks

ACTIVE_NOTEBOOKS = {}

# Returns a reference to notebook data

def get_notebook_data(notebook_name):

	# load as append binary and reading
	fileObject = open("NOTEBOOK_" + notebook_name, "ab+")
	fileObject.seek(0)
	notebook = pickle.load(fileObject)
	print(notebook)
	return notebook


# Takes the notebook name and dump everything to the notebook file

def set_notebook_data(notebook_name):

	# notebook should be opened.
	if notebook_name in ACTIVE_NOTEBOOKS:

		fileObject = ACTIVE_NOTEBOOKS[notebook_name]['file']

		# could delete data present in the notebook file
		fileObject.seek(0)
		fileObject.truncate(0)
		
		# dump the notebook data
		pickle.dump(ACTIVE_NOTEBOOKS[notebook_name]['data'], fileObject)