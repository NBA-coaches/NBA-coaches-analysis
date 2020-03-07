from bs4 import BeautifulSoup as bs
import requests
import re
from csv import writer

def urlRequest(url):
    req = requests.get(url)
    if req.status_code == 200:
        return req.text
    else:
        return None


def parseHTML(url):
    if urlRequest(url) != None:
        return bs(urlRequest(url), "html.parser")
    else:
        return None

def getTeams(soup):
    teamsList = []
    for a in soup.findAll('table')[0].find_all('a'):
        teamsList.append(a['href'][7:10])
    return teamsList

def getSeasonPage(url, team, year):
    return parseHTML(url+'/'+team+'/'+year+'.html')

def getCoachs(page):
    if (page != None):
        meta = page.find(id='meta').get_text()
        coaches = re.findall("Coach.*$", meta, re.MULTILINE)[0].split(', ')
        coaches[0] = re.sub(r'^\w+\S\s', '', coaches[0])
        balance = []
        for i in range(len(coaches)):
            balance.append(re.search(r'\((.*?)\)',coaches[i]).group(1))
            coaches[i] = re.sub(r'\s\(\d*\S+\d*\)', '', coaches[i])
        return coaches, balance
    else:
        return None

def makeCSV(name):
    file = open(name+'.csv', 'w+')
    return file

def append_list_as_row(file_name, values):
    with open(file_name, 'a+', newline='', encoding='cp1255') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(values)
    write_obj.close()

def makeCoachesDataSet(url):
    teamsList = getTeams(parseHTML(url))
    for team in teamsList:
        csvfile = makeCSV(team)
        csvfile.close()
        for year in range(1946, 2019):
            yearlist = [str(year)]
            season = getSeasonPage(url, team, str(year))
            if season != None:
                coaches, balances = getCoachs(season)
                for i in range(len(coaches)):
                    yearlist.append(coaches[i])
                    yearlist.append(balances[i])
                    print(yearlist)
                    append_list_as_row(csvfile.name, yearlist)




url = 'http://www.basketball-reference.com/teams'
makeCoachesDataSet(url)



