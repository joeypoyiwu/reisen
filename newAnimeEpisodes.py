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

class colorText:
    def __init__(self, arg: str):
        self.arg = arg
    def __new__(cls, arg):
        greenText = colored(str(arg), "green")
        blueText = colored(str(arg), "blue")
        redText = colored(str(arg), "red")
        yellowText = colored(str(arg) , "yellow")
        return [greenText, blueText, redText, yellowText]

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
        # self.newDirColored = colored(self.newDir, "green")
        print(f'Checking file age information - currently set accepted file age is: {colorText(acceptedFileAge)[1]}...')
        if self.fileInfo:
            if self.fileInfo[2] and self.fileInfo[0] >= self.fileInfo[1]:
                print (f"\nFile is older than {colorText(acceptedFileAge)[1]} minutes. \nChecking for matching folder in second directory: {colorText(dir2)[1]}")
                # if dir1 does not exist, a new one will be created with the name of the name of the file
                if not os.path.exists(self.newDir):
                    print (f"\n{colorText('NO DIRECTORY FOUND')[2]}: Creating new directory: {colorText(self.newDir)[0]}")
                    # creates new directory with the new file name within dir2
                    os.makedirs(self.newDir)
                return self.newDir
            elif self.fileInfo [2] and self.fileInfo[0] < self.fileInfo[1]:
                print ("\nFile is not old enough - " + colorText('ABORTING')[2])
                exit() # probably not the best way to exit, but works for now.
        elif self.fileInfo == None:
            print (f"\nWill not be checking file age - checking for matching folder in second directory in: {colorText(dir2)[1]}")
            if not os.path.exists(self.newDir):
                print (f"\n{colorText('NO DIRECTORY FOUND')[2]}: Creating new directory: {colorText(self.newDir)[0]}")
                # creates new directory with the new file name within dir2
                os.makedirs(self.newDir)
            return self.newDir

    def moveToDir(self):
        newDir = self.getDir()
        print (f"\n>> Found match - moving file: {colorText(self.originalName)[0]} \n\n>> From directory: {colorText(dir1)[0]} \n\n>> To target directory: {colorText(self.newDir)[0]}")
        print('―' * 100)  # U+2015, Horizontal Bar
        os.chdir(dir2)
        shutil.move(dir1 + self.originalName, newDir + "/" + self.originalName)
