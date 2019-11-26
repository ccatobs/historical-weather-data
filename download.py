#!/usr/bin/env python3

import os
import shutil
import tempfile
import urllib.request
import zipfile

from bs4 import BeautifulSoup

base_url = "http://www.submm.caltech.edu/submm.org/site/weather/"
datadir = "./data/"

print(f"scraping data from {base_url}")
with urllib.request.urlopen(base_url + "cc.html") as response:
    soup = BeautifulSoup(response.read(), "html.parser")
    datalinks = [link["href"] for link in soup.findAll('a') if "txt" in link.attrs["href"]]

if not os.path.exists(datadir):
    os.mkdir(datadir)
assert os.path.isdir(datadir)

for i,datalink in enumerate(datalinks):
    print(f"downloading ({i}/{len(datalinks)}) {datalink}")
    url = base_url + datalink
    with urllib.request.urlopen(url) as response:
        with tempfile.TemporaryFile() as tf:
            shutil.copyfileobj(response, tf)
            tf.seek(0)
            with zipfile.ZipFile(tf, 'r') as zf:
                zf.extractall(datadir)

