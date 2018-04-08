"""

Description:
This script is to generate data for given (Address, Postal-Code) tuples


Example Zillow Data Schema

{'extended_data': {'bathrooms': '2.0',
                   'bedrooms': '3',
                   'complete': True,
                   'finished_sqft': '2090',
                   'fips_county': '36081',
                   'last_sold_date': None,
                   'last_sold_price': None,
                   'lot_size_sqft': '3841',
                   'tax_assessment': '1072000.0',
                   'tax_assessment_year': '2017',
                   'usecode': 'SingleFamily',
                   'year_built': '1925'},
 'full_address': {'city': 'Forest Hills',
                  'latitude': '40.710752',
                  'longitude': '-73.843789',
                  'state': 'NY',
                  'street': '100-39 75th Ave',
                  'zipcode': '11375'},
 'links': {'comparables': ...,
           'graphs_and_data': ...,
           'home_details': ...,
           'map_this_home': ...,
 'local_realestate': {'fsbo_link': ...,
                      'overview_link': ...,
                      'region_id': '273757',
                      'region_name': 'Forest Hills',
                      'region_type': 'neighborhood',
                      'sale_link': ...,
                      'zillow_home_value_index': None},
 'similarity_score': None,
 'zestimate': {'amount': 1376218,
               'amount_change_30days': 2881,
               'amount_currency': 'USD',
               'amount_last_updated': '04/07/2018',
               'valuation_range_high': 1445029,
               'valuation_range_low': 1307407},
 'zpid': '32005113'}


"""

import logging
import argparse

import pandas as pd

import zillow
# from geocodio import GeocodioClient


def get_args(args=None):

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file",
                        required=True,
                        help="CSV file containing tuples of address "
                             "and postal code combinations.")
    parser.add_argument("-o", "--output-file")
    parser.add_argument("--zillow-key", required=True,
                        help="File containing zillow API key.")
    return vars(parser.parse_args(args))


def retrieve_zillow_data(address_df, api_key):
    api = zillow.ValuationApi()
    zillow_data = dict()
    for address, postal_code in address_df.itertuples(index=False):
        try:
            data = api.GetDeepSearchResults(api_key, address, postal_code)
            zillow_data[address] = data.get_dict()
        except zillow.error.ZillowError:
            logging.info("Could not retrieve data for address: {}; {}"
                         .format(address, postal_code))
            print("Could not retrieve data for address: {}, {}"
                  .format(address, postal_code), flush=True)
    return zillow_data


def format_zillow_data(zillow_data):
    pass


def main():
    parsed_args = get_args()

    with open(parsed_args["zillow_key"], 'r') as fh:
        zillow_key = fh.readline().strip()
    address_df = pd.read_csv(parsed_args["input_file"])

    zillow_data = retrieve_zillow_data(address_df, api_key=zillow_key)
    zillow_data_df = pd.DataFrame.from_dict(zillow_data)
    zillow_data_df.to_csv(parsed_args["output_file"])
    # with open(parsed_args["output_file"], 'w') as fh:
    #     json.dump(zillow_data, fh)


if __name__ == "__main__":
    main()

"""
import pdb, traceback, sys
if __name__ == '__main__':
    try:
        main()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
"""
