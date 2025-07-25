from abc import ABC, abstractmethod


class Alter(ABC):
    '''
    Alters a province.
    '''
    
    @abstractmethod
    def apply(self, province):
        '''
        Applies the given alteration to a province

        Params
        - province: the province to alter.
        '''
        pass
