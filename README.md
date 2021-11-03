# Reisen-CLI

This repository hosts two scripts that are meant to be used for the purposes of organizing video files in the format of:

`[FansubGroup] Anime Title/Movie - 00 (1080p) [123ABC].mkv/avi/mp4`

It is currently not parsing other patterns explicitly, although there are plans to implement them. Some examples of patterns that don't work create the right directory name are:

```
[Mezashite] Aikatsu! ‒ 101 [6936887B].mkv
Darker_Than_Black_Ep14_[720p,BluRay,x264]_-_THORA.mkv
[Hiryuu] Maji de Watashi ni Koi Shinasai!! 05 [Hi10P 1280x720 H264] [6AC9A59E].mkv
[ANBU-Frostii]_Tokyo_Magnitude_8_-_01_-_[720p][E5C69941].mkv
[B-G_&_w.0.0.f]_Shigofumi_01.DVD(H.264_DD2.0)_[E6F70A9A].mkv
[Scum] Nanatsu no Bitoku - 03 [WEB+TV][2610F90B].mkv
```

## What is the purpose of this?

A very specific, personal use case, one of which I'm hoping to expand more so that it can be useful to anybody for any media format.

For my purposes, I am automating the organization and moving of several media files that are all dumped into one general directory (directory A) with no organization. With the automation, all files matching this format in directory A will be moved to a second directory (directory B), and will create a new directory in directory B to group the video files in if the names are the same. I'm not great at explaining things.

I have my Plex server listening on directory B for metadata purposes. This automation allows me to just specify a source and destination folder and it will do the work for me.

## What does it do?

Both scripts do two things:

1. Looks in a directory for files, and for each file the filename will be parsed via Regex, and then moved to a specified directory. You can also choose not to specify a directory by removing the variable `destination` and rename files in bulk in one directory, but #2 will not apply.
2. When moving the file, the script will check to see the age of the file and if it's at least 10 minutes old. After it checks the file is more than 10 minutes old, it will then check if there exists a directory the specified directory (`destination`). If it exists, the script will move the file over to the matching directory name as the filename. If a directory with the same title as the filename does not exist, the script will create a new directory in the specified directory (`destination`), and move it there. 

To download and use, you can install it via:
`pip install --extra-index-url https://test.pypi.org/simple/ reisen`

### Demo

![anime-mover](https://i.imgur.com/3K9NSNs.gif)

## How do I run it??

Run `reisen -h` or `reisen --help` to get started.

### Commands

#### `reisen organize` 

`reisen organize` will move files in a directory to another directory. It will also check against the directory it is moving files to to see if there is a folder name mathcing the title name of the filename.

`reisen organize` will also require at least both options `--parse` and `--move`. The option `--age` is option.

### `reisen generate`

`reisen generate` will generate an executable file via `pyinstaller` that can be run as a regular executable.

This is useful if you would like to automate the task `reisen organize` on Windows Task Scheduler.

## TODO 

### Make destination directory optional

Code currently does not support a good and easy way to specify not using a second directory without making more than a few lines of correction. Future improves include writing logic to check on the existence of a second directory variable and if it's specified, and then running specific code to execute.

### Add logging

Would be nice to log output to a file as well. Helps if running the executable on an automatic job.

### Add more regex to parse more patterns

Currently limited by a fairly specific format, so its usefulness isn't very high right now, but it's getting there.

### Refactor `colorText` class

I'm pretty sure this can be done way better than the way I have this written and implemented.

### Add tests

Write stub tests to assert output

### Add automated CI/CD

Plan is to use Jenkins

### Add logic to output message if no files are in directories

Currently there is nothing in place to notify the user in the case that there is nothing in the directory
