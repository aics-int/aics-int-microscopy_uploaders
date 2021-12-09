#file uploader for a single local file 
from aicsfiles import FileManagementSystem
fms = FileManagementSystem()
file_path = r'C:\Users\Brian\OneDrive\Desktop\AICS_Brian\3500004647_Scan_7-28-2021-7-07-16-AM_Well_C8_Ch1_-1um.tiff'
file_name = open(file_path).name.split('\\')[-1]

metadata = file_name.split("_")

plate_barcode = metadata[0]

ts = metadata[2].split('-')
scan_date = ts[0] + '-'+ ts[1] + '-'+ ts[2]
scan_time = ts[4] + '-'+ ts[5] + '-'+ ts[6]

row = metadata[4][0]
col = metadata[4][1:]

additional_metadata = {
    "microsocpy": {
        "plate_barcode": [plate_barcode], 
        "celigo": {
            "scan_time": [scan_time],
            "scan_date": [scan_date],
            "row": [row],
            "coll": [col]
        }
    }
}

fms_file = fms.upload_file(file_path, file_type="image", metadata=additional_metadata)