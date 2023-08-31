import os
import glob
import json

from Excel_split_merge_tool.resources.configs import Configs
from tqdm import tqdm
import pandas as pd

class ExcelSplitMergeTool:

    def __init__(self):
        pass

# -------------------------------------------------------------------------- #

    def split_excel_file(self, file_path:str) -> None:

        file = self.read_excel(file_path)
        num_output_file = Configs.NUM_OUPUT_FILE

        rows_per_file = file.shape[0] // num_output_file
        remainder_rows = file.shape[0] % num_output_file

        output_dir = "OUTPUT"
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)  

        start_idx = 0

        for i in range(num_output_file):

            end_idx = start_idx + rows_per_file

            if i < remainder_rows:
                end_idx += 1

            data = file[start_idx:end_idx]

            file_name = os.path.splitext(os.path.basename(file_path))[0]
            output_file_path = os.path.join(output_dir, f"{file_name}_split_{i+1}.xlsx")
            data.to_excel(output_file_path)

            print(f"Saved {output_file_path}")

        print("Split file Successful")

# -------------------------------------------------------------------------- #

    def merge_file(self):

        output_file = glob.glob(os.path.join("file_merge", "*.xlsx"))

        excel_lst = []

        for file in tqdm(range(len(output_file))):

            output = pd.read_excel(output_file[file])
            excel_lst.append(output)

        combined = pd.concat(excel_lst, axis=0)
        output_file_path = os.path.join('merge_file', 'combined_file.xlsx')
        combined.to_excel(output_file_path, index=False)

        print("Merge file Successful")
    
# -------------------------------------------------------------------------- #

    def read_excel(self, file_path:str):
        
        path = pd.read_excel(file_path)

        return path
    
# -------------------------------------------------------------------------- #