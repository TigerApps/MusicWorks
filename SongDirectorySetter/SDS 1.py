import os
import id3reader
import shutil

class TAG(object):
    def __init__(self,file_name):
##        file = open(file_name,'r')  
##        file.seek(-128, 2)
##        self.tag = file.read(128)
##        self.Title = self.tag[3:33].strip()
##        self.Artist = self.tag[33:63].strip()
##        self.Album = self.tag[63:93].strip()
##        self.Year = self.tag[93:97].strip()
##        self.Comment = self.tag[97:127].strip()
##        self.Genre = self.tag[127].strip()

        id3r = id3reader.Reader(file_name)
        self.Title = id3r.getValue('title')
        self.Artist = id3r.getValue('performer')
        self.Album = id3r.getValue('album')
        self.Track = id3r.getValue('track')
        self.Year = id3r.getValue('year')
       

    def getTitle(self):
        return self.Title
    def getArtist(self):
        return self.Artist
    def getAlbum(self):
        return self.Album
    def getTrack(self):
        return self.Track
    def getYear(self):
        return self.Year
   

                            
def IndexSongs(ARTIST,ALBUM,directory):
   for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
               test = TAG(root+'/'+file)
               artist_temp = SetArtist(test)
               album_temp = SetAlbum(test)

               if artist_temp not in ARTIST:
                    ARTIST[artist_temp] = [album_temp,]     

               elif album_temp not in ARTIST[artist_temp]:
                    ARTIST[artist_temp].append(album_temp)
               
               if album_temp in ALBUM:
                   ALBUM[album_temp] += 1
               else:
                   ALBUM[album_temp] = 1
              

def SetAlbum(test):
    album_temp = test.getAlbum()
    if album_temp != None:
        for char in "/\:*?\"<>|":
               if char in album_temp:
                    album_temp = album_temp.replace(char,'')
                
    if album_temp == None or album_temp == '':
            album_temp = "unknown"
    return album_temp

def SetArtist(test):
    artist_temp = test.getArtist()
    if artist_temp != None :     
        for char in "/\:*?\"<>|":
               if char in artist_temp:
                   artist_temp = artist_temp.replace(char,'')
              
    if artist_temp == None or artist_temp == '':
            artist_temp = "unknown"
    return artist_temp
            
    
def Folders(ARTIST,ALBUM,directory):
    try:
        os.mkdir("YourMusic")
    except:
        print "AlreadExists"
        #return

    os.chdir("YourMusic")
    for artist_temp in ARTIST:
        if not os.path.exists(artist_temp):
            os.mkdir(artist_temp)
        os.chdir(artist_temp)
        for album_temp in ARTIST[artist_temp]:
            if not os.path.exists(album_temp):
                os.mkdir(album_temp)
        os.chdir("../")
    os.chdir("../")

    print "Copying Files Now...."
    Copy(ARTIST,ALBUM,directory)
    
        
def Copy(ARTIST,ALBUM,directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
               test = TAG(root+'/'+file)   
               artist_temp = SetArtist(test)
               album_temp = SetAlbum(test)
               shutil.copy(root+'/'+file,"YourMusic/"+artist_temp+"/"+album_temp+"/")

               

def MyFun():
    
    ARTIST = {}
    ALBUM  = {}
    print "Rename your Music Directory to \"Music\" \nDelete any Directory Named \"YourMusic\" \nPress any Key to Continue.."
    raw_input()
    directory = "Music/"
    
            
    IndexSongs(ARTIST,ALBUM,directory)
    Folders(ARTIST,ALBUM,directory)
    print "Youza!"
    raw_input()
    
        

MyFun()
