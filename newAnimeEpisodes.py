import os
import re
import shutil
import datetime

# directory is the initial directory the video will be downloaded to
# directory2 is the directory to move the video to

directory = r"D:\Users\Joey\Documents\Temp\videos\\" # enter directory to move from
directory2 = r"D:\Users\Joey\Documents\Temp\newvideos\\" # enter directory to move to
acceptedFileAge = 10 # unit is in minutes

def regex_decorator(function):
    def wrapper(arg1):
        func = function(arg1) # pass in string as argument
        fileNameReplaceWithSpace = func.replace("_", " ")
        removeBrackets = re.sub(r'([\(\[][\d\-\w\s~]*[\)\]])', '', fileNameReplaceWithSpace)
        removeFileExtension = re.sub(r'\.[avi|mkv|mp4]*', '', removeBrackets).strip()
        removeDashAndFollowingText = re.sub(r'( - [\w\d]*\Z)', "", removeFileExtension)
        renamedFilename = re.match(r'([\w\W]*)', removeDashAndFollowingText)
        return renamedFilename.group(1) # returns string matched by re
    return wrapper

class parsedFilename:
    def __init__(self, fileName):
        self.name = fileName

    # will return parsed file name with underscores replaced with spaces, no brackets, no dashes ('-'), and no text following the dashes.
    @regex_decorator
    def parse(self):
        return str(self.name)

class checkAge(object):
    def __init__(self, originalFileName):
        self.name = originalFileName

    def check(self):
        fileAge = datetime.datetime.fromtimestamp(os.path.getmtime(directory + self.name))
        now = datetime.datetime.now()   
        delta = str(now - fileAge)
        acceptInterval = str(datetime.timedelta(minutes=acceptedFileAge))
        isCorrectFile = re.search(r'.([mkv|avi|mp4])', self.name)
        fileInfo = [delta, acceptInterval, isCorrectFile]
        return fileInfo


class moveFile(object):
    def __init__(self, fileInfo, newFileName, originalFileName):
        try:
            self.newName = newFileName
            self.originalName = originalFileName
            self.fileInfo = fileInfo
        except TypeError:
            print ('Missing parameters :(')

    def getDir(self):
        newDir = directory2 + self.newName
        #checks to see if the values of `isCorrectFile` and `delta` is greater than or equal to the value of `acceptInterval`
        if self.fileInfo[2] and self.fileInfo[0] >= self.fileInfo[1]:
            print ("New File Name: " + self.newName)
            # if directory does not exist, a new one will be created with the name of the name of the file
            if not os.path.exists(newDir):
                print (newDir)
                # creates new directory with the new file name within directory2
                os.makedirs(newDir)
            return newDir
        else:
            return newDir
        
    def moveToDir(self):
        newDir = self.getDir()
        print ("Found match: {}, moving to target dir: {}".format(self.originalName, newDir))
        os.chdir(directory2)
        shutil.move(directory + self.originalName, newDir + "/" + self.originalName)
