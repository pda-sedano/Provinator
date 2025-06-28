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
        # self.province_ids = province_ids
        # self.patterns_to_search = patterns_to_search
        # self.new_owner = new_owner
        # self.keywords = keywords
        # self.block_to_append_keyword = block_to_append_keyword
    
    def filter_by_province_ids(province_ids):
        '''
        Adds a filter specifying that only files with the given province ids should be affected.

        Params
        - province_ids: the ids of the desired provinces.
        '''
        pass

    def filter_by_patterns(patterns):
        '''
        Adds a filter specifying that only files containing the given patterns should be affected.

        Params
        - patterns: A list of patterns, currently tuples of the form (lhs, rhs) representing the pattern "lhs = rhs"
        '''
        pass

    def set_block_append_keyword(keyword):
        '''
        Specifies a keyword dictating which block of text patterns will be appended to.
        Patterns will be appended to the first block containing the given keyword.
        '''
        pass

    def patterns_to_add(patterns):
        '''
        Specifies a list of patterns to add to the province file. Currently these are only of the form "lhs = rhs".
        If a pattern of the form "lhs = different rhs" already exists, it will be modified in-place to "lhs = rhs".
        Else, the pattern "lhs = rhs" will be appended either to the end of the file, or based on the specification
        set by 'set_block_append_keyword'.

        Params
        - patterns: A list of patterns, currently tuples of the form (lhs, rhs)
        '''
        pass

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
            