import click
from app.newAnimeEpisodes import *

@click.command()
@click.option('--parse', default=False, is_flag=True, required=True, help='Will parse the filenames for files in a given directory via regex. The parser will remove any brackets and characters within the brackets, replace underscores with spaces, and remove any dash charcters (-) and charcters following the dash. This will not rename the file.')
@click.option('--age', default=False, is_flag=True, required=False, help='Checks file age and compares it to a specified accepted time interval set by `acceptedFileAge`')
@click.option('--move', default=False, is_flag=True, required=True, help='Moves the file in a directory to another directory that is specified.')

def organize(parse, age, move):
    baseDir = click.prompt('Enter the directory you want to move FROM', type = str)
    targetDir = click.prompt('\nEnter the directory you want to move TO', type = str)
    initialDir = os.listdir(baseDir)

    if parse and age and move:
        setMinutes = click.prompt('\nEnter the amount of minutes you want the file age to be before parsing and moving', type = int)
        for originalFileName in initialDir:  
            newFileName = parsedFilename(str(originalFileName)).parse()
            fileInfo = checkAge(originalFileName, setMinutes, baseDir).check()
            runFileActions = moveFile(str(newFileName), str(originalFileName), baseDir, targetDir, fileInfo)
            runFileActions.moveToDir()
    elif parse and move and not age:
        for originalFileName in initialDir:  
            fileInfo = None
            newFileName = parsedFilename(str(originalFileName)).parse()
            runFileActions = moveFile(str(newFileName), str(originalFileName), baseDir, targetDir, fileInfo)
            runFileActions.moveToDir()
    else:
        click.echo(f'{colorText("ERROR")[2]}: Missing arguments in command line - please review with --help to check what options are available.')
        return