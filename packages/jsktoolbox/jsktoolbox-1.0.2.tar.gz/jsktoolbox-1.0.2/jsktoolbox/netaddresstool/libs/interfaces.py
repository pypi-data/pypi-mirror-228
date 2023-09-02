# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 24.06.2023

  Purpose: intrfaces class.
"""

from abc import ABC, abstractmethod


class ILt(ABC):
    """Less then.

    x < y
    """

    @abstractmethod
    def __lt__(self, value):
        pass


class ILe(ABC):
    """Less then or equal.

    x <= y
    """

    @abstractmethod
    def __le__(self, value):
        pass


class IEq(ABC):
    """Equal.

    x == y
    """

    @abstractmethod
    def __eq__(self, value):
        pass


class INe(ABC):
    """Negative.

    x != y
    """

    @abstractmethod
    def __ne__(self, value):
        pass


class IGt(ABC):
    """Greater then.

    x > y
    """

    @abstractmethod
    def __gt__(self, value):
        pass


class IGe(ABC):
    """Greater than or equal to.

    x >= y
    """

    @abstractmethod
    def __ge__(self, value):
        pass


class IComparators(IEq, IGe, IGt, ILe, ILt, INe):
    """A set of comparators."""

    pass


# #[EOF]#######################################################################
