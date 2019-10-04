import sys, getopt
sys.path.append('.')
import tvheadend
import fernsehserie
def main(argv):
    fileName = ''
    debug = False
    try:
        opts, args = getopt.getopt(argv,"dhf:")
    except getopt.GetoptError:
        print('fernsehserie-de.py -s "Show Name" -e "Episode name" ') #change
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('fernsehserie-de.py -s "Show Name" -e "Episode name" ') #change
            sys.exit()
        elif opt in ("-f"):
            fileName = arg
        elif opt in ("-d"):
            debug = True

    (show, episode) = tvheadend.tvheadend(fileName, debug)
    number = fernsehserie(show, episode, debug)
    return number





if __name__ == "__main__":
    #print(sys.version)
    main(sys.argv[1:])