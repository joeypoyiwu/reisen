import click
import configparser
from pathlib import Path
import subprocess
import shutil, os
import platform
from app.newAnimeEpisodes import colorText

@click.command()
@click.option('--source', required=True, type=str, help='Enter path of directory to move from')
@click.option('--destination', required=True, type=str, help='Enter path of directory to move to')
@click.option('--exe', required=True, type=str, help='Enter path of directory for the executable to be placed')

def generate(source, destination, exe):
    '''
    Generate an executable file with user specified directories, which uses a modified script to run the equivalent of `reisen organize`. 
    
    
    This is useful if you would like to run the task automatically through Windows Task Scheduler.
    '''
    if source and destination and exe:
        source = Path.home().joinpath(source)
        destination = Path.home().joinpath(destination)
        exe = Path.home().joinpath(exe)

        config = configparser.ConfigParser()
        config.optionxform = str
        fileDir = Path(__file__).parent.absolute() # gets current directory of this script
        filePath = fileDir.joinpath('reisen_exec.py') # gets path of reisen_exec.py to move
        reisenPath = exe.joinpath('reisen_exec')
        execPath = reisenPath.joinpath('dist')

        if Path.is_dir(reisenPath):
            shutil.copy(filePath, reisenPath) # should move reisen_exec.py to current dir of user
        else:
            os.mkdir(reisenPath) # creates folder in current directory, e.g. C:/Users/John/reisen_exec
            shutil.copy(filePath, reisenPath) # should move reisen_exec.py to current dir of user

        dirsFile = Path(str(reisenPath) + '/config.ini') # creates file config.ini in current directory where the reisen got called
        dirsFile.touch(exist_ok=True)
        config.read(dirsFile)
        if config.has_section('DIRECTORIES'):
            config.set('DIRECTORIES', 'BASE_DIR', str(source) + '\\')
            config.set('DIRECTORIES', 'TARGET_DIR', str(destination) + '\\')
        else:
            config.add_section('DIRECTORIES')
            config.set('DIRECTORIES', 'BASE_DIR', str(source) + '\\')
            config.set('DIRECTORIES', 'TARGET_DIR', str(destination) + '\\')

        with open(dirsFile, 'w') as configFile:
            config.write(configFile)

        os.chdir(reisenPath)
        if dirsFile:
            OS = platform.system()
            if OS == 'Windows':
                subprocess.call(r'pyinstaller --onefile --add-data "config.ini;." reisen_exec.py')
            elif OS == 'Darwin':
                subprocess.call(r'pyinstaller --onefile --add-data "config.ini:." reisen_exec.py')
            click.echo(colorText('\nSUCCESS! ')[0] + f'\n\nSingle file executable built and completed. You can find the executable file here:')
            click.echo(colorText(f'\n{execPath}\n')[1])
        else:
            click.echo(colorText(f'\nMissing {dirsFile}')[2] + ' file. Double check the directory you passed through the option "--exe"')
    else:
        click.echo(f'{colorText("ERROR")[2]}: Missing arguments in command line - please review with --help to check what options are available.\n')
        return
