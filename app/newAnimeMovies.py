# import os
# import re
# import shutil
# import datetime


# # directory is the initial directory the video will be downloaded to
# # directory2 is the directory to move the video to

# directory = "" #enter directory to move from
# directory2 = "" #enter directory to move to
# fileAge = 30 # unit is in minutes
# os.chdir(directory)

# arr = os.listdir(directory)

# print(arr)

# for fname in arr:
#     print (fname)
#     rname = fname.replace("_", " ")
#     matchedGroup = re.match('(?:\[[\w-]*\]) ([~\w\s!\?-]*)(?:\[[\w\-\s]*\])*\.(?:mkv|avi|mp4)', str(rname))
#     fileAge = datetime.datetime.fromtimestamp(os.path.getmtime(directory + fname))
#     now = datetime.datetime.now()
#     delta = now - fileAge
#     acceptInterval = datetime.timedelta(minutes=fileAge)

#     if matchedGroup and delta >= acceptInterval:
#         print ("Matched Group: " + str(matchedGroup.group(1)))
#         epNum = re.search('( - [\d\w]*)', matchedGroup.group(1))
#         print("epNum: " + str(epNum.group(1)))
#         newName = str(matchedGroup.group(1)).replace(str(epNum.group(1)), "")
#         if newName[-1:] == " ":
#             newName = newName[:-1]
#         print ("New Name: " + newName)
#         if not os.path.exists(directory2 + newName):
#             print (directory2 + newName)
#             os.makedirs(directory2 + newName)
#         print ("Found match, " + str(fname) +  " moving to target dir: " + newName)
#         os.chdir(directory2)
#         shutil.move(directory + fname, directory2 + newName + "\\" + matchedGroup.group(0))
        