import os
import shutil
import tempfile
import zipfile
import pandas as pd
from src.configuration.config import TEMP_PATH
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from src.utils.File_Handling_Utils.File_Handle import extract, Create_Dirs
from src.utils.Dicom_Utils.Dicom_Utils import Convert_into_training_data
from src.configuration.config import columns_CT, columns_seg, CT_CSV_Name, SEG_CSV_Name

router = APIRouter()

@router.post("/predict/")
async def download(file: UploadFile = File(...)):
    fd, zip_path = tempfile.mkstemp(suffix=".zip", dir=TEMP_PATH, prefix='tmp')
    try:
        with os.fdopen(fd, 'wb') as tmp:
            data = await file.read()
            tmp.write(data)
        extract_dir = tempfile.mkdtemp(dir=TEMP_PATH)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        dicom_files = extract(extract_dir)
        CT_dir, SEG_dir = Create_Dirs()
        CT, SEG = Convert_into_training_data(dicom_files, CT_dir, SEG_dir)
        if CT:
            CT_df = pd.DataFrame(CT, columns=columns_CT)
            CT_CSV_PATH = os.path.join(CT_dir, CT_CSV_Name)
            CT_df.to_csv(CT_CSV_PATH , index=False)
        if SEG:
            SEG_df = pd.DataFrame(SEG, columns=columns_seg)
            SEG_CSV_PATH = os.path.join(SEG_dir, SEG_CSV_Name)
            SEG_df.to_csv(SEG_CSV_PATH , index=False)
        return {"message": "Files uploaded and processed successfully."}
    finally:
        os.remove(zip_path)
        shutil.rmtree(extract_dir)