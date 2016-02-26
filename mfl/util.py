import time
import datetime

def convert_to_timestamp(date_string):
    return time.mktime(datetime.datetime.strptime(date_string, "%m/%d/%Y").timetuple())

def concat(values):
    return ','.join([str(s) for s in values])