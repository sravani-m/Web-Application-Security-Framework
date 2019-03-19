import json

# Information required by flask

ABSOLUTE_PATH = '../Backend'
UPLOAD_FOLDER = ABSOLUTE_PATH+'/uploads'

# Check for uploading any file

ALLOWED_EXTENSIONS = set(['npz', 'csv', 'tsv', 'pkl', 'pickle', 'txt'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Used in selecting module name in sklearn.
# Can be replaced

PREPROC = ['preprocessing', 'impute']
SUPER = ['ensemble', 'gaussian_process', 'kernel_ridge', 'linear_model', 'neighbours', 'svm' ,'tree']
UNSUPER = ['cluster', 'decomposition']

# Used for Wrapping and Unwrapping data for communication

json_decoder = json.JSONDecoder()
json_encoder = json.JSONEncoder()

# Used to create weak references to dictionary

class weakdict(dict):
	pass

# Check if string in JSON object is float
# there is no str.isfloat

def str_isfloat(s):
	try:
		float(s)
		return True
	except:
		return False

