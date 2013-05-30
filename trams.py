#!/usr/bin/python3
# -- coding: utf-8 --
import urllib
from x256 import x256
from BeautifulSoup import BeautifulSoup


def colorize(fg,bg):
	return '\x1b[38;5;' + str(x256.from_hex(fg[1:])) + 'm' + '\x1b[48;5;' + str(x256.from_hex(bg[1:])) + 'm'

endcolor = '\x1b[0m'

page = urllib.urlopen("http://wap.vasttrafik.se/QueryForm.aspx?hpl=Godhemsgatan+(G%C3%B6teborg)").read()
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
	trams.append(dict(num=num.font.text,numbg=num['bgcolor'],numfg=num.font['color'],to=to.font.text,next=next.font.text,nextnext=nextnext.font.text))

for tram in trams:
	print colorize(tram['numfg'],tram['numbg'])+'\t'+tram['num']+'\t'+endcolor+'\t'+tram['to']+'\t\t\x1b[1m'+tram['next']+'\x1b[0m\t'+tram['nextnext']

