from abc import ABC, abstractmethod


class Filter(ABC):
    '''
    A filter which checks whether a province matches given conditions.
    '''

    @abstractmethod
    def matches(self, province) -> bool:
        '''
        Determines whether or not the given province matches the conditions of the filter.

        Params
        - province: The province to check using the filter.

        Returns
        - A bool specifying whether the province matches the filter's conditions.
        '''
        pass
