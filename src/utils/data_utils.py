import swifter
from dataclasses import dataclass
from functools import cached_property
import pandas as pd
from pathlib import Path
import ast

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


def prepro_cmu_movies(movies_df: pd.DataFrame) -> pd.DataFrame:
    new_df = movies_df.copy()
    new_df["languages"] = new_df["languages"].swifter.apply(lambda lang_dict_as_str: list(ast.literal_eval(lang_dict_as_str).values()))
    new_df["countries"] = new_df["countries"].swifter.apply(lambda lang_dict_as_str: list(ast.literal_eval(lang_dict_as_str).values()))
    new_df["genres"] = new_df["genres"].swifter.apply(lambda lang_dict_as_str: list(ast.literal_eval(lang_dict_as_str).values()))
    def parse_release_date(release_date_str):
        # The release date is :
        #       either empty
        #       or YYYY
        #       or YYYY-MM-DD
        # --> since we're simply inetrested in the year, we can just take the first 4 characters  
        if isinstance(release_date_str,float):
            return release_date_str
        return release_date_str.strip()[:4]
    new_df["release_date"] = pd.to_numeric(new_df["release_date"].swifter.apply(parse_release_date), errors="coerce",downcast="unsigned") # this will set a NaN wherever we don't have a date
    return new_df