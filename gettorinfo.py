import io
import sys
import pycurl
import re

PORT = 9150

def getbody(url):
    'Connects to the torbundle tor service and returns data'
    out = io.BytesIO()  #Will hold the IO output data
    curl = pycurl.Curl()   #Uses pycurl to gain a connection through your tor services
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.PROXY, '127.0.0.1')
    curl.setopt(pycurl.PROXYPORT, PORT)
    curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME)
    curl.setopt(pycurl.WRITEFUNCTION, out.write)  #Load the site data into out.write
    
    curl.perform() #HTTP request
    curl.close()

    return out.getvalue().decode("utf-8")  #The data needs converted from bytes to easily read.
    

def geturls(html):
    'Takes a string and extracts url patterns'
    urls = []

    #Note that this regex pattern only grabs top level domains up to length 5. Other may exists but it will not catch them.
    reg_obj = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,5}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
    temp_domains = reg_obj.findall(html)

    #There will be some empty strings returned which is filtered out here
    if temp_domains != []:
        for temp in temp_domains:
            for tem in temp:
                if tem != '':
                    urls.append(tem)

    return urls

if __name__ == '__main__':
    'prints the URLs html code or extracted URLs'
    url = 'https://www.torproject.org/'

    if len(sys.argv) >= 2:  #If the command line supplies the first argument change the url 
        url = sys.argv[1]
    body = getbody(url)
    if len(sys.argv) <= 2:   #Print the default or the provided URLs HTML code
        print(body)
    if  '-url' in sys.argv:  #Print all extracted URLs if the -url tag is present.
        urls = geturls(body)
        for url in urls:
            print(url)
