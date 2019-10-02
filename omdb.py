def main(argv):
    show_name = ''
    episode_name = ''
    debug = False
    try:
        opts, args = getopt.getopt(argv,"dhs:e:")
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
#prep the search url
show_name = urllib.parse.quote(show_name)




if __name__ == "__main__":
    #print(sys.version)
    main(sys.argv[1:])