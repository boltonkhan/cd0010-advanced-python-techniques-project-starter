"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
import math


class SupportedFormats:
    """Encapsulate supported formatting."""

    def __init__(self):
        """Construct the object of `SupportedFormats` class."""
        self.supported_formats = {'csv', 'json'}

    def __str__(self):
        """Return a string representation of `SupportedFormats` class."""
        return self.supported_formats_str

    @property
    def supported_formats_str(self):
        """Return string representation of supported formats."""
        str_f = ''
        for i, f in enumerate(self.supported_formats):
            if i < len(self.supported_formats) - 1:
                str_f += f"'{f}' ,"
            else:
                str_f += f"'{f}'"
        return str_f


def serialize(approaches, format):
    """Prepare data to write to the file with proper formating.

    :param approaches: An iterable of `CloseApproach` objects.
    :param format: (str). Supported formating: 'csv', 'json'.
    """
    sp = SupportedFormats()
    sp.supported_formats = {'csv', 'json'}
    assert \
        format.lower() in sp.supported_formats, \
        f"Unsupported format. Supported formats: {sp}"

    result = []

    def get_neo_model(app, format):
        """Return an representation of `NEO` object to write it into a file on the specified format.

        param app: A `CloseApproach` objects.
        param format: (str). Supported formating: 'csv', 'json'.
        return dict: A model of NEO object represends specified format.
        """
        neo_model = {}

        if format == 'csv':
            neo_model = {
                'neo' : {
                    'designation': app.neo.designation,
                    'name': '' if app.neo.name is None else app.neo.name,
                    'diameter_km': app.neo.diameter if(
                        not math.isnan(float(app.neo.diameter))) else float('nan'),
                    'potentially_hazardous': 'True' if app.neo.hazardous else 'False'
                }
            }

        if format == 'json':
            neo_model = {
                'neo' : {
                    'designation': app.neo.designation,
                    'name': '' if app.neo.name is None else app.neo.name,
                    'diameter_km': app.neo.diameter if (not math.isnan(float(app.neo.diameter)))
                                                    else float('nan'),
                    'potentially_hazardous': app.neo.hazardous
                }
            }

        return neo_model

    def get_ca_model(app):
        """Return an representation of `CloseApproach` object to write it into a file.

        param app: A `CloseApproach` objects.
        return dict: A representation of `CloseApproach` object.
        """
        ca_model = {
            'datetime_utc': app.time_str,
            'distance_au': app.distance,
            'velocity_km_s': app.velocity,
            }
        return ca_model

    #Formatting for csv file
    if format.lower() == 'csv':
        for app in approaches:

            row = {**get_neo_model(app,'csv')['neo'], **get_ca_model(app)}
            result.append(row)

    #formatting for json file
    if format.lower() == 'json':
        for app in approaches:
            row = {**get_ca_model(app), **get_neo_model(app, 'json')}
            result.append(row)

    return result


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )

    res = serialize(results, 'csv')

    with open(filename, 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(res)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    res = serialize(results, 'json')
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(res, file, indent=4)
