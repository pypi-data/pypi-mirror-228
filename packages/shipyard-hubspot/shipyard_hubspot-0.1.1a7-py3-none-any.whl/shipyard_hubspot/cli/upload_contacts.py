import sys
import time
import argparse

from shipyard_hubspot import HubspotClient
from shipyard_templates import ExitCodeException



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--access-token", dest="access_token", required=True)

    parser.add_argument("--import-name", dest="import_name", required=True)
    parser.add_argument("--filename", dest="filename", required=True)
    parser.add_argument("--import_operation", dest="import_operation", required=True)
    parser.add_argument("--file_format", dest="file_format", required=True)
    return parser.parse_args()


def main():
    args = get_args()
    client = HubspotClient(access_token=args.access_token)
    try:
        import_job_id = client.import_contact_data(import_name=args.import_name,
                                                   filename=args.filename,
                                                   import_operations=args.import_operation,
                                                   file_format=args.file_format).get("id")

        while client.get_import_status(import_job_id).get("state") not in {"FAILED",
                                                                           "CANCELED",
                                                                           "DONE",
                                                                           None}:
            client.logger.info('Waiting for import to complete...')
            time.sleep(30)
    except ExitCodeException as e:
        client.logger.error(e)
        sys.exit(e.exit_code)


if __name__ == "__main__":
    main()
