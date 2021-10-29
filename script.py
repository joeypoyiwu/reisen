from newAnimeEpisodes import *

os.chdir(directory)

initialDir = os.listdir(directory) 

for originalFileName in initialDir:
    newFileName = parsedFilename(str(originalFileName)).parse()
    fileInfo = checkAge(originalFileName).check()
    runFileActions = moveFile(fileInfo, str(newFileName), str(originalFileName))
    runFileActions.moveToDir()