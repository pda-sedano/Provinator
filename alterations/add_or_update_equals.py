import re
from alter import Alter


class AddOrUpdateEquals(Alter):
    '''
        Specifies a list of equalities of the form "lhs = rhs" to add to the province file.
        If a pattern of the form "lhs = different rhs" already exists, it will be modified in-place to "lhs = rhs".
        Else, the pattern "lhs = rhs" will be appended either to the end of the file, or based on the specification
        set by 'block_append_keyword'.
    '''

    def __init__(self, patterns: list[tuple[str, str]], block_append_keyword: str):
        '''
        Creates an AddOrUpdateEquals object.
        
        Params
        - patterns: A list of tuples of the form (lhs, rhs)
        - block_append_keyword: string specifying a keyword to append block
        '''
        self.patterns = patterns
        self.block_append_keyword = block_append_keyword
    
    def apply(self, province):
        for lhs, rhs in self.patterns:
            province.content = self._update_or_add(province.content, lhs, rhs)
        
        province.write()

    # TODO: currently doesn't append to EoF if block_append_keyword not set
    def _update_or_add(self, content, lhs, new_rhs):
        """Update or add a line in the content."""
        pattern = re.compile(rf'^{re.escape(lhs)}\s*=\s*.*$', re.MULTILINE)
        
        if pattern.search(content):
            return pattern.sub(f'{lhs} = {new_rhs}', content)
        elif self.block_append_keyword:
            return self._append_to_block_with_keyword(content, f'{lhs} = {new_rhs}')  

    # Appends to the last line of a contiguous text block containing a keyword, shifting everything
    # after down by one line.
    def _append_to_block_with_keyword(self, content, line_to_append):
        lines = content.splitlines(keepends=True)

        blocks = []
        current_block = []
        block_start_idx = None

        # Step 1: Split into blocks with their starting line numbers
        for idx, line in enumerate(lines):
            if line.strip():  # Non-blank
                if current_block == []:
                    block_start_idx = idx
                current_block.append(line)
            else:  # Blank line
                if current_block:
                    blocks.append((block_start_idx, current_block))
                    current_block = []
                    block_start_idx = None
        if current_block:  # EOF-end block
            blocks.append((block_start_idx, current_block))

        # Step 2: Find the first block with the keyword
        for start_idx, block in blocks:
            if any(self.block_append_keyword in line for line in block):
                insert_idx = start_idx + len(block)
                lines.insert(insert_idx, line_to_append.rstrip() + "\n")
                break  # Only first match

        return ''.join(lines)
