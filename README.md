# Reisen-CLI

This repository hosts two scripts that are meant to be used for the purposes of organizing video files in the format of:

`[FansubGroup] Anime Title/Movie - 00 (1080p) [123ABC].mkv/avi/mp4`

It is currently not parsing other patterns explicitly, although there are plans to implement them. Some examples of patterns that don't work create the right directory name are:

```
[Kira-Fansub]Bokurano_04_(DVD_x264_848x480_24fps_AAC) [4E938D1E].mkv
Clannad_Ep07_[1080p,BluRay,x264]_-_THORA_SS-Eclipse.mkv
Darker_Than_Black_Ep05_[720p,BluRay,x264]_-_THORA.mkv
Fate_Stay_Night_Ep05_The_Two_Magi_Part1_[720p,BluRay,x264]_-_THORA.mkv
[Tormaid]_Full_Metal_Panic_FUMOFFU_02_(Blu-Ray_960x720_Dual_Audio_FLAC).mkv
[RUELL-Raws] GUNDAM SEED HDR. EP34 (BD 1920x1080 x264 DualFLAC+ENGSub).mkv
[Coalgirls]_Ga-Rei_Zero_08_(1280x720_Blu-Ray_FLAC)_[8AA522B5].mkv
Genesis_of_Aquarion_-_14_[3xR][Blu-ray.720p.H264.FLAC.AC3]_[8B55E3F6].mkv
[Hiryuu] Maji de Watashi ni Koi Shinasai!! 05 [Hi10P 1280x720 H264] [6AC9A59E].mkv
[Coalgirls]_Toradora_12_(1280x720_H.264_AAC)_[AF2F719F].mkv
aria_the_animation_06[h264.vorbis][niizk].mkv
onegai_teacher_05[h264.vorbis][niizk].mkv
```

The majority of these formats are for older episodes and series - newer series typically follow a very standard format noted above:

`[FansubGroup] Anime Title/Movie - 00 (1080p) [123ABC].mkv/avi/mp4`

## What is the purpose of this?

A very specific, personal use case, one of which I'm hoping to expand more so that it can be useful to anybody for any media format.

For my purposes, I am automating the organization and moving of several media files that are all dumped into one general directory (directory A) with no organization. With the automation, all files matching this format in directory A will be moved to a second directory (directory B), and will create a new directory in directory B to group the video files in if the names are the same. I'm not great at explaining things.

I have my Plex server listening on directory B for metadata purposes. This automation allows me to just specify a source and destination folder and it will do the work for me.

## What does it do?

Both scripts do two things:

1. Looks in a directory for files, and for each file the filename will be parsed via Regex, and then moved to a specified directory. You can also choose not to specify a directory by removing the variable `destination` and rename files in bulk in one directory, but #2 will not apply.
2. When moving the file, the script will check to see the age of the file and if it's at least 10 minutes old. After it checks the file is more than 10 minutes old, it will then check if there exists a directory the specified directory (`destination`). If it exists, the script will move the file over to the matching directory name as the filename. If a directory with the same title as the filename does not exist, the script will create a new directory in the specified directory (`destination`), and move it there. 

To download and use, you can install it via:
`pip install reisen`

### Demo

![anime-mover](https://i.imgur.com/8tcTbxw.gif)

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
