import re
from pathlib import Path

# The Provinator will be baaaach
class Provinator:
    def __init__(
        self,
        provinces_folder,
        # province_ids,
        # patterns_to_search,
        # new_owner, keywords,
        # block_to_append_keyword=None
    ):
        '''
        Creates a new Provinator. Allows programmaticaly altering EU4 province files.

        Params
            - provinces_folder: Path to the folder containing the provinces.
        '''
        self.provinces_folder = provinces_folder
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
        for file in Path(self.provinces_folder).rglob('*.txt'):
            with file.open('r', encoding='latin-1') as f:
                content = f.read()

            contains_key_pattern = False

            # Check if file contains trade_goods = slaves
            for pattern in self.patterns_to_search:
                if re.search(rf'^{pattern[0]}\s*=\s*{pattern[1]}', content, re.MULTILINE):
                    print(f"File {file.name} contains {pattern[0]} = {pattern[1]}")
                    # Perform actions if needed
                    # For example, you can update or add a line
                    contains_key_pattern = True
                    break
            # pattern = re.compile(r'trade_goods\s*=\s*slaves', re.MULTILINE)

            if contains_key_pattern or file.name.startswith(tuple(map(str, self.province_ids))):
                print(f"Processing file: {file.name}")

                # Update or add lines for each keyword
                for keyword in self.keywords:
                    content = self.update_or_add(content, keyword, self.new_owner)

                # Write the updated content back to the file
                with file.open('w', encoding='latin-1') as f:
                    f.write(content)

    def update_or_add(self, content, lhs, new_rhs):
        """Update or add a line in the content."""
        pattern = re.compile(rf'^{re.escape(lhs)}\s*=\s*.*$', re.MULTILINE)
        
        if pattern.search(content):
            return pattern.sub(f'{lhs} = {new_rhs}', content)
        elif self.block_to_append_keyword:
            return append_to_block_with_keyword(content, self.block_to_append_keyword, f'{lhs} = {new_rhs}')   


# Appends to the last line of a contiguous text block containing a keyword, shifting everything
# after down by one line.
def append_to_block_with_keyword(content, keyword, line_to_append):
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
        if any(keyword in line for line in block):
            insert_idx = start_idx + len(block)
            lines.insert(insert_idx, line_to_append.rstrip() + "\n")
            break  # Only first match

    return ''.join(lines)         
