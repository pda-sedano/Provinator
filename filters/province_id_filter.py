from filter import Filter


class ProvinceIdFilter(Filter):
    def __init__(self, ids: list[int]) -> None:
        self.ids = ids


    def matches(self, province) -> bool:
        return province.path.name.startswith(tuple(map(str, self.ids)))
