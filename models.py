"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

These classes are designed to handle data extracted from NASA's datasets, including
handling missing or incomplete information such as unknown names or diameters.

You will edit this file in Task 1.
"""

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    Represents a near-Earth object with attributes such as its primary designation,
    optional name, diameter, and whether it's classified as potentially hazardous.

    This class also maintains a list of associated close approaches, which is initially
    empty but populated in the `NEODatabase` constructor.
    """

    def __init__(self, designation, name=None, diameter=None, hazardous=False):
        """Initialize a `NearEarthObject`.

        :param designation: The primary designation of the NEO (required, unique).
        :param name: The IAU name of the NEO (optional).
        :param diameter: The diameter of the NEO in kilometers (optional). If not provided, defaults to NaN.
        :param hazardous: Boolean flag indicating whether the NEO is potentially hazardous (default is False).
        """
        self.designation = designation
        self.name = name if name else None
        self.diameter = float(diameter) if diameter else float('nan')
        self.hazardous = bool(hazardous)

        # Initialize an empty list for close approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Get the full name of the NEO.

        :return: A string representing the full name of the NEO, combining its designation and name.
        """
        if self.name:
            return f"{self.designation} ({self.name})"
        return f"{self.designation}"

    def __str__(self):
        """Return a user-friendly string representation of the NEO.

        :return: A string describing the NEO with its designation, diameter, and hazardous status.
        """
        return f"A NearEarthObject {self.fullname} has a diameter of {self.diameter:.3f} km and is " \
               f"{'potentially hazardous' if self.hazardous else 'not potentially hazardous'}."

    def __repr__(self):
        """Return a developer-friendly string representation of the NEO.

        :return: A string containing the NEO's designation, name, diameter, and hazardous status.
        """
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    Represents the details of a close approach of a near-Earth object to Earth, including
    the date and time of closest approach, the nominal distance in astronomical units,
    and the relative velocity in kilometers per second.

    This class also holds a reference to the associated `NearEarthObject`. Initially,
    the NEO reference is set to `None` but is populated later in the `NEODatabase` constructor.
    """

    def __init__(self, designation, time, distance, velocity):
        """Initialize a `CloseApproach`.

        :param designation: The primary designation of the NEO involved in the close approach.
        :param time: The date and time of closest approach, provided as a string.
        :param distance: The nominal approach distance in astronomical units.
        :param velocity: The relative approach velocity in kilometers per second.
        """
        self._designation = designation
        # Convert time from string to datetime object using helper function.
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)

        # Initialize the NEO reference as None.
        self.neo = None

    @property
    def time_str(self):
        """Get the formatted string representation of the approach time.

        :return: A string representing the approach time in a readable format.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return a user-friendly string representation of the close approach.

        :return: A string describing the close approach with its time, NEO designation, distance, and velocity.
        """
        return f"On {self.time_str}, '{self._designation}' approaches Earth at a distance of " \
               f"{self.distance:.2f} AU and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return a developer-friendly string representation of the close approach.

        :return: A string containing the approach time, distance, velocity, and associated NEO.
        """
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
