import os
import re
import shutil
import datetime
from dotenv import load_dotenv
from termcolor import colored

# load .env file
load_dotenv()

dir1 = os.getenv('BASEDIR')
dir2 = os.getenv('TARGETDIR')
acceptedFileAge = int(os.getenv('SET_MINUTES'))

#reusable regex parser for other potential functions
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

class getColoredText:
    dir1Colored = colored(dir1, "green")
    dir2Colored = colored(dir2, "green")
    acceptedFileAgeColored = colored(f"{acceptedFileAge} minutes", "blue")
    noDirColored = colored("NO DIRECTORY FOUND", "red")
    abortColored = colored("ABORTING", "red", "on_grey")

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
        fileAge = datetime.datetime.fromtimestamp(os.path.getmtime(dir1 + self.name))
        now = datetime.datetime.now()   
        delta = str(now - fileAge)
        acceptInterval = str(datetime.timedelta(minutes=acceptedFileAge))
        isCorrectFile = re.search(r'.([mkv|avi|mp4])', self.name)
        fileInfo = [delta, acceptInterval, isCorrectFile]
        return fileInfo

class moveFile(object):

    def __init__(self, newFileName, originalFileName, fileInfo=None):
        try:
            self.newName = newFileName
            self.originalName = originalFileName
            self.fileInfo = fileInfo
        except TypeError:
            print ('Missing parameters :(')

    def getDir(self):
        self.newDir = dir2 + self.newName
        self.newDirColored = colored(self.newDir, "green")
        print(f'Checking file age information - currently set accepted file age is: {getColoredText.acceptedFileAgeColored}...')
        if self.fileInfo:
            if self.fileInfo[2] and self.fileInfo[0] >= self.fileInfo[1]:
                print (f"\nFile is older than {getColoredText.acceptedFileAgeColored}, checking for matching folder in second directory: {getColoredText.dir2Colored}")
                # if dir1 does not exist, a new one will be created with the name of the name of the file
                if not os.path.exists(self.newDir):
                    print (f"\n{getColoredText.noDirColored}: Creating new directory: {self.newDirColored}")
                    # creates new directory with the new file name within dir2
                    os.makedirs(self.newDir)
                return self.newDir
            elif self.fileInfo [2] and self.fileInfo[0] < self.fileInfo[1]:
                print ("\nFile is not old enough - " + getColoredText.abortColored)
                exit() # probably not the best way to exit, but works for now.
        elif self.fileInfo == None:
            print (f"\nWill not be checking file age - checking for matching folder in second directory in: {getColoredText.dir2Colored}")
            if not os.path.exists(self.newDir):
                print (f"\n{getColoredText.noDirColored}: Creating new directory: {self.newDirColored}")
                # creates new directory with the new file name within dir2
                os.makedirs(self.newDir)
            return self.newDir

    def moveToDir(self):
        newDir = self.getDir()
        originalNameColored = colored(self.originalName, "green")
        print (f"\n>> Found match - moving file: {originalNameColored} \n\n>> From directory: {getColoredText.dir1Colored} \n\n>> To target directory: {self.newDirColored}")
        print('―' * 100)  # U+2015, Horizontal Bar
        os.chdir(dir2)
        shutil.move(dir1 + self.originalName, newDir + "/" + self.originalName)
