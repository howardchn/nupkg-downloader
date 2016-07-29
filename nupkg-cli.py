from urllib.request import urlopen
from html.parser import HTMLParser
from os import path
from os import getcwd
import sys

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

downloaded_urls = []
def download_nupkg(url, targetdir): 
    if not url in downloaded_urls:  
        downloaded_urls.append (url)
        print ('Parsing Dependency:', url)
        response = urlopen(url)
        content = str(response.read())

        parser = NupkgHTMLParser();
        parser.feed(content);
        parser.close()

        if (parser.pkgUrl != ''):
            download_url(parser.pkgUrl, targetdir)

        host = getHost(url)
        for dependency in parser.dependencies:
            dependencyUrl = host + dependency
            download_nupkg(dependencyUrl, targetdir)

def download_url(url, dirname):
    print ('Downloading package:', url)
    pkgResponse = urlopen(url)
    pkgUrl = str(pkgResponse.url)
    pkgName = path.basename(pkgUrl)
    pkgFullname = path.join(dirname, pkgName)
    with open (pkgFullname, 'wb') as output:
        output.write(pkgResponse.read())

def getHost(url):
    schema = ''
    domain = ''
    if '://' in url:
        schema = url[:url.index('://') + 3]
        url = url.strip(schema)

    domain = url[:url.index('/')]
    host = ''.join([schema, domain])
    return host

def strip_arg(arg):
    arg = arg.strip()
    arg = arg.strip('"')
    arg = arg.strip("'")
    return arg

def help (): 
    print ('''This is NuGet package downloader. It downloads the package and its dependencies recursively.
    \tusage: nupkg-cli.py nupkg_url [out_dir] [-h | --h]''')

def get_download_list (list_path):
    with open (list_path, 'r') as file:
        lines = file.readlines ()
        return lines

def main (argv):
    url = '' # 'https://www.nuget.org/packages/NetTopologySuite' 
    output_dir = getcwd()
    
    if len (argv) == 1 or '-h' in argv or '--h' in argv:
        help()
    else: 
        if len (argv) >= 2:
            url = strip_arg (argv[1]) 
        if len (argv) >= 3:
            output_dir = strip_arg (argv[2])
        if not bool (url):
            help()
        else:
            ext = path.splitext (url)[1]
            if ext == '.txt':
                urls = get_download_list(url)
                for tmp_url in urls:
                    download_nupkg(tmp_url, output_dir)
            else:
                download_nupkg(url, output_dir)
            print ('Task complete.')
    
main (sys.argv)

# python nupkg-cli.py E:\VS-Git\Python\nupkg-downloader\tasks.txt E:\VS-Git\ThinkGeo-NuPkgs


