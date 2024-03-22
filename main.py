import argparse
from datetime import datetime
import os
from pathlib import Path
import re
import subprocess
from zoneinfo import ZoneInfo

def extract_datestring(path, expression='_(\\d{2,}+)_(\\d{2,}+)'):
    filename = Path(path).stem
    match = re.search(expression, filename)

    return ''.join(list(match.groups()))

def format_delta(delta):
   hours = re.findall('\\d+', str(delta))[0]
   prefix = '-' if delta < 0 else '+'
      
   return '{}{}:00'.format(prefix, hours)

def adjust_datetime(source, target_tz, source_tz='UTC', source_format='%Y%m%d%H%M%S%f'):
  source_tz = source_tz if source_tz is not None else 'UTC'
  source_format = source_format if source_format is not None else '%Y%m%d%H%M%S%f'

  return datetime.strptime(source, source_format).replace(tzinfo=ZoneInfo(source_tz)).astimezone(tz=ZoneInfo(target_tz))

def update(path, mytime):
  print('Updating {} to {}...'.format(path, mytime))

  try:
     cmd = 'exiftool -AllDates="{}" -QuickTime:CreationDate="{}" "{}"'.format(mytime, mytime, path)
     subprocess.run([cmd], shell=True, check=True, capture_output=True)
  except subprocess.CalledProcessError as err:
    print('Error updating: {} STDOUT: {})'.format(err.stderr.decode('utf-8'), err.stdout.decode('utf-8')))

def get_all_files(dir, prefix=None):
  if os.path.isfile(dir):
    return [dir]
  
  paths = []

  for file in Path(dir).glob('*.mp4'):
    if (prefix == None or str(file.name).startswith(prefix)):
      paths.append(os.path.join(dir, file))

  return paths

if __name__ == '__main__':
  # Get path from arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('path', type=str)
  parser.add_argument('--target_tz', type=str, required=True)
  parser.add_argument('--source_tz', type=str)
  parser.add_argument('--format', type=str)
  parser.add_argument('--prefix', type=str, required=False)
  args = parser.parse_args()

  # Get all files
  files = get_all_files(r'{}'.format(args.path), args.prefix)

  # Rename
  for file in files:
    datestring = extract_datestring(file)
    adjusted_datetime = adjust_datetime(datestring, args.target_tz, args.source_tz, args.format)
    update(file, adjusted_datetime)
