"""A database encapsulating collections of NEOs and close approaches.

A `NEODatabase` holds an linked data set of NEOs and close approaches.
It provides methods to fetch an NEO by designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.
"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches
        self._designation_to_neo = {}
        self._name_to_neo = {}

        for neo in self._neos:
            self._designation_to_neo[neo.designation.lower()] = neo
            if neo.name is not None:
                self._name_to_neo[neo.name.lower()] = neo

        for app in self._approaches:
            neo = self._designation_to_neo[app.designation.lower()]
            app.neo = self._designation_to_neo[app.designation.lower()]
            neo.approaches.append(app)

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its designation.

        :param designation: The primary designation of the NEO.
        :return: The `NEO` with the desired designation, or `None`.
        """
        designation = designation.lower()
        neo = self._designation_to_neo.get(designation)

        if neo is None:
            return None
        return neo

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        name = name.lower()
        neo = self._name_to_neo.get(name)

        if neo is None:
            return None
        return neo

    def query(self, filters=()):
        """Query close approaches to match a collection of filters.

        This generates a stream of `CloseApproach` objects that match
        all of the provided filters.

        If no arguments are provided, generate all known close approaches.

        :param filters: A collection of filters.
        :return: A stream of matching `CloseApproach` objects.
        """
        for approach in self._approaches:

            semaphor = True
            for a_filter in filters:
                if not a_filter(approach):
                    semaphor = False
                    break

            if semaphor:
                yield approach
