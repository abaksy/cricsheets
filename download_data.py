import requests
import os
import zipfile

url_map = {
    'Test': 'https://cricsheet.org/downloads/tests_json.zip',
    'ODI': 'https://cricsheet.org/downloads/odis_json.zip',
    'T20I': 'https://cricsheet.org/downloads/t20s_json.zip',
    'IPL': 'https://cricsheet.org/downloads/ipl_json.zip'
}

def download_data(tournament:str):
    print("Downloading files ....")

    download_link = url_map.get(tournament, None)
    if download_link is None:
        print("Enter a valid tournament!")
        exit(1)
    response = requests.get(download_link, allow_redirects=True)
    print(response.headers.get('content-type'))

    open(f'{tournament}.zip', 'wb').write(response.content)

    if tournament in os.getcwd():
        os.removedirs(tournament)
        
    os.mkdir(tournament)

    print("Extracting files ....")

    zf = zipfile.ZipFile(f"{tournament}.zip")
    zf.extractall(path=os.path.join(os.getcwd(), tournament))

    print("Data is downloaded!")

    os.remove(f"{tournament}.zip")
