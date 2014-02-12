#File to String Function
def file_to_string(filename):
	try:
		with open(filename,"r") as opened_file:
			return opened_file.read();
	except:
		return "";