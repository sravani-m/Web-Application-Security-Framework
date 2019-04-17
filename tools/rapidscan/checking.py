'''import sys
import subprocess
import shlex

cmds = ['date', 'sleep 2', 'date']

cmds = [shlex.split(x) for x in cmds]

outputs =[]
for cmd in cmds:
    print(cmd)
    outputs.append(subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate())

for line in outputs:
    print ">>>" + line[0].strip()
    
from subprocess import Popen, PIPE
p = Popen("python sqlmap.py -u http://www.site.com/se
ction.php?id=51", stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
p.stdin.write('n') # sends a space to the running process
p.stdin.write('C') # sends a space to the running process
p.stdin.flush() # if the above isn't enough, try adding a flush'''
#!/usr/bin/env python
import subprocess
cmd = ["./rapidscan.py","https://latesthackingnews.com"]
c =subprocess.check_output(cmd)
print(c)
