from bs4 import BeautifulSoup as bs
import requests
import selenium


def urlRequest(url):
    return requests.get(url)

def parseHTML(req):
    return bs(open(req), "html.parser")
