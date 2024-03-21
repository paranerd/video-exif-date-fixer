import argparse
import os
import re
import subprocess
import sys

def extract_datetime(filename):
    matches = re.findall('\\d{2,}+', filename)
    return int(''.join(matches[:2]))

def format_delta(delta):
   hours = re.findall('\\d+', str(delta))[0]
   prefix = '-' if delta < 0 else '+'
      
   return '{}{}:00'.format(prefix, hours)

def update(path, delta):
  print('Updating {}...'.format(path))

  filename = os.path.basename(path)
  datetime = extract_datetime(filename)

  corrected_datetime = datetime + delta * 10**7
  formatted_delta = format_delta(delta)

  try:
     cmd = 'exiftool -QuickTime:CreationDate={}{} {}'.format(corrected_datetime, formatted_delta, path)
     subprocess.run([cmd], shell=True, check=True, capture_output=True)
  except subprocess.CalledProcessError as err:
    print('Error updating: {} STDOUT: {})'.format(err.stderr.decode('utf-8'), err.stdout.decode('utf-8')))

def get_all_files(dir, prefix=None, extension='.mp4'):
  paths = []

  for file in os.listdir(dir):
    if (prefix == None or file.startswith(prefix)) and file.endswith(extension):
      paths.append(os.path.join(dir, file))

  return paths

if __name__ == '__main__':
  # Get path from arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('path', type=str)
  parser.add_argument('delta', type=int)
  parser.add_argument('--prefix', type=str, required=False)
  parser.add_argument('--extension', type=str, required=False)
  args = parser.parse_args()

  # Get all files
  files = get_all_files(args.path, args.prefix, args.extension)

  # Rename
  for file in files:
     update(file, args.delta)
