import os
import json
import subprocess
from datetime import datetime, timedelta
import requests
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("DFBlocks")
CACHE_FILE = os.path.join(os.path.dirname(__file__), "cached_blocks.json")
CACHE_EXPIRATION = timedelta(hours=24)
QUICKTYPE_INSTALLED = False
NODE_MODULES_PATH = "node_modules/quicktype/dist/index.js"  # Path to quicktype executable in ./node_modules/



def check_quicktype_installed():
    try:
        subprocess.run([NODE_MODULES_PATH, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def fetch_blocks(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
  
def generate_code_from_blocks(blocks):
    module_dir = os.path.dirname(__file__)
    temp_db_json = os.path.join(module_dir, "temp_db.json")
    dfdb_py = os.path.join(module_dir, "dfdb.py")

    with open(temp_db_json, "w") as f:
        json.dump(blocks, f)

    global QUICKTYPE_INSTALLED
    if not QUICKTYPE_INSTALLED:
        QUICKTYPE_INSTALLED = check_quicktype_installed()

    if QUICKTYPE_INSTALLED:
        subprocess.run([NODE_MODULES_PATH, temp_db_json, "-o", dfdb_py])
    else:
        LOGGER.error("Quicktype not detected, please install with:\n npm install quicktype")

def load_cached_blocks():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cached_data = json.load(f)
            timestamp = cached_data.get("timestamp")
            if timestamp and datetime.utcnow() - datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ") < CACHE_EXPIRATION:
                return cached_data.get("blocks")

    return None

def save_blocks_to_cache(blocks):
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    data = {"timestamp": timestamp, "blocks": blocks}
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

def load_dfdb():
    cached_blocks = load_cached_blocks()
    if cached_blocks:

        from .dfdb import dfdb_from_dict
        return dfdb_from_dict(cached_blocks)

    LOGGER.info("Fetching and generating types, Might take a while")
    blocks = fetch_blocks("https://dfonline.dev/public/dbc.json")
    save_blocks_to_cache(blocks)
    generate_code_from_blocks(blocks)
    from .dfdb import dfdb_from_dict
    return dfdb_from_dict(blocks)


import time

start = time.time()
diamondfire = load_dfdb()
end = time.time()

LOGGER.info("DFDB took %f seconds", end - start)



