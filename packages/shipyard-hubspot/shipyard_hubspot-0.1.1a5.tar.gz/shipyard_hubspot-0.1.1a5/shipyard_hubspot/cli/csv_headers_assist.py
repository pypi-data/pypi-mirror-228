import csv
import argparse

from shipyard_hubspot import HubspotClient


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--access-token", dest="access_token", required=True)
    parser.add_argument("--csv-file", dest="csv_file")
    return parser.parse_args()


def extract_csv_headers(csv_filename):
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        return next(reader)


def headers_match(headers, hubspot_property_names):
    return all(header in hubspot_property_names for header in headers)


def log_unmatched_headers(client, headers, hubspot_property_names):
    if unmatched_headers := [
        header for header in headers if header not in hubspot_property_names
    ]:

        client.logger.info('Detected issues with the following header(s):')
        for header in unmatched_headers:
            client.logger.info(header)


def main():
    args = get_args()
    client = HubspotClient(access_token=args.access_token)
    hubspot_properties = client.get_available_contact_properties()
    hubspot_property_names = [hubspot_property['name'] for hubspot_property in hubspot_properties]

    if args.csv_file:
        client.logger.info(f'Checking if all headers in {args.csv_file} exist in the Hubspot properties.')
        headers = extract_csv_headers(args.csv_file)
        if headers_match(headers, hubspot_property_names):
            client.logger.info('All headers in the CSV file are valid hubspot properties.')
        else:
            log_unmatched_headers(client, headers, hubspot_property_names)
    else:
        client.logger.info(
            'The name value is what you will use in the csv header. The label value is what you will see in the Hubspot UI.')
        client.logger.info(
            'The description value is what you will see in the Hubspot UI. The type value is the datatype.')
        client.logger.info(f"\n{'-' * 10}")  # 10 dashes as a separator
        for hubspot_property in hubspot_properties:
            client.logger.info(f'Name: {hubspot_property["name"]}')
            client.logger.info(f'Label: {hubspot_property["label"]}')
            client.logger.info(f'Description: {hubspot_property["description"]}')
            client.logger.info(f'Type: {hubspot_property["type"]}')
            client.logger.info(f"\n{'-' * 10}")  # 10 dashes as a separator


if __name__ == "__main__":
    main()
