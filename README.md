# Reisen-CLI

This repository hosts two scripts that are meant to be used for the purposes of organizing video files in the format of:

`[FansubGroup] Anime Title/Movie - 00 [123ABC].mkv/avi/mp4`

## What does it do?

Both scripts do two things:

1. Looks in a directory for files, and for each file the filename will be parsed via Regex, and then moved to a specified directory. You can also choose not to specify a directory by removing the variable `TARGETDIR` and rename files in bulk in one directory, but #2 will not apply.
2. When moving the file, the script will check to see the age of the file and if it's at least 10 minutes old. After it checks the file is more than 10 minutes old, it will then check if there exists a directory the specified directory (`TARGETDIR`). If it exists, the script will move the file over to the matching directory name as the filename. If a directory with the same title as the filename does not exist, the script will create a new directory in the specified directory (`TARGETDIR`), and move it there. 

To download and use, you can clone this repo and run the task on demand, or on a cron job or task scheduler if you're on Windows.

### Demo

![anime-mover](https://i.imgur.com/3K9NSNs.gif)

## How can I configure it?

Change the name of the `.env_template` file to `.env`, and fill out desired parameters.

### Changing the file age timer

You can change the variable `SET_MINUTES` in the `.env_template` file to any integer of your choosing in minutes.

For example - to set the accepted time to wait before parsing & moving the file is 30 minutes long, change `SET_MINUTES` to:

`SET_MINUTES = 30`

## TODO 

### Make Second Directory Optional

Code currently does not support a good and easy way to specify not using a second directory without making more than a few lines of correction. Future improves include writing logic to check on the existence of a second directory variable and if it's specified, and then running specific code to execute.

### Refactor `newAnimeMovies.py`

Change code to use classes similar to `newAnimeEpisodes.py`. Or remove it altogether - it's currently not being used at all.

### Refactor `colorText` class

I'm pretty sure this can be done way better than the way I have this written and implemented.

### Add tests

Write stub tests to assert output

### Add automated CI/CD

Plan is to use Jenkins

### Add logic to output message if no files are in directories

Currently there is nothing in place to notify the user in the case that there is nothing in the directory
