#!/usr/bin/python
import simplejson as json
import datetime 
from optparse import OptionParser 
import subprocess
import csv

parser = OptionParser()
parser.add_option("-f", "--filename", dest="name", help="the filename of the csv file")

(options, args)=parser.parse_args()

if options.filename != None:
	csv_filename = str(options.filename)
else:
	csv_filename = "foobar.csv"
print "csv file is " csv_filename

input
csvReader = csv.reader(open(csv_filename, "rb"), delimiter=',', quotechar='"')


output_file.close()

#title_abc = "fatdog"
#url = "google.com"
#url_text = "google.com"
#id_abc=repr(123)
#html_message =  "<p><font face='Arial, Helvetica, sans-serif'><b>Project :</b>" + title_abc + "</font></p>";
#html_message += "<p><font face='Arial, Helvetica, sans-serif'><b>Where:</b>&nbsp;</font>" ;
#html_message += "<a href=" + url + " style='color: #1155cc;' target=''><font face='Arial, Helvetica, sans-serif'>" + url_text + "</font></a></p>";
#html_message += "<p><font face='Arial, Helvetica, sans-serif'><b>Tagline :</b>" + title_abc + "</font></p>";
#html_message += "<p><p><a href=http://news.ycombinator.com/item?id=" + id_abc + " style='color: #1155cc;' target='_blank'><font face='Arial, Helvetica, sans-serif'>HN Discussions</font></a></p>";  
#test(html_message)
