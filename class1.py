
import sys
import getopt
import ssl
import urllib.request
import urllib.parse
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd

def main(argv):
    show_name = ''
    episode_name = ''
    try:
        opts, args = getopt.getopt(argv,"hs:e:")
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile> error error') #change
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>') #change
            sys.exit()
        elif opt in ("-s"):
            show_name = arg
        elif opt in ("-e"):
            episode_name = arg
    print('Show name is ' + show_name)
    print('episode name is ' + episode_name)
    
    #prep the search url
    show_name = urllib.parse.quote(show_name)
    url = 'https://www.fernsehserien.de/suche/' + show_name
    #values = {'s':'show_name','submit':'search'}
    print("URL is: " + url)

    #get the search page
    #data = urllib.parse.urlencode(values)
    #data = data.encode('utf-8')
    req = urllib.request.Request(url) 
    resp = urllib.request.urlopen(req) 
    respData = resp.read() 
    soup = BeautifulSoup(respData, features="html.parser")

    #parse the search page to get the link to the series
    link = soup.find("main")
    link = link.find("ul")
    link = link.find("li")
    link = link.find("a")
    link = link['href']

    #construct episode url
    url = 'https://www.fernsehserien.de' + link + '/episodenguide'
    print("URL to show page is: " + url)

    #get show page
    req = urllib.request.Request(url) 
    resp = urllib.request.urlopen(req) 
    respData = resp.read() 
    soup = BeautifulSoup(respData, features="html.parser")

    #parse show page
    #first find the table
    table = soup.find("main")
    table = table.find("article")
    table = table.find("table")  
    #convert the usable entries into a matrix
    tr_elements = table.find_all('tr', attrs={'class': 'ep-hover episode-desktop'})
    cols = len(tr_elements)
    rows = 0
    for tr in tr_elements:
        rows = max(rows, len(tr))
    print("Table is of size" + str(cols) + "x" + str(rows))
    Matrix = [[''] * rows for x in range(cols)]
    for i in range(cols):
        td_elements = tr_elements[i].find_all('td')
        for j in range(rows):
            try:
                if td_elements[j].text.strip():
                    Matrix[i][j] = td_elements[j].text.strip()
            except IndexError:
                pass
    #print the Matrix
    for row in Matrix:
        value = ''
        for e in row:
            value = value + e + "|"
        print(value)
    #find the episode
    for row in Matrix:
        if episode_name in row[4]: #should replace 4 with some way to search for the coloumn with the most letters across al rows
            print("the episode was found in " + row[4])
            


    

    #print("Staffel: " + str(staffel) + " Episode: " + episode)

    

if __name__ == "__main__":
    #print(sys.version)
    main(sys.argv[1:])


#page = "https://www.fernsehserien.de/suche/" + name
#print(page)



