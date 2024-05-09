import os
name_before = 'java'
name_after = 'txt'

def get_list(path):
    all_name = os.listdir(path)
    return all_name

def find_file(path, name_before):
    file_name = []
    for i in get_list(path):
        i = os.path.join(path, i)
        try:
            if i.split('.')[2] == name_before:
                file_name.append(i)
        except:
            pass
    return file_name

def change_name(path, name_before, name_after):
    # find_file(path)
    for i in find_file(path, name_before):
        print(i.split('.')[1] + '.' + name_after)
        os.renames(i, '.' + i.split('.')[1] + '.' + name_after)

def main():
    change_name('./txt_files', name_before, name_after)


