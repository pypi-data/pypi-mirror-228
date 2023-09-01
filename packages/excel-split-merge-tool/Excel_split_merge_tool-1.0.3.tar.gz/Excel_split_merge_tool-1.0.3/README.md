# Excel Manipulation Utility

This utility provides functions to split and merge Excel files efficiently. It can split a single Excel file into multiple smaller files and merge multiple Excel files into a single combined file.

## Features

- Split a single Excel file into multiple smaller files based on a specified number of output files.
- Merge multiple Excel files from a specified directory into a single combined Excel file.

## Installation

1. Clone or download this repository to your local machine.
2. Ensure you have Python>=3.9 installed.
3. Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```
   
## Usage

### Split Excel File
```python
from excel_utils import ExcelSplitter

splitter = ExcelSplitter()
file_path = "path_to_input_excel_file.xlsx"
splitter.split_excel_file(file_path)

```
Replace **"path_to_input_excel_file.xlsx"** with the actual path to the Excel file you want to split. The split files will be saved in an "OUTPUT" directory.

### Merge Excel Files
```python
from excel_utils import ExcelMerger

merger = ExcelMerger()
folder_path = "path_to_folder_with_excel_files"
merger.merge_file(folder_path)

```
Replace "path_to_folder_with_excel_files" with the actual path to the folder containing the Excel files you want to merge. The combined file will be saved in a "merge_file" directory.

## Configuration

You can adjust the configuration settings in the Configs class in the config.py file to customize the behavior of the utility.

## Project Directory Structure
```
├── Excel_split_merge_tool
│  └── resources
│  |    ├── __init__.py
│  |    └── configs.py
│  ├── __init__.py
│  └── ExcelSplitMergeTool.py
    
```