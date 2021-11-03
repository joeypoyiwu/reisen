import os
import re
import shutil
import datetime
from termcolor import colored

#I'm no regex expert, so to double check, you can use regex101.com
class regexPatterns:
    removeBrackets = r'\[(.*?)\]' # removes brackets and its contents
    removeParantheses = r'([\(\[][\d\-\w\s~]*[\)\]])' # removes parantheses and its contents
    removeFileExtensions = r'\.[avi|mkv|mp4]*' # removes file extensions matching the ones given
    removeDash = r'( - [\w\d]*\Z)' # removes dashes and any text following it
    removeDigitsTrailingDash = r'( - [\w\d]{1,3})' # same thing as removeDash, but with a quantifier
    removeRemainingDashes = r'-$' # removes any dashes remaining
    removeUnicodeDashes = r'([\u2010-\uFF0D] [\d]*)' # removes any funky dashes that are encoded differently
    removeEpWithDigits = r'[eE][pP]\d{1,2}' # removes any string that are eP/Ep/ep/EP and any numbers following
    removeEp = r'\d{1,3}$' # removes episode number
    removeWhitespace = r'[ \t]+$' # removes white spaces at the end of the line just in case
    removeWeirdFormatting = r' \S+(?=\((.*?)\)$)\((.*?)\)$' # don't really have a better name for this - removes weird paranthese formatting
    matchFile = r'([\w\W]*)' # will use re.match and get new file name

#reusable regex parser for other potential functions
def regex_decorator(function):
    def wrapper(arg1):
        func = function(arg1) # pass in string as argument
        fileNameReplaceWithSpace = func.replace("_", " ")
        removeBrackets = re.sub(regexPatterns.removeBrackets, '', fileNameReplaceWithSpace)
        removeParantheses = re.sub(regexPatterns.removeParantheses, '', removeBrackets)
        removeFileExtension = re.sub(regexPatterns.removeFileExtensions, '', removeParantheses).strip()
        removeDash = re.sub(regexPatterns.removeDash, '', removeFileExtension)
        removeDigitsTrailingDash = re.sub(regexPatterns.removeDigitsTrailingDash, '', removeDash)
        removeRemainingDashes = re.sub(regexPatterns.removeRemainingDashes, '', removeDigitsTrailingDash)
        removeUnicodeDashes = re.sub(regexPatterns.removeUnicodeDashes, '', removeRemainingDashes)
        removeEpWithDigits = re.sub(regexPatterns.removeEpWithDigits, '', removeUnicodeDashes)
        removeEp = re.sub(regexPatterns.removeEp, '', removeEpWithDigits)
        removeWhitespace = re.sub(regexPatterns.removeWhitespace, '', removeEp)
        removesWeirdFormatting = re.sub(regexPatterns.removeWeirdFormatting, '', removeWhitespace)
        removeAsciiFuckery = removesWeirdFormatting.encode("ascii", "ignore").decode("utf-8")
        renamedFilename = re.match(regexPatterns.matchFile, removeAsciiFuckery)
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
    def __init__(self, originalFileName, setMinutes, source):
        self.name = originalFileName
        self.setMinutes = setMinutes
        self.source = source + "/"

    def check(self):
        fileAge = datetime.datetime.fromtimestamp(os.path.getmtime(self.source + self.name))
        now = datetime.datetime.now()   
        delta = now - fileAge
        acceptInterval = datetime.timedelta(minutes=self.setMinutes)
        isCorrectFile = re.search(r'.([mkv|avi|mp4])', self.name)
        fileInfo = [delta, acceptInterval, isCorrectFile]
        return fileInfo

class moveFile(object):

    def __init__(self, newFileName, originalFileName, source, destination, fileInfo=None):
        try:
            self.newName = newFileName
            self.originalName = originalFileName
            self.destination = destination + "/"
            self.source = source + "/"
            self.fileInfo = fileInfo
        except TypeError:
            print ('Missing parameters :(')

    def getDir(self):
        self.newDir = self.destination + self.newName + "/"
        if self.fileInfo is not None:
            print(f'\nChecking file age information - currently set accepted file age is: {colorText(self.fileInfo[1])[1]} minutes')
            if self.fileInfo[2] and self.fileInfo[0] >= self.fileInfo[1]:
                print (f"\nFile {colorText(self.originalName)[0]} is older than {colorText(self.fileInfo[1])[1]} minutes. \n\nChecking for matching folder in second directory: {colorText(self.destination)[1]}")
                # if dir1 does not exist, a new one will be created with the name of the name of the file
                if not os.path.exists(self.newDir):
                    print (f"\n{colorText('NO DIRECTORY FOUND')[2]}: Creating new directory: {colorText(self.newDir)[1]}/")
                    # creates new directory with the new file name within dir2
                    os.makedirs(self.newDir + "/")
                return self.newDir
            elif self.fileInfo [2] and self.fileInfo[0] < self.fileInfo[1]:
                print ("\nFile is not old enough - " + colorText('ABORTING')[2])
                exit() # probably not the best way to exit, but works for now.
        elif self.fileInfo == None:
            print (f"\nWill not be checking file age - checking for matching folder in second directory in: {colorText(self.destination)[1]}")
            if not os.path.exists(self.newDir):
                print (f"\n{colorText('NO DIRECTORY FOUND')[2]}: Creating new directory: {colorText(self.newDir)[0]}")
                # creates new directory with the new file name within dir2
                os.makedirs(self.newDir + "/")
            return self.newDir

    def moveToDir(self):
        newDir = self.getDir() + "/"
        print (f"\n>> Found match - moving file: {colorText(self.originalName)[0]} \n\n>> From directory: {colorText(self.source)[0]} \n\n>> To target directory: {colorText(self.newDir)[0]}")
        print('―' * 100)  # U+2015, Horizontal Bar
        os.chdir(self.destination + "/")
        shutil.move(self.source + self.originalName, newDir + self.originalName)
