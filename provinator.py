import re
from pathlib import Path
from province import Province


# The Provinator will be baaaach
class Provinator:
    def __init__(self, provinces_folder: Path, filter_mode: str):
        '''
        Creates a new Provinator. Allows programmaticaly altering EU4 province files.

        Params
            - provinces_folder: Path to the folder containing the provinces.
            - filter_mode: "or" | "and". Whether to only accept files which match ALL filters, or those which match ANY filters
        '''
        self.provinces_folder = provinces_folder
        self.provinces = []
        self.filters = []
        self.alterations = [] # TODO: what about ordering here?
        self.filter_mode = filter_mode

    
    # TODO: All this seems way too coupled between the filter and the Provinator. Think about how I'd unit test this.
    # How to fix?
    def add_filter(self, province_filter):
        '''
        Adds a filter for the provinces.

        Params
        - province_filter: Filter to add.
        '''
        self.filters.append(province_filter)

    def add_alteration(self, alteration):
        '''
        Adds an alteration that will be applied to the provinces.

        Params
        - alteration: The alteration to add.
        '''
        self.alterations.append(alteration)

    def provinate(self):
        '''
        Performs filtering and alteration on a set of province files
        '''
        for file in Path(self.provinces_folder).rglob('*.txt'):
            self.provinces.append(Province(file))
            self.provinces = list(filter(self._filter_helper, self.provinces))

            for province in self.provinces:
                for alteration in self.alterations:
                    alteration.apply(province)

    def _filter_helper(self, province):
        for province_filter in self.filters:
            if self.filter_mode == 'or' and province_filter.matches(province):
                return True
            elif self.filter_mode == 'and' and not province_filter.matches(province):
                break
            
        return False
            