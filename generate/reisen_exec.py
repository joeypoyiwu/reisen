import os, re, sys
import configparser
import shutil
import datetime

config = configparser.ConfigParser()
configPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

config.read(configPath)

dir1 = config['DIRECTORIES']['BASE_DIR']
dir2 = config['DIRECTORIES']['TARGET_DIR']

# dir1 = 'D:\Users\Joey\Documents\Temp\videos\\'
# dir2 = 'D:\Users\Joey\Documents\Temp\newvideos\\'

os.chdir(dir1)

arr = os.listdir(dir1)

for fname in arr:
    print (fname)
    rname = fname.replace("_", " ")
    rname = re.sub(r'([\(\[][\d\-\w\s~]*[\)\]])', '', rname)
    rname = re.sub(r'\.[avi|mkv|mp4]*', '', rname).strip()
    rname = re.sub(r'( - [\w\d]*\Z)', "", rname)
    print (rname)
    matchedGroup = re.match(r'([\w\W]*)', rname)
    print (matchedGroup.group(1))
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

