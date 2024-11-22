#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2024-11-20 23:59:22

import sys
import os
DIR_PATH = os.path.join(
  os.path.dirname(
    os.path.abspath(__file__)
  ), 
  "build/project/python/lib/python3.12/site-packages/project"
)
FILE_PATH = os.path.join(DIR_PATH, "settings_secret.py")
TEMPLAGE = """\
AWS = {{
  "cognito":{{
    "userPoolID":"{userPoolID}",
    "clientID":"{clientID}",
  }}
}}
MAPPING_PATH = "{MAPPING_PATH}"
DEBUG = {DEBUG}
"""

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\

""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-u", "--userPoolID", metavar="userPoolID", required=True, help="userPoolID")
  parser.add_argument("-c", "--clientID", metavar="clientID", required=True, help="clientID")
  parser.add_argument("-m", "--MAPPING_PATH", metavar="MAPPING_PATH", required=True, help="MAPPING_PATH")
  parser.add_argument("-d", "--DEBUG", metavar="DEBUG", required=True, help="DEBUG")

  # parser.add_argument("-", "--", action="store_true", help="")
  options = parser.parse_args()
  return options

def main():
  options = parse_args()
  if os.path.exists(FILE_PATH):
    print(f"File already exists: {FILE_PATH}")
    sys.exit()
  os.makedirs(DIR_PATH, exist_ok=True)
  with open(FILE_PATH, "w") as f:
    f.write(
      TEMPLAGE.format(
        userPoolID=options.userPoolID,
        clientID=options.clientID,
        MAPPING_PATH=options.MAPPING_PATH,
        DEBUG=options.DEBUG
      )
    )

if __name__ == '__main__':
  main()
