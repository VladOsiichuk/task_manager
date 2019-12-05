from typing import Any, List


class ListResponse:
    def __init__(self, results: List[Any], count: int, limit: int = 0, offset: int = 0):
        self.results = results
        self.limit = limit
        self.offset = offset
        self.count = count
