"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
import math
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    def __init__(self, designation, name=None, diameter=None, hazardous =False):
        """Create a new `NearEarthObject`.

        :param designation: (str) Unique NEO identyfier.
        :param name: (str) Optional NEO name.
        :param diameter: (float)  Optional, Neo diameter in km.
        :param hazardous: (bool) Is Neo marked as potentially hazardous to Earth.
        """
        self.designation = designation
        assert self.designation is not None and self.designation != '', \
           f"Attribute designation is required. Value: '{designation}' is not allowed"
        self.name = None if name is None else name
        self.diameter = float('nan') if math.isnan(float(diameter)) else float(diameter)
        assert self.diameter > float(0) or math.isnan(float(diameter))
        self.hazardous = False if not hazardous else bool(hazardous)
        self.approaches = []

    @property
    def fullname(self):
        """Returns a representation of the full name of this NEO."""
        return f"'{self.designation} {self.name}'"

    @property
    def _str_hazardous(self):
        """Returns a human readable representation of 'hazardous' attribute use in __str__."""
        if self.hazardous:
            return "is"
        return "is not"

    def str_diameter(self):
        """Returns a human readable representation of 'diameter' attribute use in __str__."""
        if math.isnan(float(self.diameter)):
            return "an uknown diameter"
        return f"a diameter of {self.diameter: .3f} km"

    def __str__(self):
        """Return `str(self)`."""
        return f"A NearEarthObject {self.fullname} has {self.str_diameter} " \
            f"and {self._str_hazardous} potentially hazardous"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    def __init__(self, designation, time, distance, velocity):
        """Create a new `CloseApproach`.

        :param designation: (str) Unique NEO identyfier.
        :param time: (datetime.datetime) UTC time of close-approach.
        :param distance: (float) Nominal approach distance (au).
        :param velocity: (float) Velocity relative to the approach body at close approach (km/s).
        """
        self.designation = designation
        assert designation is not None and designation != '', \
           f"Attribute designation is required. Value: '{designation}' is not allowed"

        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)
        self.neo = None

    @property
    def neo(self):
        """Attribute for the referenced NEO, originally None."""
        return self.__neo

    @neo.setter
    def neo(self, neo):
        """Attribute for the referenced NEO, originally None."""
        self.__neo = neo

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time."""
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return f"At {self.time_str}, {self.neo.fullname} approaches Earth at a distance of " \
           f"{self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
