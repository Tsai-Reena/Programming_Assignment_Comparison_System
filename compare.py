import argparse
import re
import difflib
import sys
import pandas as pd
import os

allowLogs = True  # Set this variable to True or False as needed

# Exceptions: Specify the keywords that the statements in your code start with.
# For example, if a statement in your code is "server_id = 103", you can specify "server_id" as an exception.
exceptions = []

# Display additional info about data processing


def log_print(*args):
    if allowLogs:
        print("------", *args, '\n')

# Remove newline characters from the line


def filterLine(line: str):
    filteredLine = re.sub(r"(\n|\\n|\r)+", "", line)
    return filteredLine.strip()

# Filter out empty strings from the list


def filterList(lst: list):
    filteredList = [line for line in lst if line != ""]
    return filteredList

# Checks whether line starts with exception keyword


def isLineHaveException(line: str):
    if exceptions:
        for excp in exceptions:
            if line.startswith(excp):
                return True
    return False

# Compare the contents of two files
def differ(file1, file2, encode_mode):
    global exceptions
    file1_path = file1
    file2_path = file2

    print(f"\nComparing {file1} and {file2}")

    try:
        # Attempt to open the files
        with open(file1_path, 'r', encoding=encode_mode) as firstFile, open(file2_path, 'r', encoding=encode_mode) as secondFile:
            # Read the lines from the files
            raw_file1_lines = firstFile.readlines()
            raw_file2_lines = secondFile.readlines()

    except FileNotFoundError as e:
        log_print(f"Error: {e}")
        sys.exit(1)  # Terminate the script with a non-zero exit code

    # Check if the files are identical
    if raw_file1_lines == raw_file2_lines:
        return "No differences found\n"

    # Filter the lines in each file
    filtered_file1_lines = [filterLine(line) for line in raw_file1_lines]
    filtered_file2_lines = [filterLine(line) for line in raw_file2_lines]

    # Filter out empty lines
    filtered_file1_lines = filterList(filtered_file1_lines)
    filtered_file2_lines = filterList(filtered_file2_lines)

    # Check if the filtered files are identical
    if filtered_file1_lines == filtered_file2_lines:
        return "No differences found\n"

    # Find the differences between the files
    maxLines = max(len(filtered_file1_lines), len(filtered_file2_lines))
    lineCounter = 0
    totalDifferences = 0

    while lineCounter < maxLines:
        try:
            file1_line = filtered_file1_lines[lineCounter]
            file2_line = filtered_file2_lines[lineCounter]

            if file1_line != file2_line:
                # Check for exceptions
                if isLineHaveException(file1_line) and isLineHaveException(file2_line):
                    log_print('EXCEPTION:', file1_line, '\n', file2_line)
                else:
                    print(
                        f'The difference N-{lineCounter}:\n File {file1}: In < {file1_line} > \n File {file2}: In < {file2_line} >\n')

                    totalDifferences += 1

        except IndexError:
            # If the line numbers are not equal
            moreLineFile = filtered_file1_lines if len(
                filtered_file1_lines) == maxLines else filtered_file2_lines

            larger_file = file1 if moreLineFile == filtered_file1_lines else file2
            print(
                f'Only file {larger_file} has: < {moreLineFile[lineCounter]} >\n')
            totalDifferences += 1

        lineCounter += 1

    print(f"Total Differences Found: {totalDifferences}")

    # Return difference percentage
    matcher = difflib.SequenceMatcher(
        None, filtered_file1_lines, filtered_file2_lines)
    fileSimilarity = round(matcher.ratio() * 100, 2)
    return fileSimilarity

def write_csv(file1_path, file2_path, encode_mode):
    try:
        if os.path.exists('compare_result.csv'):
            df = pd.read_csv('compare_result.csv', index_col=0) # 設置第一行為index
            print(df)
            if not (df["file_name"] == file2_path).any():
                new_row = pd.DataFrame({"file_name": [file2_path], file1_path: [differ(file1_path, file2_path, encode_mode)]})
                df = pd.concat([df, new_row], ignore_index=True) # ignore index for 忽略原本的 index 0 號，並修改成符合當下 df
            else:
                row_index = df.index[df["file_name"] == file2_path].tolist()[0] # 抓 file2_path 的 index
                df.at[row_index, file1_path] = differ(file1_path, file2_path, encode_mode) # 修改 [file2_path, file1_path] 的 value
        else:
            df = pd.DataFrame({"file_name": [file2_path], file1_path: [differ(file1_path, file2_path, encode_mode)]})
        df.to_csv('compare_result.csv')
    except Exception as e:
        print(f"An error occurred: {e}")

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f
