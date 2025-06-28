import pathlib
provinces_folder = '/Users/gsvboti/Library/Application Support/Steam/steamapps/common/Europa Universalis IV/history/provinces'

folder_path = pathlib.Path(provinces_folder)

# original_owner = 'MAM'
new_owner = 'LAN'

phrases = ["owner = ", "controller = ", "add_core ="]

for file in folder_path.iterdir():
    print(file.suffix)
    print(file)
    if file.suffix == '.txt':
        # Open the file (read-only as an example)
        with file.open('r', encoding='latin-1') as f:
            content = f.read()

        if f'add_core = {original_owner}' not in content and f'add_core = {new_owner}' not in content:
            content = content.replace(f'controller = {new_owner}', f'controller = {new_owner}\nadd_core = {new_owner}')

        for phrase in phrases:
            content = content.replace(phrase + original_owner, phrase + new_owner)

        with file.open('w', encoding='latin-1') as f:
            f.write(content)
