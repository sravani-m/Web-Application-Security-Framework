from flask import Flask
from flask import request
from flask_cors import CORS
from flask import jsonify

import subprocess
import json
import random
import os
import pickle

import psutil

from globals import ABSOLUTE_PATH, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, allowed_file, PREPROC, SUPER, UNSUPER, json_decoder, json_encoder, weakdict, str_isfloat
from usertable_handler import create_new_user_table, user_table_exists
from notebook_handler import ACTIVE_NOTEBOOKS, create_notebook_global_table, get_notebook_data, notebook_global_table_exist, set_notebook_data

app = Flask(__name__)

CORS(app)

json_decoder = json.JSONDecoder()
json_encoder = json.JSONEncoder()


class VulnerabilityScanTools:
	def cmd_rsp(self,cmd):
		try:
			rsp = subprocess.check_output(cmd)
		except Exception as e:
			print(e)
			rsp = None
		return rsp

	def sslyzer_scan(self,domain,scan_type):
		print("sslyze scan")
		cmd = ["sslyze","--regular",domain]
		op = self.cmd_rsp(cmd)
		sslyzer_op = op.split("\n")
		line_num = start = end = 0

		if scan_type=="full":
			for line in sslyzer_op:
				if 'SCAN RESULTS' in line:
					start = line_num
				if 'SCAN COMPLETED' in line:
					end = line_num
				line_num = line_num + 1
			sslyzer_op = sslyzer_op[start+2:end]
		
		scan_op = "\n".join(sslyzer_op)
		print(scan_op)
		print("sslyzer")
		return scan_op

	def xsser_scan(self,domain):
		os.chdir("../tools/xsser")
		print(os.getcwd())
		cmd = ["xsser","-u",domain]
		op = self.cmd_rsp(cmd)
		print(op)

		return op
		
	def nikto_scan(self,domain):
		print("nikto")
		os.chdir("../tools/nikto/program")
		path_config = os.getcwd()+"/nikto.conf.default"
		cmd = ["perl","nikto.pl","-config",path_config,"-Tuning","9","-host",domain]
		print(cmd)
		op = self.cmd_rsp(cmd)
		print(op)

		return -1
		# parse the output for full scan and half scan
#perl nikto.pl -config /home/sravya/Desktop/checking_install/nikto/program/nikto.conf.default -Tuning 9 -host www.isanalytics.com

@app.route("/",methods = ["GET"])
def show_ui():
	return "hello"

#USERNAME INFO
@app.route("/check_username_exists/<check_username_exists_json>", methods = ["GET"])
def check_username_exists(check_username_exists_json):
		check_username_exists_dict = json_decoder.decode(check_username_exists_json)

		print("\n",check_username_exists_dict,"\n")
		# if new installation, create new user table
		if not (user_table_exists()):
			create_new_user_table()

		# check user table is username exists
		fileObject = open("USERTABLE", "rb")
		table = pickle.load(fileObject)
		print("\n",table,"\n")
		if any(obj['username'] == check_username_exists_dict['username'] for obj in table):
			print("exists")
			return json_encoder.encode({"message":"Success", "comment":"Username exists"})

		return json_encoder.encode({"message":"Success", "comment": "Username available"})


@app.route("/check_username_and_password_matches", methods = ["POST"])
def check_username_and_password_matches():
	try:

		# if new installation, create a new user table
		if not (user_table_exists()):
			create_new_user_table()

		# extract from POST request form data wrapped in json
		username = request.json['username']
		password = request.json['password']

		# open user table and check if username and password match.
		fileObject = open("USERTABLE", "rb")
		table = pickle.load(fileObject)

		if (any(username == obj['username'] and password == obj['password'] for obj in table)):
			return json_encoder.encode({"message":"Success", "comment":"Username and password match"})

		return json_encoder.encode({"message":"Success", "comment":"Username and password does not match"})
	except:
		return json_encoder.encode({"message":"Failure", "comment": "Other error"})



@app.route("/add_user", methods = ["POST"])
def add_user():
	try:
		user = request.json		
		print(user)

		# if new installation, create a new user table
		if not (user_table_exists()):
			create_new_user_table()

		fileObject = open("USERTABLE", "rb")
		table = pickle.load(fileObject)
		fileObject.close()

		# newly created user does not have any notebooks
		obj = 	{
					"username": user['username'],
					"password": user['password'],
					"created_notebooks": []
				}
		
		table.append(obj)

		# save updated user table
		fileObject = open("USERTABLE", "wb")
		pickle.dump(table, fileObject)
		fileObject.close()

		return json_encoder.encode({"message":"success"})
	except:
		return json_encoder.encode({"message":"failure"})



@app.route("/check_notebook_name_exists/<check_notebook_name_exists_json>", methods = ["GET"])
def check_notebook_name_exists(check_notebook_name_exists_json):
	check_notebook_name_exists_dict = json_decoder.decode(check_notebook_name_exists_json)

	# if new installation, create global notebooks table
	if not (notebook_global_table_exist()):
		create_notebook_global_table()

	# opens the global notebooks table, and checks whether notebook exists
	fileObject = open("NOTEBOOKS_DATA", "rb")
	table = pickle.load(fileObject)

	if any(obj['notebook_name'] == check_notebook_name_exists_dict['notebook_name'] for obj in table):
		return json_encoder.encode({"message":"Success", "comment":"Notebook name exists"})

	return json_encoder.encode({"message":"Success", "comment": "Notebook name available"})



