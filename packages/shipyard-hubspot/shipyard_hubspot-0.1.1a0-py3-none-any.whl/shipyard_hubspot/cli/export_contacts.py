import sys
import time
import requests
import argparse

from shipyard_hubspot import HubspotClient
from shipyard_templates import ExitCodeException


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--access-token", dest="access_token", required=True)
    parser.add_argument("--export-name", dest="export_name", required=True)
    parser.add_argument("--list-id", dest="list_id", required=True)
    parser.add_argument("--object-properties", dest="object_properties", required=True)
    return parser.parse_args()


def download_export(export_download_url, destination_filename):
    """
    Method for downloading an export file

    :param export_download_url: The export download URL
    :param destination_filename: The destination filename
    :return: None
    """
    response = requests.get(url=export_download_url, stream=True)
    response.raise_for_status()
    with open(destination_filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f'Downloaded export file to {destination_filename}')


def main():
    args = get_args()
    client = HubspotClient(access_token=args.access_token)
    object_properties = [obj.strip() for obj in args.object_properties.split(",")]  # Clean up the input

    try:
        client.logger.info(f'Attempting to export list {args.list_id} with object properties {object_properties}')
        export_details = client.export_list(export_name=args.export_name, list_id=args.list_id,
                                            object_properties=object_properties)

        client.logger.info(f'Export details: {export_details}')
        export_id = export_details['id']

        while client.get_export(export_id).get("status") in {"PROCESSING", "PENDING"}:
            client.logger.info(' Waiting 30 seconds...')
            time.sleep(30)

        client.logger.info(f'Downloading export file {export_id}')
        download_export(client.get_export(export_id).get("result"), f"{export_id}.csv")

    except ExitCodeException as e:
        client.logger.error(e)
        sys.exit(e.exit_code)


if __name__ == "__main__":
    main()
