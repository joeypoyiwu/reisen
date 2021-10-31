from os import rename
from newAnimeEpisodes import *
import click

os.chdir(dir1)
initialDir = os.listdir(dir1) 

@click.command()
@click.option('--parse', default=False, is_flag=True, help='Will parse the filenames for files in a given directory via regex. The parser will remove any brackets and characters within the brackets, replace underscores with spaces, and remove any dash charcters (-) and charcters following the dash. This will not rename the file.')
@click.option('--age', default=False, is_flag=True, help='Checks file age and compares it to a specified accepted time interval set by `acceptedFileAge`')
@click.option('--move', default=False, is_flag=True, help='Moves the file in a directory to another directory that is specified.')

def organizeFiles(parse, age, move):
    for originalFileName in initialDir:
        if parse and age and move: 
            newFileName = parsedFilename(str(originalFileName)).parse()
            fileInfo = checkAge(originalFileName).check()
            runFileActions = moveFile(str(newFileName), str(originalFileName), fileInfo)
            runFileActions.moveToDir()
        elif parse and move:
            fileInfo = None
            newFileName = parsedFilename(str(originalFileName)).parse()
            runFileActions = moveFile(str(newFileName), str(originalFileName), fileInfo)
            runFileActions.moveToDir()
        else:
            click.echo('Missing arguments in command line - please review with --help to check what options are available.')
            return

if __name__ == '__main__':
    organizeFiles()