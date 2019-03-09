from flask import Flask
from flask import request
from flask_cors import CORS
from flask import jsonify

import subprocess
import json
import random

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
		return -1

@app.route('/vulnerability_scan_tool/<tools_json>/',methods = ["GET"])
def pick_tool(tools_json):
	print("here")
	status_code = -1
	status_message = 'Error'
	return_data = None

	tools_dict = json_encoder.encode({"name":"sslyzer","id":1})
	tools_dict = json_decoder.decode(tools_dict)
	tool_id = tools_dict["id"]
	tool_name = tools_dict["name"] 
	
	if tool_name=="sslyzer":
		ss = VulnerabilityScanTools()
		ss.sslyzer_scan("www.pes.edu:443","full")

	return "success"



	
	

	
