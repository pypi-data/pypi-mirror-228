import re
from typing import Optional
from typing import Tuple

from pydantic import RootModel


point_matcher = re.compile("([+-]?[0-9]+[.]*[0-9]*) ([+-]?[0-9]+[.]*[0-9]*)")


class Point(RootModel[str]):
    @property
    def regex_match_point(self) -> Tuple[Optional[str], Optional[str]]:
        if not hasattr(self, "_match"):
            match = point_matcher.findall(self.root)
            if len(match) == 1:
                self._match = match
            else:
                self._match = [(None, None)]
        return self._match[0][0], self._match[0][1]

    @property
    def x(self) -> Optional[str]:
        return self.regex_match_point[0]

    @property
    def y(self) -> Optional[str]:
        return self.regex_match_point[1]
