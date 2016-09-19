from urllib.request import urlopen
from html.parser import HTMLParser
from os import path
from os import getcwd
import sys

class WorldDataHTMLParser (HTMLParser):
    def __init__(self):
        super(WorldDataHTMLParser, self).__init__()
        self.pkgUrl = ''
        self.folders = []
        self.inFolder = False

    def handle_starttag(self, tag, attrs):
        attrsDict = dict(attrs)
        if tag == 'table':
            self.inFolder = True

        if self.inFolder and tag == 'td':
            print(tag)

    def handle_endtag(self, tag):
        if self.inFolder and tag == 'table':
            self.inFolder = False

page_url = 'http://vdstech.com/osm-data.aspx'
response = urlopen(page_url)
content = str(response.read())

parser = WorldDataHTMLParser()
parser.feed(content)
parser.close()