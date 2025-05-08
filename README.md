# Video EXIF Date Editor

This fixes an issue in Synology Photos where videos would end up with the wrong date caused by changing timezones and thus breaking media timelines.

## Prerequisites

Exiftool needs to be installed.

## Usage

`python3 main.py [path-to-video-files] --target_tz [timezone]`

The source timezone is taken from the filename and assumed to be UTC but can be adjusted using `--source_tz`

To list all available timezone names call the tool without any options

## Example

A video file recorded at 2024:01:01_18:00:00 (UTC) with a target timezone of 'America/New York' will end up as 2024:01:01_14:00:00-04:00.

If you don't know the name of the target timezone, you may simply use `Etc/GMT+1`, `Etc/GMT-5`, etc., instead
