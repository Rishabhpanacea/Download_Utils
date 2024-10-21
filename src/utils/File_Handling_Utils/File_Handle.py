import os
import zipfile
import tempfile
from src.configuration.config import Data_Folder

def extract(directory):
    dicom_files = []
    for filename in os.listdir(directory):
        _, file_extension = os.path.splitext(filename)
        file_path = os.path.join(directory, filename)
        if file_extension == '.zip':
            extract_dir = tempfile.mkdtemp(dir=directory)
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            os.remove(file_path)    
            dicom_files = dicom_files + extract(extract_dir)
        elif file_extension == '.dcm':
            print("dcm")
            dicom_files.append(file_path)
        elif len(file_extension) == 0:
            dicom_files = dicom_files + extract(file_path)
    
    return dicom_files

def Create_Dirs():
    # count = sum(1 for entry in os.scandir(Data_Folder) if entry.is_file())
    print("Data folder:-",os.listdir(Data_Folder))
    count = len(os.listdir(Data_Folder)) + 1
    print('no. of dir:-',count)
    directory = os.path.join(Data_Folder,f'directory_{count}')
    os.mkdir(directory)
    CT_Dir = os.path.join(directory, 'CT_Data')
    SEG_Dir = os.path.join(directory, 'SEG_Data')
    os.mkdir(CT_Dir)
    os.mkdir(SEG_Dir)
    return CT_Dir, SEG_Dir