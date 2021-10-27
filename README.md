# anime-video-file-rename-and-mover

This repository hosts two scripts that are meant to be used for the purposes of organizing video files in the format of:

`[FansubGroup] Anime Title/Movie - 00 [123ABC].mkv/avi/mp4`

## What does it do?

Both scripts do two things:

1. Looks in a directory for files, and for each file the filename will be renamed via Regex, and then moved to a specified directory. You can also choose not to specify a directory by removing the variable `directory2` and rename files in bulk in one directory, but #2 will not apply.
2. When moving the file, the script will check to see the age of the file and if it's at least 10 minutes old. After it checks the file is more than 10 minutes old, it will then check if there exists a directory the specified directory (`directory2`). If it exists, the script will move the file over to the matching directory name as the filename. If a directory with the same title as the filename does not exist, the script will create a new directory in the specified directory (`directory2`), and move it there. 

To download and use, you can clone this repo and run the task on demand, or on a cron job or task scheduler if you're on Windows.

## How can I configure it?

### Changing the file age timer

You can change the variable `fileAge` to any integer of your choosing in minutes like such:

For waiting until the accepted time to wait before renaming & moving the file is 30 minutes long, change `fileAge` to:

`fileAge = 30`

## TODO 

### No Second Directory

Code currently does not support a good and easy way to specify not using a second directory without making more than a few lines of correction. Future improves include writing logic to check on the existence of a second directory variable and if it's specified, and then running specific code to execute.

And no, I am not good at naming repositories.