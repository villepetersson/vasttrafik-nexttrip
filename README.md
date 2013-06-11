# Next trip CLI tool

Prints upcoming trams for stops in western Sweden, by scraping Västtrafik's site. Written in python2.

## Uses
* BeautifulSoup
* fuzzywuzzy
* x256

To use this app, fetch them using pip.

## Usage
```
usage: trams.py [-h] [--reload] [--force] [stopname [stopname ...]]

positional arguments:
  stopname      Name of the bus/tram stop.

optional arguments:
  -h, --help    show this help message and exit
  --reload, -r  update stops list.
  --force, -f   force best search hit.
```

Made by Ville Petersson, 2013.