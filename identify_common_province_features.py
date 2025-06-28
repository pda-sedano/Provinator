import pathlib

provinces_folder = '/Users/gsvboti/Library/Application Support/Steam/steamapps/common/Europa Universalis IV/history/provinces'

patterns = ["discovered_by"]
occurrences = [0] * len(patterns)
non_occurence_files = []
num_files = 0


for province_file in pathlib.Path(provinces_folder).rglob('*.txt'):
    num_files += 1

    with open(province_file, 'r', encoding='latin-1') as file:
        content = file.read()
    
    # Check for specific patterns
    for i, pattern in enumerate(patterns):
        if pattern in content:
            occurrences[i] += 1
        else:
            non_occurence_files.append(province_file.name)

# Print the results
print(f"Total number of files processed: {num_files}")

for i, pattern in enumerate(patterns):
    if occurrences[i] == num_files:
        print(f"Pattern '{pattern}' found in all files.")

    else:
        print(f"Pattern '{pattern}' found in {occurrences[i]} out of {num_files} files.")
        print(f"Files in which '{pattern}' does not occur:")
        for file_name in non_occurence_files:
            print(f"  {file_name}")

    print("\n\n")  # Print some newlines for better readability
        
