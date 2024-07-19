"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You will edit this file in Tasks 2 and 3.
"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    This class contains a collection of NEOs and close approaches. It maintains
    auxiliary data structures to facilitate fetching NEOs by primary designation
    or name, and to speed up querying for close approaches that match specified
    criteria.
    """

    def __init__(self, neos, approaches):
        """Initialize a new `NEODatabase` instance.

        This constructor links the provided collections of NEOs and close approaches.
        Each `CloseApproach` object is linked to its corresponding `NearEarthObject`
        based on the `_designation` attribute of the `CloseApproach` and the
        `designation` attribute of the `NearEarthObject`.

        :param neos: A collection of `NearEarthObject` instances.
        :param approaches: A collection of `CloseApproach` instances.
        """
        self._neos = neos
        self._approaches = approaches

        # Create auxiliary data structures for quick lookups
        self._designation_dict = {neo.designation: neo for neo in neos}
        self._name_dict = {neo.name: neo for neo in neos if neo.name}

        # Link NEOs and their close approaches
        for approach in self._approaches:
            neo = self._designation_dict.get(approach._designation)
            approach.neo = neo
            if neo:
                neo.approaches.append(approach)

    def get_neo_by_designation(self, designation):
        """Retrieve an NEO by its primary designation.

        This method looks up an NEO by its unique primary designation. If no NEO
        with the given designation is found, it returns `None`.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the specified primary designation, or `None` if not found.
        """
        return self._designation_dict.get(designation)

    def get_neo_by_name(self, name):
        """Retrieve an NEO by its name.

        This method looks up an NEO by its name. If no NEO with the given name is
        found, it returns `None`. NEOs with an empty name or `None` are not included.

        :param name: The name of the NEO to search for.
        :return: The `NearEarthObject` with the specified name, or `None` if not found.
        """
        return self._name_dict.get(name)

    def query(self, filters=()):
        """Query close approaches based on specified filters.

        This method generates `CloseApproach` objects that match all provided filters.
        If no filters are provided, it yields all known close approaches.

        The results are generated in internal order, which is often chronological but
        not guaranteed to be sorted.

        :param filters: A sequence of functions to apply as filters on `CloseApproach` objects.
        :return: An iterator yielding `CloseApproach` objects that match the filters.
        """
        for approach in self._approaches:
            if all(f(approach) for f in filters):
                yield approach
