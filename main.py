import argparse
import os
import re
import subprocess
import sys

def extract_datetime(filename):
    matches = re.findall('\\d{2,}+', filename)
    return int(''.join(matches))

def format_delta(delta):
   hours = re.findall('\\d+', str(delta))[0]
   prefix = '-' if delta < 0 else '+'
      
   return '{}{}:00'.format(prefix, hours)

def update(path, delta):
  filename = os.path.basename(path)
  args = ['exiftool', filename]
  datetime = extract_datetime(filename)

  corrected_datetime = datetime + delta * 10**7
  formatted_delta = format_delta(delta)

  args.append('-AllDates={0}{1}'.format(corrected_datetime, formatted_delta))

  subprocess.check_call(args, executable="/usr/local/bin/exiftool", stdout=sys.stdout, stderr=sys.stderr)

  print('Updated {} to {}{}'.format(path, corrected_datetime, formatted_delta))

def get_all_files(dir):
  paths = []

  for file in os.listdir(dir):
    if file.endswith('.mp4'):
      paths.append(os.path.join(dir, file))

  return paths

if __name__ == '__main__':
  # Get path from arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('path', type=str)
  parser.add_argument('delta', type=int)
  args = parser.parse_args()

  # Get all files
  files = get_all_files(args.path)

  # Rename
  for file in files:
     update(file, args.delta)
