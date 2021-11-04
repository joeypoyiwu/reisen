from os import path
import click
from glob import glob
from pathlib import Path
from app.newAnimeEpisodes import *

@click.command()
@click.option('--source', required=True, type=str, help='Enter absolute path of directory to move from')
@click.option('--destination', required=True, type=str, help='Enter absolute path of directory to move to')
@click.option('--parse', default=False, is_flag=True, required=True, help='Will parse the filenames for files in a given directory via regex. The parser will remove any brackets and characters within the brackets, replace underscores with spaces, and remove any dash charcters (-) and charcters following the dash. This will not rename the file.')
@click.option('--age', default=False, is_flag=True, required=False, help='Checks file age and compares it to a specified accepted time interval set by `acceptedFileAge`')
@click.option('--move', default=False, is_flag=True, required=True, help='Moves the file in a directory to another directory that is specified.')

def organize(source, destination, parse, age, move):

    '''
    Organizes media files in one directory to another directory.
    
    
    Reisen will look for a matching directory with a parsed name of the filenames in the base directory.
    
    
    Reisen will then either move the file if there is a match, or create a directory and then move the file.
    '''
    types = ('.avi', '.mkv', '.mp4')
    initialDir = os.listdir(source)
    initialDirGlob = glob(str(source) + '/**/', recursive=True)

    if parse and age and move:
        setMinutes = age
        if not initialDir:
            click.echo(colorText(f'ERROR: ')[2] + 'Empty directory. Please double check that you specified the right path. \n')
        else:
            for dir in initialDirGlob:
                filePath = os.listdir(dir)
                for originalFileName in filePath:
                    if os.path.isdir(source + '/' + originalFileName)==False and not originalFileName.endswith( types ):
                        click.echo(colorText(f'\nERROR: ')[2] + f'Found file that does not end in file types: ')
                        click.echo(colorText(f'{types}')[1] + '\n')
                        click.echo(f'Skipping file: ' + colorText(f'{originalFileName}')[1] + '\n')
                        click.echo('―' * 100)  # U+2015, Horizontal Bar
                    elif originalFileName.endswith( types ):
                        newFileName = parsedFilename(str(originalFileName)).parse()
                        fileInfo = checkAge(originalFileName, setMinutes, dir).check()
                        runFileActions = moveFile(str(newFileName), str(originalFileName), dir, destination, fileInfo)
                        runFileActions.moveToDir()
                    elif os.path.isdir(source + '/' + originalFileName)==True and len(os.listdir(source + '/' + originalFileName)) == 0:
                        click.echo(colorText(f'\nWARNING: ')[2] + f'Found objects that are not video files or empty directories in: ')
                        click.echo(colorText(f'\n{source}\n')[0])
                        click.echo(f'Files or folders in question: ' + colorText(source + '/' + originalFileName)[1] + '\n      ')
                        click.echo("Please double check your specified base directory and remove any files and/or empty directories that are not video files that match: ")
                        click.echo(colorText(f'{types}')[1] + '\n')
                        click.echo('―' * 100)  # U+2015, Horizontal Bar
    elif parse and move and not age:
        if not initialDir:
            click.echo(colorText(f'ERROR: ')[2] + 'Empty directory. Please double check that you specified the right path. \n')
        else:
            for dir in initialDirGlob:
                filePath = os.listdir(dir)
                for originalFileName in filePath:
                    fileInfo = None
                    if os.path.isdir(source + '/' + originalFileName)==False and not originalFileName.endswith( types ):
                        click.echo(colorText(f'\nERROR: ')[2] + f'Found file that does not end in file types: ')
                        click.echo(colorText(f'{types}')[1] + '\n')
                        click.echo(f'Skipping file: ' + colorText(f'{originalFileName}')[1] + '\n')
                        click.echo('―' * 100)  # U+2015, Horizontal Bar
                    elif originalFileName.endswith( types ):
                        newFileName = parsedFilename(str(originalFileName)).parse()
                        runFileActions = moveFile(str(newFileName), str(originalFileName), dir, destination, fileInfo)
                        runFileActions.moveToDir()
                    elif os.path.isdir(source + '/' + originalFileName)==True and len(os.listdir(source + '/' + originalFileName)) == 0:
                        click.echo(colorText(f'\nWARNING: ')[2] + f'Found objects that are not video files or empty directories in: ')
                        click.echo(colorText(f'\n{source}\n')[0])
                        click.echo("Please double check your specified base directory and remove any files and/or empty directories that are not video files that match: ")
                        click.echo(colorText(f'{types}')[1] + '\n')
                        click.echo('―' * 100)  # U+2015, Horizontal Bar
    elif parse and not move and not age:
        click.echo(f'{colorText("ERROR")[2]}: Missing option flag {colorText("--move")[2]}.\n ')
    elif move and not parse and not age:
        click.echo(f'{colorText("ERROR")[2]}: Missing option flag {colorText("--parse")[2]}.\n ')
    elif source or destination==None:
        click.echo(f'{colorText("ERROR")[2]}: Missing parameters in options for {colorText("--source")[2]} and {colorText("--destination")[2]}. \n\nMake sure if you specify something with "--" you also pass a value. Check {colorText("--help")[1]} or {colorText("-h")[1]} for help.\n')
    else:
        click.echo('WAAAAAAAAAAAAAAAAACK')