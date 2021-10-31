from typing import Tuple


class AreaCoordinates:

    _left_upper: Tuple
    _left_lower: Tuple
    _right_upper: Tuple
    _right_lower: Tuple

    def __init__(self, coordinates: Tuple) -> None:
        self._left_upper = (coordinates[3], coordinates[0])
        self._right_lower = (coordinates[1], coordinates[2])

        self._left_lower = (coordinates[3], coordinates[2])
        self._right_upper = (coordinates[1], coordinates[0])

    @property
    def left_upper(self):
        return self._left_upper

    @property
    def left_lower(self):
        return self._left_lower

    @property
    def right_upper(self):
        return self._right_upper

    @property
    def right_lower(self):
        return self._right_lower

    @property
    def coordinates_to_ret(self):
        return self._left_lower + self._right_upper

    @property
    def coordinates_to_blur(self):
        return self._left_upper + self._right_lower
