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

	# if notebook has not been loaded yet
	if notebook_name not in ACTIVE_NOTEBOOKS:

		# load as append binary and reading
		fileObject = open("NOTEBOOK_" + notebook_name, "ab+")
		
		# pickle needs the file pointer to point to starting of the file
		fileObject.seek(0)

		notebook = pickle.load(fileObject)

		# create a reference of the notebook in ACTIVE_NOTEBOOKS
		proxy_notebook = weakref.proxy(notebook)

		# add data required to the ACTIVE_NOTEBOOKS
		ACTIVE_NOTEBOOKS[notebook_name] = {'data':notebook, 'file':fileObject}
		
		return proxy_notebook
	
	# if already present and open
	else:

		# return just the reference to the data
		return weakref.proxy(ACTIVE_NOTEBOOKS[notebook_name]['data'])


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