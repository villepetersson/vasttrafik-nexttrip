#!/usr/bin/python2
# -- coding: utf-8 --
import urllib
from fuzzywuzzy import process
from x256 import x256
from BeautifulSoup import BeautifulSoup
from time import strftime
import argparse
import os

def colorize(fg,bg):
	return '\x1b[38;5;' + str(x256.from_hex(fg[1:])) + 'm' + '\x1b[48;5;' + str(x256.from_hex(bg[1:])) + 'm'

endcolor = '\x1b[0m'

def generate_stops():
	page = urllib.urlopen("http://wap.vasttrafik.se/QueryForm.aspx").read()
	soup = BeautifulSoup(page, convertEntities=BeautifulSoup.HTML_ENTITIES)

	stops = open(os.path.join(os.path.expanduser("~"),".config","vasttrafikstops"),"w+")

	string = ""
	# Find all stops in the list.
	for option in soup.body.find('select', attrs={'id':'DropDownListStop'}).findAll('option'):
		string+=option.text.encode('utf-8')+"\n"

	stops.write(string)
	stops.close()

def find_stop(stopnames):
	stops = list()
	fewerstops = list()
	allstops = open(os.path.join(os.path.expanduser("~"),".config","vasttrafikstops")).read().decode('utf-8').split('\n')

	# Because the fuzzywuzzy matching is slow, single out the possible results first.
	for line in allstops:
		for stopname in stopnames:
			if stopname.upper() in line.upper():
				fewerstops.append(line)
				break

	stops = process.extract(stopnames, fewerstops, limit=10)

	return stops

def get_trams(stopname="Godhemsgatan+(Göteborg)"):
	page = urllib.urlopen("http://wap.vasttrafik.se/QueryForm.aspx?hpl=%s"%(stopname)).read()
	soup = BeautifulSoup(page, convertEntities=BeautifulSoup.HTML_ENTITIES)

	trams = list()

	# Find all trams in the list.
	for tr in soup.body.find('table', attrs={'id':'GridViewForecasts'}).findAll('tr'):
		# Skip the header.
		if tr['class']=="darkblue_pane":
			continue

		num = tr.findNext('td')
		to = num.findNext('td')
		next = to.findNext('td')
		nextnext = next.findNext('td').findNext('td')
		trams.append(dict(num=num.font.text,numbg=num['bgcolor'],numfg=num.font['color'],to=to.font.text,next=next.font.text.replace('Nu','0'),nextnext=nextnext.font.text))

	return trams

def print_stopname(stopname):
	print "\n\x1b[1m%s\x1b[0m, %s\n"%(stopname,strftime("%c"))

def print_trams(tramdict):
	#trams.sort(key=lambda tram: tram['next'])
	for tram in tramdict:
		print colorize(tram['numfg'],tram['numbg'])+'\t'+tram['num']+'\t'+endcolor+'\t'+tram['to']+(20-len(tram['to']))*' '+'\t\x1b[1m'+tram['next']+'\x1b[0m\t'+tram['nextnext']

def main(argv,force):                         
	stops = list()
	stops = find_stop(argv)

	if len(stops)==1 or force:
		try:
			trams = get_trams(stops[0][0].encode('utf-8'))
			print_stopname(stops[0][0].encode('utf-8'))
			print_trams(trams)
		except Exception:
			print "No departures found."
	elif len(stops)==0:
		print "No such stop exists."
	else:
		i = 0
		for stop in stops:
			print "%s: %s"%(str(i), stop[0])
			i+=1

		select = raw_input("Select: ")
		try:
			print_stopname(stops[int(select)][0].encode('utf-8'))
			print_trams(get_trams(stops[int(select)][0].encode('utf-8')))
		except Exception:
			print "No departures found."                 


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("stopname", help="Name of the bus/tram stop.",nargs='*')
	parser.add_argument("--reload", "-r", help="update stops list.",action="store_true")
	parser.add_argument("--force", "-f", help="force best search hit.",action="store_true")
	args = parser.parse_args()

	if args.reload or not os.path.exists(os.path.join(os.path.expanduser("~"),".config","vasttrafikstops")):
		print "Generating stops file..."
		generate_stops()
		print "Generated stops file."

	main([x.decode('utf-8') for x in args.stopname],args.force)
