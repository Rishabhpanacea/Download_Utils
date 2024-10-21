import os
import numpy as np
import pydicom
from PIL import Image
# from src.configuration.config import Data_Folder


def CT_Data(dicom_file_path, CT_directory):
    try:
        dicom_dataset = pydicom.dcmread(dicom_file_path)
        sop_instance_uid = dicom_dataset.SOPInstanceUID
        study_uid = dicom_dataset.StudyInstanceUID
        series_uid = dicom_dataset.SeriesInstanceUID
        array = np.array(dicom_dataset.pixel_array)

        array_normalized = ((array - np.min(array)) / (np.max(array) - np.min(array)) * 255).astype(np.uint8)
        image = Image.fromarray(array_normalized, mode='L')
        output_filename = f'CT_{sop_instance_uid}.png'
        # count = sum(1 for entry in os.scandir(Data_Folder) if entry.is_file())
        # directory = os.path.join(Data_Folder,f'directory{count+1}')
        # os.mkdir(directory)
        output_filepath = os.path.join(CT_directory , output_filename)
        image.save(output_filepath)
        return [sop_instance_uid, study_uid, series_uid, output_filepath]
    
    except Exception as e:
        print(f"Error reading {dicom_file_path}: {e}")
        return None, None
    
    

def SEG_Data(seg_file_path, SEG_directory):
    try:
        seg_dataset = pydicom.dcmread(seg_file_path)
        if seg_dataset.Modality != 'SEG':
            raise ValueError("The provided DICOM file is not a SEG object.")
        
        referenced_sop_ids = []

        # Access the Per-Frame Functional Groups Sequence
        for item in seg_dataset.PerFrameFunctionalGroupsSequence:
            # Access the Derivation Image Sequence
            if 'DerivationImageSequence' in item:
                for derivation_image_item in item.DerivationImageSequence:
                    # Access the Source Image Sequence
                    if 'SourceImageSequence' in derivation_image_item:
                        for source_image_item in derivation_image_item.SourceImageSequence:
                            sop_instance_uid = source_image_item.ReferencedSOPInstanceUID
                            referenced_sop_ids.append(sop_instance_uid)

        seg_sop_instance_uid = seg_dataset.SOPInstanceUID
        print(seg_dataset.pixel_array.shape)
        pixel_data = []
        print("Pixel shape",len(seg_dataset.pixel_array.shape))

        if len(seg_dataset.pixel_array.shape) == 3:
            print("no.of seg",seg_dataset.pixel_array.shape[0])
            for i in range(0,seg_dataset.pixel_array.shape[0]):
                array = np.array(seg_dataset.pixel_array[i])
                array_normalized = ((array - np.min(array)) / (np.max(array) - np.min(array)) * 255).astype(np.uint8)
                image = Image.fromarray(array_normalized, mode='L')
                output_filename = f'Output_Seg_{referenced_sop_ids[i]}.png'
                output_filepath = os.path.join(SEG_directory,output_filename)
                image.save(output_filepath)
                pixel_data.append(output_filepath)

        else:
            array = np.array(seg_dataset.pixel_array)
            image = Image.fromarray(array)
            output_filename = f'Output_Seg_{referenced_sop_ids[0]}.png'
            output_filepath = os.path.join(SEG_directory,output_filename)
            image.save(output_filepath)
            pixel_data.append(output_filepath)
        
        output_list = []
        for i in range(0,len(referenced_sop_ids)):
            output_list.append([seg_sop_instance_uid, referenced_sop_ids[i], pixel_data[i]])
        print('I am here')    
        return output_list

    except Exception as e:
        print(f"Error reading {seg_file_path}: {e}")
        return []
    


def Convert_into_training_data(dicom_files, CT_directory, SEG_directory):
    CT = []
    SEG = []
    for file in dicom_files:
        data = pydicom.dcmread(file)
        if data.Modality == 'CT':
            CT.append(CT_Data(file, CT_directory))
        elif data.Modality == 'SEG':  
            SEG = SEG + SEG_Data(file, SEG_directory)
    return CT,SEG
    