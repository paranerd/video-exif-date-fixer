# Video EXIF Date Editor

This fixes an issue in Synology Photos where videos would end up with the wrong date caused by changing timezones and thus breaking media timelines.



## Prerequisites

Exiftool needs to be installed.

## Usage

`python3 main.py [path-to-video-files] [timezone-delta]`

## Example

A video file recorded at 2024:01:01_18:00:00 fixed with a delta of -5 will end up as 2024:01:01_13:00:00-05:00.
