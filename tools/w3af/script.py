file_name = "clickjacking.w3af"
f = open(file_name,"r")
tmp_f = open("tmp.w3af","w")
url = "http://pesuacademy.com"

lines = f.readlines()

for index in range(len(lines)):
	if 'target' in lines[index]:
		lines.insert(index+1,"set target "+url+"\n")
		break

print(lines)

for line in lines:
	tmp_f.write(line)
