from abc import ABC, abstractmethod


class Alter(ABC):
    '''
    Alters a province.
    '''
    
    @abstractmethod
    def apply(self):
        '''
        Applies the given alteration.
        '''
        pass
