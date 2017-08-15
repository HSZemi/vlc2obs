#! /usr/bin/env python3

import xml.etree.ElementTree as ET
import requests
import sys
import time
import json

last_value = ''
new_value = ''
logfile = 'log/log_{}.log'.format(time.time())

db = None
with open("db.json", "r") as j:
	db = json.load(j)

default = "{} Kevin MacLeod (incompetech.com)\nLicensed under Creative Commons: By Attribution 3.0 License\nhttp://creativecommons.org/licenses/by/3.0/"

try:
	with open(logfile, 'w') as log:
		while True:
			r = requests.get("http://127.0.0.1:8080/requests/status.xml", auth=('','passwort'))

			root = ET.fromstring(r.text)

			#root = tree.getroot()
			artist = ''
			title = ''
			filename=''

			information = root.find('information')
			for meta in information.findall('category'):
				if meta.attrib['name'] == 'meta':
					for info in meta:
						if info.attrib['name'] == 'title':
							title = info.text
						if info.attrib['name'] == 'artist':
							artist = info.text
						if info.attrib['name'] == 'filename':
							filename = info.text

			if(title == ""):
				title = filename
			new_value = "{} - {}".format(artist, title)
			
			if new_value != last_value:
				print("Updating to:\n{}".format(new_value))
				with open("information.txt", "w") as f:
					if(artist in db and title in db[artist]):
						print(db[artist][title], file=f)
					else:
						print(default.format(title), file=f)
				print("{time}\t{artist}\t{title}".format(time=time.time(), artist=artist, title=title ),file=log)
				log.flush()
				last_value = new_value
			time.sleep(2)
except KeyboardInterrupt:
	print("Exiting...")
	sys.exit(0)