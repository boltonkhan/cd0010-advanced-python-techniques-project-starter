"""Provide filters for querying close approaches and limit the results.

The `create_filters` function produces a collection of objects
that is used by the `query` method to generate a stream of `CloseApproach`
objects that match all of the desired criteria.
The arguments to `create_filters` are provided by the main module
and originate from the user's command-line options.

This function can be thought to return a collection of instances of
subclasses of `AttributeFilter` - a 1-argument callable
(on a `CloseApproach`) constructed from a comparator
(from the `operator` module), a reference value, and a class method `get`
that subclasses can override to fetch an attribute of interest
from the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced
by an iterator.

You'll edit this file in Tasks 3a and 3c.
"""
import operator
import itertools


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    """A general superclass for filters on comparable attributes.

    An `AttributeFilter` represents the search criteria pattern comparing
    some attribute of a close approach to a reference value.
    It essentially functions as a callable predicate for whether
    a `CloseApproach` object satisfies the encoded criterion.

    It is constructed with a comparator operator and a reference value, and
    calling the filter (with __call__) executes `get(approach) OP value`
    (in infix notation).

    Concrete subclasses can override the `get` classmethod to provide custom
    behavior to fetch a desired attribute from the given `CloseApproach`.
    """

    def __init__(self, op, value):
        """Construct a new `AttributeFilter`.

        The reference value will be supplied as the second (right-hand side)
        argument to the operator function. For example, an `AttributeFilter`
        with `op=operator.le` and `value=10` will, when called on an approach,
        evaluate `some_attribute <= 10`.

        :param op: A 2-argument predicate comparator (such as `operator.le`).
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Get an attribute of interest from a close approach.

        Concrete subclasses must override this method to get an attribute of
        interest from the supplied `CloseApproach`.

        :param approach: A `CloseApproach` on which to evaluate this filter.
        :return: The value of an attribute of interest,
        comparable to `self.value` via `self.op`.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        """Return string representation of `AttributeFilter` class."""
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, " \
               f"value={self.value})"


class DateFilter(AttributeFilter):
    """Specific class for date filters."""

    @classmethod
    def get(cls, approach):
        """Get a date value from a close approach.

        param: A `CloseApproach` on which to evaluate this filter.
        return: datetime.date. Date of the close approach.
        """
        return approach.time.date()


class DistanceFilter(AttributeFilter):
    """Specific class for distances filters."""

    @classmethod
    def get(cls, approach):
        """Get a distance value from a close approach.

        param: A `CloseApproach` on which to evaluate this filter.
        return: float. Distance of a close approach.
        """
        return approach.distance


class VelocityFilter(AttributeFilter):
    """Specific class for vwlocity filters."""

    @classmethod
    def get(cls, approach):
        """Get a velocity value from a close approach.

        param: A `CloseApproach` on which to evaluate this filter.
        return: float. Velocity of a close approach
        """
        return approach.velocity


class DiameterFilter(AttributeFilter):
    """Specific class for diameters filters."""

    @classmethod
    def get(cls, approach):
        """Get a diameter value from a close approach.

        param: A `CloseApproach` on which to evaluate this filter.
        return: float. Diameter of a close approach
        """
        return approach.neo.diameter


class HazardousFilter(AttributeFilter):
    """Specific class for date hazardous."""

    @classmethod
    def get(cls, approach):
        """Get a hazardous value from a close approach.

        param: A `CloseApproach` on which to evaluate this filter.
        return: bool. Is the close approach validated as hazardous.
        """
        return approach.neo.hazardous


def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    """Create a collection of filters from user-specified criteria.

    :param date: A `date` on which a `CloseApproach` occurs.
    :param start_date: A `date` on or after which a `CloseApproach` occurs.
    :param end_date: A `date` on or before which a `CloseApproach` occurs.
    :param distance_min: A minimum approach distance for a `CloseApproach`.
    :param distance_max: A maximum approach distance for a `CloseApproach`.
    :param velocity_min: A minimum velocity for a `CloseApproach`.
    :param velocity_max: A maximum velocity for a `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a `CloseApproach`.
    :param hazardous: Is the `CloseApproach` is potentially hazardous.
    :return: A collection of filters for use with `query`.
    """
    filters = []

    if date is not None:
        filters.append(DateFilter(operator.eq, date))

    if start_date is not None:
        filters.append(DateFilter(operator.ge, start_date))

    if end_date is not None:
        filters.append(DateFilter(operator.le, end_date))

    if distance_min is not None:
        filters.append(DistanceFilter(operator.ge, float(distance_min)))

    if distance_max is not None:
        filters.append(DistanceFilter(operator.le, float(distance_max)))

    if velocity_min is not None:
        filters.append(VelocityFilter(operator.ge, float(velocity_min)))

    if velocity_max is not None:
        filters.append(VelocityFilter(operator.le, float(velocity_max)))

    if diameter_min is not None:
        filters.append(DiameterFilter(operator.ge, float(diameter_min)))

    if diameter_max is not None:
        filters.append(DiameterFilter(operator.le, float(diameter_max)))

    if hazardous is not None:
        filters.append(HazardousFilter(operator.eq, bool(hazardous)))

    return filters


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    if n is None or n == 0:
        return iterator

    return itertools.islice(iterator, n)
