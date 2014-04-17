
import urllib2
import string


def Fetch(artist,title):
    url = 'http://www.azlyrics.com/lyrics/' + artist + '/' + title + '.html'
    try:
        req = urllib2.Request(url)
    except:
        return
    response = urllib2.urlopen(req)
    return response
    
def Write(response,artist,title):
    flag = 0
    #outFile = open(WordFormat(title)+".txt",'w')
    outFile = open(title.strip()+".txt",'w')
    
    outFile.write(artist + " - " + title)
    outFile.write("\t\t\tby TigerApps\n\n")
    for line in response:
        if "end of lyrics" in line:
            flag = 0
        elif flag == 1:
            if "<i>" in line:
                continue
            line = line.replace("<br />","")
            outFile.write(line)
        elif "start of lyrics" in line:
            flag = 1
    outFile.close()

def MakeDict(inFile):
    temp = {}
    for line in inFile:
        List = []
        List = line.split('--')
        try:
            temp[List[0]] = List[1]
        except:
            pass
    return temp
        
def DoiT(ARTIST_TITLE):
    for artist in ARTIST_TITLE.keys():
        response = Fetch(WordFormat(artist),WordFormat(ARTIST_TITLE[artist]))
        Write(response,artist,ARTIST_TITLE[artist])

def WordFormat(word):
     word = word.lower()
     word = word.strip('\n')
     word = word.replace(" ","")
     return word

def SaveLyrics():
    ARTIST_TITLE = {}
    
    inFile = open("List.txt",'r')
    print "working...."
    ARTIST_TITLE = MakeDict(inFile)
    DoiT(ARTIST_TITLE)
    print "youza!"

SaveLyrics()
