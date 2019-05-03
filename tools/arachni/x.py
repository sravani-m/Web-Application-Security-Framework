import os
import subprocess

path_dir = os.getcwd()
os.chdir("./bin")
cmd = ["./try"]
try:
	rsp = subprocess.check_output(cmd)
except Exception as e:
	print(e)
	rsp = None
cmd1 = ["unzip","-o","test_scan_report.html.zip", "-d", "output"]
try:
	rsp = subprocess.check_output(cmd1)
except Exception as e:
	print(e)
	rsp = None
print(os.getcwd())

#./arachni_reporter *.afr --reporter=html:outfile=test_scan_report.html.zip
#unzip test_scan_report.html.zip -d output
