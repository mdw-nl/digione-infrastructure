import os
from pydicom import dcmread
"""This function can be used to change the patient ids of dicom files"""

def adding_treatment_site(patient_ids, data_folder):
    """Hardcode the treatment sides where we want filter on in the XNAT projects"""
    
    for ids, folder in zip(patient_ids, os.listdir(data_folder)):
        folder_path = os.path.join(data_folder, folder)
        
        for file in os.listdir(folder_path):
            if file.endswith(".dcm"):
                file_path = os.path.join(folder_path, file)
                ds = dcmread(file_path)
                ds.PatientID = ids
                ds.save_as(file_path)
                

if __name__ == '__main__':
    ids = ["PYTIM05", "PYTIM06"]
    folder_path = "data/dicom_datasets"
    adding_treatment_site(ids, folder_path)