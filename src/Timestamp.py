#!/usr/bin/python
import time

class Timestamp:
    hour = -1
    minute = -1

    def __init__(self, date):
	self.year = int(date[0:4])
    	self.month = int(self.month_name_to_num(date[5:8]))
    	self.day = int(date[9:11])
	try:
	    self.hour = int(date[12:14])
	    self.minute = int(date[15:17])
	except ValueError:
	    return

    def month_name_to_num(self, month):
	return time.strptime(month, '%b').tm_mon

    def json(self):
        json = ''
        units = ["year", "month", "day", "hour", "minute"]
        value = {"year":self.year, "month":self.month, "day":self.day, 
                 "hour":self.hour, "minute":self.minute}
        for key in units:
            json += '"' + key + '":' + str(value[key]) + ','
        return '{' + json[:-1] + '}'

def main():
    # Test Timestamp class:
    p = Timestamp("2222 Jan 26 0210") # full date
    print p.year, p.month, p.day, p.hour, p.minute
    print p.json()

    q = Timestamp("2000 Feb 13") # no hours/minutes
    print q.year, q.month, q.day, q.hour, q.minute
    print q.json()


if __name__ == "__main__":
    main()

