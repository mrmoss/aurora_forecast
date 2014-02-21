import time

def month_name_to_num(month):
    return time.strptime(month, '%b').tm_mon

def get_current_date():
    return time.strftime("%Y %m %d")

def date_to_json(year, month, day):
    format_text =  '"year" : ' + str(year) 
    format_text += ', "month" : ' + str(month)
    format_text += ', "day" : ' + str(day)
    return format_text

def time_to_json(hour, minute):
    format_text =  ', "hour" : ' + str(hour)
    format_text += ', "minute" : ' + str(minute)
    return format_text

def time_predicted(date):
    year = date[0:4]
    month = month_name_to_num(date[5:8])
    day = date[9:11]
    json = '{ "time_predicted" : { ' + date_to_json(year, month, day)
    json += time_to_json(-1, -1) + '}'
    return json

def parse28(input_text):
    now = get_current_date()
    print now
    document = input_text.split("\n")
    # Set up array of json objects
    output_text = '[ '
    for line in document:
	# As of the project creation, all lines in the file are either comments,
	# or they start with the year. So testing for isdigit() is sufficient
	if line[0:4].isdigit():
	    json = time_predicted(line[0:11])
	    kp_value = line[-1]	# kp is all we need, and it is at the end of line.
	    json += ', "forecast" : "28day", "kp" : ' + str(kp_value) + '}, '

	    output_text += json
    # Remove the off-by-1 comma made by the loop.
    output_text = output_text[:-2]
    return output_text + ' ]'
	    

def main():
    print parse28("2014 Feb 11    150		5	3\n2014 Feb 12	    111		5	2")


if __name__ == "__main__":
    main()