@app.route("/get_user_notebooks/<get_user_notebooks_json>", methods = ["GET"])
def get_user_notebooks(get_user_notebooks_json):
	get_user_notebooks_dict = json_decoder.decode(get_user_notebooks_json)

	# opens user table and returns list of notebooks opened by that user
	table = pickle.load(open("USERTABLE", "rb"))

	print("table",table,get_user_notebooks_dict)

	for obj in table:
		if (obj['username'] == get_user_notebooks_dict['username']):
			print("username match")
			return json_encoder.encode({"message":"Success", "notebook_names":obj['notebooks']})

	return json_encoder.encode({"message":"Failure"})



@app.route("/add_notebook", methods = ["POST"])
def add_notebook():
	print("changed")
	try:
		# notebook is of type weakdict to create references of it
		notebook = dict(request.json)
		print("\n",notebook,"\n")
		# creating a reference of notebook's data
		# weakdict_notebook = weakref.proxy(notebook)

		fileObject = open("NOTEBOOK_"+notebook['notebook_name'], "wb")
		pickle.dump(notebook, fileObject)
		fileObject.close()

		# if new installation, create a global notebooks table
		if not (notebook_global_table_exist()):
			create_notebook_global_table()

		# open global notebooks table and add notebook configuration
		fileObject = open("NOTEBOOKS_DATA", "rb")
		table = pickle.load(fileObject)
		fileObject.close()
		table.append({
						"notebook_name": notebook['notebook_name'],
						"CPU_count": int(notebook['CPU_count']),
					})

		fileObject = open("NOTEBOOKS_DATA", "wb")
		pickle.dump(table, fileObject)
		fileObject.close()

		

		fileObject = open("USERTABLE", "rb")
		table = pickle.load(fileObject)
		fileObject.close()

		for obj in table:
			if obj['username']==notebook["username"]:
				obj['notebooks'].append(notebook["notebook_name"])

		fileObject = open("USERTABLE","wb")
		pickle.dump(table, fileObject)
		fileObject.close()

		return json_encoder.encode({"message":"Success", "comment": "Notebook created"})
	except:
		return json_encoder.encode({"message":"Failure", "comment": "Other error"})



@app.route("/get_devices/", methods = ["GET"])
def get_devices():
	# Currently works only on Linux
	# Fails on windows.
	# Check for unix
	if(os.name == 'posix'):
		n_cpu = psutil.cpu_count()

	# if new installation, create a global notebooks table
	if not (notebook_global_table_exist()):
		create_notebook_global_table()

	table = pickle.load(open("NOTEBOOKS_DATA", "rb"))
	a_cpu = n_cpu - sum(obj["CPU_count"] for obj in table)

	return json_encoder.encode({"message":"Success", "CPU_available": a_cpu})



@app.route("/load_existing_notebook/<notebook_details>/", methods = ["GET"])
def load_existing_notebook_details(notebook_details):
	# Send data to UI to load back existing notebook
	print(notebook_details)
	data = json_decoder.decode(notebook_details)
	notebook = get_notebook_data(data['notebook_name'])
	dct = {}
	for key in notebook:
		dct[key] = notebook[key]

	return json_encoder.encode({"message": "Success", "notebook_data": dct})



@app.route('/get_scan_results/<vulnerabilities_json>/',methods = ["GET"])
def pick_tool(vulnerabilities_json):
	print("here")
	status_code = -1
	status_message = 'Error'
	return_data = ""
	print(vulnerabilities_json)
	# vulnerabilities_dict = json_encoder.encode(vulnerabilities_json)	
	vulnerabilities_dict = json_decoder.decode(vulnerabilities_json)
	vulnerabilities = vulnerabilities_dict["vulnerabilities"]

	username = vulnerabilities_dict["username"]
	print("\nusername: "+username+"\n")
	
	url = vulnerabilities_dict["url"]
	url = url.strip('\"')
	print("\n "+vulnerabilities_dict["url"]+"\n")
	
	if "ssl" in vulnerabilities:
		url = url.split('//')
		if url[0]=='https:' or url[0]=='http:' :
			url.pop(0)
		url_modified = ''.join(map(str,url))
		url_modified = url_modified.split('/')
		url_modified_stripped = url_modified[0]
		print(url_modified_stripped)
		ss = VulnerabilityScanTools()
		return_data+=ss.sslyzer_scan("www.pes.edu:443","full")
	elif "xsser" in vulnerabilities:
		ss = VulnerabilityScanTools()
		return_data+=ss.xsser_scan("https://hack.me/")
	elif "nikto" in vulnerabilities:
		ss = VulnerabilityScanTools()
		return_data+=ss.nikto_scan("www.isanalytics.com")
	
	print("Notebook name",vulnerabilities_dict["notebook_name"]);
	#setting notebook data
	fileObject = open("NOTEBOOK_"+vulnerabilities_dict["notebook_name"], "rb")
	table = pickle.load(fileObject)
	print(type(table))
	fileObject.close()
	
	table["url"] = vulnerabilities_dict["url"]
	table["vulnerabilities"] = vulnerabilities_dict["vulnerabilities"]
	table["report"] = return_data
	
	fileObject = open("NOTEBOOK_"+vulnerabilities_dict["notebook_name"], "wb")
	pickle.dump(table, fileObject)
	fileObject.close()

	print("return data",return_data)
	return json_encoder.encode({"message":"Success","report":return_data})
