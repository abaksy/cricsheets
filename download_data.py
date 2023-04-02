import argparse
import requests
import os
import zipfile
import process_data

url_map = {
    'Test': 'https://cricsheet.org/downloads/tests_json.zip',
    'ODI': 'https://cricsheet.org/downloads/odis_json.zip',
    'T20I': 'https://cricsheet.org/downloads/t20s_json.zip',
    'IPL': 'https://cricsheet.org/downloads/ipl_json.zip'
    }

def download_data(tournament:str, download_link: str):
    print("Downloading files ....")
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



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tournament", type=str)
    parser.add_argument("-p", "--people-registry", default=False, action='store_true')
    parser.add_argument("-d", "--download-files", default=False, action='store_true')
    parser.add_argument("-b", "--build-data", default=False, action='store_true')
    parser.add_argument("-n", "--num-files", default=-1, type=int)
    args = parser.parse_args()

    print("NUM FILES: ", args.num_files)

    tournament = args.tournament
    download_link = url_map.get(tournament, None)
    if download_link is None:
        print("Enter a valid tournament!")
        exit(1)

    update = args.download_files
    build_data = args.build_data

    if update is not None and update:
        download_data(tournament, download_link)
        

    if args.people_registry:
        process_data.build_people_registry(tournament)

    if build_data:
        process_data.build_all_data(f"{tournament}/", args.num_files)
        

if __name__ == "__main__":
    main()