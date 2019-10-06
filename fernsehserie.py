
import sys
import getopt
import urllib.request
import urllib.parse
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


#gets the episode number in formate SxxExx given a show and episode name


def fernsehserie(show_name, episode_name, debug = False):
    #prep the search url
    show_name = urllib.parse.quote(show_name)
    url = 'https://www.fernsehserien.de/suche/' + show_name
    #values = {'s':'show_name','submit':'search'}
    if debug:
        print("URL is: " + url)

    #get the search page
    req = urllib.request.Request(url) 
    resp = urllib.request.urlopen(req)
    if debug:
        print("Response URL is: " + str(resp.geturl()))
    if "suche" in str(resp.geturl()):
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
        if debug:
            print("URL to show page is: " + url)
    else:
        url = str(resp.geturl()) + '/episodenguide'

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
    rowx = len(tr_elements)
    col = 0
    for tr in tr_elements:
        col = max(col, len(tr))
    Matrix = [[''] * (col + 1) for x in range(rowx)]
    for i in range(rowx):
        td_elements = tr_elements[i].find_all('td')
        for j in range(col):
            try:
                if not td_elements[j].text.strip().isspace():
                    Matrix[i][j] = remove_text_inside_brackets(td_elements[j].text.strip()).strip()
            except IndexError:
                pass
        Matrix[i][col] = str(levenshtein(Matrix[i][6], episode_name))
    #print the Matrix
    if debug:
        printMatrix(Matrix)
    #find the episode
    #replaced by using the levensthein algorithmen to determine the closest match and not just 
    #looking for exact matches
    # location = -1
    # for i in range(len(Matrix)):
    #     inrow = False
    #     for cell in Matrix[i]:
    #         if not cell.find(episode_name) == -1:
    #             inrow = True
    #             location = i
    #     if inrow:
    #         if debug:
    #             stringy = ""
    #             for cell in Matrix[location]:
    #                 stringy = stringy + cell + "|"
    #             print("Found in this line: " + stringy)
    #         break
    # if location == -1:
    #     print("An episode by this name could not be found mybe there was an error try with `-d`")
    # else:
    #     season_number = str(Matrix[location][3])[:-1]
    #     if len(season_number) == 1:
    #         season_number = "0" + season_number
    #     number = "S" + season_number + "E" + Matrix[location][4]
    #     print("The episodes number is: " + number)
        

    #find the location using the results of the levenshtein algorithm
    df = pd.DataFrame(Matrix)
    df=df.drop(0,axis=1)
    df=df.drop(2,axis=1)
    df=df.drop(5,axis=1)
    df[10] = df[10].astype(int)
    df = df.sort_values(by=10 , na_position='last')
    if debug:
        print(df)
    season_number = str(df[3].iloc[0])[:-1]
    if len(season_number) == 1:
        season_number = "0" + season_number
    number = "S" + season_number + "E" + str(df[4].iloc[0])
    if debug:
        print("The episodes number is: " + number)

    return number

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = [[0] * size_y for x in range(size_x)]
    for x in range(size_x - 1 ):
        matrix [x ][0] = x
    for y in range(size_y - 1):
        matrix [0][y] = y

    for x in range(1, size_x - 1):
        for y in range(1, size_y - 1):
            if seq1[x-1] == seq2[y-1]:
                matrix [x][y] = min(
                    matrix[x-1][y] + 1,
                    matrix[x-1][y-1],
                    matrix[x][y-1] + 1
                )
            else:
                matrix [x][y] = min(
                    matrix[x-1][y] + 1,
                    matrix[x-1][y-1] + 1,
                    matrix[x][y-1] + 1
                )
    #print (matrix)
    return (matrix[size_x - 2][size_y - 2])

def remove_text_inside_brackets(text, brackets="()"):
    count = [0] * (len(brackets) // 2) # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b: # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close # `+1`: open, `-1`: close
                if count[kind] < 0: # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else: # character is not a [balanced] bracket
            if not any(count): # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars)

def printMatrix(m):
    for row in m:
            value = ''
            for e in row:
                value = value + e + "|"
            print(value)    

def main(argv):
    show_name = ''
    episode_name = ''
    debug = False
    try:
        opts = getopt.getopt(argv,"dhs:e:")
    except getopt.GetoptError:
        print('fernsehserie-de.py -s "Show Name" -e "Episode name" ') #change
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('fernsehserie-de.py -s "Show Name" -e "Episode name" ') #change
            sys.exit()
        elif opt in ("-s"):
            show_name = arg
        elif opt in ("-e"):
            episode_name = arg
        elif opt in ("-d"):
            debug = True
           
    if debug:
        print('Show name is ' + show_name)
        print('episode name is ' + episode_name)
    number = fernsehserie(show_name, episode_name, debug)
    print(number)
    

if __name__ == "__main__":
    #print(sys.version)
    main(sys.argv[1:])





