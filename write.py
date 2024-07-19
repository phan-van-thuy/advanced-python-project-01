"""Write a stream of close approaches to CSV or to JSON.

This module provides two functions: `write_to_csv` and `write_to_json`. Each function
takes an iterable of `CloseApproach` objects and a file path to write the data.

The file extension determines which function is invoked by the main module. The
output format is specified in `README.md`.

You'll edit this file in Part 4.
"""

import csv
import json

def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    Each row in the CSV file corresponds to a single close approach and its associated
    near-Earth object. The output file includes columns for approach details and NEO attributes.

    :param results: An iterable of `CloseApproach` objects to be written to the CSV file.
    :param filename: A file path where the CSV data will be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for approach in results:
            writer.writerow({
                'datetime_utc': approach.time_str,
                'distance_au': approach.distance,
                'velocity_km_s': approach.velocity,
                'designation': approach._designation,
                'name': approach.neo.name if approach.neo.name else '',
                'diameter_km': approach.neo.diameter if approach.neo.diameter else '',
                'potentially_hazardous': 'True' if approach.neo.hazardous else 'False'
            })

def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The JSON file will contain a list of dictionaries, each representing a close approach
    with its details and the associated near-Earth object attributes.

    :param results: An iterable of `CloseApproach` objects to be written to the JSON file.
    :param filename: A file path where the JSON data will be saved.
    """
    data = []
    for approach in results:
        data.append({
            'datetime_utc': approach.time_str,
            'distance_au': approach.distance,
            'velocity_km_s': approach.velocity,
            'neo': {
                'designation': approach._designation,
                'name': approach.neo.name if approach.neo.name else '',
                'diameter_km': approach.neo.diameter if approach.neo.diameter else '',
                'potentially_hazardous': approach.neo.hazardous,
            }
        })

    with open(filename, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=2)
