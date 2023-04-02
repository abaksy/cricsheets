import argparse
import download_data
import process_data


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
    

    update = args.download_files
    build_data = args.build_data

    if update is not None and update:
        download_data.download_data(tournament)
        

    if args.people_registry:
        process_data.build_people_registry(tournament)

    if build_data:
        process_data.build_all_data(f"{tournament}/", args.num_files)
        

if __name__ == "__main__":
    main()