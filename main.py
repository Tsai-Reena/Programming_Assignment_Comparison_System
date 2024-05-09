import unzip
import compare
import change_name
import argparse
import re
import difflib
import sys
import pandas as pd
import os
import zipfile
import shutil

allowLogs = True  # Set this variable to True or False as needed

exceptions = []

def main():
    # 要解壓縮的資料夾
    file_name = input("Input the zip file name: ")
    source_file = f'.\{file_name}.zip'
    while not os.path.isfile(source_file):
        file_name = input("Wrong input. Please input the zip file name: ")
        source_file = f'.\{file_name}.zip'

    # 解壓縮
    extracted_folder = 'unzip_file'
    files_path = 'original_files'
    file_change_name_path = f'{files_path}_txt'
    
    # 修改副檔名
    name_before = input("Input the language(java or cpp): ")
    while name_before != 'java' and name_before != 'cpp':
        name_before = input("Wrong input. Please input the language(java or cpp): ")
    name_after = 'txt'
    
    # 文檔比對
    base = f'./{file_change_name_path}/'
    if name_before == 'java':
        encode_mode = 'utf-8'
    elif name_before == 'cpp':
        encode_mode = 'Big5'
    
    # 執行
    unzip.collectfiles(source_file, extracted_folder,files_path, file_change_name_path, [name_before])
    change_name.change_name('./' + file_change_name_path, name_before, name_after)
    for i in compare.findAllFile(base):
        for j in compare.findAllFile(base):
            compare.write_csv(f"{base}{i}", f"{base}{j}", encode_mode)
            
if __name__ == "__main__":
    main()