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
        property_msg = 'The name value is what you will use in the csv header. The label value is what you will see in the Hubspot UI.' \
                    '\nThe description value is what you will see in the Hubspot UI. The type value is the datatype.'
        '\nThe following properties are available for use in the CSV file:'

        property_msg += (f"\n{'-' * 10}")  # 10 dashes as a separator
        for hubspot_property in hubspot_properties:
            property_msg += f'\nName: {hubspot_property["name"]}'
            property_msg += f'\nLabel: {hubspot_property["label"]}'
            property_msg += f'\nDescription: {hubspot_property["description"]}'
            property_msg += f'\nType: {hubspot_property["type"]}'
            property_msg += f"\n{'-' * 10}"  # 10 dashes as a separator
        
        client.logger.info(property_msg)


if __name__ == "__main__":
    main()
