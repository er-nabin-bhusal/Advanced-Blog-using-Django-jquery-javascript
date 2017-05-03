import re
import datetime
import math
from django.utils.html  import strip_tags

def count_words(html_string):
	# html_string= """
	# <h1>this is title </>"""
	word_string = strip_tags(html_string)
	matching_list = re.findall(r'\w+',word_string)
	count = len(matching_list)
	return count

def get_read_time(html_string):
	count = count_words(html_string)
	read_time_min = math.ceil(count/200.0)#assuming 200 words per minute#to round down math.floor
	# read_time_sec = read_time_min*60
	# read_time = str(datetime.timedelta(minutes=read_time_min))
	return int(read_time_min)