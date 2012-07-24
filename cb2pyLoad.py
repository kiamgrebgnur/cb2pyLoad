#!/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import time
import os
import urllib2
import sys
import getopt

VERSION="0.1"
DEBUG=False
VERBOSE=False
DEST="add_coll"
CB_WAIT = 2 # in sec


def usage():
	print """
	
pyLoad Clipboard Extension
###########################

the script looks for links in the clipboard and send them to pyLoad via pyLoadCli

	-d\t\t\t- set debug on (default is off)
	-v\t\t\t- set verbose on (default is off)
	-q\t\t\t- send links to queue (default is collector)
	-w\t\t\t- time to check clipboard (default is 2s)
	-h\t\t\t- print help
	-version\t\t- print version

		"""
	exit()


if len(sys.argv) > 1:
	try:
		opts,remain = getopt.getopt(sys.argv[1:],'dvqw:hversion',['version'])
	
		for opt, arg in opts:
			if opt == "-d":
				DEBUG = True
			elif opt == "-v":
				VERBOSE = True
			elif opt == "-q":
				DEST = "add"
			elif opt == "-w":
				CB_WAIT = arg
			elif opt == "--version":
				print "v"+VERSION
				exit()
			elif opt == "-h":
				usage()
	except:
		usage()
	


url_filter = [
	'http://www.boerse.bz/out/?url=',
	'htp://foo.de',
	'http://www.bar.com'
]


old_cb = ""
url_list = ""

if DEBUG:
	print "get clipboard handle..."

cb = gtk.clipboard_get()

while True:

	name=""
	url_list=""
	
	time.sleep(CB_WAIT)

	if DEBUG:
		print "get clipboard data..."

	cb_text = cb.wait_for_text()
	
	if old_cb == cb_text:
		if DEBUG:
			print "old clipboard data == new, skip..."
		continue
	else:
		old_cb = cb_text
	
	if DEBUG:
		print "clipboard before filter:", cb_text
	
	for filter_string in url_filter:
		cb_text = cb_text.replace(filter_string,"")
	
	if DEBUG:
		print "clipboard after filter:", cb_text

	if DEBUG:
		print "clean clipboard..."

	urls = cb_text.replace('\n','')
	urls = urls.replace('\r','')
	urls = urls.split("http://")
	
	if DEBUG:
		print "raw url list:", urls


	for url in urls:
		if DEBUG:
			print "test url:",url

		if url == '':
			if DEBUG:
				print "url empty, skip..."
			continue
		
		url = "http://" + url
		
		if DEBUG:
			print "test if url is accessible..."

		try:
			test_url = urllib2.urlopen(url)
			if DEBUG:
				print "url is on :)"
		except:
			if DEBUG:
				print "url if off :("
			continue
			
		if name == "":
			name = url.split("/")[-1]
		
		if DEBUG or VERBOSE:
			print "link name:",name
			print "url:", url

		url_list = url_list + " " + url

		if DEBUG:
			print "url list:", url_list

	if url_list != "":
	
		command = "/usr/bin/pyLoadCli add_coll " + name + " " + url_list
		if DEBUG or VERBOSE:
			print "pyLoadCli command:", "'" + command + "'"
		
		pyl = os.popen(command).readlines()
		if DEBUG:
			print "pyLoadCli response:", pyl

		if DEBUG or VERBOSE:
			print "link(s) added! :)"
	




