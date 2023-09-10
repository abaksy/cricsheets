import argparse
import logging
import download_data
import process_data


def main():

    # basic logging config for file-based logging
    logging.basicConfig(
        filename=".cricsheet_log",
        level=logging.INFO,
        format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # set a format which is simpler for console use
    formatter = logging.Formatter("%(pathname)s - %(levelname)s - %(message)s")
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger("").addHandler(console)

    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tournament", type=str, choices=['IPL', 'ODI', 'Test', 'T20I'])
    parser.add_argument("-p", "--people-registry", default=False, action="store_true")
    parser.add_argument("-d", "--download-files", default=False, action="store_true")
    parser.add_argument("-b", "--build-data", default=False, action="store_true")
    parser.add_argument("-n", "--num-files", default=-1, type=int)
    args = parser.parse_args()

    tournament = args.tournament

    update = args.download_files
    build_data = args.build_data

    if update is not None and update:
        download_data.download_data(tournament, logger)

    if args.people_registry:
        process_data.build_people_registry(tournament, logger)

    if build_data:
        process_data.build_all_data(tournament, f"{tournament}/", args.num_files, logger)


if __name__ == "__main__":
    main()
