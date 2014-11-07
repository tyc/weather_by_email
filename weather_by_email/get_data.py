#!/usr/bin/python
import urllib2
import simplejson as json
import smtplib
import datetime 
import time
import re
from mailsnake import MailSnake
from optparse import OptionParser 
import subprocess

htmltext_template = open('email_template.html').read()

def get_json_data(url):
	req = urllib2.Request(url)
	opener = urllib2.build_opener()
	f = opener.open(req)
	json_obj = json.load(f)
	return json_obj


def sent_email(forecast, location,email):
	SMTP_SERVER = 'smtp.mandrillapp.com'
	SMTP_PORT = 587

	sender = 'tehn.yit.chin@gmail.com'
	recipient = str(email)
	subject = "Daily Forecast for " + str(location)
	body = ""

	body = "" + body + forecast + ""

	headers = ["From: " + sender,
		   "Subject: " + subject,
		   "To: " + recipient,
		   "MIME-Version: 1.0",
		   "Content-Type: text/html"]
	headers = "\r\n".join(headers)

	session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

	session.ehlo()
	session.starttls()
	session.ehlo
	session.login(sender, 'BhhZZCYgpLQpxrpjLWLgbQ')

	session.sendmail(sender, recipient, headers + "\r\n\r\n" + forecast)
	session.quit()
	return None

#parse the input options and use it code.
parser = OptionParser()
parser.add_option("-t", "--town", dest="town", help="town")
parser.add_option("-c", "--country", dest="country", help="country")
parser.add_option("-e", "--email", dest="email", help="email address")

(options, args)=parser.parse_args()

if options.country == None:
	options.country = "Germany"

if options.town == None:
	options.town = "Leichlingen"

if options.email == None:
	options.email = "tehn.yit.chin@gmail.com"



# get the list of email addresses
opts = {'stream': True}
export = MailSnake('7726f9f014ed1511f11722f300bbbd43-us9', api='export', requests_opts=opts)
subscribers_list = export.list(id='1b1f1ee8be')
	
lines = 0
for list_member in subscribers_list():
	
	if lines > 0: # skip header row
		options.email = list_member[0]
		options.town = list_member[1]
		options.country = list_member[2]
		
		location = str(options.town) + "," + str(options.country)
		current_temp_url = "http://api.openweathermap.org/data/2.5/weather?APPID=ea2609c80dcead10bc52f803ff53eaa8&q="+str(location);
		current_temp_json_obj = get_json_data(current_temp_url)

		print time.strftime("%Y%m%d-%H%M%S") + ' Processing for weather data for ' + str(options.email) + ' for ' + str(location)

# check that the location is known.
		if (current_temp_json_obj["cod"] == 200):
			temp_celcuis = int(current_temp_json_obj["main"]["temp"]) - 273;
			
			forecast_temp_url = "http://api.openweathermap.org/data/2.5/forecast/daily?APPID=ea2609c80dcead10bc52f803ff53eaa8&units=metric&cnt=2&q="+str(location)
			forecast_temp_json_obj = get_json_data(forecast_temp_url)
			
			forecast_temp_max = int(forecast_temp_json_obj["list"][1]["temp"]["max"])
			forecast_temp_min = int(forecast_temp_json_obj["list"][1]["temp"]["min"])
			forecast_temp_morn = int(forecast_temp_json_obj["list"][1]["temp"]["morn"])
			forecast_temp_eve = int(forecast_temp_json_obj["list"][1]["temp"]["eve"])
			forecast_temp_night = int(forecast_temp_json_obj["list"][1]["temp"]["night"])
			forecast_temp_status = str(forecast_temp_json_obj["list"][1]["weather"][0]["description"])
			forecast_time_date = datetime.datetime.fromtimestamp(int(forecast_temp_json_obj["list"][1]["dt"])).strftime('%A, %d %B %Y')
			forecast_temp_status = str(forecast_temp_status)
				
#build up the HTML email by inserting some custom text from the weather forecast
			htmltext = htmltext_template
			htmltext = re.sub('\$WBE_LOCATION\$',str(location),htmltext)
			htmltext = re.sub('\$WBE_DATE_TIME\$',str(forecast_time_date),htmltext)
			htmltext = re.sub('\$WBE_FORECAST\$',str(forecast_temp_status),htmltext)
			htmltext = re.sub('\$WBE_FORECAST_TEMP_MIN\$',str(forecast_temp_min),htmltext)
			htmltext = re.sub('\$WBE_FORECAST_TEMP_MAX\$',str(forecast_temp_max),htmltext)
			htmltext = re.sub('\$WBE_FORECAST_TEMP_MORNING\$',str(forecast_temp_morn),htmltext)
			htmltext = re.sub('\$WBE_FORECAST_TEMP_AFTERNOON\$',str(forecast_temp_eve),htmltext)
			htmltext = re.sub('\$WBE_FORECAST_TEMP_EVENING\$',str(forecast_temp_night),htmltext)
			sent_email(htmltext,location,options.email)
		
		
		elif (current_temp_json_obj["cod"] == 404):
			print "The location is " + str(location) + " unknown."
	
	lines += 1
