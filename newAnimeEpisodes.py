import os
import re
import shutil
import datetime

# directory is the initial directory the video will be downloaded to
# directory2 is the directory to move the video to

directory = "" #enter directory to move from
directory2 = "" #enter directory to move to
fileAge = 10 # unit is in minutes
os.chdir(directory)

arr = os.listdir(directory) 

print(arr)

for fname in arr:
    print (fname) #sanity check
    # regex magic below - removes any bracket characters, file extension names common within fansub media files, and replaces underscores with space.
    rname = fname.replace("_", " ")
    rname = re.sub(r'([\(\[][\d\-\w\s~]*[\)\]])', '', rname)
    rname = re.sub(r'\.[avi|mkv|mp4]*', '', rname).strip()
    rname = re.sub(r'( - [\w\d]*\Z)', "", rname)
    print (rname)
    matchedGroup = re.match(r'([\w\W]*)', rname)
    print (matchedGroup.group(1))
    # records how old the file is & compares the age of the file to the specified accepted interval in `acceptInterval` before renaming the file and moving it
    fileAge = datetime.datetime.fromtimestamp(os.path.getmtime(directory + fname))
    now = datetime.datetime.now()
    delta = now - fileAge
    acceptInterval = datetime.timedelta(minutes=fileAge)
    isCorrectFile = re.search(r'.([mkv|avi|mp4])', fname)

    if isCorrectFile and delta >= acceptInterval:
        print ("Matched Group: " + str(matchedGroup.group(1)))
        newName = str(matchedGroup.group(1))
        print ("New Name: " + newName)
        # if directory does not exist, a new one will be created with the name of the name of the file
        if not os.path.exists(directory2 + newName):
            print (directory2 + newName)
            os.makedirs(directory2 + newName)
        print ("Found match, " + str(fname) +  " moving to target dir: " + newName)
        os.chdir(directory2)
        shutil.move(directory + fname, directory2 + newName + "/" + fname)
        