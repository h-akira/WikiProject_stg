import sys
import os
import boto3
DIR_PATH = os.path.join(
  os.path.dirname(
    os.path.abspath(__file__)
  ), 
  "..",
  "build/project/python/lib/python3.12/site-packages/project"
)
FILE_PATH = os.path.join(DIR_PATH, "settings_secret.py")
TEMPLATE = """\
AWS = {{
  "account": "{account}",
  "region": "{region}",
  "cognito":{{
    "userPoolID":"{userPoolID}",
    "clientID":"{clientID}"
  }},
  "ACM":{{
    "arn":"{ACM_ARN}"
  }}
}}
MAPPING_PATH = "{MAPPING_PATH}"
DEBUG = {DEBUG}
"""
if os.path.exists(FILE_PATH):
  print(f"File already exists: {FILE_PATH}")
  sys.exit()
os.makedirs(DIR_PATH, exist_ok=True)
MAPPING_PATH = os.getenv("settings_secret_MAPPING_PATH")
if MAPPING_PATH == "None":
  MAPPING_PATH = ""
SOURCE = TEMPLATE.format(
  account=boto3.client('sts').get_caller_identity()["Account"],
  region=os.getenv("settings_secret_region"),
  userPoolID=os.getenv("settings_secret_userPoolID"),
  clientID=os.getenv("settings_secret_clientID"),
  ACM_ARN=os.getenv("settings_secret_ACM_ARN"),
  MAPPING_PATH=MAPPING_PATH,
  DEBUG=os.getenv("settings_secret_DEBUG")
)
with open(FILE_PATH, "w") as f:
  f.write(SOURCE)
print("File created: ", FILE_PATH)
print("=== settings_secret.py ===")
print(SOURCE)
