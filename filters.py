"""Provide filters for querying close approaches and limit the generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function returns a collection of instances of subclasses of `AttributeFilter`,
which are callable (on a `CloseApproach`) constructed from a comparator (from the
`operator` module), a reference value, and a class method `get` that subclasses
can override to fetch an attribute of interest from the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

You will edit this file in Tasks 3a and 3c.
"""

import operator
from datetime import datetime

class UnsupportedCriterionError(NotImplementedError):
    """Exception raised for unsupported filter criteria."""
    pass

class AttributeFilter:
    """Base class for filters on comparable attributes.

    An `AttributeFilter` represents a criterion for comparing some attribute of a
    `CloseApproach` object (or its associated NEO) to a reference value. It functions
    as a callable predicate to determine if a `CloseApproach` object meets the criterion.

    The filter is initialized with a comparator operator and a reference value. Calling
    the filter (using `__call__`) evaluates `get(approach) OP value` where `OP` is the
    comparator.

    Subclasses should override the `get` class method to provide custom behavior for
    retrieving the desired attribute from the given `CloseApproach`.
    """

    def __init__(self, op, value):
        """Initialize an `AttributeFilter` with a comparator and reference value.

        The comparator (`op`) is a binary predicate function (e.g., `operator.le`),
        and the reference value is compared against an attribute of the `CloseApproach`.

        :param op: A 2-argument predicate comparator (e.g., `operator.le`).
        :param value: The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """Apply the filter to a `CloseApproach` instance.

        This method evaluates the condition `self.get(approach) OP self.value`.

        :param approach: A `CloseApproach` instance to filter.
        :return: `True` if the `CloseApproach` meets the criterion, otherwise `False`.
        """
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """Retrieve an attribute from a `CloseApproach` instance.

        This method must be overridden by subclasses to fetch the attribute to be compared.

        :param approach: A `CloseApproach` instance.
        :return: The value of the attribute to compare.
        :raise UnsupportedCriterionError: If not overridden by subclasses.
        """
        raise UnsupportedCriterionError("Subclasses must override this method.")

    def __repr__(self):
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__}, value={self.value})"

class DateFilter(AttributeFilter):
    """Filter for `CloseApproach` dates."""
    
    @classmethod
    def get(cls, approach):
        """Retrieve the date of a `CloseApproach`."""
        return approach.time.date()

class DistanceFilter(AttributeFilter):
    """Filter for `CloseApproach` distances."""
    
    @classmethod
    def get(cls, approach):
        """Retrieve the distance of a `CloseApproach`."""
        return approach.distance

class VelocityFilter(AttributeFilter):
    """Filter for `CloseApproach` velocities."""
    
    @classmethod
    def get(cls, approach):
        """Retrieve the velocity of a `CloseApproach`."""
        return approach.velocity

class DiameterFilter(AttributeFilter):
    """Filter for NEO diameters associated with `CloseApproach` objects."""
    
    @classmethod
    def get(cls, approach):
        """Retrieve the diameter of the NEO associated with a `CloseApproach`."""
        return approach.neo.diameter

class HazardousFilter(AttributeFilter):
    """Filter for hazardous NEOs associated with `CloseApproach` objects."""
    
    @classmethod
    def get(cls, approach):
        """Retrieve the hazardous status of the NEO associated with a `CloseApproach`."""
        return approach.neo.hazardous

def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    """Create a collection of filters based on user-specified criteria.

    This function generates a list of `AttributeFilter` instances based on the
    provided arguments. Each argument corresponds to a different filter criterion
    used to select `CloseApproach` objects.

    Filters are created for exact matches, ranges, and boolean checks as specified.

    :param date: Exact date for which the `CloseApproach` must occur.
    :param start_date: The earliest date for a matching `CloseApproach` to occur.
    :param end_date: The latest date for a matching `CloseApproach` to occur.
    :param distance_min: Minimum distance for a matching `CloseApproach`.
    :param distance_max: Maximum distance for a matching `CloseApproach`.
    :param velocity_min: Minimum velocity for a matching `CloseApproach`.
    :param velocity_max: Maximum velocity for a matching `CloseApproach`.
    :param diameter_min: Minimum diameter of the NEO for a matching `CloseApproach`.
    :param diameter_max: Maximum diameter of the NEO for a matching `CloseApproach`.
    :param hazardous: Boolean indicating if the NEO must be hazardous.
    :return: A list of filters compatible with the `query` method.
    """
    filters = []

    if date:
        filters.append(DateFilter(operator.eq, date))
    if start_date:
        filters.append(DateFilter(operator.ge, start_date))
    if end_date:
        filters.append(DateFilter(operator.le, end_date))
    if distance_min:
        filters.append(DistanceFilter(operator.ge, distance_min))
    if distance_max:
        filters.append(DistanceFilter(operator.le, distance_max))
    if velocity_min:
        filters.append(VelocityFilter(operator.ge, velocity_min))
    if velocity_max:
        filters.append(VelocityFilter(operator.le, velocity_max))
    if diameter_min:
        filters.append(DiameterFilter(operator.ge, diameter_min))
    if diameter_max:
        filters.append(DiameterFilter(operator.le, diameter_max))
    if hazardous is not None:
        filters.append(HazardousFilter(operator.eq, hazardous))

    return filters

def limit(iterator, n=None):
    """Limit the number of items produced by an iterator.

    This function yields at most `n` items from the given iterator. If `n` is None
    or zero, all items from the iterator are yielded.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to yield.
    :yield: The first `n` values from the iterator, or all values if `n` is None.
    """
    if n is None or n == 0:
        yield from iterator
    else:
        for _, value in zip(range(n), iterator):
            yield value
