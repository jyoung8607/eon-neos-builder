#!/usr/bin/env python
import sys
import os
import json
import hashlib
import requests

def sha256_checksum(filename, block_size=65536):
  sha256 = hashlib.sha256()
  with open(filename, 'rb') as f:
    for block in iter(lambda: f.read(block_size), b''):
      sha256.update(block)
  return sha256.hexdigest()

def download(url, fhash, finalname):
  try:
    assert sha256_checksum(finalname).lower() == fhash.lower()
    print("already downloaded %s" % url)
    return
  except Exception:
    pass

  print("downloading %s with hash %s" % (url, fhash))
  os.system("curl -O %s" % url)
  fn = url.split("/")[-1]
  assert sha256_checksum(fn).lower() == fhash.lower()
  print("hash check pass")
  os.system("rm -f %s; ln -s %s %s" % (finalname, fn, finalname))

if __name__ == "__main__":
  #up = requests.get("https://raw.githubusercontent.com/commaai/eon-neos/master/update.json").json()
  up = json.loads(open('/home/batman/openpilot/installer/updater/update.json').read())
  download(up['ota_url'], up['ota_hash'], "ota-signed-latest.zip")
