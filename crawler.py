from bs4 import BeautifulSoup as bs
import requests
import selenium


def urlRequest(url):
    return requests.get(url).text

def parseHTML(req):
    return bs(req, "html.parser")

def getTeams(soup):
    teamsList = []
    for a in soup.findAll('table')[0].find_all('a'):
        teamsList.append(a['href'][7:10])
    return teamsList

def getTeamPage(url):
    soup = parseHTML(urlRequest(url))
    #TODO



req = urlRequest("http://www.basketball-reference.com/teams")
soup = parseHTML(req)
print(getTeams(soup))
