"""Extract data on NEOs and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `Neo`s.

The `load_approaches` function extracts close approach data
from a JSON file, formatted as described in the project instructions,
into a collection of `CloseApproach` objects.

The main module calls these functions with the arguments provided
at the command line, and uses the collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []

    csv_fields = {
        "designation": 3,
        "name": 4,
        "diameter": 15,
        "hazardous": 7
    }

    def _is_empty(field):
        """Check if the given field is None or empty string.

        param: field (str) : value to check.
        returns: bool value.
        """
        return False if field is None or field != '' else True

    def _normalize_diameter(diameter):
        """Check if the given field is a float attribute.

        param: diameter (str) : value to check.
        returns: float or 'nan'.
        """
        try:
            return float(diameter)
        except ValueError:
            return 'nan'

    def _normalize_hazardous(hazardous):
        """Convert enum Y/N to bool value.

        param: hazardous (str) : value to check.
        returns: bool.
        """
        if hazardous.upper() == 'Y':
            return True
        return False

    with open(neo_csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        for i, row in enumerate(reader):
            if i:

                des = row[csv_fields["designation"]]
                if _is_empty(des):
                    continue

                if row[csv_fields["name"]] == '':
                    name = None
                else:
                    name = row[csv_fields["name"]]

                diam = _normalize_diameter(row[csv_fields["diameter"]])
                haz = _normalize_hazardous(row[csv_fields["hazardous"]])
                neo = NearEarthObject(des, name, diam, haz)

                neos.append(neo)

    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file.
    :return: A collection of `CloseApproach`es.
    """
    app_vals = {
        'designation': 0,
        'time': 3,
        'distance': 4,
        'velocity': 7
        }

    close_approaches = []

    with open(cad_json_path, 'r', encoding='utf-8') as file:
        reader = json.load(file)

        for app in reader['data']:

            des = app[app_vals["designation"]].strip()
            time = app[app_vals["time"]]
            distance = app[app_vals["distance"]].strip()
            velocity = app[app_vals["velocity"]].strip()
            close_app = CloseApproach(des, time, distance, velocity)
            close_approaches.append(close_app)

    return close_approaches
