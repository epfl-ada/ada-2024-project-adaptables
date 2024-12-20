from dataclasses import dataclass
from functools import cached_property
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from prettytable import PrettyTable
from ..utils.general_utils import number_to_emoji

VALID_FILETYPES = [".csv",".tsv",".txt"]

@dataclass
class ProjectDataset:
    # Helper class to represent one of our datasets and metadata regarding it
    # 4 arguments :
    #     - `path` is the path to the dataset
    #     - `name` is how we decided to name the dataset, and how we will reference it in our Markdown explanations/report
    #     - `description` is a brief description of the dataset
    #     - `columns_descriptions` is a dictionnary containing all the columns of our dataset, as well as a short description for each of those columns


    path:str
    name:str
    description:str
    columns_descriptions:dict[str,str]

    def __str__(self):
        return self.name

    def __post_init__(self):
        p = Path(self.path)
        if not p.exists():
            raise ValueError(f"Path validation for {self}: {self.path} (-> {p.absolute().as_posix()}) does not exist!")
        if not p.is_file():
            raise ValueError(f"Path validation for {self}: {self.path} is not a file!")
        if p.suffix not in VALID_FILETYPES:
            raise ValueError(f"Path validation for {self}: {self.path} is not of the expected type (one of {', '.join(VALID_FILETYPES)}), but rather {p.suffix}!")

    @cached_property
    def __file_separator(self):
        p = Path(self.path)
        match p.suffix:
            case ".csv":
                return ","
            case ".tsv" | ".txt":
                return "\t"
            
    
    def get_columns(self):
        return list(self.columns_descriptions.keys())

    @cached_property
    def df(self):
        # Infer if file has headers heuristically by looking if it the first line is a string with no spaces and commas
        with open(self.path,"r") as f:
            first_line = f.readline()
            has_headers = " " not in first_line and ("," in first_line or first_line.lower().isalpha()) 

        return pd.read_csv(
            self.path,sep=self.__file_separator,
            header=0 if has_headers else None,
            names=self.columns_descriptions.keys()
        )


def describe_datasets(all_datasets: list[ProjectDataset]):
    print(f"We will use {len(all_datasets)} datasets in total, namely {', '.join(str(ds) for ds in all_datasets)}.\
          \n Here is a decription of all of them:")

    for i,ds in enumerate(all_datasets):
        print(f"- {number_to_emoji(i+1)} \033[4m{ds.name}\033[0m\n")
        print(f"{ds.description}\n")
        table = PrettyTable()
        table.field_names = ["Column/Fearure", "Description"]
        table.align['Description'] = 'l'
        table.max_width["Description"] = 40
        
        for column_name, column_description in ds.columns_descriptions.items():
            table.add_row([column_name, column_description+'\n'])

        print(table)
        print("\n")

def preload_datasets(all_datasets: list[ProjectDataset]):
    for dataset in tqdm(all_datasets,total=len(all_datasets),desc="Preloading datasets..."):
        _ = dataset.df