import os
import glob

from Excel_split_merge_tool.resources.configs import Configs
from tqdm import tqdm
import pandas as pd

class ExcelSplitMergeTool:

    def __init__(self):
        pass

# -------------------------------------------------------------------------- #

    def split_excel_file(self, file_path:str):
        
        """
        Split an Excel (.xlsx) file into multiple smaller files
        based on the specified number of output files
    
        This function reads an Excel file from the given 'file_path'
        and divides its content into a specified number of output files, 
        distributing the rows as evenly as possible. 
        If there is a remainder in row distribution, 
        the extra rows are distributed among the first few output files.
        
        Parameters:
            file_path (str): The path to the input Excel file.
        
        Returns:
            Excel file (.xlsx) file follow by NUM_OUPUT_FILE.
            
        Example:
            splitter = ExcelSplitter()
            splitter.split_excel_file("input.xlsx")
        
        """

        file = pd.read_excel(file_path)
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
            
            output_file_path = os.path.join(
                output_dir, 
                f"{file_name}_split_{i+1}.xlsx"
            )
            
            data.to_excel(output_file_path)

            print(f"Saved {output_file_path}")

        print("Split file Successful")

# -------------------------------------------------------------------------- #

    def merge_file(self, folder_path:str):
        
        """
        Merge multiple Excel files within a specified directory into a single combined Excel file.
        
        This function reads all Excel files within the provided 'folder_path', 
        combines their contents row-wise, and saves
        the combined data as a new Excel file named 'combined_file.xlsx' in a separate directorynamed 'merge_file'.
        
        Parameters:
            folder_path (str): The path to the directory containing the Excel files to be merged.
        
        Returns:
            None
        
        Example:
            merger = ExcelMerger()
            folder_path = "folder_with_excel_files"
            merger.merge_file(folder_path)
        
        """

        output_file = glob.glob(os.path.join(folder_path, "*.xlsx"))

        excel_lst = []

        for file in tqdm(range(len(output_file))):

            output = pd.read_excel(output_file[file])
            excel_lst.append(output)

        combined = pd.concat(excel_lst, axis=0)
        file_name = os.path.basename(file)
        output_file_path = os.path.join(f"Merge_{file_name}")
        combined.to_excel(output_file_path, index=False)

        print("Merge file Successful")
    
# -------------------------------------------------------------------------- #