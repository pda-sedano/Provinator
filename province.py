from pathlib import Path


class Province:
    '''
    Represents an EU4 province.
    '''

    def __init__(self, path: Path):
        '''
        Instantiates an EU4 province.

        Params
        - path: Path to the province file.
        '''
        self.path = path
        self.content = self._read()

    def _read(self):
        with self.path.open() as f:
            return f.read()
        
    def write(self):
        with self.path.open('w') as f:
            f.write(self.content)
