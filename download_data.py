import requests
import os
import logging
from http import HTTPStatus
import zipfile

url_map = {
    'Test': 'https://cricsheet.org/downloads/tests_json.zip',
    'ODI': 'https://cricsheet.org/downloads/odis_json.zip',
    'T20I': 'https://cricsheet.org/downloads/t20s_json.zip',
    'IPL': 'https://cricsheet.org/downloads/ipl_json.zip'
}

def download_data(tournament:str, logger: logging.Logger):
    logger.info("Downloading files ....")

    download_link = url_map.get(tournament, None)
    if download_link is None:
        logger.error("Invalid tournament name")
        exit(1)
    response = requests.get(download_link, allow_redirects=True)
    if response.status_code < HTTPStatus.OK or response.status_code > HTTPStatus.IM_USED:
        logging.error(f"Error in downloading files:: Return code: {response.status_code}")
    else:
        logging.info("Downloaded archive successfully!")

    open(f'{tournament}.zip', 'wb').write(response.content)

    logger.info("Cleaning up existing data")
    if tournament in os.getcwd():
        os.removedirs(tournament)
        
    os.mkdir(tournament)

    logger.info("Extracting files")

    zf = zipfile.ZipFile(f"{tournament}.zip")
    zf.extractall(path=os.path.join(os.getcwd(), tournament))

    logging.info("Data downloaded and extracted!")

    os.remove(f"{tournament}.zip")
