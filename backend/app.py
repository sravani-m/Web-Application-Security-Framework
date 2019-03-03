from flask import Flask
from flask import request
from flask_cors import CORS
from flask import jsonify

import json
import random

app = Flask(__name__)

CORS(app)

json_decoder = json.JSONDecoder()
json_encoder = json.JSONEncoder()

class VulnerabilityScanTools:
	def sslyzer_scan(self):
		print("sslyzer")
		return -1
	

@app.route('/vulnerability_scan_tool/<tools_json>/',methods = ["GET"])
def pick_tool(tools_json):
	print("here")
	status_code = -1
	status_message = 'Error'
	return_data = None

	
	#tools_dict = json_encoder.encode({"name":"sslyzer","id":1})
	tools_dict = json_decoder.decode(tools_dict)
	tool_id = tools_dict["id"]
	tool_name = tools_dict["name"] 
	
	if tool_name=="sslyzer":
		ss = VulnerabilityScanTools()
		ss.sslyzer_scan()

	return "success"



	
	

	
