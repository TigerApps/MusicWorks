import os
import id3reader
import shutil

class TAG(object):
    def __init__(self,file_path):
##        file = open(file_name,'r')  
##        file.seek(-128, 2)
##        self.tag = file.read(128)
##        self.Title = self.tag[3:33].strip()
##        self.Artist = self.tag[33:63].strip()
##        self.Album = self.tag[63:93].strip()
##        self.Year = self.tag[93:97].strip()
##        self.Comment = self.tag[97:127].strip()
##        self.Genre = self.tag[127].strip()

        id3r = id3reader.Reader(file_path)
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
   

                            
def IndexSongs(ARTIST,Artists,ALBUM,directory,NotDone):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
               print root+'/'+file

               try:
                   test = TAG(root+'/'+file)
               except:
                   NotDone.append(root+'/'+file)
                   continue
                
               artist_temp = SetArtist(test)
               album_temp = SetAlbum(test)

               if artist_temp not in ARTIST:
                    ARTIST[artist_temp] = [album_temp,]
                    Artists[artist_temp] = 1
               elif album_temp not in ARTIST[artist_temp]:
                    ARTIST[artist_temp].append(album_temp)
                    Artists[artist_temp] += 1
               else: 
                    Artists[artist_temp] += 1
               
               if album_temp in ALBUM:
                   ALBUM[album_temp] += 1
               else:
                   ALBUM[album_temp] = 1
              

def SetAlbum(test):
    album_temp = test.getAlbum()
    if album_temp != None:
        for char in "./\:*?\"<>|":
               if char in album_temp:
                    album_temp = album_temp.replace(char,'')
                
    if album_temp == None or album_temp == '':
            album_temp = "unknown"
    album_temp = album_temp.strip()
    return album_temp

def SetArtist(test):
    artist_temp = test.getArtist()
    if artist_temp != None :     
        for char in "./\:*?\"<>|":
               if char in artist_temp:
                   artist_temp = artist_temp.replace(char,'')
              
    if artist_temp == None or artist_temp == '':
            artist_temp = "unknown"
    artist_temp = artist_temp.strip()
    return artist_temp
            
    
def Folders(ARTIST,Artists,ALBUM,directory,NotDone):
    

    os.chdir("YourMusic")
    for artist_temp in ARTIST:
        if Artists[artist_temp] > 4:   
            if not os.path.exists(artist_temp):
                os.mkdir(artist_temp)
            os.chdir(artist_temp)
            for album_temp in ARTIST[artist_temp]:
                if ALBUM[album_temp] > 5 and album_temp != "unknown":
                    if not os.path.exists(album_temp):
                        os.mkdir(album_temp)
            os.chdir("../")
    os.chdir("../")

    print "Copying Files Now...."
    Copy(ARTIST,Artists,ALBUM,directory,NotDone)
    
        
def Copy(ARTIST,Artists,ALBUM,directory,NotDone):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3"):
               artist_temp = None
               album_temp = None
               sFile = (root+'/'+file)

               try:
                   test = TAG(sFile)
               except:
                   continue
                
               artist_temp = SetArtist(test)
               album_temp = SetAlbum(test)

              
               if Artists[artist_temp] > 4:                   
                   if ALBUM[album_temp] > 5 and album_temp != "unknown":
                        try:
                            shutil.copy(sFile,"YourMusic/"+artist_temp+"/"+album_temp+"/")
                        except:
                            NotDone.append(sFile)
                            continue
                   else:
                        try:
                            shutil.copy(sFile,"YourMusic/"+artist_temp+"/")
                        except:
                            NotDone.append(sFile)
                            continue
               else:
                    os.chdir("YourMusic")
                    if not os.path.exists("Random"):
                        os.mkdir("Random")
                    os.chdir("../")
                    
                    try:
                        shutil.copy(sFile,"YourMusic/Random/")
                    except:
                        NotDone.append(sFile)
                        continue
                   
               

def MyFun():
    
    ARTIST = {}
    Artists = {}
    ALBUM  = {}
    NotDone = []
    print "Rename your Music Directory to \"Music\" \nDelete any Directory Named \"YourMusic\" \nPress any Key to Continue.."
    raw_input()
    directory = "Music/"

    try:
        os.mkdir("YourMusic")
    except:
        print "AlreadExists"
        #return
            
    IndexSongs(ARTIST,Artists,ALBUM,directory,NotDone)
    Folders(ARTIST,Artists,ALBUM,directory,NotDone)
    print "Youza!"
    
    
    if len (NotDone) > 0:
        print "NotDoneList Created!"
        outFile = open("NotDoneList.txt",'w')
        for path in NotDone:
            outFile.write(path+"\n")

    raw_input("\nPress any Key to End\n")
    
        

MyFun()
