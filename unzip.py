import os
import zipfile
import shutil

def collectfiles(source_file, extracted_folder, files_path, file_change_name_path, suffix):

    # 創建資料夾
    if os.path.exists(extracted_folder):
        shutil.rmtree(extracted_folder)
    os.makedirs(extracted_folder, exist_ok=True)
    if os.path.exists(files_path):
        shutil.rmtree(files_path)
    os.makedirs(files_path, exist_ok=True)
    if os.path.exists(file_change_name_path):
        shutil.rmtree(file_change_name_path)
    os.makedirs(file_change_name_path, exist_ok=True)

    # 解壓縮
    ZIP = zipfile.ZipFile(source_file)
    ZIP.extractall(extracted_folder)
    ZIP.close()

    filelist = [] # 儲存要 copy 的文件名

    for dirpath, dirnames, filenames in os.walk(extracted_folder):
        for file in filenames:
            file_type = file.split('.')[-1] # 副檔名
            if(file_type in suffix):
                file_fullname = os.path.join(dirpath, file)
                filelist.append(file_fullname)
    for file in filelist:
        print(file)
        shutil.copy(file, files_path)
        shutil.copy(file, file_change_name_path)
    if os.path.exists(extracted_folder):
        shutil.rmtree(extracted_folder)
    
def main():
    # 要解壓縮的資料夾
    source_file = input("Please input the file name: ") + ".zip"

    # 解壓縮後的目標資料夾路徑
    extracted_folder = 'unzip_file'
    files_path = 'files'
    file_change_name_path = 'files_txt'
    
    collectfiles(source_file, extracted_folder, files_path, file_change_name_path, ['java', 'cpp'])

if __name__ == "__main__":
    main()
    