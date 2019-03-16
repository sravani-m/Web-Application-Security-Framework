from flask import Flask
from flask import request
from flask_cors import CORS
from flask import jsonify

import subprocess
import json
import random
import os

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
		return -1

	def xsser_scan(self,domain):
		os.chdir("../xsser")
		print("xsser")
		cmd = ["xsser","-u",domain]
		op = self.cmd_rsp(cmd)
		print(op)

		return -1
		
	def nikto_scan(self,domain):
		print("nikto")
		os.chdir("../nikto/program")
		path_config = os.getcwd()+"/nikto.conf.default"
		cmd = ["perl","nikto.pl","-config",path_config,"-Tuning","9","-host",domain]
		print(cmd)
		op = self.cmd_rsp(cmd)
		print(op)

		return -1
		# parse the output for full scan and half scan
#perl nikto.pl -config /home/sravya/Desktop/checking_install/nikto/program/nikto.conf.default -Tuning 9 -host www.isanalytics.com

#http://localhost:5000/get_scan_results/%7B%22vulnerabilities%22:[%22xss%22,%22sql_injection%22]%7D/
@app.route('/get_scan_results/<vulnerabilities_json>/',methods = ["GET"])
def pick_tool(vulnerabilities_json):
	print("here")
	status_code = -1
	status_message = 'Error'
	return_data = None

	print(vulnerabilities_json)
	vulnerabilities_dict = json_encoder.encode(vulnerabilities_json)	
	vulnerabilities_dict = json_decoder.decode(vulnerabilities_json)
	vulnerabilities = vulnerabilities_dict["vulnerabilities"]

	if "ssl" in vulnerabilities:
		ss = VulnerabilityScanTools()
		ss.sslyzer_scan("www.pes.edu:443","full")
	elif "xsser" in vulnerabilities:
		ss = VulnerabilityScanTools()
		ss.xsser_scan("https://hack.me/")
	elif "nikto" in vulnerabilities:
		ss = VulnerabilityScanTools()
		ss.nikto_scan("www.isanalytics.com")


	
	return "success"



	
	

	
