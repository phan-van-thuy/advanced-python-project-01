"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You will edit this file in Task 2.
"""

import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Extract near-Earth objects from a CSV file.

    This function reads near-Earth object data from a CSV file and creates a collection
    of `NearEarthObject` instances based on the data.

    The CSV file should contain columns for primary designation (`pdes`), name (`name`),
    diameter (`diameter`), and whether the object is hazardous (`pha`).

    :param neo_csv_path: Path to the CSV file containing near-Earth object data.
    :return: A list of `NearEarthObject` instances created from the CSV data.
    """
    neos = []
    with open(neo_csv_path, 'r') as infile:
        reader = csv.DictReader(infile)
        for line in reader:
            neos.append(NearEarthObject(
                designation=line['pdes'],
                name=line['name'] if line['name'] else None,
                diameter=float(line['diameter']) if line['diameter'] else float('nan'),
                hazardous=line['pha'] == 'Y'
            ))
    return neos


def load_approaches(cad_json_path):
    """Extract close approaches from a JSON file.

    This function reads close approach data from a JSON file and creates a collection
    of `CloseApproach` instances based on the data.

    The JSON file should contain a key `data` with a list of lists, where each inner list
    contains information about a close approach. The relevant fields are:
    designation, time, distance, and velocity.

    :param cad_json_path: Path to the JSON file containing close approach data.
    :return: A list of `CloseApproach` instances created from the JSON data.
    """
    approaches = []
    with open(cad_json_path, 'r') as infile:
        contents = json.load(infile)
        for approach in contents['data']:
            approaches.append(CloseApproach(
                designation=approach[0],
                time=approach[3],
                distance=approach[4],
                velocity=approach[7]
            ))
    return approaches
