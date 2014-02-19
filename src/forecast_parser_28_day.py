from time import strptime

def date_to_json(year, month, day):
    formatted =  '"year" : ' + str(year) 
    formatted += ', "month" : ' + str(month)
    formatted += ', "day" : ' + str(day)
    return formatted

def time_to_json(hour, minute):
    formatted =  ', "hour" : ' + str(hour)
    formatted += ', "minute" : ' + str(minute)
    return formatted

def parse28(text):
    document = text.split("\n")
    output_text = '[ '
    for line in document:
	if line[0:4].isdigit():
	    year = line[0:4]
	    month = strptime(line[5:8], '%b').tm_mon
	    day = line[9:11]
	    kp_value = line[-1]
	    json = '{ "Time_predicted" : { ' + date_to_json(year, month, day)
	    json += time_to_json(-1, -1) + '} , "Kp" : ' + str(kp_value) + '}'

	    output_text += json
    return output_text + ' ]'
	    

def main():
    print parse28("2014 Feb 11    150		5	3\n2014 Feb 12	    111		5	2")


if __name__ == "__main__":
    main()
