import sys, getopt
def main(argv):
    file = ''
    debug = False
    try:
        opts, args = getopt.getopt(argv,"hdf:")
    except getopt.GetoptError:
        print('fernsehserie-de.py -s "Show Name" -e "Episode name" ') #change
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('fernsehserie-de.py -s "Show Name" -e "Episode name" ') #change
            sys.exit()
        elif opt in ("-f"):
            file = arg
        elif opt in ("-d"):
            debug = True
    tvheadend(file, debug)

def tvheadend(file="String", debug = False):
    if debug:
        print("The file given is:" + file)
    show = file[:file.find('.')]

    title = file.split('.')[1]
    #print("First " + title)
    title = title[:title.find(', ')]
    #print("Second " + title)
    if "." in title:
        title = title[:title.rfind('.') + 1]
    if "Serie" in title or "Dramedy" in title:
        title = title[:title.rfind(" ")]


    
    if debug:
        print("The show is: " + show + " and the Episode: " + title)
    return (show, title)




if __name__ == "__main__":
    #print(sys.version)
    main(sys.argv[1:])