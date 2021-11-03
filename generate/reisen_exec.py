import os, re, sys
import configparser
import shutil
import datetime

config = configparser.ConfigParser()
configPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

config.read(configPath)

dir1 = config['DIRECTORIES']['BASE_DIR']
dir2 = config['DIRECTORIES']['TARGET_DIR']

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

os.chdir(dir1)

arr = os.listdir(dir1)

for fname in arr:
    rname = fname.replace("_", " ")
    removeBrackets = re.sub(regexPatterns.removeBrackets, '', rname)
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
    matchedGroup = re.match(regexPatterns.matchFile, removeAsciiFuckery)
    fileAge = datetime.datetime.fromtimestamp(os.path.getmtime(dir1 + fname))
    now = datetime.datetime.now()
    delta = now - fileAge
    acceptInterval = datetime.timedelta(minutes=30)
    isCorrectFile = re.search(r'.([mkv|avi|mp4])', fname)

    if isCorrectFile and delta >= acceptInterval:
        print ("Matched Group: " + str(matchedGroup.group(1)))
        newName = str(matchedGroup.group(1))
        print ("newName: " + newName)
        if not os.path.exists(dir2 + newName):
            print (dir2 + newName)
            os.makedirs(dir2 + newName)
        print ("Found match, " + str(fname) +  " moving to target dir: " + newName)
        os.chdir(dir2)
        shutil.move(dir1 + fname, dir2 + newName + "/" + fname)

