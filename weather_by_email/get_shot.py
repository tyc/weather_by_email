#!/usr/bin/python
import datetime
import os
import subprocess
import urlparse
from optparse import OptionParser

# app configuration
APP_ROOT = os.path.dirname(os.path.realpath(__file__))
MEDIA_ROOT = os.path.join(APP_ROOT, 'static')
MEDIA_URL = '/static/'
PHANTOM = '/usr/local/bin/phantomjs'
SCRIPT = os.path.join(APP_ROOT, 'screenshot.js')

parser = OptionParser()
parser.add_option("-u", "--url", dest="url", help="url to get a snapshot of")
parser.add_option("-i", "--id", dest="itemid", default="000", help="specify news_hacker article")
(options, args)=parser.parse_args()

if options.url is not None:
        url = str(options.url)
	print "getting snapshot of " + url
	url_base = urlparse.urlsplit(url)  
	filename = str(url_base.netloc) + "." + str(options.itemid) + ".png" 
	outfile = os.path.join(MEDIA_ROOT, filename)
	params = [PHANTOM, SCRIPT, url, outfile]

	exitcode = subprocess.call(params)

