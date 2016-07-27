from urllib.request import urlopen
from html.parser import HTMLParser
from os import path

class NupkgHTMLParser (HTMLParser):
    def __init__ (self):
        super(NupkgHTMLParser, self).__init__()
        self.pkgUrl = ''
        self.dependencies = []
        self.dependenciesInTracking = False

    def handle_starttag (self, tag, attrs):
        if tag == 'a':
            attrsDict = dict(attrs)
            if self.dependenciesInTracking and 'href' in attrsDict:
                self.dependencies.append(attrsDict['href'])
            elif 'title' in attrsDict:
                if attrsDict['title'] == 'Download the raw nupkg file.':
                    self.pkgUrl = attrsDict['href']

        if tag == 'ul':
            attrsDict = dict(attrs)
            if 'class' in attrsDict and attrsDict['class'] == 'dependencySet':
                self.dependenciesInTracking = True

    def handle_endtag (self, tag):
        if self.dependenciesInTracking and tag == 'ul':
            self.dependenciesInTracking = False

def downloadNupkg(url, targetdir): 
    print ('Parsing Dependency:', url)
    response = urlopen(url)
    content = str(response.read())

    parser = NupkgHTMLParser();
    parser.feed(content);
    parser.close()

    if (parser.pkgUrl != ''):
        downloadUriTo(parser.pkgUrl, targetdir)

    host = getHost(url)
    for dependency in parser.dependencies:
        dependencyUrl = host + dependency
        downloadNupkg(dependencyUrl, targetdir)

    print ('Task complete.')

def downloadUriTo(url, dirname):
    print ('Downloading package:', url)
    pkgResponse = urlopen(url)
    pkgUrl = str(pkgResponse.url)
    pkgName = path.basename(pkgUrl)
    pkgFullname = path.join(dirname, pkgName)
    with open (pkgFullname, 'wb') as output:
        output.write(pkgResponse.read())
        output.close()

def getHost(url):
    schema = ''
    domain = ''
    if '://' in url:
        schema = url[:url.index('://') + 3]
        url = url.strip(schema)

    domain = url[:url.index('/')]
    host = ''.join([schema, domain])
    return host

downloadNupkg('https://www.nuget.org/packages/NetTopologySuite/', r'e:\')
